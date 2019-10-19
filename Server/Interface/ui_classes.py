from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import user_management, query_management
import json 

class ui_widgets:

	def accounts_ui(self):
		heading = QLabel('Manage Accounts')
		heading.setObjectName('main_screen_heading')

		create_accounts_button = QPushButton('Create Accounts', self)
		create_accounts_button.setFixedSize(200, 50)
		create_accounts_button.clicked.connect(self.create_accounts)
		create_accounts_button.setObjectName("topbar_button")

		delete_account_button = QPushButton('Delete Account', self)
		delete_account_button.setFixedSize(200, 50)
		delete_account_button.clicked.connect(lambda:self.delete_account(accounts_table.selectionModel().selectedRows()))
		delete_account_button.setObjectName("topbar_button")

		accounts_model = self.manage_models(self.db, 'accounts')
		accounts_model.setHeaderData(0, Qt.Horizontal, 'Username')
		accounts_model.setHeaderData(1, Qt.Horizontal, 'Password')
		accounts_model.setHeaderData(2, Qt.Horizontal, 'Type')
		accounts_table = self.generate_view(accounts_model)

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(create_accounts_button)
		head_layout.addWidget(delete_account_button)
		head_layout.setStretch(0, 80)
		head_layout.setStretch(1, 10)
		head_layout.setStretch(2, 10)
		head_widget = QWidget()
		head_widget.setLayout(head_layout)


		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(accounts_table)
		
		main_layout.setStretch(0,10)
		main_layout.setStretch(1,90)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, accounts_model

	def submissions_ui(self):
		heading = QLabel('All Runs')
		heading.setObjectName('main_screen_heading')

		allow_submission_label = QLabel('Allow submissions : ')
		allow_submission_label.setObjectName('main_screen_content')

		submission_allowed_flag = self.check_submission_allowed()
		
		allow_submission_button = QCheckBox('')
		allow_submission_button.setFixedSize(30, 30)
		allow_submission_button.setChecked(submission_allowed_flag)
		allow_submission_button.stateChanged.connect(self.allow_submissions_handler)

		submission_model = self.manage_models(self.db, 'submissions')

		submission_model.setHeaderData(0, Qt.Horizontal, 'Run ID')
		submission_model.setHeaderData(1, Qt.Horizontal, 'Local ID')
		submission_model.setHeaderData(2, Qt.Horizontal, 'Client ID')
		submission_model.setHeaderData(3, Qt.Horizontal, 'Language')
		submission_model.setHeaderData(4, Qt.Horizontal, 'Source File')
		submission_model.setHeaderData(5, Qt.Horizontal, 'Problem Code')
		submission_model.setHeaderData(6, Qt.Horizontal, 'Status')
		submission_model.setHeaderData(7, Qt.Horizontal, 'Time')

		submission_table = self.generate_view(submission_model)

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(allow_submission_label)
		head_layout.addWidget(allow_submission_button)
		head_layout.setStretch(0, 80)
		head_layout.setStretch(1, 10)
		head_layout.setStretch(2, 10)
		
		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(submission_table)
		main_layout.setStretch(0,5)
		main_layout.setStretch(1,95)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		main.show()
		return main, submission_model


	def client_ui(self):
		heading = QLabel('Connected Clients')
		heading.setObjectName('main_screen_heading')

		allow_login_label = QLabel('Allow Logins : ')
		allow_login_label.setObjectName('main_screen_content')

		login_allowed_flag = self.check_login_allowed()
		
		allow_login_button = QCheckBox('')
		allow_login_button.setFixedSize(30, 30)
		allow_login_button.setChecked(login_allowed_flag)
		allow_login_button.stateChanged.connect(self.allow_login_handler)

		client_model = self.manage_models(self.db, 'connected_clients')
		client_model.setHeaderData(0, Qt.Horizontal, 'Client ID')
		client_model.setHeaderData(1, Qt.Horizontal, 'Username')
		client_model.setHeaderData(2, Qt.Horizontal, 'Password')

		client_view = self.generate_view(client_model)

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(allow_login_label)
		head_layout.addWidget(allow_login_button)
		head_layout.setStretch(0, 80)
		head_layout.setStretch(1, 10)
		head_layout.setStretch(2, 10)
		

		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(client_view)
		main_layout.setStretch(0,5)
		main_layout.setStretch(1,95)		

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, client_model

	def judge_ui(self):
		heading = QLabel('Manage Judges')
		heading.setObjectName('main_screen_heading')

		#judge_model = self.manage_models(self.db, )

		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addStretch(5)

		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def query_ui(self):
		heading = QLabel('All Clarifications')
		heading.setObjectName('main_screen_heading')

		reply_button = QPushButton('Reply')
		reply_button.setFixedSize(200, 50)
		reply_button.clicked.connect(lambda: self.query_reply(query_view.selectionModel().currentIndex().row()))
		reply_button.setObjectName("topbar_button")

		query_model = self.manage_models(self.db, 'queries')
		query_model.setHeaderData(0, Qt.Horizontal, 'Query ID')
		query_model.setHeaderData(1, Qt.Horizontal, 'Client ID')
		query_model.setHeaderData(2, Qt.Horizontal, 'Query')
		query_model.setHeaderData(3, Qt.Horizontal, 'Response')

		query_view = self.generate_view(query_model)

		head_layout = QHBoxLayout()
		head_layout.addWidget(heading)
		head_layout.addWidget(reply_button)
		head_widget = QWidget()
		head_widget.setLayout(head_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(head_widget)
		main_layout.addWidget(query_view)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, query_model


	def leaderboard_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Leaderboard')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def problem_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Manage Problems')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def language_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Manage Languages')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def stats_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Server Stats')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def settings_ui(self):
		heading = QLabel('Server Settings')
		heading.setObjectName('main_screen_heading')

		# Contest Time Management
		## Contest Time Settings Label:
		contest_time_label = QLabel('Contest Time Settings:')
		contest_time_label.setObjectName('main_screen_sub_heading')

		# Set contest time 
		
		contest_duration_label = QLabel('> Contest Duration: ')
		contest_duration_label.setObjectName('main_screen_content')
		contest_duration_label.setFixedSize(200, 20)

		contest_time_entry = QLineEdit()
		contest_time_entry.setText(self.config["Contest Duration"])
		contest_time_entry.setPlaceholderText('HH:MM')
		contest_time_entry.setFixedSize(80, 30)
		contest_time_entry.setToolTip('You will not be able to edit this when contest starts.')

		contest_time_layout = QHBoxLayout()
		contest_time_layout.addWidget(contest_duration_label)
		contest_time_layout.addWidget(contest_time_entry)
		contest_time_layout.addStretch(1)
		contest_time_layout.setSpacing(5)
		contest_time_layout.setContentsMargins(5, 0, 10, 0)
		contest_time_widget = QWidget()
		contest_time_widget.setLayout(contest_time_layout)

		contest_extension_label = QLabel("> Extend/Shorten contest by: ")
		contest_extension_label.setObjectName('main_screen_content')
		minutes_label = QLabel(" Minutes")
		minutes_label.setObjectName('main_screen_content')

		change_time_entry = QSpinBox()
		change_time_entry.setMinimum(-30)
		change_time_entry.setMaximum(30)
		change_time_entry.setValue(0)
		change_time_entry.setToolTip('Extend or Shorten contest (in minutes.)')


		change_time_layout = QHBoxLayout()
		change_time_layout.addWidget(contest_extension_label)
		change_time_layout.addWidget(change_time_entry)
		change_time_layout.addWidget(minutes_label)
		change_time_layout.addStretch(1)
		change_time_layout.setSpacing(5)
		change_time_layout.setContentsMargins(5, 0, 10, 0)
		change_time_widget = QWidget()
		change_time_widget.setLayout(change_time_layout)


		# Start, Stop, Pause contest
		set_button = QPushButton('Set')
		set_button.setFixedSize(70, 25)
		set_button.setObjectName('interior_button')
		#set_button.clicked.connect(self.contest_settings)
		start_button = QPushButton('Start', self)
		start_button.setFixedSize(70, 25)
		start_button.setObjectName('interior_button')
		start_button.clicked.connect(lambda: ui_widgets.preprocess_contest_broadcasts(self, 'START', contest_time_entry.text()))

		update_button = QPushButton('Update', self)
		update_button.setFixedSize(70, 25)
		update_button.setObjectName('interior_button')
		update_button.clicked.connect(lambda: ui_widgets.preprocess_contest_broadcasts(self, 'UPDATE'))

		stop_button = QPushButton('Stop', self)
		stop_button.setFixedSize(70, 25)
		stop_button.setObjectName('interior_button')
		stop_button.clicked.connect(lambda: ui_widgets.preprocess_contest_broadcasts(self, 'STOP'))
		
		
		contest_buttons_layout = QHBoxLayout()
		contest_buttons_layout.addWidget(set_button)
		contest_buttons_layout.addWidget(start_button)
		contest_buttons_layout.addWidget(update_button)
		contest_buttons_layout.addWidget(stop_button)

		contest_buttons_layout.addStretch(1)
		contest_buttons_layout.setSpacing(10)
		contest_buttons_widget = QWidget()
		contest_buttons_widget.setLayout(contest_buttons_layout)

		time_management_layout = QVBoxLayout()
		time_management_layout.addWidget(contest_time_label)
		time_management_layout.addWidget(contest_time_widget)
		time_management_layout.addWidget(change_time_widget)
		time_management_layout.addWidget(contest_buttons_widget)
		time_management_widget = QWidget()
		time_management_widget.setLayout(time_management_layout)
		time_management_widget.setObjectName('content_box')



		main_layout = QVBoxLayout()
		main_layout.addWidget(heading)
		main_layout.addWidget(time_management_widget)
		main_layout.setSpacing(10)
		main_layout.addStretch(1)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main, contest_time_entry

	def preprocess_contest_broadcasts(self, signal, extra_data = 'NONE'):
		if signal == 'START':
			self.process_event('START', extra_data)	#In interface file
		elif signal == 'UPDATE':
			self.process_event('UPDATE', extra_data)
		elif signal == 'STOP':
			self.process_event('STOP', extra_data)

		return


	def reports_ui(self):
		main_layout = QVBoxLayout()
		heading = QLabel('Generate Report')
		heading.setObjectName('main_screen_heading')

		main_layout.addWidget(heading)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


	def about_us_ui(self):
		head1 = QLabel('Made with <3 by team Bitwise')
		head1.setObjectName('about_screen_heading')
		head1.setAlignment(Qt.AlignCenter)

		head2 = QLabel('Guess what! The BitsOJ project is open source!!! ')
		head2.setObjectName('main_screen_content')
		head2.setAlignment(Qt.AlignCenter)

		head3 = QLabel('Contribute at https://github.com/peeesspee/BitsOJ')
		head3.setObjectName('main_screen_content')
		head3.setAlignment(Qt.AlignCenter)



		main_layout = QVBoxLayout()
		main_layout.addWidget(head1)
		main_layout.addWidget(head2)
		main_layout.addWidget(head3)
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		main.setObjectName("main_screen");
		return main


class new_accounts_ui(QMainWindow):
	pwd_type = 'Random'
	client_no = 0
	judge_no = 0
	data_changed_flags = ''
	
	def __init__(self, data_changed_flags, parent=None):
		super(new_accounts_ui, self).__init__(parent)
		self.data_changed_flags = data_changed_flags
		self.setWindowTitle('Add new accounts')
		self.setFixedSize(300, 200)
		main = self.add_new_accounts_ui()
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)


		return

	def combo_box_data_changed(text):
		new_accounts_ui.pwd_type = str(text)

	def client_updater(text):
		new_accounts_ui.client_no = int(text)
		return
	def judge_updater(text):
		new_accounts_ui.judge_no = int(text)
		return

	def add_new_accounts_ui(self):
		label1 = QLabel('Clients')

		client_entry = QSpinBox()
		client_entry.setMinimum(0)
		client_entry.setMaximum(500)
		client_entry.valueChanged.connect(new_accounts_ui.client_updater)
		
		# client_entry.textEdited.connect(new_accounts_ui.client_updater)
		# client_entry.setInputMask('9000')

		label2 = QLabel('Judges')

		judge_entry = QSpinBox()
		judge_entry.setMinimum(0)
		judge_entry.setMaximum(10)
		judge_entry.valueChanged.connect(new_accounts_ui.judge_updater)
		# judge_entry.textEdited.connect(new_accounts_ui.judge_updater)
		# judge_entry.setInputMask('9000')

		label3 = QLabel('Password Type:')

		password_type_entry = QComboBox()
		password_type_entry.addItem('Random')
		password_type_entry.addItem('Easy')
		password_type_entry.activated[str].connect(new_accounts_ui.combo_box_data_changed)

		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(200, 50)
		confirm_button.clicked.connect(lambda:new_accounts_ui.final_account_status(self))
		confirm_button.setDefault(True)
		
		
		layout = QGridLayout()
		layout.addWidget(label1, 0, 0)
		label1.setStyleSheet('''Qlabel{text-align : center; }''')
		layout.addWidget(client_entry, 0, 1)
		layout.addWidget(label2, 1, 0)
		layout.addWidget(judge_entry, 1, 1)
		layout.addWidget(label3, 2, 0)
		layout.addWidget(password_type_entry, 2, 1)


		layout.setColumnMinimumWidth(0,50)
		layout.setColumnMinimumWidth(1,50)
		layout.setColumnStretch(0, 1)
		layout.setColumnStretch(1, 1)
		layout.setRowStretch(0, 1)
		layout.setRowStretch(1, 1)
		layout.setVerticalSpacing(10)
		upper_widget = QWidget()
		upper_widget.setLayout(layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(upper_widget)
		main_layout.addWidget(confirm_button)
		
		main = QWidget()
		main.setLayout(main_layout)

		label1.setObjectName('account_label')
		label2.setObjectName('account_label')
		label3.setObjectName('account_label')
		client_entry.setObjectName('account_spinbox')
		judge_entry.setObjectName('account_spinbox')
		password_type_entry.setObjectName('account_combobox')
		confirm_button.setObjectName('account_button')
		main.setObjectName('account_window')
		
		return main
		
	def final_account_status(self):
		user_management.generate_n_users(new_accounts_ui.client_no, new_accounts_ui.judge_no, new_accounts_ui.pwd_type)
		# Reset the critical section flag
		self.data_changed_flags[4] = 0
		# Indicate new insertions in accounts
		self.data_changed_flags[5] = 1
		self.close()

class query_reply_ui(QMainWindow):
	button_mode = 1
	query = ''
	query_id = ''
	client_id = ''
	def __init__(self, data_changed_flags,data_to_client, query, client_id, query_id, parent=None):
		super(query_reply_ui, self).__init__(parent)
		query_reply_ui.button_mode = 1

		self.data_changed_flags = data_changed_flags
		self.data_to_client = data_to_client
		query_reply_ui.query = query
		query_reply_ui.query_id = query_id
		query_reply_ui.client_id = client_id

		self.setWindowTitle('Reply')
		self.setFixedSize(400,400)
		main = self.main_query_reply_ui()
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		return

	def main_query_reply_ui(self):
		query_heading = QLabel('New Clarification')
		query_sub_heading = QLabel('Query:')
		response_sub_heading = QLabel('Response:')
		
		query_text = QTextEdit()
		query_text.setText(query_reply_ui.query)
		query_text.setReadOnly(True)

		response_entry = QTextEdit()
		response_entry.setPlaceholderText('Max. 500 Characters')

		
		broadcast_setting_label = QLabel('Reply to: ')
		send_to_client_rbutton = QRadioButton('Client')
		send_to_all_rbutton = QRadioButton('All')
		send_to_client_rbutton.setChecked(True)
		send_to_all_rbutton.setChecked(False)
		send_to_client_rbutton.toggled.connect(lambda: query_reply_ui.send_mode_setter(self, send_to_client_rbutton))
		send_to_all_rbutton.toggled.connect(lambda: query_reply_ui.send_mode_setter(self, send_to_all_rbutton))

		radiobutton_layout = QHBoxLayout()
		radiobutton_layout.addWidget(broadcast_setting_label)
		radiobutton_layout.addWidget(send_to_client_rbutton)
		radiobutton_layout.addWidget(send_to_all_rbutton)
		radiobutton_layout.addStretch(1)
		radiobutton_layout.setSpacing(50)
		
		radiobutton_widget = QWidget()
		radiobutton_widget.setLayout(radiobutton_layout)
		radiobutton_widget.setContentsMargins(25,0,0,0)


		confirm_button = QPushButton('Confirm')
		confirm_button.setFixedSize(150, 30)
		confirm_button.clicked.connect(lambda:query_reply_ui.final_status(self, response_entry.toPlainText()))
		confirm_button.setDefault(True)

		cancel_button = QPushButton('Cancel')
		cancel_button.setFixedSize(150, 30)
		cancel_button.clicked.connect(lambda:query_reply_ui.cancel(self))
		cancel_button.setDefault(True)

		button_layout = QHBoxLayout()
		button_layout.addWidget(confirm_button)
		button_layout.addWidget(cancel_button)
		button_layout.addStretch(1)
		#button_layout.setSpacing(5)

		button_widget = QWidget()
		button_widget.setLayout(button_layout)


		main_layout = QVBoxLayout()
		main_layout.addWidget(query_heading)
		main_layout.addWidget(query_sub_heading)
		main_layout.addWidget(query_text)
		main_layout.addWidget(response_sub_heading)
		main_layout.addWidget(response_entry)
		main_layout.addWidget(radiobutton_widget)
		main_layout.addWidget(button_widget)
		main = QWidget()
		main.setLayout(main_layout)

		confirm_button.setObjectName('account_button')
		cancel_button.setObjectName('account_button')
		query_heading.setObjectName('main_screen_heading')
		broadcast_setting_label.setObjectName('main_screen_content')
		main.setObjectName('account_window')
		query_sub_heading.setObjectName('main_screen_sub_heading')
		response_sub_heading.setObjectName('main_screen_sub_heading')
		send_to_all_rbutton.setObjectName('interior_rbutton')
		send_to_client_rbutton.setObjectName('interior_rbutton')
		return main

	def send_mode_setter(self, rbutton):
		if rbutton.text() == 'Client':
			if rbutton.isChecked() == True:
				query_reply_ui.button_mode = 1
		else:
			if rbutton.isChecked() == True:
				query_reply_ui.button_mode = 2

		return

	def final_status(self, response):
		if query_reply_ui.button_mode == 2:
			send_type = 'Broadcast'
		else:
			send_type = 'Client'
		message ={
		'Code' : 'QUERY',
		'Query' : query_reply_ui.query,
		'Response' : response,
		'Mode' : send_type,
		'Query ID' : query_reply_ui.query_id,
		'Client ID' : query_reply_ui.client_id
		}
		message = json.dumps(message)
		self.data_to_client.put(message)
		query_management.update_query(query_reply_ui.query_id, response)
		self.data_changed_flags[8] = 0
		self.data_changed_flags[9] = 1
		self.close()

	def cancel(self):
		self.data_changed_flags[8] = 0
		self.close()

 