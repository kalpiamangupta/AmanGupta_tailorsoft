import mysql.connector as mysql

class DbConnection:
    @staticmethod
    def createConnection():
        con = mysql.connect(host='localhost', database='tailorsoft', user='root', password='')
        return con
