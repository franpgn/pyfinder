# -*- coding: utf-8 -*-
import os
import sqlite3
import logging
from request_data import RequestData

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
        # fetch inputs once
        name = request_data.get_user_data().get_name()
        cpf = request_data.get_user_data().get_cpf()
        date = request_data.get_user_data().get_date()

        if name:
            query += ' nome LIKE ?'
            if cpf:
                query += ' AND cpf = ?'
                if date:
                    query += ' AND nasc = ?'
                    query += ' LIMIT 1000'
                    cursor.execute(
                        query,
                        (f'%{name}%', cpf, date)
                    )
                else:
                    query += ' LIMIT 1000'
                    cursor.execute(
                        query,
                        (f'%{name}%', cpf)
                    )
            else:
                query += ' LIMIT 1000'
                cursor.execute(
                    query,
                    (f'%{name}%',)
                )

        elif cpf:
            query += ' cpf = ?'
            if date:
                query += ' AND nasc = ?'
                query += ' LIMIT 1000'
                cursor.execute(
                    query,
                    (cpf, date)
                )
            else:
                query += ' LIMIT 1000'
                cursor.execute(
                    query,
                    (cpf,)
                )

        elif date:
            query += ' nasc = ?'
            if name:
                query += ' AND nome LIKE ?'
                query += ' LIMIT 1000'
                cursor.execute(
                    query,
                    (date, f'%{name}%')
                )
            else:
                query += ' LIMIT 1000'
                cursor.execute(
                    query,
                    (date,)
                )

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
