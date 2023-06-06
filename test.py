import psycopg2
import random

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="budget",
    user="postgres",
    password="1q2w3e4r5t6yAli!!"
)
    
# Create a cursor object to execute SQL queries
cur = conn.cursor()

# Get the car part number from the user
part_number = input("Enter car part number to search: ")

# Execute the SQL query to fetch the car part by number
cur.execute("SELECT * FROM carparts WHERE number = %s", (part_number,))

# Fetch the row from the result set
row = cur.fetchone()

# Display the car part if found
if row:
    print("Car Part Found:")
    print("Number:", row[0])
    print("Name:", row[1])
    print("Price:", row[2])
    print("Inventory:", row[3])
    print("Description:", row[4])
else:
    print("Car Part not found.")

# Close the cursor and connection
cur.close()
conn.close()