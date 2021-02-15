import json


class Json:
    def __init__(self, path_to_json, encoding: str = 'utf-8'):
        self.path_to_json = path_to_json
        self.encoding = encoding

    def get_json(self):
        try:
            with open(self.path_to_json, encoding=self.encoding) as read_file:
                data = json.load(read_file)

            return data
        except Exception as e:
            raise ValueError('Неудалось получить данные с json\t' + str(e))

    def set_json(self, context: dict, indent: int = 4, write_method: str = 'w'):
        try:
            with open(self.path_to_json, write_method, encoding=self.encoding) as write_file:
                json.dump(context, write_file, indent=indent)
        except Exception as e:
            raise ValueError('Неудалось загрузить данные в json\t' + str(e))
