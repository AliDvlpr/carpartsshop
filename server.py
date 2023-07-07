import socket
import threading
import psycopg2

def handle_client(client_socket, client_address):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        
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
                client_socket.sendall("enter part id:\n".encode())
                part_id_data = client_socket.recv(1024)
                
                if part_id_data:
                    try:
                        part_id = int(part_id_data.decode().strip())
                        
                        client_socket.sendall("amount of parts you buy:\n".encode())
                        reduce_amount_data = client_socket.recv(1024)
                        
                        if reduce_amount_data:
                            try:
                                reduce_amount = int(reduce_amount_data.decode().strip())
                                response = handle_option_4(part_id, reduce_amount)
                            except ValueError:
                                response = "Invalid input. Please enter a number.\n"
                                
                    except ValueError:
                        response = "Invalid input. Please enter a number.\n"
            else:
                response = "Invalid option. Please try again.\n"
        except ValueError:
            response = "Invalid input. Please enter a number.\n"
        
        client_socket.sendall(response.encode())

    print(f"Client {client_address} disconnected")
    client_socket.close()

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

def handle_option_4(part_id, reduce_amount):
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

    # Display the matching car part and update inventory
    response = ""
    if rows:
        row = rows[0]
        
        response += "Car Part Found:\n"
        response += f"Number: {row[0]}\n"
        response += f"Name: {row[1]}\n"
        response += f"Price: {row[2]}\n"
        response += f"Old Inventory: {row[3]}\n"
        response += f"New Inventory: {row[3] - reduce_amount}\n"
        response += f"Description: {row[4]}\n\n"

        # Calculate the updated inventory value
        updated_inventory = row[3] - reduce_amount

        # Execute the SQL query to update the inventory
        cur.execute("UPDATE carparts SET inventory = %s WHERE number = %s", (updated_inventory, part_id))
        conn.commit()

        response += "Your transaction is completed.\n"
        
    else:
        response += "Car Part not found.\n"

    # Close the cursor and connection
    cur.close()
    conn.close()
    
    return response

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)  # Maximum number of queued connections

print('Server is running. Waiting for connections...')

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Client {client_address} connected")

    # Start a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
