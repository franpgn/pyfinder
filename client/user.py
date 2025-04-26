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

    def export_user(self):
        data = {
            "nome": self.__name,
            "cpf": self.__cpf,
            "data": self.__date
        }
        filename = "data.json"
        with open(filename, "w") as file:
            json.dump(data, file)

    def import_user(self):
        filename = "data.json"
        with open(filename, "r") as file:
            data = json.load(file)
            self.__name = data["nome"]
            self.__cpf = data["cpf"]
            self.__date = data["data"]