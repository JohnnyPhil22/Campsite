import tkinter as tk
import subprocess

# commands to exec files within directory
def go_client():
    p=subprocess.Popen('python3 code/client.py', shell=True)
def go_serv_win():
    p=subprocess.Popen('python3 code/server.py', shell=True)

x = tk.Tk()
x.title('Chat App')
x.iconbitmap('logo.ico')

#logo
logox = tk.PhotoImage(file='resources/logo.png')

sos = tk.Label(image=logox)
sos.pack(pady=(10,5))
client = tk.Frame(x)
cli = tk.Button(client, text='Client', command=go_client, padx=40)
cli.pack(padx=20, pady=(10,5))
ser = tk.Button(client, text='Server', command=go_serv_win, padx=40)
ser.pack(padx=20, pady=(5,10))

client.pack(padx = 5)

x.resizable(False,False)
x.mainloop()