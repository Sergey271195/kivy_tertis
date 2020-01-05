import sqlite3


class BdManager():
    def __init__(self, name, table, *args, **kwargs):
        self.name = name
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
        self.table = table
        self.lastname = None
        self.firstname = None
        self.loggin = False
        self.time = None  
        self.create_table()  

    def conenct_to_db(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
        self.name = name

    def login(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        self.loggin = True

    def create_table(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=(?)", (self.table,))
        if self.cursor.fetchall() == []:
            self.cursor.execute('''Create Table ''' + self.table + ''' (
                firstname text,
                lastname text,
                totalgames integer,
                totaltime real,
                highscore integer
                )''')
        else:
            pass


    def get_table_list(self):
        self.cursor.execute('SELECT * FROM ' + self.table)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    def delete_player(self, firstname):
        self.cursor.execute("DELETE FROM " + self.table +" WHERE firstname = (?)", (firstname,))
        self.connection.commit()
    
    def check_if_exist(self, firstname, lastname):
        self.cursor.execute('SELECT * FROM ' + self.table + 
        ' WHERE firstname = (?) AND lastname = (?)', (firstname, lastname))
        if self.cursor.fetchall() == []:
            print("Allowed ID")
            return False
        else:
            print(f"Name {firstname} {lastname} has been taken")
            return True

    def update_score(self, newscore):
        self.cursor.execute('SELECT highscore, totalgames FROM ' + self.table + 
        ' WHERE firstname = (?) AND lastname = (?)', (self.firstname, self.lastname))
        for score, games in self.cursor.fetchall():
            totalgames = games
            highscore = score
        if newscore >= highscore:
            print(f"New highscore: {newscore}")
            self.cursor.execute('UPDATE ' + self.table + 
        ' SET highscore = (?), totalgames = totalgames+1 WHERE firstname = (?) AND lastname = (?)', 
        (newscore, self.firstname, self.lastname))
        self.connection.commit()

    def get_leaderboard(self):
        self.list = list()
        self.cursor.execute("SELECT  firstname, lastname, highscore FROM "+self.table + " ORDER BY highscore DESC")
        for row in self.cursor.fetchall():
            for col in row:
                print(col)
                self.list.append(col)
        print(self.list)

    def get_leaderboard_names(self):
        self.name_list = list()
        self.cursor.execute("SELECT  firstname, lastname FROM "+self.table + " ORDER BY highscore DESC")
        for row in self.cursor.fetchall():
                self.name_list.append(row)
        return(self.name_list)

    def get_leaderboard_score(self):
        self.score_list = list()
        self.cursor.execute("SELECT  highscore FROM "+self.table + " ORDER BY highscore DESC")
        for row in self.cursor.fetchall():
            for col in row:
                self.score_list.append(col)
        return(self.score_list)

    def add_player(self, firstname, lastname):
        if self.check_if_exist(firstname, lastname):
            pass
        else:
            self.cursor.execute("INSERT INTO " + self.table +" VALUES ('"+firstname+"','"+lastname+"',0,0,0)")
            self.connection.commit()


