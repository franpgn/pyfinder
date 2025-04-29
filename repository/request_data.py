import json
from repository.user import User

class RequestData:
    def __init__(self, request_id: int, user_data: User):
        self.__request_id = request_id
        self.__user_data = user_data

    def to_dict(self):
        return {
            "request_id": self.__request_id,
            "user_data": self.__user_data.to_dict()
        }

    @staticmethod
    def from_dict(data):
        user_data = User.from_dict(data["user_data"])
        return RequestData(data["request_id"], user_data)

    def get_request_id(self):
        return self.__request_id

    def get_user_data(self):
        return self.__user_data

    @staticmethod
    def import_request(data_bytes):
        try:
            if not data_bytes:
                return None
            data = json.loads(data_bytes.decode('utf-8'))
            request_id = data["request_id"]
            user_data = User(data["user_data"]["name"],
                             data["user_data"]["cpf"],
                             data["user_data"]["date"])
            request_data = RequestData(request_id, user_data)
            return request_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None

    @staticmethod
    def export_request(request_id: int, user_data: User):
        if not isinstance(user_data, User):
            raise ValueError("user_data must be an instance of User")
        request_data = RequestData(request_id, user_data)
        return json.dumps(request_data.to_dict()).encode('utf-8')

if __name__ == "__main__":
    # Example usage
    data = ('{ "request_id": 1, "user_data": { "nome": "John Doe", "cpf": "12345678900", "data": "01/01/2000" }}').encode('utf-8')

    request_data = RequestData.import_request(data)

    exported = RequestData.export_request(request_data.get_request_id(), request_data.get_user_data())

    print(exported)  # Output: 1
