from file_creation import file_manager
from connection import manage_connection
from login_request import authenticate_judge 
from communicate_server import communicate_server

rabbitmq_username = "judge1"
rabbitmq_password = "judge1"
# host = "192.168.43.239"
host = 'localhost'


channel,connection = manage_connection.initialize_connection(rabbitmq_username,rabbitmq_password,host)

print(type (channel))
print("................ BitsOJ Judge .................\n")

status = ''
while (status != 'VALID'):
	authenticate_judge.login(channel, host)
	status = authenticate_judge.login_status

	

while (status == 'VALID'):
	print("\nJudge Authenticated")
	communicate_server.listen_server()



manage_connection.terminate_connection(connection)

