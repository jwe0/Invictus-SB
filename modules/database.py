import sqlite3

class Database:
    def __init__(self) -> None:
        pass

    def messageloggeradd(self, id, username, message, time):
        conn = sqlite3.connect("Databases/messages.db")
        c = conn.cursor()
        c.execute("INSERT INTO messages VALUES (?, ?, ?, ?)", (id, username, message, time))
        conn.commit()
        conn.close()

    def messageloggerget(self, username):
        conn = sqlite3.connect("Databases/messages.db")
        c = conn.cursor()
        values = c.execute("SELECT * FROM messages WHERE userid= ?", (username,)).fetchall()
        conn.close()
        return values