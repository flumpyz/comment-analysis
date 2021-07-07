import sqlite3
import datetime as dt

class SQL:

    def __init__(self, name):
        self.name = name

    def connect(self):
        self.conn = sqlite3.connect(str(self.name) + ".db", check_same_thread=False)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def create_table_for_admins(self):

        self.connect()
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS Admins 
                        (u_name text,
                        FOREIGN KEY (u_name) REFERENCES User (user_name) ON DELETE CASCADE)""")
        self.close()

    def create_table_for_moderators(self):

        self.connect()
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS Moderators 
                        (u_name text,
                        FOREIGN KEY (u_name) REFERENCES User (user_name) ON DELETE CASCADE)""")
        self.close()

    def insert_into_comments_table(self, _id, comment):

        self.connect()
        self.cursor.execute(f"""INSERT INTO Comments VALUES ('{_id}', '{comment}')""")
        self.close()

    def insert_into_admins_table(self, u_name):
        self.connect()
        self.cursor.execute(f"""INSERT INTO Admins VALUES ('{u_name}')""")
        self.close()

    def insert_into_moderators_table(self, u_name):
        self.connect()
        self.cursor.execute(f"""INSERT INTO Moderators VALUES ('{u_name}')""")
        self.close()

    def create_favourites_table(self):

        self.connect()
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS Favourites
                        (person_id text PRIMARY KEY, youtube_link text)""")
        self.close()

    def number_of_links(self, user_id):

        self.connect()
        self.cursor.execute(f"""SELECT COUNT(*) FROM Favourites WHERE person_id = '{user_id}'""")
        number = self.cursor.fetchall()
        return number
        self.close()

    def insert_into_favourites_table(self, person_id, youtube_link):

        self.connect()
        quantity_of_links = self.number_of_links(person_id)

        if quantity_of_links == 10:
            print('''You exceeded the limit for storing links in Favorites
                  Please delete one of the entries and repeat the operation''')
        else:
            self.cursor.execute(f"""INSERT INTO Favourites VALUES ('{person_id}','{youtube_link}')""")
        self.close()

    def check_in_favourites(self, username, link):
        self.connect()
        self.cursor.execute(f"""SELECT * FROM Favourites WHERE person_id = '{username}' and youtube_link = '{link}'""")
        result = self.cursor.fetchall()
        return result
        self.close()

    def delete_from_favourites_table(self, user_id, link):

        self.connect()
        self.cursor.execute(f"""DELETE FROM Favourites WHERE youtube_link = '{link}' and person_id = '{user_id}'""")
        self.close()

    def delete_from_admins_table(self, name):

        self.connect()
        self.cursor.execute(f"""DELETE FROM Admins WHERE u_name = '{name}'""")
        self.close()

    def delete_from_moderators_table(self, name):

        self.connect()
        self.cursor.execute(f"""DELETE FROM Moderators WHERE u_name = '{name}'""")
        self.close()

    def print_favorites_table(self, user_id):

        self.connect()
        self.cursor.execute(f"""SELECT * FROM Favourites WHERE person_id = '{user_id}'""")
        massive = self.cursor.fetchall()
        return massive
        self.close()

    def create_user_table(self):

        self.connect()
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS User 
                        (user_name text PRIMARY KEY, status text, date text)""")
        self.close()

    def insert_into_user_table(self, user_name, user_status):

        self.connect()
        date_of_entry = dt.date.today()
        self.cursor.execute(f"""INSERT INTO User VALUES ('{user_name}', '{user_status}', '{date_of_entry}')""")
        self.close()

    def print_user_table(self):

        self.connect()
        self.cursor.execute(f"SELECT * from User")
        result = self.cursor.fetchall()
        return result
        self.close()

    def update_state_in_user_table(self, user_name, number_state):

        self.connect()
        self.cursor.execute(f"UPDATE User set status = '{number_state}' where user_name = '{user_name}'")
        self.close()

    def get_user_state(self, user_name):

        self.connect()
        self.cursor.execute(f"select * from User where user_name = '{user_name}'")
        result = self.cursor.fetchall()
        return result
        self.close()

    def get_user_admin(self, name):
        self.connect()
        self.cursor.execute(f"select u_name from Admins where u_name = '{name}'")
        result = self.cursor.fetchone()
        return result
        self.close()

    def get_user_moderator(self, name):
        self.connect()
        self.cursor.execute(f"select u_name from Moderators where u_name = '{name}'")
        result = self.cursor.fetchone()
        return result
        self.close()

    def get_user(self, name):
        self.connect()
        self.cursor.execute(f"select user_name from User where user_name = '{name}'")
        result = self.cursor.fetchone()
        return result
        self.close()

    def create_statistic_table(self):

        self.connect()
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS Statistic 
                        (u_name text, action text, date text, video_url text,
                        FOREIGN KEY (u_name) REFERENCES User (user_name) ON DELETE CASCADE)""")
        self.close()

    def insert_into_statistic_table(self, name, action, video_url):

        self.connect()
        date_of_entry = dt.date.today()
        self.cursor.execute(f"""INSERT INTO Statistic VALUES ('{name}', '{action}', '{date_of_entry}', '{video_url}')""")
        self.close()

    def print_actions_from_statistic_table(self, action):

        self.connect()
        date_of_entry = dt.date.today()
        self.cursor.execute(
            f"select * from Statistic where date <= (select date('now')) and date >= (select date('now', '-7 days')) and action = '{action}'")
        result = self.cursor.fetchall()
        return result

    def check_new_users(self, date):

        self.connect()
        self.cursor.execute(f"Select * from User where date = '{date}'")
        result = self.cursor.fetchall()
        return result
        self.close

    def check_week_new_users(self):

        self.connect()
        date_of_entry = dt.date.today()
        self.cursor.execute(
            f"select count(*) from User where date <= (select date('now')) and date >= (select date('now', '-7 days'))")
        result = self.cursor.fetchall()
        return result
        self.close()

    def get_user_statistic(self, username):
        self.connect()
        self.cursor.execute(f"Select video_url From Statistic Where u_name = '{username}' ORDER BY ROWID DESC LIMIT 5")
        result = self.cursor.fetchall()
        return result



class Interaction:

    def __init__(self, database):
        self.database = database

    def create_statistic_table(self):
        self.database.create_statistic_table()

    def create_table(self, name):
        self.database.create_table(name)

    def create_table_for_comments(self):
        self.database.create_table_for_comments()

    def create_favourites_table(self):
        self.database.create_favourites_table()

    def create_user_table(self):
        self.database.create_user_table()

    def input_data(self, data):
        self.database.insert(data)

    def extract_obj_by_id(self, _id):
        obj = self.database.extract_obj_by_id(_id)
        return obj

    def check_actuality_by_id(self, _id):
        res = self.database.check_actuality_by_id(_id)
        return res

    def insert_into_comments_table(self, video_id, comment):
        self.database.insert_into_comments_table(video_id, comment)

    def insert_into_admins_table(self, u_name):
        self.database.insert_into_admins_table(u_name)

    def print_comments(self, _id):
        text = self.database.print_comments(_id)
        return text

    def get_user_admin(self, name):
        res = self.database.get_user_admin(name)
        return res

    def get_user_moderator(self, name):
        res = self.database.get_user_moderator(name)
        return res

    def get_user(self, name):
        res = self.database.get_user(name)
        return res

    def insert_into_favourites_table(self, person_id, youtube_link):
        self.database.insert_into_favourites_table(person_id, youtube_link)

    def delete_from_admins_table(self, name):
        self.database.delete_from_admins_table(name)

    def delete_from_moderators_table(self, name):
        self.database.delete_from_moderators_table(name)

    def delete_from_favourites_table(self, user_id, link):
        self.database.delete_from_favourites_table(user_id, link)

    def print_favorites_table(self, user_id):
        string = self.database.print_favorites_table(user_id)
        return string

    def create_table_for_admins(self):
        self.database.create_table_for_admins()

    def insert_into_user_table(self, user_name, user_status):
        self.database.insert_into_user_table(user_name, user_status)

    def print_user_table(self):
        result = self.database.print_user_table()
        return result

    def check_new_users(self, date):
        result = self.database.check_new_users(date)
        return result

    def update_state_in_user_table(self, user_name, number_state):
        self.database.update_state_in_user_table(user_name, number_state)

    def get_user_state(self, user_name):
        result = self.database.get_user_state(user_name)
        return result

    def insert_into_statistic_table(self, name, action, video_url):
        self.database.insert_into_statistic_table(name, action, video_url)

    def print_actions_from_statistic_table(self, action):
        result = self.database.print_actions_from_statistic_table(action)
        return result

    def check_week_new_users(self):
        result = self.database.check_week_new_users()
        return result

    def check_in_favourites(self, username, link):
        result = self.database.check_in_favourites(username, link)
        return result

    def create_table_for_moderators(self):
        self.database.create_table_for_moderators()

    def insert_into_moderators_table(self, u_name):
        self.database.insert_into_moderators_table(u_name)

    def get_user_statistic(self, username):
        result = self.database.get_user_statistic(username)
        return result