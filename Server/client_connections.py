import pika
from database_management import client_authentication

class manage_clients():
	channel = ''

	# This function continously listens for client messages 
	def listen_clients(channel1):
		manage_clients.channel = channel1
		# Clients send requests on client_requests
		# As soon as a new message is recieved, it is sent to client_message_handler for further processing
		channel1.basic_consume(queue = 'client_requests', on_message_callback = manage_clients.client_message_handler, auto_ack = True)
		channel1.start_consuming()

	# This function works on client messages and passes them on to their respective handler function
	def client_message_handler(ch, method, properties, body):
		# Decode the message sent by client
		# First 5 characters contain metadata
		client_message = str(body.decode("utf-8"))
		
		print("[ PING ] Recieved a new client message.")
		print (client_message)
		if client_message[0:6] == 'Login ':
			manage_clients.client_login_handler(client_message[6:])

	# This function handles all client login requests
	def client_login_handler(client_message):
		# Client sends the username, password, clientID as "username+password+clientID", so we split it.
		# Default value of clientID is "Null" (String)
		try:
			client_username, client_password, client_id = client_message.split(' ')
		except Exception as error:
			print("[ ERROR ] Client data parsing error : " + str(error))
			print("[ DEBUG ] Client message was : " + str(client_message))

		print("[ LOGIN ] " + "[ " + client_id + " ] > " + client_username + "@" + client_password)

		
		manage_clients.channel.queue_bind(exchange = "connection_manager", queue = client_username)
		# Validate the client from the database
		status = client_authentication.validate_client(client_username, client_password)

		# If login is successful:
		if status == True:
			# If client logs in for the first time:
			if client_id == "Null":
				client_id = client_authentication.generate_new_client_id()

			print("[ " + client_username + " ] Assigned : [ " + client_id + " ]")

			# Reply to be sent to client
			server_message = "Hello buddy!!"
			message = "Valid+" +  client_id + "+" + server_message

			print("[ SENT ] " + message)

			# The client listens on its own queue, whose name = client_username (Hard-coded)
			# This queue is declared in the client.py file
			manage_clients.channel.basic_publish(exchange = 'connection_manager', routing_key = client_username, body = message)

		# If login is not successful:
		elif status == False:
			print("[ " + client_username + " ] NOT verified.")

			# Reply Invalid credentials to client
			# Every response sent to client has 5 initial characters which specify what server is going to talk about.
			# Invld signifies an invalid login attempt.
			message = "Invld"
			print(client_username)
			try:
				manage_clients.channel.basic_publish(exchange = 'connection_manager', routing_key = client_username, body = message)
			except Exception as error:
				print("[ Error ] " + str(error))

			print ("Done")

	