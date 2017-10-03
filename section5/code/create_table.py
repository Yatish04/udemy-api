import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

create_user_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_user_table)

create_item_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_item_table)

cursor.execute("INSERT INTO items VALUES ('chair', 15.99)")

connection.commit()

connection.close()
