import sqlite3


class SQL:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `Users`").fetchall()

    def get_status(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT status FROM `Users` WHERE `user_id` = ?", (user_id,)).fetchone()[0]

    def subscriber_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `Users` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=3):
        with self.connection:
            return self.cursor.execute("INSERT INTO `Users` (`user_id`, `status`) VALUES(?,?)",
                                       (user_id, status))


    def close(self):
        self.connection.close()
