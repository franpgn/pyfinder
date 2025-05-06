# -*- coding: utf-8 -*-
import os
import sqlite3
import logging
from repository.request_data import RequestData

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s',)

class Worker:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    @staticmethod
    def database_query(request_data: RequestData, db_path: str):
        logger = logging.getLogger('Worker')
        conn = sqlite3.connect(db_path)

        logger.info('Database connection established')
        logger.debug('Current PID : %s', os.getpid())

        cursor = conn.cursor()
        query = 'SELECT * FROM cpf WHERE'
        if request_data.get_user_data().get_name():
            query += ' nome LIKE %?%'
            if request_data.get_user_data().get_cpf():
                query += ' AND cpf = ?'
                if request_data.get_user_data().get_date():
                    query += ' AND nasc = ?'
                    query += ' LIMIT 0, 1000'
                    cursor.execute(query, (request_data.get_user_data().get_name(), request_data.get_user_data().get_cpf(), request_data.get_user_data().get_date()))
                else:
                    query += ' LIMIT 0, 1000'
                    cursor.execute(query, (request_data.get_user_data().get_name(), request_data.get_user_data().get_cpf()))
            else:
                query += ' LIMIT 0, 1000'
                cursor.execute(query, (request_data.get_user_data().get_name(),))
        elif request_data.get_user_data().get_cpf():
            query += ' cpf = ?'
            if request_data.get_user_data().get_date():
                query += ' AND nasc = ?'
                query += ' LIMIT 0, 1000'
                cursor.execute(query, (request_data.get_user_data().get_cpf(), request_data.get_user_data().get_date()))
            else:
                query += ' LIMIT 1000'
                cursor.execute(query, (request_data.get_user_data().get_cpf(),))
        elif request_data.get_user_data().get_date():
            query += ' nasc = ?'
            if request_data.get_user_data().get_name():
                query += ' AND nome LIKE %?%'
                query += ' LIMIT 0, 1000'
                cursor.execute(query, (request_data.get_user_data().get_date(), request_data.get_user_data().get_name()))
            else:
                query += ' LIMIT 0, 1000'
                cursor.execute(query, (request_data.get_user_data().get_date(),))
        result = cursor.fetchall()

        users = []
        for row in result:
            user = {
                "name": row[1],
                "cpf": row[0],
                "gender": row[2],
                "date": row[3]
            }
            users.append(user)

        response = {
            "response_id": request_data.get_request_id(),
            "user_data": users
        }
        return response