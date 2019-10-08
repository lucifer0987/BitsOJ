import sqlite3
import sys
import random
import string

global client_id_counter

class manage_database():
	cur = None
	conn = None
	def initialize_database():
		try:
			conn = sqlite3.connect('server_database.db', check_same_thread = False)
			cur = conn.cursor()
			manage_database.cur = cur
			manage_database.conn = conn
		except Exception as error:
			print ("[ CRITICAL ERROR ]Database connection error : " + str(error))
		
		try:	
			cur.execute("create table if not exists accounts(user_name varchar2(10) PRIMARY KEY, password varchar2(15), client_type varchar2(10))")
			cur.execute("create table if not exists connected_clients(client_id varchar2(3) PRIMARY KEY, user_name varchar2(10), password varchar2(10))")
			cur.execute("create table if not exists submissions(run_id varchar2(5) PRIMARY KEY, client_id varchar2(3), language varchar2(3), source_file varchar2(30),problem_code varchar(4), verdict varchar2(2), timestamp text)")
			cur.execute("create table if not exists scoreboard(client_id varchar2(3), problems_solved integer, total_time text)")
		except Exception as error:
			print("[ CRITICAL ERROR ] Table creation error : " + str(error))

		return conn, cur

	def reset_database(conn):
		cur = conn.cursor()
		try:
			cur.execute("drop table if exists accounts")
			cur.execute("drop table if exists submissions")
			cur.execute("drop table if exists scoreboard")
			cur.execute("drop table if exists connected_clients")
		except:
			print("Database drop error")



	def insert_user(user_name, password, ctype, cur, conn):
		try:
			cur.execute("INSERT INTO accounts VALUES (?,?,?)",(user_name, password, ctype,))
			conn.commit()
		except Exception as error:
			print("[ CRITICAL ERROR ] Database insertion error : " + str(error))

	def get_cursor():
		return manage_database.cur

	def get_connection_object():
		return manage_database.conn

class previous_data(manage_database):
	def get_last_run_id():
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT max(run_id) FROM submissions")
			data =  cur.fetchall()

			if(data[0][0] == ''):
				return 0
			else:
				return int(data[0][0])
		except:
			return 0

	def get_last_client_id():
		global client_id_counter
		try:
			cur = manage_database.get_cursor()
			cur.execute("SELECT max(client_id) FROM connected_clients")
			data =  cur.fetchall()
			if(data[0][0] != ''):
				client_id_counter = int(data[0][0])
			else:
				client_id_counter = 1

		except:
			client_id_counter = 1


class client_authentication(manage_database):

	#This function validates the (user_name, password, client_id) in the database.
	def validate_client(user_name, password):
		#Validate client in database
		cur = manage_database.get_cursor()
		cur.execute("SELECT exists(SELECT * FROM accounts WHERE user_name = ? and password = ?)", (user_name,password,))
		validation_result = cur.fetchall()
		
		if validation_result[0][0] == 1:
			return True
		else:
			return False

	#This function generates a new client_id for new connections
	def generate_new_client_id():
		global client_id_counter
		client_id = str("{:03d}".format(client_id_counter))
		client_id_counter = client_id_counter + 1
		return client_id

	def add_connected_client(client_id, user_name, password):
		cur = manage_database.get_cursor()
		conn = manage_database.get_connection_object()
		try:
			cur.execute("INSERT INTO connected_clients values(?, ?, ?)", (client_id, user_name, password, ))
		except:
			pass
		conn.commit()
		return	
		
	# Get client_id when user_name is known
	def get_client_id(user_name):
		cur = manage_database.get_cursor()
		try:
			cur.execute("SELECT client_id FROM connected_clients WHERE user_name = ?", (user_name, ))
			client_id = cur.fetchall()
			return client_id[0][0]
		except Exception as error:
			print("[ ERROR ] : The user does not have a client id yet.")

	# Get user_name when client_id is known
	def get_client_username(client_id):
		cur = manage_database.get_cursor()
		try:
			cur.execute("SELECT user_name FROM connected_clients WHERE client_id = ?", (client_id, ))
			client_username = cur.fetchall()
			return client_username[0][0]
		except Exception as error:
			print("[ ERROR ] : Could not fetch username.")

	# Check if a client with given client_id is connected in the system
	def check_connected_client(user_name ):
		cur = manage_database.get_cursor()
		cur.execute("SELECT exists(SELECT * FROM connected_clients WHERE user_name = ?)", (user_name,))
		existence_result = cur.fetchall()

		if existence_result[0][0] == 1:
			return True
		else:
			return False


class submissions_management(manage_database):
	def insert_submission(run_id, client_id, language, source_file_name, problem_code, verdict, timestamp):
		#cur.execute("create table submissions(run_id varchar2(5) PRIMARY KEY, client_id varchar2(3), language varchar2(3), source_file varchar2(30), verdict varchar2(2), timestamp text, problem_code varchar(4))")
		cur = manage_database.get_cursor()
		conn = manage_database.get_connection_object()
		try:
			cur.execute("INSERT INTO submissions values(?, ?, ?, ?, ?, ?, ?)", (run_id, client_id, language, source_file_name, problem_code, verdict, timestamp, ))
			conn.commit()
		except Exception as error:
			print("[ ERROR ] Could not insert into submission : " + str(error))
		return

	def update_submission_status(run_id, verdict):
		cur = manage_database.get_cursor()
		conn = manage_database.get_connection_object()
		try:
			cur.execute("UPDATE submissions SET verdict = ? WHERE run_id = ?", (verdict, run_id,))
			conn.commit()
		except Exception as error:
			print("[ ERROR ] Could not update submission submission : " + str(error))
		return

	def view_submissions():
		cur = manage_database.get_cursor()
		try:
			cur.execute("SELECT * FROM submissions")
			submission_data = cur.fetchall()
			return submission_data
		except:
			print("[ ERROR ] Could not view submissions")
			return Null

class user_management(manage_database):
	def generate_n_users(no_of_clients, no_of_judges, password_type):
		cur = manage_database.get_cursor()
		# Get max client and judge usernames till now
		try:
			cur.execute("SELECT max(user_name) from accounts where client_type = 'CLIENT'")
			max_client_username = int(cur.fetchall()[0][0][4:])
		except:
			max_client_username = 0

		try:
			cur.execute("SELECT max(user_name) from accounts where client_type = 'JUDGE'")
			max_judge_username = int(cur.fetchall()[0][0][5:])
		except:
			max_judge_username = 0
		
		client_list = user_management.generate_clients(no_of_clients, max_client_username)
		judge_list = user_management.generate_judges(no_of_judges, max_judge_username)
		client_pass_list = user_management.generate_passwords(max_client_username, no_of_clients, password_type)
		judge_pass_list = user_management.generate_passwords(max_judge_username, no_of_judges, password_type)

		# INSERTIONS INTO DATABASE [ CRITICAL SETION ]
		cur.execute("begin")
		try:
			for i in range(0, no_of_clients):
				cur.execute("INSERT into accounts values (?, ?, ? )" , (client_list[i], client_pass_list[i], 'CLIENT'))

			for i in range(0, no_of_judges):
				cur.execute("INSERT into accounts values (?, ?, ? )" , (judge_list[i], judge_pass_list[i], 'JUDGE'))

			cur.execute("commit")

		except:
			print('[ CRITICAL ] Database insertion error! Roll back')
			cur.execute("rollback")

		# INSERTION FINISHED
		return

	def generate_clients(no_of_clients, max_so_far):
		client_list = list()
		for i in range(max_so_far+1, max_so_far+no_of_clients+1):
			client_list.append('team' + str(i))

		return client_list
	
	def generate_judges(no_of_judges, max_so_far):
		judge_list = list()
		for i in range(max_so_far+1, max_so_far+no_of_judges+1):
			judge_list.append('judge' + str(i))
		return judge_list
		
	def generate_passwords(prev, number, type):
		password_list = list()
		chars=string.ascii_uppercase + string.digits+string.ascii_lowercase
		for i in range(0, number):
			if type == 'Easy':
				password = 'Bits'+str(i + prev + 1)
			elif type == 'Random':
				password = ''.join(random.choice(chars) for _ in range(6))

			password_list.append(password)
		return password_list

	def delete_user(user_name):
		try:
			cur = manage_database.get_cursor()
			conn = manage_database.get_connection_object()
			cur.execute("DELETE FROM accounts WHERE user_name = ?",(user_name,))
			conn.commit()
		except Exception as error:
			print("[ CRITICAL ERROR ] Database deletion error : " + str(error))


