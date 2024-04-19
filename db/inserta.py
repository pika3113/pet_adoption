import sqlite3
import os

# Insert a new animal into the database
def insert_animal(database_name, name, age, photograph, sex, adoption_fee, description, pet_type):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    # Convert image file to binary data
    with open(photograph, 'rb') as file:
        photo_data = file.read()
   
    #print(type(photo_data))  # Debug print
    
    cursor.execute('''INSERT INTO Animals (name, age, photograph, sex, adoption_fee, description, pet_type) 
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (name, age, photo_data, sex, adoption_fee, description, pet_type))
    
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    database_name = r"C:\Users\pika\Documents\cp 2024\Pet Adoption\db\adoptionc.db"
    pics_folder = os.path.abspath("Documents\cp 2024\Pet Adoption\db\pics")

    # Inserting
    try:
        photograph_path = os.path.join(pics_folder, "1.png")
        print(photograph_path)
        insert_animal(database_name, "Rawr",2, photograph_path, "Female", 100.0, "Another cute and playful cat", "Cat")
        print("Insertion successful")
    except Exception as e:
        print("Error during insertion:", e)
