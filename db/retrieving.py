import sqlite3
import os
from PIL import Image
import io

# Function to retrieve all animals from the database
def get_all_animals(database_name):
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT * FROM Animals''')
        animals = cursor.fetchall()
        
        conn.close()
        return animals
    except sqlite3.Error as e:
        print("Error retrieving animals:", e)

# Function to display an image from binary data
def display_image_from_blob(image_blob):
    try:
        image_stream = io.BytesIO(image_blob)
        image = Image.open(image_stream)
        image.show()
    except Exception as e:
        print("Error displaying image:", e)

# Example usage
if __name__ == "__main__":
    database_name = "adoption_center.db"
    
    # Retrieving all animals
    animals = get_all_animals(database_name)
    if animals:
        for animal in animals:
            print("Name:", animal[1])
            print("Age:", animal[2])
            print("Sex:", animal[4])
            print("Adoption Fee:", animal[5])
            print("Description:", animal[6])
            print("Pet Type:", animal[7])
            
            # Displaying the image
            display_image_from_blob(animal[3])
    else:
        print("No animals found in the database.")