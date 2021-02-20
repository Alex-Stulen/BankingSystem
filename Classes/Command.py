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
                # print(command_list)
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

    def get_command(self, *args, **kwargs):
        """
            The function must not be static because otherwise the given function will not be found in the object

            :param args:
            :param kwargs:
            :return: command list
        """

        try:
            command_line = str(input('Введите команду: '))
            # command = command_line.split(' ')
            if command_line.find('"') != -1 and command_line.find(' : ') != -1:
                command = command_line.split(' : ')
                args = command[1].split('"')
                args = args[0].split(' ') + [args[1]]
                args = [item for item in args if item != '']
                command = command[0].split(' ')
                command = command + args
            elif command_line.find(' : ') != -1:
                command = command_line.split(' : ')
                command = command[0].split(' ') + command[1].split(' ')
            else:
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
                    if str(value) == 'spending':
                        data = list(list(key.items())[0])
                        table.add_row([data[0], data[1]['price'], data[1]['salary'], data[1]['rest_money']])

                print(table)
        except Exception as e:
            raise Exceptions.GetJsonError('Неудалось получить данные о тратах\t' + str(e))

    def get_month_spending(self, args, **kwargs):
        try:
            data = self.class_db_data.get_json()
            data = data['month'][str(args[0])]
            print(data)

            if len(data) == 0:
                print('--Нет данных--')
            else:
                table = PrettyTable()
                table.field_names = ['Month', '№', 'Spending', 'Salary', 'Rest Money', 'Description']

                for key, value in data.items():
                    print(key, value)
                    table.add_row([
                        args[0],
                        key,
                        value['price'],
                        value['salary'],
                        value['rest_money'],
                        value['description']
                    ])

                print(table)
        except Exception as e:
            raise Exceptions.GetJsonError('Неудалось получить данные месяца о тратах\t' + str(e))

    def set_month_detail(self, args, **kwargs):
        try:
            data = self.class_db_data.get_json()
            data = data.get('month')
            args_ = {
                f'{args[0]}': {
                    f'{args[1]}': {
                        'price': args[2],
                        'salary': args[3],
                        'rest_money': int(args[3]) - int(args[2]),
                        'description': args[4],
                    }
                }
            }

            if data is not None:
                data_ = data.get(f'{args[0]}')
                if data_ is not None:
                    args_ = {
                        f'{args[1]}': {
                            'price': args[2],
                            'salary': args[3],
                            'rest_money': int(args[3]) - int(args[2]),
                            'description': args[4],
                        }

                    }
                    data[args[0]].update(args_)
                    data = {
                        'month': data
                    }
                else:
                    data.update(args_)

            else:
                data = {
                    'month': {}
                }
                data['month'].update(args_)

            self.class_db_data.set_json(data)
        except Exception as e:
            raise Exceptions.SetJsonError('Неудалось загрузить детальные данные о тратах за месяц\t' + str(e))

    def set_spending(self, args, **kwargs):
        try:
            data = self.class_db_data.get_json()
            data['spending'] = {
                f'{args[0]}': {
                    'price': args[1],
                    'salary': args[2],
                    'rest_money': int(args[2]) - int(args[1])
                }
            }

            self.class_db_data.set_json(data)
        except Exception as e:
            raise Exceptions.SetJsonError('Неудалось записать данные о тратах\t' + str(e))

    def delete_month(self, args, **kwargs):
        try:
            data = self.class_db_data.get_json()
            if (data.get('month') is not None) and (data.get('spending') is not None):
                del data['month'][args[0]]
                del data['spending'][args[0]]

            self.class_db_data.set_json(data)
        except Exception as e:
            raise Exceptions.CorrectionJsonError('Неудалось удалить месяц\t' + str(e))

    def quit(self, *args, **kwargs):
        raise SystemExit
