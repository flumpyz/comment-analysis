import sqlite3


class DataBaserForVideos:

    @staticmethod
    def create_tables(curs, connect):
        curs.execute("""CREATE TABLE IF NOT EXISTS channels(
           id INT PRIMARY KEY);
        """)
        curs.execute("""CREATE TABLE IF NOT EXISTS videos(
            id INT PRIMARY KEY,
            name TEXT NOT NULL,
            link_to_video TEXT,
            date_of_download DATE NOT NULL,
            channel_id INT NOT NULL,
            FOREIGN KEY (channel_id) REFERENCES channels(id));
        """)
        curs.execute("""CREATE TABLE IF NOT EXISTS comments(
            id INTEGER PRIMARY KEY autoincrement,
            comment TEXT NOT NULL,
            video_id INT NOT NULL,
            FOREIGN KEY (video_id) REFERENCES videos(id));
        """)
        connect.commit()

    @staticmethod
    def insert_comments_to_database(comments, video_id):
        connection = None
        try:
            connection = sqlite3.connect('youtube.db')
            cur = connection.cursor()
            DataBaserForVideos.create_tables(cur, connection)
            for comment in comments:
                comment_information = (comment, video_id)
                cur.execute("INSERT INTO comments(comment, video_id) VALUES(?, ?);",
                            comment_information)
            connection.commit()
            cur.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if connection:
                connection.close()
                print("Соединение с SQLite закрыто")
            return video_id

    @staticmethod
    def insert_channel_to_database(channel_id):
        connection = None
        try:
            connection = sqlite3.connect('youtube.db')
            cur = connection.cursor()
            DataBaserForVideos.create_tables(cur, connection)
            cur.execute("INSERT INTO channels(id) VALUES(?);", channel_id)
            connection.commit()
            cur.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if connection:
                connection.close()
                print("Соединение с SQLite закрыто")
                return channel_id

    @staticmethod
    def insert_video_to_database(video_id, video_name, video_link, download_date, channel_id=0):
        connection = None
        video_information = (video_id, video_name, video_link, download_date, channel_id)
        video_id = None
        try:
            connection = sqlite3.connect('youtube.db')
            cur = connection.cursor()
            DataBaserForVideos.create_tables(cur, connection)
            cur.execute("INSERT INTO videos(id, name, link_to_video, date_of_download, channel_id) "
                        "VALUES(?, ?, ?, ?, ?);",
                        video_information)
            connection.commit()
            cur.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if connection:
                connection.close()
                print("Соединение с SQLite закрыто")
                return video_id

    # Реализовать. Метод должен по video_id возвращать либо True, либо False
    # True - если в базе данных есть данные о видео с данным id,
    # False - если в базе данных нет данных о видео с таким id
    @staticmethod
    def check_is_video_in_database(video_id):
        connection = None
        is_video_in_database = False
        try:
            connection = sqlite3.connect('youtube.db')
            cur = connection.cursor()
            DataBaserForVideos.create_tables(cur, connection)
            cur.execute("""SELECT * FROM videos WHERE video_id = ?""", video_id)
            lines_in_request = cur.fetchall()
            if len(lines_in_request) != 0:
                is_video_in_database = True
            cur.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if connection:
                connection.close()
                print("Соединение с SQLite закрыто")
                return is_video_in_database
