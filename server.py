import socket
import psycopg2

def handle_option_1():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        database="budget",
        user="postgres",
        password="1q2w3e4r5t6yAli!!"
    )

    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    # Execute the SQL query to fetch all car parts
    cur.execute("SELECT * FROM carparts")

    # Fetch all the rows from the result set
    rows = cur.fetchall()

        # Display the car parts
    response = ""
    for row in rows:
        response += f"Number: {row[0]}\n"
        response += f"Name: {row[1]}\n"
        response += f"Price: {row[2]}\n"
        response += f"Inventory: {row[3]}\n"
        response += f"Description: {row[4]}\n\n"

    # Close the cursor and connection
    cur.close()
    conn.close()
    
    return response

def handle_option_2(search_term): 
    # Connect to the PostgreSQL database 
    conn = psycopg2.connect( 
        host="localhost",
        database="budget",
        user="postgres",
        password="1q2w3e4r5t6yAli!!"
        ) 
    # Create a cursor object to execute SQL queries 
    cur = conn.cursor() 

    # Execute the SQL query to fetch matching car parts by name
    cur.execute("SELECT * FROM carparts WHERE name ILIKE %s", ('%' + search_term + '%',))

    # Fetch all the rows from the result set 
    rows = cur.fetchall() 
    
    # Display the matching car parts 
    response = "" 
    if rows: 
        response += "Matching car parts:\n" 
        for row in rows: 
            response += f"Number: {row[0]}\n" 
            response += f"Name: {row[1]}\n" 
            response += f"Price: {row[2]}\n" 
            response += f"Inventory: {row[3]}\n" 
            response += f"Description: {row[4]}\n\n" 

    else: 
        response = "No matching car parts found.\n" 
    # Close the cursor and connection 
    cur.close() 
    conn.close() 

    return response

def handle_option_3(part_id):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        database="budget",
        user="postgres",
        password="1q2w3e4r5t6yAli!!"
    )

    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    # Execute the SQL query to fetch matching car part by number
    cur.execute("SELECT * FROM carparts WHERE number = %s", (part_id,))

    # Fetch all the rows from the result set
    rows = cur.fetchall()

        # Display the matching car part
    response = ""
    if rows:
        response += "Matching car part:\n"
        for row in rows:
            response += f"Number: {row[0]}\n"
            response += f"Name: {row[1]}\n"
            response += f"Price: {row[2]}\n"
            response += f"Inventory: {row[3]}\n"
            response += f"Description: {row[4]}\n\n"
    else:
        response += "No matching car part found.\n"

    # Close the cursor and connection
    cur.close()
    conn.close()
    
    return response

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)
print('server is running')
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Client {client_address} connected")
    message = "hi welcome to car part shop select an operation:\n1 - see all available parts\n2 - find parts by name\n3 - find parts by id\n4 - buy parts with id\n"
    client_socket.sendall(message.encode())

    data = client_socket.recv(1024)
    if data:
        print(f"Received data: {data.decode()}")
        try:
            option = int(data.decode())
            if option == 1:
                response = handle_option_1()

            elif option == 2:
                client_socket.sendall("search:\n".encode())
                search_term_data = client_socket.recv(1024)

                if search_term_data:
                    search_term = search_term_data.decode().strip()
                    response = handle_option_2(search_term)
                    
            elif option == 3:
                client_socket.sendall("enter part id:\n".encode())
                part_id_data = client_socket.recv(1024)
                
                if part_id_data:
                    try:
                        part_id = int(part_id_data.decode().strip())
                        response = handle_option_3(part_id)
                    except ValueError:
                        response = "Invalid input. Please enter a number.\n"

            elif option == 4:
                response = "You selected option 4: buy parts with id\n"
            else:
                response = "Invalid option. Please try again.\n"
        except ValueError:
            response = "Invalid input. Please enter a number.\n"
        
        client_socket.sendall(response.encode())
    
    client_socket.close()
