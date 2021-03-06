import tkinter as tk
import socket, threading, csv
import encryption
from datetime import datetime

window = tk.Tk()
window.title("Server")
window.iconbitmap('resources/icon.ico')
SERVER = socket.gethostbyname(socket.gethostname())
encrypted_ip = encryption.encrypt(SERVER)
print(SERVER)
print(encrypted_ip)


# Top frame consisting of two buttons widgets (i.e. btnStart, btnStop)
logse = tk.PhotoImage(file='resources/server.png')
fof = tk.Label(image=logse)
fof.pack(pady=(10,5))

topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Connect", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(pady=(5, 0))

# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Code: Start to get code!")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=15, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 8080
ADDR = (SERVER, PORT)
client_name = " "
clients = []
clients_names = []

with open('../logfile.csv','a') as logfile:
    csv.writer().write('Server started at',datetime.now().strftime('%d/%/%Y %H:%M:%S'))

# Start server function
def start_server():
    global server, ADDR, PORT # code is fine without this
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)

    server.bind((ADDR))
    server.listen(5)  # server is listening for client connection

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Code: " + encrypted_ip
    lblPort["text"] = "Port: " + str(PORT)
    with open('logfile.csv','a') as logfile:
        csv.writer(logfile).write('Server started at',datetime.now().strftime('%d/%/%Y %H:%M:%S'))

# Stop server function
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)
    with open('logfile.csv','a') as logfile:
        csv.writer(logfile).write('Server stopped at',datetime.now().strftime('%d/%/%Y %H:%M:%S'))

def accept_clients(the_server, y):
    while True:
        client, addr = the_server.accept()
        clients.append(client)
        # use a thread so as not to clog the gui thread
        threading._start_new_thread(send_receive_client_message, (client, addr))

# Function to receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, clients_addr
    client_msg = " "
    # send welcome message to client
    client_name  = client_connection.recv(4096).decode()
    welcome_msg = "Welcome " + client_name + ". Use 'exit' to quit"
    client_connection.send(welcome_msg.encode())

    clients_names.append(client_name)

    update_client_names_display(clients_names)  # update client names display

    while True:
        data = client_connection.recv(4096).decode()
        if not data: break
        if data == "exit": break

        client_msg = data

        idx = get_client_index(clients, client_connection)
        sending_client_name = clients_names[idx]

        for c in clients:
            if c != client_connection:
                server_msg = str(sending_client_name + "->" + client_msg)
                c.send(server_msg.encode())

    # find the client index then remove from both lists(client name list and connection list)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    server_msg = "BYE!"
    client_connection.send(server_msg.encode())
    client_connection.close()

    update_client_names_display(clients_names)  # update client names display

# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx

# Update client name display when a new client connects OR
# When a connected client disconnects
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n")
    tkDisplay.config(state=tk.DISABLED)

window.resizable(False,False)
window.mainloop()