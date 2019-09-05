global run_id_counter
run_id_counter = 1
class submission():
	# Manage a new submission
	def new_submission(client_id, problem_code, language, time_stamp, source_code):
		print("[ SUBMIT ] "+ client_id + " for problem " + problem_code)
		run_id = submission.generate_run_id()
		file_name = "Client_Submissions/" + client_id + '_' + problem_code + '_' + run_id
		print ("[ FILE ] "+ client_id + " : " + file_name)
		submission.make_local_source_file(file_name, source_code, language)
		judge_verdict = submission.judge_submission(source_code, language, problem_code)

		return_code, error_message = judge_verdict.split('+')

		return return_code, run_id, error_message

	# Make a local backup file for the client run id
	def make_local_source_file(file_name, source_code, language):

		if language == "cpp":
			file_extension = ".cpp"
		elif language == "gcc":
			file_extension = ".c"
		elif language == "py2":
			file_extension = ".py"
		elif language == "py3":
			file_extension = ".py"
		elif language == "jva":
			file_extension = ".java"
		else:
			file_extension = ".temp"

		# w : Write mode, + : Create file if not exists
		new_file_name = file_name + file_extension
		print("[ WRITE ] " + new_file_name)
		client_local_file = open(new_file_name, "w+")
		client_local_file.write(source_code)
		client_local_file.close()
		return

	def generate_run_id():
		global run_id_counter
		run_id = str("{:05d}".format(run_id_counter))
		run_id_counter = run_id_counter + 1
		return run_id

	def judge_submission(source_code, language, problem_code):
		status = True
		if status == True:
			return "AC+No_Error"
		else:
			return "WA+Error"

	