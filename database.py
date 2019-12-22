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
        check_shops_sql = "SELECT id, name, duration, owner FROM shops"
        cur.execute(check_shops_sql)
        formatted_result = [f"{id:<5}{name:<30}{duration:<30}{owner:<30}" for id, name, duration, owner in cur.fetchall()]
        id, name, duration, owner = "Id", "Name", "Days until expire", "Owner"
        print('\n'.join([f"{id:<5}{name:<30}{duration:<30}{owner:<30}"] + [""] + formatted_result)+'\n')
    
    def check_users(self):
        cur = self.cur
        check_users_sql = "SELECT id, name, rank, num_shops, coins FROM users"
        cur.execute(check_users_sql)
        formatted_result = [f"{id:<5}{name:<30}{rank:<11}{num_shops:>11}{coins:>11}" for id, name, rank, num_shops, coins in cur.fetchall()]
        id, name, rank, num_shops, coins = "Id", "User", "Rank", "Shops owned", "Coins"
        print('\n'.join([f"{id:<5}{name:<30}{rank:<11}{num_shops:>11}{coins:>11}"] + [""] + formatted_result)+'\n')

    def update_user(self, name, rank, num_shops, coins):
        cur = self.cur
        update_user_sql = "INSERT OR REPLACE INTO users (id, name, rank, num_shops, coins) values ((SELECT id FROM users WHERE name = ?), ?, ?, ?, ?)"
        cur.execute(update_user_sql, (name, name, rank, num_shops, coins))
        self.con.commit()

    def update_user_by_data(self, user_data):
        cur = self.cur
        update_user_sql = "INSERT OR REPLACE INTO users (id, name, rank, num_shops, coins) VALUES ((SELECT id FROM users WHERE name = ?), ?, ?, ?, ?)"
        cur.execute(update_user_sql, (user_data["name"], user_data["name"], user_data["rank"], user_data["num_shops"], user_data["coins"]))
        self.con.commit()

    def get_user(self, name):
        cur = self.cur
        get_user_sql = "SELECT rank, num_shops, coins FROM users WHERE name = ?"
        cur.execute(get_user_sql, (name,))
        result = cur.fetchall()[0]
        output = {"name" : name, "rank" : result[0] , "num_shops" : result[1], "coins" : result[2]}
        return output
    
    def add_shop(self, name, duration, owner):
        cur = self.cur
        try:
            add_shop_sql = "INSERT INTO shops (name, duration, owner) VALUES (?, ?, ?)"
            cur.execute(add_shop_sql, (name, duration, owner))
            u = self.get_user(owner)
            u["num_shops"] += 1
            self.update_user_by_data(u)
            self.con.commit()
            return "success"
        except:
            return "failure"

    def update_shop_by_data(self, shop_data):
        cur = self.cur
        update_shop_sql = "INSERT OR REPLACE INTO shops (id, name, duration, owner) VALUES ((SELECT id FROM shops WHERE name = ?), ?, ?, ?)"
        cur.execute(update_shop_sql, (shop_data['name'], shop_data['name'], shop_data['duration'], shop_data['owner']))
        self.con.commit()

    def update_all_shop_durations(self):
        cur = self.cur
        remove_list = []
        get_all_shops_sql = "SELECT name, duration, owner FROM shops"
        cur.execute(get_all_shops_sql)
        shops_data = cur.fetchall()
        for i in range(len(shops_data)):
            tmp = shops_data[i]
            if tmp[1] == 0:
                remove_list.append((tmp[0], tmp[2]))
            shops_data[i] = (tmp[1] - 1, tmp[0], tmp[2])
        update_all_shops_sql = "UPDATE shops SET duration = ? WHERE name = ? AND owner = ?"
        cur.executemany(update_all_shops_sql, shops_data)
        remove_shop_sql = "DELETE FROM shops WHERE name = ? AND owner = ?"
        cur.executemany(remove_shop_sql, remove_list)
        self.con.commit()
        return remove_list
    
    def get_shop(name, owner):
        cur = self.cur
        get_shop_sql = "SELECT duration FROM shops WHERE name = ? AND owner = ?"
        cur.execute(get_shop_sql, (name, owner))
        result = cur.fetchall()[0]
        output = {"name" : name, "duration" : result[0], "owner" : owner}
        return output
    
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
        get_shops_sql = "SELECT name, duration FROM shops WHERE owner = ?"
        cur.execute(get_shops_sql, (owner,))
        return cur.fetchall()
    
    

db = MarketDatabase()

'''
db.update_user("Stan", 1, 0, 0)
db.update_user("GapingThrowrer20", 1, 0, 0)
db.update_user("atmost", 1, 0, 0)
db.update_user("Nav", 1, 0, 0)
db.update_user("Yeet Yi", 1, 0, 0)
db.check_users()
'''
db.cur.execute("DROP TABLE shops")
setup_shops_table = "CREATE TABLE shops (id integer PRIMARY KEY, name text NOT NULL UNIQUE, duration integer, owner text NOT NULL)"
db.cur.execute(setup_shops_table)
db.con.commit()
'''
db.add_shop('shop1', 5, 'Stan')
db.add_shop('shop2', 3, 'Nav')
db.check_shops()
print(db.update_all_shop_durations())
print(db.update_all_shop_durations())
print(db.update_all_shop_durations())
for shop in db.update_all_shop_durations():
    print(shop[0])

db.cur.execute("DROP TABLE users")
setup_users_table = "CREATE TABLE users (id integer PRIMARY KEY, name text NOT NULL, rank integer, num_shops integer, coins integer)"
db.cur.execute(setup_users_table)

u = db.get_user("Stan")
u["num_shops"] += 1
db.update_user_by_data(u)
db.check_users()

db.con.commit()
'''
