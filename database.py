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

    def check_shops(self):
        cur = self.cur
        check_shops_sql = "SELECT id, name, owner FROM shops"
        cur.execute(check_shops_sql)
        formatted_result = [f"{id:<5}{name:<30}{owner:<30}" for id, name, owner in cur.fetchall()]
        id, name, owner = "Id", "Name", "Owner"
        print('\n'.join([f"{id:<5}{name:<30}{owner:<30}"] + [""] + formatted_result))
    
    def check_users(self):
        cur = self.cur
        check_users_sql = "SELECT id, name, rank, num_shops FROM users"
        cur.execute(check_users_sql)
        formatted_result = [f"{id:<5}{name:<30}{rank:<20}{num_shops:>11}" for id, name, rank, num_shops in cur.fetchall()]
        id, name, rank, num_shops = "Id", "User", "Rank", "Shops owned"
        print('\n'.join([f"{id:<5}{name:<30}{rank:<20}{num_shops:>11}"] + [""] + formatted_result))

    def update_user(self, name, rank, num_shops):
        cur = self.cur
        update_user_sql = "INSERT OR REPLACE INTO users (id, name, rank, num_shops) values ((SELECT id FROM users WHERE name = ?), ?, ?, ?)"
        cur.execute(update_user_sql, (name, name, rank, num_shops))
        self.con.commit()

    def update_user_by_data(self, user_data):
        cur = self.cur
        update_user_sql = "INSERT OR REPLACE INTO users (id, name, rank, num_shops) values ((SELECT id FROM users WHERE name = ?), ?, ?, ?)"
        name = user_data["name"]
        rank = user_data["rank"]
        num_shops = user_data["num_shops"]
        cur.execute(update_user_sql, (name, name, rank, num_shops))
        self.con.commit()

    def add_shop(self, name, owner):
        cur = self.cur
        try:
            add_shop_sql = "INSERT INTO shops (name, owner) VALUES (?, ?)"
            cur.execute(add_shop_sql, (name, owner))
            u = self.get_user(owner)
            u["num_shops"] += 1
            self.update_user_by_data(u)
            self.con.commit()
            return "success"
        except:
            return "failure"

    def remove_shop(self, name, owner):
        cur = self.cur
        test_shop_exists_sql = "SELECT name FROM shops WHERE owner = ?"
        remove_shop_sql = "DELETE FROM shops WHERE name = ? AND owner = ?"
        try:
            cur.execute(test_shop_exists_sql, (owner,))
            if not name in cur.fetchall()[0]:
                return "failure"
            cur.execute(remove_shop_sql, (name, owner))
            u = self.get_user(owner)
            u["num_shops"] -= 1
            self.update_user_by_data(u)
            self.con.commit()
            return "success"
        except:
            return "failure"

    def get_shops_owned(self, owner):
        cur = self.cur
        get_shops_sql = "SELECT name FROM shops WHERE owner = ?"
        cur.execute(get_shops_sql, (owner,))
        shops = [x[0] for x in cur.fetchall()]
        return shops
    
    def get_user(self, name):
        cur = self.cur
        get_user_sql = "SELECT rank, num_shops FROM users WHERE name = ?"
        cur.execute(get_user_sql, (name,))
        result = cur.fetchall()[0]
        output = {"name" : name, "rank" : result[0] , "num_shops" : result[1]}
        return output

db = MarketDatabase()
'''
db.cur.execute("DROP TABLE shops")
setup_shops_table = "CREATE TABLE shops (id integer PRIMARY KEY, name text NOT NULL UNIQUE, owner text NOT NULL)"
db.cur.execute(setup_shops_table)
db.con.commit()
db.check_tables()

db.cur.execute("DROP TABLE users")
setup_users_table = "CREATE TABLE users (id integer PRIMARY KEY, name text NOT NULL, rank integer, num_shops integer)"
db.cur.execute(setup_users_table)

db.update_user("Stan", 1, 0)
db.update_user("GapingThrowrer20", 1, 0)
db.update_user("atmost", 1, 0)
db.update_user("Nav", 1, 0)
db.check_users()

u = db.get_user("Stan")
u["num_shops"] += 1
db.update_user_by_data(u)
db.check_users()

db.con.commit()
'''
