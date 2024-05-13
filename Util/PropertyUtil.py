import mysql.connector as sql
import time


class DBPropertyUtil:
    @staticmethod
    def getParameter():
        host = "localhost"
        database = "HMBank"
        user = "root"
        password = "goldy777"
        return {"host": host, "database": database, "user": user, "password": password}


class DBConnUtil():
    @staticmethod
    def makeConnection():
        parameters = DBPropertyUtil.getParameter()
        conn = sql.connect(host=parameters["host"], database=parameters["database"], user=parameters["user"],
                           password=parameters["password"])
        # print(parameters)
        if conn.is_connected():
            time.sleep(0.5)
            print("Connections successful")
            return conn

        else:
            print("Unable to connect")



# DBConnUtil().makeConnection()
