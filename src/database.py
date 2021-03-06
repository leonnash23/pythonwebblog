import sqlite3


class DataBase:
    con = sqlite3.Connection
    cur = sqlite3.Cursor

    def __init__(self):
        self.con = sqlite3.connect("data.db")
        self.cur = self.con.cursor()
        self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='Posts';")
        if self.cur.fetchone()[0] < 1:
            self.cur.execute("""CREATE TABLE Posts(id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title VARCHAR, text VARCHAR, img VARCHAR, data DATE  DEFAULT (datetime('now','localtime')));""")
            self.commit()

    def getAll(self):
        self.cur.execute("SELECT * FROM Posts")
        return self.cur.fetchall()

    def getById(self, post_id):
        self.cur.execute("SELECT * FROM Posts WHERE id=?;", (str(post_id),))
        return self.cur.fetchall()

    def getLastId(self):
        self.cur.execute("SELECT last_insert_rowid()")
        return self.cur.fetchall()[0][0]

    def addNew(self, title, text, img):
        self.cur.execute("INSERT INTO Posts(title,text,img) VALUES (?,?,?);", (title, text, img))
        self.commit()

    def commit(self):
        self.con.commit()






