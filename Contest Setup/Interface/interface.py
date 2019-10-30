import sys
import time
import socket
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler




class contest_setup(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowIcon(QIcon('Elements/logo.png'))
		self.setWindowTitle('BitsOJ v1.0.1 Contest Setup')
		self.resize(1200,700)

		contest_setup.init_GUI(self)
		contest_setup.client(self)
		return

	def init_GUI(self):

		#Define our top bar
		logo = QLabel(self)
		logo_image = QPixmap('../Elements/bitwise_header.png')
		logo_image2 = logo_image.scaledToWidth(104)
		logo.setPixmap(logo_image2)

		top_bar_layout = QHBoxLayout()
		top_bar_layout.setContentsMargins(15, 5, 20, 0);
		top_bar_layout.addWidget(logo)
		top_bar_layout.setStretch(0, 70)
		

		top_bar_widget = QWidget()
		top_bar_widget.setLayout(top_bar_layout)
		top_bar_widget.setObjectName('top_bar')

		self.top_tab = QTabWidget()
		self.top_tab.setObjectName('top_tab')
		self.client_tab = QWidget()
		self.server_tab = QWidget()
		self.judge_tab = QWidget()
		self.contest_tab = QWidget()

		self.top_tab.addTab(self.client_tab, "Client Config")
		self.top_tab.addTab(self.server_tab, "Server Config")
		self.top_tab.addTab(self.judge_tab, "Judge Config")
		self.top_tab.addTab(self.contest_tab, "Contest Config")


		#Define top_layout = logo_bar + main_layout
		top_layout = QVBoxLayout()
		top_layout.addWidget(top_bar_widget)
		top_layout.addWidget(self.top_tab)
		top_layout.setContentsMargins(1, 0, 1, 1)
		top_layout.setStretch(0, 8)
		top_layout.setStretch(1, 100)

		top_widget = QWidget()
		top_widget.setLayout(top_layout)
		top_widget.setObjectName("main_widget")

		# Set top_widget as our central widget
		self.setCentralWidget(top_widget)
		return

	def client(self):
		self.client_tab_layout = QVBoxLayout()
		self.tabs = QTabWidget()
		self.tabs.setObjectName('client_tabs')
		self.rabbitmq_detail = QWidget()
		self.problem_tab = QWidget()
		self.language = QWidget()
		self.contest = QWidget()

		##################################################################
		####################### PROBLEM TAB ##############################
		##################################################################

		
		problem_heading = QLabel('Problems')
		problem_heading.setObjectName('heading')
		self.problem = QHBoxLayout()
		self.problem_label = QLabel('Number of Problems : ')
		self.problem_label.setObjectName('general')
		self.problem_entry = QLineEdit()
		self.problem_entry.setFixedWidth(400)
		self.problem_entry.setFixedHeight(50)
		self.problem.addWidget(self.problem_label)
		self.problem.addWidget(self.problem_entry)
		self.problem.addStretch(1)
		self.problem.addSpacing(0)
		self.problem_tab.setLayout(self.problem)


		###################################################################
		######################## RABBITMQ TAB #############################
		###################################################################

		self.rabbitmq_creds = QVBoxLayout()
		rabbitmq_heading = QLabel('RabbitMQ Client Details')
		rabbitmq_heading.setObjectName('heading')
		self.rabbitmq_username = QHBoxLayout()
		self.rabbitmq_username_label = QLabel('RABBIT_MQ USERNAME    :   ')
		self.rabbitmq_username_label.setObjectName('general')
		self.rabbitmq_username_text = QLineEdit()
		self.rabbitmq_username_text.setPlaceholderText('Example : Client')
		self.rabbitmq_username_text.setObjectName('general_text')
		self.rabbitmq_username_text.setFixedWidth(400)
		self.rabbitmq_username_text.setFixedHeight(50)
		self.rabbitmq_username.addWidget(self.rabbitmq_username_label)
		self.rabbitmq_username.addWidget(self.rabbitmq_username_text)
		self.rabbitmq_username.addStretch(1)
		self.rabbitmq_username.addSpacing(0)
		self.username_widget = QWidget()
		self.username_widget.setLayout(self.rabbitmq_username)
		self.rabbitmq_password = QHBoxLayout()
		self.rabbitmq_password_label = QLabel('RABBIT_MQ PASSWORD   :   ')
		self.rabbitmq_password_label.setObjectName('general')
		self.rabbitmq_password_text = QLineEdit()
		self.rabbitmq_password_text.setPlaceholderText('Example : Client')
		self.rabbitmq_password_text.setObjectName('general_text')
		self.rabbitmq_password_text.setFixedWidth(400)
		self.rabbitmq_password_text.setFixedHeight(50)
		self.rabbitmq_password.addWidget(self.rabbitmq_password_label)
		self.rabbitmq_password.addWidget(self.rabbitmq_password_text)
		self.rabbitmq_password.addStretch(1)
		self.rabbitmq_password.addSpacing(0)
		self.password_widget = QWidget()
		self.password_widget.setLayout(self.rabbitmq_password)
		self.manual = QRadioButton('Manual IP')
		self.manual.setChecked(True)
		self.manual.toggled.connect(lambda:self.button_state(self.manual))
		self.automatic = QRadioButton('Automatic IP')
		self.automatic.toggled.connect(lambda:self.button_state(self.automatic))
		self.rabbitmq_host = QHBoxLayout()
		self.rabbitmq_host_label = QLabel('RABBIT_MQ HOST              :   ')
		self.rabbitmq_host_label.setObjectName('general')
		self.rabbitmq_host_text = QLineEdit()
		self.rabbitmq_host_text.setPlaceholderText('Example : 127.0.0.1')
		self.rabbitmq_host_text.setObjectName('general_text')
		self.rabbitmq_host_text.setFixedWidth(400)
		self.rabbitmq_host_text.setFixedHeight(50)
		self.rabbitmq_host.addWidget(self.rabbitmq_host_label)
		self.rabbitmq_host.addWidget(self.rabbitmq_host_text)
		self.rabbitmq_host.addWidget(self.manual)
		self.rabbitmq_host.addWidget(self.automatic)
		self.rabbitmq_host.addStretch(1)
		self.rabbitmq_host.addSpacing(0)
		self.host_widget = QWidget()
		self.host_widget.setLayout(self.rabbitmq_host)
		self.rabbitmq_button = QHBoxLayout()
		self.save_button = QPushButton('Save')
		self.save_button.setObjectName('general')
		self.save_button.setFixedSize(200,50)
		self.save_button.clicked.connect(lambda:self.save_client_rabbitmq())
		self.edit_button = QPushButton('Edit')
		self.edit_button.setObjectName('general')
		self.edit_button.setFixedSize(200,50)
		self.edit_button.clicked.connect(lambda:self.edit_client_rabbitmq())
		self.rabbitmq_button.addWidget(self.save_button, alignment=Qt.AlignRight)
		self.rabbitmq_button.addWidget(self.edit_button, alignment=Qt.AlignRight)
		self.rabbitmq_button.addStretch(1)
		self.rabbitmq_button.addSpacing(0)
		self.button_widget = QWidget()
		self.button_widget.setLayout(self.rabbitmq_button)
		self.rabbitmq_creds.addWidget(rabbitmq_heading)
		self.rabbitmq_creds.addWidget(self.username_widget)
		self.rabbitmq_creds.addWidget(self.password_widget)
		self.rabbitmq_creds.addWidget(self.host_widget)
		self.rabbitmq_creds.addWidget(self.button_widget, alignment=Qt.AlignBottom)
		self.rabbitmq_creds.addStretch(1)
		self.rabbitmq_creds.addSpacing(0)
		self.rabbitmq_detail.setLayout(self.rabbitmq_creds)
		

		#####################################################################
		###################### LANGUAGE TAB #################################
		#####################################################################

		languages = QVBoxLayout()
		language_heading = QLabel('Select Languages')
		language_heading.setObjectName('heading')
		base = QHBoxLayout()
		self.all = QRadioButton('Select All')
		self.some = QRadioButton('Manual Selection')
		self.some.setChecked(True)
		self.all.toggled.connect(lambda:self.select_language_base(self.all))
		self.some.toggled.connect(lambda:self.select_language_base(self.some))
		base.addWidget(self.all, alignment=Qt.AlignCenter)
		base.addWidget(self.some, alignment=Qt.AlignCenter)
		base.addStretch(1)
		base.addSpacing(0)
		base_widget = QWidget()
		base_widget.setLayout(base)
		self.c = QCheckBox("C",self)
		self.cplusplus = QCheckBox('C++',self)
		self.python2 = QCheckBox('PYTHON-2',self)
		self.python3 = QCheckBox("PYTHON-3",self)
		self.java = QCheckBox('JAVA',self)
		self.general = QCheckBox('TEXT ANSWER',self)

		self.c.setObjectName('checkbox')
		self.cplusplus.setObjectName('checkbox')
		self.python2.setObjectName('checkbox')
		self.python3.setObjectName('checkbox')
		self.java.setObjectName('checkbox')
		self.general.setObjectName('checkbox')

		self.language_button = QHBoxLayout()
		self.save_language_button = QPushButton('Save')
		self.save_language_button.setObjectName('general')
		self.save_language_button.setFixedSize(200,50)
		self.save_language_button.clicked.connect(lambda:self.save_client_language())
		self.edit_language_button = QPushButton('Edit')
		self.edit_language_button.setObjectName('general')
		self.edit_language_button.setFixedSize(200,50)
		self.edit_language_button.clicked.connect(lambda:self.edit_client_language())
		self.language_button.addWidget(self.save_language_button, alignment=Qt.AlignRight)
		self.language_button.addWidget(self.edit_language_button, alignment=Qt.AlignRight)
		self.language_button.addStretch(1)
		self.language_button.addSpacing(0)
		self.language_button_widget = QWidget()
		self.language_button_widget.setLayout(self.language_button)

		languages.addWidget(language_heading)
		languages.addWidget(base_widget)
		languages.addWidget(self.c)
		languages.addWidget(self.cplusplus)
		languages.addWidget(self.python2)
		languages.addWidget(self.python3)
		languages.addWidget(self.java)
		languages.addWidget(self.general)
		languages.addWidget(self.language_button_widget)
		languages.addStretch(1)
		languages.addSpacing(0)

		self.language.setLayout(languages)



		#####################################################################
		######################## CONTEST TAB ################################
		#####################################################################

		contest_tab = QVBoxLayout()
		contest_heading = QLabel('Contest Details')
		contest_heading.setObjectName('heading')
		contest_name = QHBoxLayout()
		contest_name_label = QLabel('CONTEST NAME              :   ')
		contest_name_label.setObjectName('general')
		self.contest_name_text = QLineEdit()
		self.contest_name_text.setPlaceholderText('')
		self.contest_name_text.setObjectName('general_text')
		self.contest_name_text.setFixedWidth(400)
		self.contest_name_text.setFixedHeight(50)
		contest_name.addWidget(contest_name_label)
		contest_name.addWidget(self.contest_name_text)
		contest_name.addStretch(1)
		contest_name.addSpacing(0)
		contest_name_widget = QWidget()
		contest_name_widget.setLayout(contest_name)
		contest_theme = QHBoxLayout()
		contest_theme_label = QLabel('CONTEST THEME            :   ')
		contest_theme_label.setObjectName('general')
		self.contest_theme_text = QLineEdit()
		self.contest_theme_text.setPlaceholderText('')
		self.contest_theme_text.setObjectName('general_text')
		self.contest_theme_text.setFixedWidth(400)
		self.contest_theme_text.setFixedHeight(50)
		contest_theme.addWidget(contest_theme_label)
		contest_theme.addWidget(self.contest_theme_text)
		contest_theme.addStretch(1)
		contest_theme.addSpacing(0)
		contest_theme_widget = QWidget()
		contest_theme_widget.setLayout(contest_theme)
		client_key = QHBoxLayout()
		client_key_label = QLabel('CLIENT KEY                     :   ')
		client_key_label.setObjectName('general')
		self.client_key_text = QLineEdit()
		self.client_key_text.setPlaceholderText('')
		self.client_key_text.setObjectName('general_text')
		self.client_key_text.setFixedWidth(400)
		self.client_key_text.setFixedHeight(50)
		client_key.addWidget(client_key_label)
		client_key.addWidget(self.client_key_text)
		client_key.addStretch(1)
		client_key.addSpacing(0)
		client_key_widget = QWidget()
		client_key_widget.setLayout(client_key)
		contest_duration = QHBoxLayout()
		contest_duration_label = QLabel('CONTEST DURATION     :   ')
		contest_duration_label.setObjectName('general')
		self.contest_duration_text = QLineEdit()
		self.contest_duration_text.setPlaceholderText('Duration  -  HH:MM:SS')
		self.contest_duration_text.setObjectName('general_text')
		self.contest_duration_text.setFixedWidth(400)
		self.contest_duration_text.setFixedHeight(50)
		contest_duration.addWidget(contest_duration_label)
		contest_duration.addWidget(self.contest_duration_text)
		contest_duration.addStretch(1)
		contest_duration.addSpacing(0)
		contest_duration_widget = QWidget()
		contest_duration_widget.setLayout(contest_duration)
		start_time = QHBoxLayout()
		start_time_label = QLabel('CONTEST START TIME   :   ')
		start_time_label.setObjectName('general')
		self.start_time_text = QLineEdit()
		self.start_time_text.setPlaceholderText('12 Hour - HH:MM:SS')
		self.start_time_text.setObjectName('general_text')
		self.start_time_text.setFixedWidth(400)
		self.start_time_text.setFixedHeight(50)
		self.am_pm = QComboBox()
		self.am_pm.setFixedWidth(50)
		self.am_pm.setFixedHeight(40)
		self.am_pm.setObjectName('general')
		self.am_pm.addItem('AM')
		self.am_pm.addItem('PM')
		self.hour_12 = QRadioButton('12 Hour')
		self.hour_24 = QRadioButton('24 Hour')
		self.hour_12.setChecked(True)
		self.hour_12.toggled.connect(lambda:self.select_format(self.hour_12))
		self.hour_24.toggled.connect(lambda:self.select_format(self.hour_24))

		start_time.addWidget(start_time_label)
		start_time.addWidget(self.start_time_text)
		start_time.addWidget(self.am_pm)
		start_time.addWidget(self.hour_12)
		start_time.addWidget(self.hour_24)
		start_time.addStretch(1)
		start_time.addSpacing(0)
		start_time_widget = QWidget()
		start_time_widget.setLayout(start_time)

		client_key_button = QHBoxLayout()
		self.save_client_key_button = QPushButton('Save')
		self.save_client_key_button.setObjectName('general')
		self.save_client_key_button.setFixedSize(200,50)
		self.save_client_key_button.clicked.connect(lambda:self.save_contest_tab())
		self.edit_client_key_button = QPushButton('Edit')
		self.edit_client_key_button.setObjectName('general')
		self.edit_client_key_button.setFixedSize(200,50)
		self.edit_client_key_button.clicked.connect(lambda:self.edit_contest_tab())
		client_key_button.addWidget(self.save_client_key_button, alignment=Qt.AlignRight)
		client_key_button.addWidget(self.edit_client_key_button, alignment=Qt.AlignRight)
		client_key_button.addStretch(1)
		client_key_button.addSpacing(0)
		self.client_key_button_widget = QWidget()
		self.client_key_button_widget.setLayout(client_key_button)

		contest_tab.addWidget(contest_heading)
		contest_tab.addWidget(contest_name_widget)
		contest_tab.addWidget(contest_theme_widget)
		contest_tab.addWidget(client_key_widget)
		contest_tab.addWidget(contest_duration_widget)
		contest_tab.addWidget(start_time_widget)
		contest_tab.addWidget(self.client_key_button_widget)
		contest_tab.addStretch(1)
		contest_tab.addSpacing(0)

		self.contest.setLayout(contest_tab)


		######################################################################
		######################## FINAL TAB ###################################
		######################################################################


		self.tabs.addTab(self.rabbitmq_detail, "RabbitMQ Creds")
		self.tabs.addTab(self.problem_tab, "Add Problems")
		self.tabs.addTab(self.language, "Add Language")
		self.tabs.addTab(self.contest, "Contest Config")

		

		self.client_tab_layout.addWidget(self.tabs)
		self.client_tab.setLayout(self.client_tab_layout)
		self.client_tab.setObjectName('client_tab')
		return


	def save_contest_tab(self):
		if self.contest_name_text.text() == '':
			QMessageBox.warning(self,'Message','Contest Name cannot be empty')
		elif self.contest_theme_text.text() == '':
			QMessageBox.warning(self,'Message','Contest Theme cannot be empty')
		elif self.client_key_text.text() == '':
			QMessageBox.warning(self,'Message','Client Key cannot be empty')
		else:
			self.contest_name_text.setReadOnly(True)
			self.contest_theme_text.setReadOnly(True)
			self.client_key_text.setReadOnly(True)
			self.contest_duration_text.setReadOnly(True)
			self.start_time_text.setReadOnly(True)
			self.am_pm.setEnabled(False)
			self.hour_12.setEnabled(False)
			self.hour_24.setEnabled(False)
			QMessageBox.warning(self,'Message','Contest Details has been saved')

	def edit_contest_tab(self):
		self.contest_name_text.setReadOnly(False)
		self.contest_theme_text.setReadOnly(False)
		self.client_key_text.setReadOnly(False)
		self.contest_duration_text.setReadOnly(False)
		self.start_time_text.setReadOnly(False)
		self.am_pm.setEnabled(True)
		self.hour_12.setEnabled(True)
		self.hour_24.setEnabled(True)

	def select_format(self,button):
		if button.text() == '12 Hour':
			if button.isChecked() == True:
				self.am_pm.setEnabled(True)
				self.start_time_text.setText('')
				self.start_time_text.setPlaceholderText('12 Hour - HH:MM:SS')
		else:
			if button.isChecked() == True:
				self.am_pm.setEnabled(False)
				self.start_time_text.setText('')
				self.start_time_text.setPlaceholderText('24 Hour - HH:MM:SS')

	#################### SELECT ALL LANGUAGE OR MANUAL #####################

	def select_language_base(self,button):
		if button.text() == 'Select All':
			if button.isChecked() == True:
				self.c.setChecked(True)
				self.cplusplus.setChecked(True)
				self.python2.setChecked(True)
				self.python3.setChecked(True)
				self.java.setChecked(True)
				self.general.setChecked(True)
				self.c.setDisabled(True)
				self.cplusplus.setDisabled(True)
				self.python2.setDisabled(True)
				self.python3.setDisabled(True)
				self.java.setDisabled(True)
				self.general.setDisabled(True)
		else:
			if button.isChecked() == True:
				self.c.setChecked(False)
				self.cplusplus.setChecked(False)
				self.python2.setChecked(False)
				self.python3.setChecked(False)
				self.java.setChecked(False)
				self.general.setChecked(False)
				self.c.setEnabled(True)
				self.cplusplus.setEnabled(True)
				self.python2.setEnabled(True)
				self.python3.setEnabled(True)
				self.java.setEnabled(True)
				self.general.setEnabled(True)


	########################### SAVE RABBITMQ DETAILS FOR CLIENT ###########################
	def save_client_rabbitmq(self):
		if self.rabbitmq_username_text.text() == '':
			QMessageBox.warning(self,'Message','USERNAME cannot be empty')
		elif self.rabbitmq_password_text.text() == '':
			QMessageBox.warning(self,'Message','PASSWORD cannot be empty')
		elif self.rabbitmq_host_text.text() == '':
			QMessageBox.warning(self,'Message','HOST cannot be empty')
		else:
			self.rabbitmq_username_text.setReadOnly(True)
			self.rabbitmq_password_text.setReadOnly(True)
			self.rabbitmq_host_text.setReadOnly(True)
			self.manual.setDisabled(True)
			self.automatic.setDisabled(True)
			QMessageBox.warning(self,'Message','RabbitMQ Details has been saved')

	########################## EDIT RABBITMQ DETAILS FOR CLIENT ############################
	def edit_client_rabbitmq(self):
		self.rabbitmq_username_text.setReadOnly(False)
		self.rabbitmq_password_text.setReadOnly(False)
		self.rabbitmq_host_text.setReadOnly(False)
		self.manual.setEnabled(True)
		self.automatic.setEnabled(True)

	########################### SAVE LANGUAGE DETAILS FOR CLIENT ###########################
	def save_client_language(self):
		self.c.setDisabled(True)
		self.cplusplus.setDisabled(True)
		self.python2.setDisabled(True)
		self.python3.setDisabled(True)
		self.java.setDisabled(True)
		self.general.setDisabled(True)
		self.all.setDisabled(True)
		self.some.setDisabled(True)

	########################### EDIT LANGUAGE DETAILS FOR CLIENT ###########################
	def edit_client_language(self):
		self.c.setEnabled(True)
		self.cplusplus.setEnabled(True)
		self.python2.setEnabled(True)
		self.python3.setEnabled(True)
		self.java.setEnabled(True)
		self.general.setEnabled(True)
		self.all.setEnabled(True)
		self.some.setEnabled(True)

	########################## FETCH IP ADDRESS AUTOMATICALLY ################################
	def get_ip_address(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		return s.getsockname()[0]

	################################## BUTTON STATE SIGNAL ###################################
	def button_state(self,button):
		if button.text() == 'Manual IP':
			if button.isChecked() == True:
				self.rabbitmq_host_text.setReadOnly(False)
				self.rabbitmq_host_text.setText('')
				self.rabbitmq_host_text.setPlaceholderText('Example : 127.0.0.1')
		else:
			if button.isChecked() == True:
				ip = self.get_ip_address()
				self.rabbitmq_host_text.setText(ip)
				self.rabbitmq_host_text.setReadOnly(True)


	def call_gui(self):
		pass

	################################### CLOSE BUTTON CLICKED ####################################
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

		# button_yes.setStyleSheet(open('Elements/style.qss', "r").read())
		# button_no.setStyleSheet(open('Elements/style.qss', "r").read())

		custom_close_box.exec_()

		if custom_close_box.clickedButton() == button_yes:
			event.accept()
		elif custom_close_box.clickedButton() == button_no:
			event.ignore()



class setup_window(contest_setup):
	def __init__(self):
		app = QApplication(sys.argv)
		app.setStyleSheet(open('../Elements/style.qss', "r").read())
		app.setStyle("Fusion")

		client_app = contest_setup()

		app.aboutToQuit.connect(self.closeEvent)

		client_app.showMaximized()

		app.exec_()

setup_window()
