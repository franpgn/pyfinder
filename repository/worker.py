# -*- coding: utf-8 -*-
import os
import sqlite3
from repository.request_data import RequestData


class Worker:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    @staticmethod
    def database_query(request_data: RequestData, db_path: str):
        conn = sqlite3.connect(db_path)
        print("PID ATUAL:" + str(os.getpid()))
        cursor = conn.cursor()
        query = 'SELECT * FROM cpf WHERE'
        if request_data.get_user_data().get_name():
            query += ' nome = ?'
            if request_data.get_user_data().get_cpf():
                query += ' AND cpf = ?'
                if request_data.get_user_data().get_date():
                    query += ' AND nasc = ?'
                    cursor.execute(query, (request_data.get_user_data().get_name(), request_data.get_user_data().get_cpf(), request_data.get_user_data().get_date()))
                else:
                    cursor.execute(query, (request_data.get_user_data().get_name(), request_data.get_user_data().get_cpf()))
            else:
                cursor.execute(query, (request_data.get_user_data().get_name(),))
        elif request_data.get_user_data().get_cpf():
            query += ' cpf = ?'
            if request_data.get_user_data().get_date():
                query += ' AND nasc = ?'
                cursor.execute(query, (request_data.get_user_data().get_cpf(), request_data.get_user_data().get_date()))
            else:
                cursor.execute(query, (request_data.get_user_data().get_cpf(),))
        elif request_data.get_user_data().get_date():
            query += ' nasc = ?'
            if request_data.get_user_data().get_name():
                query += ' AND nome = ?'
                cursor.execute(query, (request_data.get_user_data().get_date(), request_data.get_user_data().get_name()))
            else:
                cursor.execute(query, (request_data.get_user_data().get_date(),))
        result = cursor.fetchall()

        users = []
        for row in result:
            user = {
                "name": row[1],
                "cpf": row[0],
                "date": row[3]
            }
            users.append(user)

        response = {
            "response_id": request_data.get_request_id(),
            "user_data": users
        }
        return response


