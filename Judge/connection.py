import pika

# Class to handle connection establishment requests
class manage_connection():

	channel = ''

	# Function to establish connection
	def initialize_connection(rabbitmq_username,rabbitmq_password,host):
		try:

			connection = pika.BlockingConnection(
			pika.URLParameters(
				"amqp://" + rabbitmq_username + ":" + rabbitmq_password + "@" + host + "/%2f"
				))	
			channel = connection.channel()
			manage_connection.channel = channel

			# binding credential manager exchange and login_request queue  which send the login request from client to server
			channel.queue_bind(
				exchange = 'connection_manager', 
				queue = 'client_requests'
				)
			return channel,connection


		except Exception as error:
			print(str(error))

	def terminate_connection(connection):
		connection.close()

	def connect_me():
		# print("I am from connection and this is the channel name" + str(manage_connection.channel))
		return	manage_connection.channel