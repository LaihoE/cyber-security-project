import sqlite3

con = sqlite3.connect("db.db")
cur = con.cursor()

sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS message (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    user text,
                                    message text NOT NULL
                                ); """


cur.execute(sql_create_projects_table)