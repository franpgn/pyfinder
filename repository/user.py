import json
class User:
    def __init__(self, name: str, cpf, date):
        self.__name = name or ""
        self.__cpf = cpf.replace(".", "").replace("-", "") or ""
        self.__date = date or ""

    def to_dict(self):
        return {
            "name": self.__name,
            "cpf": self.__cpf,
            "date": self.__date
        }

    @staticmethod
    def from_dict(data):
        return User(
            name=data.get("name", ""),
            cpf=data.get("cpf", "").replace(".", "").replace("-", ""),
            date=data.get("date", "")
        )

    def get_name(self):
        return self.__name

    def get_cpf(self):
        return self.__cpf

    def get_date(self):
        return self.__date

    def export_user(self):
        user_data = {
                "nome": self.__name,
                "cpf": self.__cpf,
                "date": self.__date
        }
        data = json.dumps(user_data)
        return data

    def import_user(self, data):
        user_data = data["user_data"]
        self.__name = user_data["nome"]
        self.__cpf = user_data["cpf"]
        self.__date = user_data["data"]

        data = {
                "nome": self.__name,
                "cpf": self.__cpf,
                "date": self.__date
        }
        return data