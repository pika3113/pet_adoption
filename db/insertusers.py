import sqlite3

def insert_user(database_name, username, password, email, name, phone_number):
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        
        cursor.execute('''INSERT INTO Users (username, password, email, name, phone_number) 
                          VALUES (?, ?, ?, ?, ?)''', (username, password, email, name, phone_number))
        
        conn.commit()
        conn.close()
        print('User insertion successful')
    except sqlite3.Error as e:
        print('Error during user insertion:', e)

if __name__ == "__main__":
    database_name = "adoption_center1.db"
    # Inserting user data
    insert_user(database_name, "example_user", "password123", "user@example.com", "Example User", "1234567890")
