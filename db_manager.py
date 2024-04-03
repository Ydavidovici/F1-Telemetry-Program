import sqlite3


class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
    
    def insert_lap_data(self, data):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO lap_data (car_position, last_lap_time, current_lap_time, sector, current_lap_num)
            VALUES (?, ?, ?, ?, ?);
        ''', (data['car_position'], data['last_lap_time'], data['current_lap_time'], data['sector'], data['current_lap_num']))
        conn.commit()
        conn.close()

