from flask import Flask, redirect, url_for, render_template, request, session
import praw
import sqlite3
import base64

app = Flask(__name__)
app.secret_key = 'M4Ix0YBRAv'

database_name = "C:\\Users\\e\\Documents\\cp 2024\\Pet Adoption\\db\\adoptionc.db"

# Authenticate with your Reddit app credentials
reddit = praw.Reddit(
    client_id='pQsMMBBe93M85ynowYljrQ',
    client_secret='Z39ezCXoMAxrTEbStahQwl7NtBSsCg',
    user_agent='TopImageFinderBot/1.0 by pika7414'
)

# Function to fetch the image URL from Reddit
def get_image_url():
    subreddit_name = "OneOrangeBraincell"
    try:
        hot_posts = reddit.subreddit(subreddit_name).hot(limit=10)
        for post in hot_posts:
            if post.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                return post.url
    except:
        return None

#put name into header
def get_username():
    if session.get('username') is not None:
        return session.get('username')
    return 'Guest'
# Function to get animals from the database
def get_animals():
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Animals')
        animals = cursor.fetchall()
        conn.close()
        return animals
    except sqlite3.Error as e:
        print('Error:', e)
        return []

# Function to get image data from the database
def get_image_data(animal_id):
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute('SELECT photograph1, photograph2, photograph3 FROM Animals WHERE id = ?', (animal_id,))
        image_data = cursor.fetchone()
        conn.close()
        encoded_images = [base64.b64encode(img).decode('utf-8') if img else '' for img in image_data]
        return encoded_images
    except sqlite3.Error as e:
        print('Error:', e)
        return [None, None, None]

# Function to connect to the database
def connect():
    try:
        conn = sqlite3.connect(database_name)
        return conn
    except sqlite3.Error as e:
        print(e)
        return None

# Function to validate login credentials
def validate_login(username, password):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        if user and user[2] == password:
            return True
    return False

# Function to insert a new user into the database
def insert_user(username, password, phone):
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Users (username, password, phone) VALUES (?, ?, ?)', (username, password, phone))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print('Error:', e)
    return False

# Function to insert a new pet into the database
def insert_pet(name, age, sex, fee, desc, typee, photos, username):
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            # Check if there are at least 3 photos uploaded
            if len(photos) >= 3:
                cursor.execute("INSERT INTO Animals (name, age, sex, adoption_fee, description, pet_type, user, photograph1, photograph2, photograph3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (name, age, sex, fee, desc, typee, username, photos[0], photos[1], photos[2]))
            elif len(photos) == 2:
                cursor.execute("INSERT INTO Animals (name, age, sex, adoption_fee, description, pet_type, user, photograph1, photograph2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (name, age, sex, fee, desc, typee, username, photos[0], photos[1],))
            elif len(photos) == 1:
                cursor.execute("INSERT INTO Animals (name, age, sex, adoption_fee, description, pet_type, user, photograph1) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                               (name, age, sex, fee, desc, typee, username, photos[0]))
            else:
                cursor.execute("INSERT INTO Animals (name, age, sex, adoption_fee, description, pet_type, user) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (name, age, sex, fee, desc, typee, username))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print('Error:', e)
    return False


# Function to hash the password (not implemented for simplicity)
def hash_password(password):
    return password

# Function to check if a user is an admin
def is_admin(username):
    # Ensure username is a string
    username = str(username)

    # Connect to the SQLite database
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Retrieve the admin status for the given username
    cursor.execute("SELECT admin FROM Users WHERE username=?", (username,))
    result = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # If the result is not None and admin column is True, return True
    if result and result[0]:  
        return True
    else:
        return False
#------------------------------------
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_login(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html', is_admin=is_admin)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        phone = request.form['phone']
        if insert_user(username, password, phone):
            return redirect(url_for('login'))
        else:
            return 'Registration failed'
    return render_template('register.html',is_admin=is_admin)

# Submit pet route
@app.route('/submit_pet', methods=['GET', 'POST'])
def submit_pet():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        sex = request.form['sex']
        fee = request.form['fee']
        desc = request.form['desc']
        typee = request.form['type']
        files = request.files.getlist('pic[]')
        photos = [file.read() if file else None for file in files]
        username = session.get('username')
        if insert_pet(name, age, sex, fee, desc, typee, photos, username):
            return redirect(url_for('home'))
        else:
            return 'Submission failed'

# Home route redirect
@app.route('/')
def index():
    return redirect(url_for('home'))

# Home route
@app.route('/home')
def home():
    logged_in = 'username' in session
    user = get_username()
    return render_template('index.html', image_url=get_image_url(), logged_in=logged_in, is_admin=is_admin,user=user)

# What we do route
@app.route('/what_we_do')
def what_we_do():
    user=get_username()
    logged_in = 'username' in session
    return render_template('what_we_do.html',is_admin=is_admin,user=user, logged_in=logged_in)

# Adopt route
@app.route('/adopt')
def adopt():
    user = get_username()
    if 'username' in session:
        animals = get_animals()
        logged_in = 'username' in session
        return render_template('adopt.html', animals=animals, get_image_data=get_image_data, is_admin=is_admin,user=user, logged_in=logged_in)
    else:
        return redirect(url_for('login'))

# Donate route
@app.route('/donate')
def donate():
    user = get_username()
    if 'username' in session:
        logged_in = 'username' in session
        return render_template('donate.html', is_admin=is_admin,user=user, logged_in=logged_in)
    else:
        return redirect(url_for('login'))
    
# Profile route
@app.route('/profile')
def profile():
    user = get_username()
    if 'username' in session:
        animals_profile = get_animals_profile()
        logged_in= 'username' in session
        return render_template('profile.html', animals=animals_profile, get_image_data=get_image_data_profile, is_admin=is_admin,user=user, logged_in=logged_in)
    else:
        return redirect(url_for('login'))


    
# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Admin route
@app.route('/admin')
def admin():
    user = get_username()
    logged_in= 'username' in session
    if is_admin(session.get('username')):
        try:
            conn = connect()
            if conn:
                users = conn.execute('SELECT * FROM Users').fetchall()
                animals = conn.execute('SELECT * FROM Animals').fetchall()
                conn.close()
                return render_template('admin.html', users=users, animals=animals, is_admin=is_admin,user=user, logged_in=logged_in)
        except sqlite3.Error as e:
            print('Error:', e)
    return 'Unauthorized', 401

# Route for deleting a user
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if is_admin(session.get('username')):
        conn = connect()
        if conn:
            # Check if the user being deleted is not an admin
            cursor = conn.cursor()
            cursor.execute('SELECT admin FROM Users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            if user and user[0] == 1:
                # If the user being deleted is an admin, return unauthorized
                return 'Unauthorized: Cannot delete admin user', 401
            
            # Proceed with deleting the user if they are not an admin
            conn.execute('DELETE FROM Users WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            return redirect(url_for('admin'))
    return 'Unauthorized', 401

# Route for deleting an animal
@app.route('/delete_animal/<int:animal_id>', methods=['POST'])
def delete_animal(animal_id):
    if is_admin(session.get('username')):
        conn = connect()
        if conn:
            conn.execute('DELETE FROM Animals WHERE id = ?', (animal_id,))
            conn.commit()
            conn.close()
            return redirect(url_for('admin'))
    return 'Unauthorized', 401

#own pets functions
def get_animals_profile():
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        user_id = session.get('username')
        cursor.execute('SELECT * FROM Animals WHERE user=?', (user_id,))
        animals = cursor.fetchall()
        conn.close()
        return animals
    except sqlite3.Error as e:
        print('Error:', e)
        return []

def get_image_data_profile(animal_id):
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute('SELECT photograph1, photograph2, photograph3 FROM Animals WHERE id = ?', (animal_id,))
        image_data = cursor.fetchone()
        conn.close()
        encoded_images = [base64.b64encode(img).decode('utf-8') if img else '' for img in image_data]
        return encoded_images
    except sqlite3.Error as e:
        print('Error:', e)
        return [None, None, None]
    


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
