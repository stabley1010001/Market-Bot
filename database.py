import sqlite3
import os
class MarketDatabase:
    
    def __init__(self):
        self.con = sqlite3.connect('database.sqlite3')
        self.cur = self.con.cursor()
    
    def check_tables(self):
        cur = self.cur
        check_tables_sql = "SELECT name FROM sqlite_master WHERE type = 'table'"
        cur.execute(check_tables_sql)
        print(cur.fetchall())

    def check_users(self):
        cur = self.cur
        check_users_sql = "SELECT id, name, rank, num_shops FROM users"
        cur.execute(check_users_sql)
        formatted_result = [f"{id:<5}{name:<30}{rank:<20}{num_shops:>11}" for id, name, rank, num_shops in cur.fetchall()]
        id, name, rank, num_shops = "Id", "User", "Rank", "Shops owned"
        print('\n'.join([f"{id:<5}{name:<30}{rank:<20}{num_shops:>11}"] + [""] + formatted_result))

    def update_user(self, name, rank, num_shops):
        cur = self.cur
        update_user_sql = "INSERT INTO users (name, rank, num_shops) VALUES (?, ?, ?)"
        cur.execute(update_user_sql, (name, rank, num_shops))
        self.con.commit()

    def update_user(self, user_data):
        cur = self.cur
        self.update_user(user_data["name"], user_data["rank"], user_data["num_shops"])

    def get_user(self, name):
        cur = self.cur
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
