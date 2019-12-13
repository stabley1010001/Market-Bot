import sqlite3
import os

con = sqlite3.connect('database.sqlite3')
cur = con.cursor()

def check_tables():
    global cur
    check_tables_sql = "SELECT name FROM sqlite_master WHERE type = 'table'"
    cur.execute(check_tables_sql)
    print(cur.fetchall())

def check_users():
    global cur
    check_users_sql = "SELECT id, name, rank, num_shops FROM users"
    cur.execute(check_users_sql)
    formatted_result = [f"{id:<5}{name:<30}{rank:<20}{num_shops:>11}" for id, name, rank, num_shops in cur.fetchall()]
    id, name, rank, num_shops = "Id", "User", "Rank", "Shops owned"
    print('\n'.join([f"{id:<5}{name:<30}{rank:<20}{num_shops:>11}"] + [""] + formatted_result))

def update_user(name, rank, num_shops):
    global cur
    update_user_sql = "INSERT INTO users (name, rank, num_shops) VALUES (?, ?, ?)"
    cur.execute(update_user_sql, (name, rank, num_shops))
    con.commit()

def update_user(user_data):
    global cur
    update_user(user_data["name"], user_data["rank"], user_data["num_shops"]

def get_user(name):
    global cur
    get_user_sql = "SELECT rank, num_shops FROM users WHERE name = ?"
    cur.execute(get_user_sql, (name,))
    result = cur.fetchall()[0]
    output = {"name" : name, "rank" : result[0] , "num_shops" : result[1]}
    return output
'''
cur.execute("DROP TABLE users")
setup_users_table = "CREATE TABLE users (id integer PRIMARY KEY, name text NOT NULL, rank integer, num_shops integer, UNIQUE(id, name))"
cur.execute(setup_users_table)
update_user("Stan", 1, 0)
update_user("GapingThrowrer20", 1, 0)
update_user("atmost", 1, 0)
update_user("Nav", 1, 0)
check_users()

u = get_user("Stan")
print(u["rank"])
con.commit()
'''
