import json
class User:
    def __init__(self, name, cpf, date):
        self.__name = name
        self.__date = cpf.replace(".", "").replace("-", "")
        self.__cpf = date.toString("dd/MM/yyyy")

    def get_name(self):
        return self.__name

    def get_date(self):
        return self.__date

    def get_cpf(self):
        return self.__cpf

    def export_user(self, request_id):
        data = {
            "id": request_id,
            "data": {
                "nome": self.__name,
                "cpf": self.__cpf,
                "date": self.__date
            }
        }
        data_bytes = json.dumps(data).encode('utf-8')
        return data_bytes

    def import_user(self, data_bytes):
        data = json.loads(data_bytes.decode('utf-8'))
        request_id = data["id"]
        user_data = data["date"]
        self.__name = user_data["nome"]
        self.__cpf = user_data["cpf"]
        self.__date = user_data["data"]

        data = {
            "id": request_id,
            "data": {
                "nome": self.__name,
                "cpf": self.__cpf,
                "date": self.__date
            }
        }
        return data