import psycopg2  # driver Database (postgres)


class Connection():
    def __init__(self):
        self.user = 'postgres'
        self.password = '15032001'
        self.sslmode = 'require'
        self.dataBaseName = 'JetBov'
        self.host = 'localhost'
        self.cursor = None
        self.conn = None
        self.state = 0

    def set_user(self, user):
        self.user = user

    def set_password(self, password):
        self.password = password

    def set_sslmode(self, sslmode):
        self.sslmode = sslmode

    def set_dataBaseName(self, dataBaseName):
        self.dataBaseName = dataBaseName

    def set_host(self, host):
        self.host = host

    def get_user(self):
        return self.user

    def get_password(self):
        return self.password

    def get_sslmode(self):
        return self.sslmode

    def get_dataBaseName(self):
        return self.dataBaseName

    def get_host(self):
        return self.host

    def initConnection(self):
        if self.state == 0:
            connString = f'host={self.host} user={self.user} dbname={self.dataBaseName} password={self.password} sslmode={self.sslmode}'
            # print(connString)
            self.conn = psycopg2.connect(connString)
            self.cursor = self.conn.cursor()
            self.state = 1

    def SqlInsertCommand(self, sqlComand):
        if self.state == 0:
            self.initConnection()
        self.cursor.execute(sqlComand)
        self.conn.commit()

    def SqlResultCommand(self, sqlComand):
        if self.state == 0:
            self.initConnection()

        self.cursor.execute(sqlComand)
        return self.cursor.fetchall()

    def closeConnection(self):
        if self.state == 1:
            self.cursor.close()
            self.conn.close()
            self.state = 0
