import tkinter as tk
import subprocess

# commands to exec files within directory
def go_client():
    cmd = 'py code/client.py'
    p= subprocess.Popen(cmd, shell=True)
def go_serv_win():
    cmd = 'py code/server.py'
    p= subprocess.Popen(cmd, shell=True)
def go_server():
    cmd = 'py code/server_lin.py'
    p= subprocess.Popen(cmd, shell=True)

x = tk.Tk()
x.title('Project Campsite - Home Page')
x.iconbitmap('resources/icon.ico')

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