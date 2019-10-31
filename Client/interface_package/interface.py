import sys
import time
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from interface_package.ui_classes import *
from decrypt_problem import decrypt
from init_client import initialize_contest



global current_status 
current_status = "STOPPED" 

global Timer
# Timer = 00:00:00

# This is to ignore some warnings which were thrown when gui exited and python deleted some assests in wrong order
# Nothing critical 
def handler(msg_type, msg_log_context, msg_string):
	pass
qInstallMessageHandler(handler)



class client_window(QMainWindow):
	def __init__(self, data_changed_flag2,queue):
		super().__init__()
		# Set app icon
		self.setWindowIcon(QIcon('Elements/logo.png'))
		# Set window title
		self.setWindowTitle('BitsOJ v1.0.1 [ Client ]')
		
		# Initialize status bar
		self.status = self.statusBar()
		# self.setFixedSize(1200,700)
		self.resize(1200,700)

		self.timer = QTimer()
		self.change_flag = True
		self.timer.timeout.connect(self.update_data)
		self.timer.start(1000)

		# Make data_changed_flag accessible from the class methods
		self.data_changed_flag = data_changed_flag2
		self.queue = queue


		####################################################################
		self.db = self.init_qt_database()
		####################################################################
		# Define Sidebar buttons and their actions
		button_width = 200
		button_height = 50

		self.button_1 = QPushButton('Problems', self)
		self.button_1.setFixedSize(button_width, button_height)
		self.button_1.clicked.connect(self.view_problems)
		self.button_1.setObjectName('sidebar_button')

		self.button_2 = QPushButton('Submissions', self)
		self.button_2.setFixedSize(button_width, button_height)
		self.button_2.clicked.connect(self.view_submissions)
		self.button_2.setObjectName('sidebar_button')

		self.button_3 = QPushButton('Submit Solution', self)
		self.button_3.setFixedSize(button_width, button_height)
		self.button_3.clicked.connect(self.submit_solution)
		self.button_3.setObjectName('sidebar_button')

		self.button_4 = QPushButton('Query', self)
		self.button_4.setFixedSize(button_width, button_height)
		self.button_4.clicked.connect(self.send_query)
		self.button_4.setObjectName('sidebar_button')

		self.button_5 = QPushButton('Leaderboard', self)
		self.button_5.setFixedSize(button_width, button_height)
		self.button_5.clicked.connect(self.ranklist)
		self.button_5.setObjectName('sidebar_button')

		self.button_6 = QPushButton('About', self)
		self.button_6.setFixedSize(button_width, button_height)
		self.button_6.clicked.connect(self.show_about)
		self.button_6.setObjectName('sidebar_button') 

		#####################################################################

		#####################################################################
		# Manage tabs o the right window
		# Each tab is an object returned by the respective function associated with its UI
		# Tab UI are managed by interface_package/ui_classes.py file
		self.tab1 = ui_widgets.problems_ui(self)
		self.tab2, self.sub_model = ui_widgets.submissions_ui(self)
		self.tab3 = ui_widgets.submit_ui(self)
		self.tab4, self.query_model = ui_widgets.query_ui(self)
		self.tab5 = ui_widgets.leaderboard_ui(self)
		self.tab6 = ui_widgets.about_ui(self)

		#####################################################################

		# Add widgets to our main window 
		client_window.init_UI(self)
		return


	def init_UI(self):
		self.set_status()
		# Define layout for sidebar
		side_bar_layout = QVBoxLayout()

		#add buttons to our layout
		side_bar_layout.addWidget(self.button_1)
		side_bar_layout.addWidget(self.button_2)
		side_bar_layout.addWidget(self.button_3)
		side_bar_layout.addWidget(self.button_4)
		side_bar_layout.addWidget(self.button_5)
		side_bar_layout.addWidget(self.button_6)

		# Set stretch and Spacing 
		side_bar_layout.addStretch(1)
		side_bar_layout.addSpacing(0)

		# Define our side bar widget and set side bar layout to it
		side_bar_widget = QWidget()
		side_bar_widget.setLayout(side_bar_layout)
		side_bar_widget.setFixedWidth(215)
		side_bar_widget.setObjectName("sidebar")

		# Define out top bar
		logo = QLabel(self)
		logo_image = QPixmap('Elements/bitwise_header.png')
		logo_image = logo_image.scaledToWidth(104)
		logo.setPixmap(logo_image)

		self.timer_widget = QLCDNumber()
		self.timer_widget.setSegmentStyle(QLCDNumber.Flat)
		self.timer_widget.setDigitCount(8)
		self.timer_widget.display('00:00:00')
		self.timer_widget.setFixedSize(150,40)

		top_bar_layout = QHBoxLayout()
		top_bar_layout.setContentsMargins(15, 5, 1, 0)
		top_bar_layout.addWidget(logo)
		top_bar_layout.addWidget(self.timer_widget)
		top_bar_layout.setStretch(0, 70)

		top_bar_widget = QWidget()
		top_bar_widget.setLayout(top_bar_layout)
		top_bar_widget.setObjectName('top_bar')

		# Define our right side screens corresponding to buttons on the sidebar
		# Basically right screens are tab widgets whose tabs are hidden, 
		# and we map sidebar buttons to each tab switch :)
		# Since sidebars are not natively supported by pyqt5
		self.right_widget = QTabWidget()
		self.right_widget.setObjectName("main_tabs")

		self.right_widget.addTab(self.tab1, '')
		self.right_widget.addTab(self.tab2, '')
		self.right_widget.addTab(self.tab3, '')
		self.right_widget.addTab(self.tab4, '')
		self.right_widget.addTab(self.tab5, '')
		self.right_widget.addTab(self.tab6, '')

		# Screen 1 will be our initial screen
		self.right_widget.setCurrentIndex(0)

		# Define the combined layout for sidebar + right side screns
		main_layout = QHBoxLayout()
		main_layout.addWidget(side_bar_widget)
		main_layout.addWidget(self.right_widget)

		# setstretch( index, stretch_value )
		main_layout.setStretch(0, 10)
		main_layout.setStretch(1, 100)
		main_layout.setContentsMargins(10, 1 ,10, 1)
		# Define our main widget = sidebar + windows
		main_widget = QWidget()
		main_widget.setObjectName("screen_widget")
		main_widget.setLayout(main_layout)

		#Define top_layout = logo bar + main_layout
		top_layout = QVBoxLayout()
		top_layout.addWidget(top_bar_widget)
		top_layout.addWidget(main_widget)
		top_layout.setContentsMargins(1, 0, 1, 1)
		top_layout.setStretch(0, 8)
		top_layout.setStretch(1, 92)

		top_widget = QWidget()
		top_widget.setLayout(top_layout)
		top_widget.setObjectName("top_widget")

		# Set top_widget as our central widget
		self.setCentralWidget(top_widget)

		return

	def view_problems(self):
		self.right_widget.setCurrentIndex(0)

	def view_submissions(self):
		self.right_widget.setCurrentIndex(1)

	def submit_solution(self):
		self.right_widget.setCurrentIndex(2)

	def send_query(self):
		self.right_widget.setCurrentIndex(3)

	def ranklist(self):
		self.right_widget.setCurrentIndex(4)

	def show_about(self):
		self.right_widget.setCurrentIndex(5)


	##################################################################################

	def update_data(self):
		if self.data_changed_flag[0] == 1:
			self.setWindowTitle('BitsOJ v1.0.1 [ CLIENT ][ RUNNING ]')
			self.start_contest()
			self.set_status()
			self.data_changed_flag[0] = 2
		# If data has changed in submission table

		if self.data_changed_flag[0] == 3:
			self.setWindowTitle('BitsOJ v1.0.1 [ CLIENT ][ STOPPED ]')
			self.stop_contest()
			self.set_status()
			self.data_changed_flag[0] = 4

		if self.data_changed_flag[1] ==1:
			self.sub_model.select()
			# self.notify()
			# reset data_changed_flag
			self.data_changed_flag[1] = 0

		if self.data_changed_flag[1] == 2:
			self.sub_model.select()
			self.notify()
			# reset data_changed_flag
			self.data_changed_flag[1] = 0

		# If data has changed in query table
		if(self.data_changed_flag[2] == 1):
			self.query_model.select()
			# self.notify()
			# reset data_changed_flag
			self.data_changed_flag[2] =0

		if(self.data_changed_flag[2] == 2):
			self.query_model.select()
			self.notify()
			# reset data_changed_flag
			self.data_changed_flag[2] =0

		if(self.data_changed_flag[3] == 1):
			# message = self.queue.get()
			message = 'Under Progress'
			QMessageBox.warning(self, 'Error', message)
			self.data_changed_flag[3] = 0

		if(self.data_changed_flag[4] == 2):
			try:
				initialize_contest.contest_end_time()
				self.data_changed_flag[4] = 1
			except Exception as Error:
				print(str(Error))

		if(self.data_changed_flag[4] == 1):
			try:
				total_time = initialize_contest.return_contest_end_time()
				current_time = time.time()
				elapsed_time = time.strftime('%H:%M:%S', time.gmtime(total_time - current_time ))
				self.timer_widget.display(elapsed_time)
				self.set_status()
				if elapsed_time == '00:00:00':
					self.data_changed_flag[4] = 0
					self.data_changed_flag[0] = 3
			except Exception as Error:
				print(str(Error))

		if(self.data_changed_flag[5] == 1):
			QMessageBox.warning(self, 'Alert', 'You are disconnected by the admin.\nPlease contact Administrator.')
			QApplication.quit()
		if(self.data_changed_flag[5] == 2):
			QMessageBox.warning(self, 'Alert', 'All Clients are disconnected by the admin.\nPlease contact Administrator.')
			QApplication.quit()
		return

	####################################################################################


	#####################################################################################

	def closeEvent(self, event):
		message = "Pressing 'Yes' will SHUT the Client.\nAre you sure you want to exit?"
		detail_message = "Any active contest might end prematurely. "

		custom_close_box = QMessageBox()
		custom_close_box.setIcon(QMessageBox.Critical)
		custom_close_box.setWindowTitle('Warning!')
		custom_close_box.setText(message)
		custom_close_box.setInformativeText(detail_message)


		custom_close_box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		custom_close_box.setDefaultButton(QMessageBox.No)

		button_yes = custom_close_box.button(QMessageBox.Yes)
		button_yes.setText('Yes')
		button_no = custom_close_box.button(QMessageBox.No)
		button_no.setText('No')

		button_yes.setObjectName("close_button_yes")
		button_no.setObjectName("close_button_no")

		button_yes.setStyleSheet(open('Elements/style.qss', "r").read())
		button_no.setStyleSheet(open('Elements/style.qss', "r").read())

		custom_close_box.exec_()

		if custom_close_box.clickedButton() == button_yes:
			event.accept()
		elif custom_close_box.clickedButton() == button_no:
			event.ignore()


	##################################################################################
	# Database related functions 
	def init_qt_database(self):
		try:
			db = QSqlDatabase.addDatabase('QSQLITE')
			db.setDatabaseName('client_database.db')
			return db
		except:
			print('[ CRITICAL ] Database loading error......')

	def manage_models(self, db, table_name):
		if db.open():
			model = QSqlTableModel()
			model.setTable(table_name)
			model.setEditStrategy(QSqlTableModel.OnFieldChange)
			model.select()
		return model

	def generate_view(self, model):
		table = QTableView() 
		table.setModel(model)
		# Enable sorting in the table view 
		table.setSortingEnabled(True)
		# Enable alternate row colors for readability
		table.setAlternatingRowColors(True)
		# Select whole row when clicked
		table.setSelectionBehavior(QAbstractItemView.SelectRows)
		# Allow only one row to be selected 
		table.setSelectionMode(QAbstractItemView.SingleSelection)
		# fit view to whole space 
		table.resizeColumnsToContents()
		# Make table non editable
		table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		# Set view to delete when gui is closed
		table.setAttribute(Qt.WA_DeleteOnClose)

		horizontal_header = table.horizontalHeader()
		horizontal_header.setSectionResizeMode(QHeaderView.Stretch)
		vertical_header = table.verticalHeader()
		#vertical_header.setSectionResizeMode(QHeaderView.Stretch)
		vertical_header.setVisible(False)
		return table

	#########################################################################################

	def view_submission(self, selected_row):
		try:
			source_file = self.sub_model.index(selected_row, 3).data()
			run = self.sub_model.index(selected_row, 1).data()
			verdict = self.sub_model.index(selected_row, 2).data()
			language = self.sub_model.index(selected_row, 4).data()
		except Exception as Error:
			print(" [ Error ] : " + str(Error))
		if source_file == None:
			QMessageBox.warning(self, 'Message', 'Please select submission to view. ')
		else:
			try:
				self.window = view_submission_ui(self.data_changed_flag,source_file,verdict,language,run)
				self.window.show()
			except Exception as Error:
				print(str(Error))
		


	def view_reply(self,selected_row):
		try:
			query = self.query_model.index(selected_row, 0).data()
			response = self.query_model.index(selected_row, 1).data()
		except Exception as Error:
			print(' [ Error ] : ' + str(Error))
		if query == None:
			QMessageBox.warning(self, 'Message', 'Please select query to view. ')
		else:
			self.window = view_query_ui(self.data_changed_flag, query, response)
			self.window.show()
		

	#########################################################################################

	def set_status(self):
		global current_status
		self.status.showMessage(current_status)

	#########################################################################################


	def start_contest(self):
		global current_status
		global Timer
		with open('contest.json', 'r') as contest:
			data = json.load(contest)
		current_status = 'RUNNING'
		Timer = data["Duration"]
		decrypt.decrypting()
		QMessageBox.warning(self, 'Info', 'Contest has been STARTED.\nNow you can view problems.')

	def stop_contest(self):
		global current_status
		current_status = 'STOPPED'
		QMessageBox.warning(self, 'Message', 'Contest has been ended.\n You can not submit solution any more ')


	def notify(self):
		if self.data_changed_flag[1] == 2:
			QMessageBox.warning(self, 'Message', 'Submission verdict received ')
		if self.data_changed_flag[2] == 2:
			QMessageBox.warning(self, 'Message', 'Query Response received ')		


class init_gui(client_window):
	def __init__(self, data_changed_flag,queue):
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		app.setStyleSheet(open('Elements/style.qss', "r").read())
		# If user is about to close window
		app.aboutToQuit.connect(self.closeEvent)

		# make a reference of App class
		client_app = client_window(data_changed_flag,queue)

		client_app.showMaximized()
		# server_app.showNormal()
		# Close the server as soon as close buton is clicked
		app.exec_()



