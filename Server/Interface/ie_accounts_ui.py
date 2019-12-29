from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from database_management import user_management
from account_io import *

class ie_accounts_ui(QMainWindow):
	filename = './accounts.xlsx'
	def __init__(self, data_changed_flags, parent=None):
		super(ie_accounts_ui, self).__init__(parent)
		ie_accounts_ui.data_changed_flags = data_changed_flags
		self.setGeometry(700, 350, 300, 200)
		self.setWindowTitle('Import/Export Accounts')
		self.setFixedSize(500, 300)
		main = self.add_ie_accounts_ui()
		self.setCentralWidget(main)
		self.setWindowFlag(Qt.WindowCloseButtonHint, False)
		return

	def add_ie_accounts_ui(self):
		label1 = QLabel('File Location: ')
		file_entry = QLineEdit()
		file_entry.setText(ie_accounts_ui.filename)
		file_entry.setPlaceholderText('Enter file name (.xlsx Files only)')
		top_layout = QHBoxLayout()
		top_layout.addWidget(label1)
		top_layout.addWidget(file_entry)
		top_widget = QWidget()
		top_widget.setLayout(top_layout)
		
		import_button = QPushButton('Import')
		import_button.setFixedSize(100, 30)
		import_button.clicked.connect(
			lambda:ie_accounts_ui.import_manager(
				self, 
				file_entry.text()
			)
		)
		export_button = QPushButton('Export')
		export_button.setFixedSize(100, 30)
		export_button.clicked.connect(
			lambda:ie_accounts_ui.export_manager(
				self, 
				file_entry.text()
			)
		)
		cancel_button = QPushButton('Close')
		cancel_button.setFixedSize(100, 30)
		cancel_button.clicked.connect(
			lambda:ie_accounts_ui.cancel(
				self
			)
		)
		cancel_button.setDefault(True)
		button_layout = QHBoxLayout()
		button_layout.addWidget(import_button)
		button_layout.addWidget(export_button)
		button_layout.addWidget(cancel_button)
		button_widget = QWidget()
		button_widget.setLayout(button_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(top_widget)
		main_layout.addWidget(button_widget)
		main = QWidget()
		main.setLayout(main_layout)

		import_button.setObjectName('interior_button')
		export_button.setObjectName('interior_button')
		cancel_button.setObjectName('interior_button')
		label1.setObjectName('main_screen_content')
		main.setObjectName('account_window')
		return main
		
	def import_manager(self, filename):
		if filename == ''  or ie_accounts_ui.validate_filename(filename) == 0:
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Information)
			info_box.setWindowTitle('Alert')
			info_box.setText('Please enter a valid file path/name.')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return

		print('[ ACCOUNT ] Import Accounts from ' + filename )
		u_list, p_list, t_list = io_manager.read_file(filename)
		if len(u_list) != 0:
			user_management.add_sheet_accounts(u_list, p_list, t_list)
		elif p_list[0] != 'FNF':
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Error')
			info_box.setText('File could not be read.')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return
		else:
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Critical)
			info_box.setWindowTitle('Error')
			info_box.setText('File not found, or is locked.')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return
		# Reset the critical section flag
		ie_accounts_ui.data_changed_flags[4] = 0
		# Indicate new insertions in accounts
		ie_accounts_ui.data_changed_flags[5] = 1
		self.close()

	def export_manager(self, filename):
		if filename == '' or ie_accounts_ui.validate_filename(filename) == 0:
			info_box = QMessageBox()
			info_box.setIcon(QMessageBox.Information)
			info_box.setWindowTitle('Alert')
			info_box.setText('Please enter a valid file path/name.')
			info_box.setStandardButtons(QMessageBox.Ok)
			info_box.exec_()
			return

		
		print('[ ACCOUNT ] Export Accounts to ' + filename)
		u_list, p_list, t_list = user_management.get_sheet_accounts()
		io_manager.write_file(u_list, p_list, t_list)
		# Reset the critical section flag
		ie_accounts_ui.data_changed_flags[4] = 0
		# Indicate new insertions in accounts
		ie_accounts_ui.data_changed_flags[5] = 1
		self.close()

	def cancel(self):
		# Reset the critical section flag
		ie_accounts_ui.data_changed_flags[4] = 0
		self.close()

	def validate_filename(filename):
		if filename[-5:] == '.xlsx':
			return 1
		return 0