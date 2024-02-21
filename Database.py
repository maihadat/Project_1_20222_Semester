import mysql.connector
from Cloud_Service import CloudService


class DatabaseConnector:
    def __init__(self, table, password="qwedfgbnm123"):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password
        )
        self.schema = 'project1_database'
        self.table = table
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute('USE ' + self.schema)

    def insert(self, data):
        if type(data) == list:
            sql = "INSERT INTO " + self.table + " VALUES " + str(data)[1:-1]
            self.mycursor.execute(sql)
        elif type(data) == tuple:
            sql = "INSERT INTO " + self.table + " VALUES " + str(data)
            self.mycursor.execute(sql)
        else:
            print('Type of data is not valid')

    def truncate(self):
        sql = 'TRUNCATE TABLE ' + self.table
        self.mycursor.execute(sql)

    def commit(self):
        self.mydb.commit()

    def select(self, column=''):
        if column == '':
            self.mycursor.execute("SELECT * FROM " + self.table)
            myresult = self.mycursor.fetchall()
            return myresult
        else:
            self.mycursor.execute("SELECT" + column + "FROM " + self.table)
            myresult = self.mycursor.fetchall()
            return myresult

    def update_security_service(self, secure, id):
        sql = "UPDATE service\n" \
              "SET security_service = " + '"' + secure + '"' + "\n" \
              "WHERE service_id=" + id
        self.mycursor.execute(sql)
        self.commit()








