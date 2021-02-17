from . import Exceptions
from prettytable import PrettyTable


class Command:
    def __init__(self, class_db_data=None):
        self.class_db_data = class_db_data

        Command.check_classes_db([self.class_db_data])

    @staticmethod
    def check_classes_db(array_classes):
        for item in array_classes:
            if item is None:
                raise Exceptions.ClassDdIsNone('Классы Базыданных = None')

        return

    @staticmethod
    def define_command(dict__, command_list: list, index: int = 0):
        try:

            if index >= len(command_list) or type(dict__) is str:
                return dict__, command_list[index:]

            if dict__[command_list[index]]:
                return Command.define_command(dict__[command_list[index]], command_list, index + 1)
        except Exception as e:
            raise Exceptions.UnknownCommand('Неудалось определить команду\t' + str(e))

    def run_command(self, command_func, args):
        try:
            func_dict = globals()[__class__.__name__].__dict__
            func = func_dict[command_func]
            func(self, args)
        except Exception as e:
            raise Exceptions.RunFunctionError('Неудалось запустить функцию\t' + str(e))

    @staticmethod
    def get_command():
        try:
            command_line = str(input('Введите команду: '))
            command = command_line.split(' ')

            return command
        except Exception as e:
            raise Exceptions.InvalidString('Неудалось считать строку\t' + str(e))

    def get_spending(self, *args, **kwargs):
        try:
            data = self.class_db_data.get_json()

            if len(data) == 0:
                print('--Нет данных--')
            else:

                table = PrettyTable()
                table.field_names = ['Month', 'Spending', 'Salary', 'Rest Money']

                for value, key in data.items():
                    table.add_row([int(value), int(key['price']), int(key['salary']), int(key['rest_money'])])

                print(table)
        except Exception as e:
            raise Exceptions.GetJsonError('Неудалось получить данные о тратах\t' + str(e))

    def get_month_spending(self):
        try:
            data = self.class_db_data.get_json()

            if len(data) == 0:
                print('--Нет данных--')
        except Exception as e:
            print(str(e))


    def set_spending(self, args, **kwargs):
        try:
            data = self.class_db_data.get_json()
            data[args[0]] = {
                'price': args[1],
                'salary': args[2],
                'rest_money': int(args[2]) - int(args[1])
            }

            self.class_db_data.set_json(data)
        except Exception as e:
            raise Exceptions.SetJsonError('Неудалось записать данные о тратах\t' + str(e))

    def delete_month(self, args, **kwargs):
        try:
            data = self.class_db_data.get_json()
            del data[args[0]]

            self.class_db_data.set_json(data)
        except Exception as e:
            raise Exceptions.CorrectionJsonError('Неудалось удалить месяц\t' + str(e))

    def quit(self, *args, **kwargs):
        raise SystemExit
