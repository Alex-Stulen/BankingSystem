from Classes import Command, Json
from config import *


DB_DATA = DATABASE_DATA
DB_COMMANDS = DATABASE_COMMANDS

Json_data = Json.Json(path_to_json=DB_DATA['DB_PATH'])
Json_commands = Json.Json(path_to_json=DB_COMMANDS['DB_PATH'])

COMMAND = Command.Command(class_db_data=Json_data)


def main():

	commands_dict = Json_commands.get_json()

	work_end = False
	while not work_end:
		command = COMMAND.get_command()
		# print(command)
		define_command = COMMAND.define_command(dict__=commands_dict, command_list=command)
		define_command = list(define_command)

		try:
			COMMAND.run_command(command_func=define_command[0], args=define_command[1])
		except Exception as e:
			print(e)

	return 0


if __name__ == "__main__":
	main()
