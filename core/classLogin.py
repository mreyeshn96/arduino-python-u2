import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
import pymysql.cursors

from core.app_config import *


class LoginController:

    def __init__(self):
        pass

    def check(self, username: str, password: str):
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        currentCursor = conn.cursor()
        query = "SELECT user_id FROM user WHERE user_name LIKE '{0}' AND user_password LIKE '{1}'".format(username,
                                                                                                          password)
        currentCursor.execute(query)

        if currentCursor.rowcount > 0:
            return True
        else:
            return False
