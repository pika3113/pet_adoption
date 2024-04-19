import sqlite3
import os

#create a new SQLite database
def create_database(database_name):
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        
        # Create Animals table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Animals (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            age INTEGER,
                            photograph1 BLOB,
                            photograph2 BLOB,
                            photograph3 BLOB,
                            sex TEXT,
                            adoption_fee REAL,
                            description TEXT,
                            pet_type TEXT,
                            user TEXT
                        )''')
        
        # Create Users table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL,
                            phone INTEGER,
                            admin INTEGER DEFAULT 0
                        )''')
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print('error:', e)

if __name__ == "__main__":
    database_name = r"C:\Users\e\Documents\cp 2024\Pet Adoption\db\adoptionc.db"
    create_database(database_name)
    
    
    
    
