import json
from unidecode import unidecode

class User:
    def __init__(self, name: str, cpf, gender, date):
        self.__name = unidecode(name.upper()) or ""
        self.__cpf = cpf.replace(".", "").replace("-", "") or ""
        self.__gender = "Female" if (gender == "F" or gender == "Female") else ( "Male" if (gender == "M" or gender == "Male") else ( "" if gender == "" else ""))
        self.__date = date or ""

    def to_dict(self):
        return {
            "name": self.__name,
            "cpf": self.__cpf,
            "gender": self.__gender,
            "date": self.__date
        }

    @staticmethod
    def from_dict(data):
        return User(
            name=data.get("name", ""),
            cpf=data.get("cpf", ""),
            gender=data.get("gender", ""),
            date=data.get("date", "")
        )

    def get_name(self):
        return self.__name

    def get_cpf(self):
        return self.__cpf

    def get_gender(self):
        return self.__gender

    def get_date(self):
        return self.__date

    def export_user(self):
        user_data = {
                "nome": unidecode(self.__name.upper()),
                "cpf": self.__cpf,
                "gender": "Female" if (self.__gender == "F" or self.__gender == "Female") else ( "Male" if (self.__gender == "M" or self.__gender == "Male") else ( "" if self.__gender == "" else "")),
                "date": self.__date
        }
        data = json.dumps(user_data)
        return data

    def import_user(self, data):
        user_data = data["user_data"]
        self.__name = unidecode(user_data["nome"].upper())
        self.__cpf = user_data["cpf"]
        self.__gender = "Female" if (user_data["gender"] == "F" or user_data["gender"] == "Female") else ( "Male" if (user_data["gender"] == "M" or user_data["gender"] == "Male") else ( "" if user_data["gender"] == "" else ""))
        self.__date = user_data["data"]

        data = {
                "nome": self.__name,
                "cpf": self.__cpf,
                "gender": self.__gender,
                "date": self.__date
        }
        return data