import sqlite3

conn = sqlite3.connect('targets.db')
c = conn.cursor()

# Create the targets table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS targets
             (id INTEGER PRIMARY KEY, 
             hostname text, 
             mode text, 
             port integer, 
             wordlists text, 
             additional_keywords text, 
             status text, 
             login_param text, 
             password_param text,
             path
             )''')

conn.commit()
conn.close()
