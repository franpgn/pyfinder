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

        # fetch inputs once
        name = request_data.get_user_data().get_name()
        cpf = request_data.get_user_data().get_cpf()
        date = request_data.get_user_data().get_date()

        # Build the query based on available filters
        conditions = []
        params = []

        if name:
            conditions.append('nome LIKE ?')
            params.append(f'%{name}%')

        if cpf:
            conditions.append('cpf = ?')
            params.append(cpf)

        if date:
            conditions.append('nasc = ?')
            params.append(date)

        # If no conditions were added, the query should be invalid
        if not conditions:
            raise ValueError("At least one filter (name, cpf, or date) is required.")

        # Join all conditions with AND and ensure there is space before AND
        query += ' ' + ' AND '.join(conditions)

        query += ' LIMIT 1000'

        # Execute the query with the parameters
        cursor.execute(query, tuple(params))

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
