from operator import ne
import tkinter as tk
from tkinter import N, NE, NW, SW, Entry, messagebox
import socket, threading



window = tk.Tk()
window.title("Client")
username = " "


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP
SERVER = extract_ip()
#SERVER = socket.gethostbyname(socket.gethostname())

def bob():
    l = miu.get()
    global SERVER, PORT, ADDR
    SERVER = l
    print(SERVER)
    PORT = 8080
    ADDR = (SERVER, PORT)

logse = tk.PhotoImage(file='resources/client.png')
fof = tk.Label(image=logse)
fof.pack(pady=(10,5), side=tk.TOP, anchor=NE, padx=5)
    
secframe = tk.Frame(window)
pq = tk.Label(secframe, text=f'[{SERVER}]').pack(side=tk.LEFT)
sensei = tk.Label(secframe, text = "IP:").pack(side=tk.LEFT)
miu = tk.Entry(secframe)
miu.pack(side=tk.LEFT)
tnConnect = tk.Button(secframe, text="Change", command=bob)
tnConnect.pack(side=tk.LEFT)
secframe.pack(side=tk.TOP, anchor=NE, padx=5)


topFrame = tk.Frame(window)


lblName = tk.Label(topFrame, text = "Name:").pack(side=tk.LEFT)
entName = tk.Entry(topFrame)
entName.pack(side=tk.LEFT)
btnConnect = tk.Button(topFrame, text="Connect", command=lambda : connect())
btnConnect.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, anchor=NE, padx=5)

displayFrame = tk.Frame(window)
lblLine = tk.Label(displayFrame, text="*********************************************************************").pack()
scrollBar = tk.Scrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(displayFrame, height=20, width=55)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
tkDisplay.tag_config("tag_your_message", foreground="blue")
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
displayFrame.pack(side=tk.TOP)
bottomFrame = tk.Frame(window)
tkMessage = tk.Text(bottomFrame, height=2, width=55)
tkMessage.pack(side=tk.LEFT, padx=(5, 0), pady=(5, 10))
tkMessage.config(highlightbackground="grey", state="disabled")
tkMessage.bind("<Return>", (lambda event: getChatMessage(tkMessage.get("1.0", tk.END))))
bottomFrame.pack(side=tk.BOTTOM, anchor=SW)
def connect():
    global username, client
    if len(entName.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        username = entName.get()
        connect_to_server(username)

# network client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#SERVER = input('SERVER:')
#SERVER = siu
#SERVER = socket.gethostbyname(socket.gethostname())

PORT = 8080
ADDR = (SERVER, PORT)

def connect_to_server(name):
    global client, PORT, ADDR
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        client.send(name.encode()) # Send name to server after connecting
        entName.config(state=tk.DISABLED)
        btnConnect.config(state=tk.DISABLED)
        tkMessage.config(state=tk.NORMAL)
        # start a thread to keep receiving message from server
        # do not block the main thread :)
        threading._start_new_thread(receive_message_from_server, (client, "m"))
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + SERVER + " on port: " + str(PORT) + " Server may be Unavailable. Try again later")
def receive_message_from_server(sck, m):
    while True:
        from_server = sck.recv(4096).decode()
        if not from_server: break
        # display message from server on the chat window
        # enable the display area and insert the text and then disable.
        # why? Apparently, tkinter does not allow us insert into a disabled Text widget :(
        texts = tkDisplay.get("1.0", tk.END).strip()
        tkDisplay.config(state=tk.NORMAL)
        if len(texts) < 1:
            tkDisplay.insert(tk.END, from_server)
        else:
            tkDisplay.insert(tk.END, "\n\n"+ from_server)
        tkDisplay.config(state=tk.DISABLED)
        tkDisplay.see(tk.END)
        # print("Server says: " +from_server)
    sck.close()
    window.destroy()
def getChatMessage(msg):
    msg = msg.replace('\n', '')
    texts = tkDisplay.get("1.0", tk.END).strip()
    # enable the display area and insert the text and then disable.
    # why? Apparently, tkinter does not allow use insert into a disabled Text widget :(
    tkDisplay.config(state=tk.NORMAL)
    if len(texts) < 1:
        tkDisplay.insert(tk.END, "You->" + msg, "tag_your_message") # no line
    else:
        tkDisplay.insert(tk.END, "\n\n" + "You->" + msg, "tag_your_message")
    tkDisplay.config(state=tk.DISABLED)
    send_mssage_to_server(msg)
    tkDisplay.see(tk.END)
    tkMessage.delete('1.0', tk.END)
def send_mssage_to_server(msg):
    client_msg = str(msg)
    client.send(client_msg.encode())
    if msg == "exit":
        client.close()
        window.destroy()
    print("Sending message")
window.mainloop()