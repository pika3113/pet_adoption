import sqlite3
import os

def insert_animal(database_name, name, age, photograph1, photograph2, photograph3, sex, adoption_fee, description, pet_type):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    # Convert image file to binary data
    photo_data1 = None
    photo_data2 = None
    photo_data3 = None
    
    if os.path.exists(photograph1):
        with open(photograph1, 'rb') as file:
            photo_data1 = file.read()
    if os.path.exists(photograph2):
        with open(photograph2, 'rb') as file:
            photo_data2 = file.read()
    if os.path.exists(photograph3):
        with open(photograph3, 'rb') as file:
            photo_data3 = file.read()
    
    # Inserting with available photos
    cursor.execute('''INSERT INTO Animals (name, age, photograph1, photograph2, photograph3, sex, adoption_fee, description, pet_type) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (name, age, photo_data1, photo_data2, photo_data3, sex, adoption_fee, description, pet_type))
    conn.commit()
    print("Insertion successful")
    
    conn.close()

if __name__ == "__main__":
    database_name = r"C:\Users\e\Documents\cp 2024\Pet Adoption\db\adoptionc.db"
    pics_folder = os.path.abspath("Documents\cp 2024\Pet Adoption\db\pics")
    print("Pics folder:", pics_folder)  # Print out the pics_folder for debugging
    # Inserting
    try:
        insert_animal(database_name, "Rawr", 2, os.path.join(pics_folder, "1.png"), os.path.join(pics_folder, "2.png"), os.path.join(pics_folder, "3.webp"), "Female", 100.0, "Another cute and playful cat", "Cat")
    except Exception as e:
        print("Error during insertion:", e)
