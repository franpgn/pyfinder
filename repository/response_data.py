import json
from repository.user import User

class ResponseData:
    def __init__(self, response_id: int, user_list_data: list[User]):
        self.__response_id = response_id
        self.__user_list_data = user_list_data

    def to_dict(self):
        return {
            "request_id": self.__response_id,
            "user_data": [user.to_dict() for user in self.__user_list_data]
        }

    @staticmethod
    def from_dict(data):
        user_list_data = [User.from_dict(user) for user in data["user_data"]]
        return ResponseData(data["request_id"], user_list_data)

    def get_response_id(self):
        return self.__response_id

    def get_user_list_data(self):
        return self.__user_list_data

    @staticmethod
    def import_response(data_bytes):
        if isinstance(data_bytes, str):
            data_list = json.loads(data_bytes)
        elif isinstance(data_bytes, dict):
            data_list = data_bytes
        elif isinstance(data_bytes, bytes):
            data_list = json.loads(data_bytes.decode('utf-8'))
        else:
            raise TypeError(f"Unsupported data type: {type(data_bytes)}")

        response_id = data_list["request_id"] if "request_id" in data_list else data_list["response_id"]

        user_list = []
        user_data = data_list["user_data"]
        if isinstance(user_data, list):
            for data in user_data:
                user_list.append(User(data["name"], data["cpf"], data["gender"], data["date"]))
        else:
            user_list.append(User(user_data["name"], user_data["cpf"], user_data["gender"], user_data["date"]))

        return ResponseData(response_id, user_list)

    @staticmethod
    def export_response(response_data):
        response_data = ResponseData(response_data.get_response_id(), response_data.get_user_list_data())
        return json.dumps(response_data.to_dict()).encode('utf-8')