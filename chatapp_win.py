from cgitb import text
import imp
import tkinter as tk
import subprocess
from turtle import color

# commands to exec files within directory
def go_client():
    cmd = 'py client.py'
    p= subprocess.Popen(cmd, shell=True)
def go_serv_win():
    cmd = 'py server.py'
    p= subprocess.Popen(cmd, shell=True)
def go_server():
    cmd = 'py server_lin.py'
    p= subprocess.Popen(cmd, shell=True)


x = tk.Tk()
x.title('Chat App')

client = tk.Frame(x)
cli = tk.Button(client, text='Client', command=go_client, padx=40)
cli.pack(padx=20, pady=10)

client.pack(padx = 5)

server = tk.LabelFrame(x)
l = tk.Label(server,text='Server Options')
l.pack(padx=10, pady=5)
ser = tk.Button(server, text='Windows', command=go_serv_win)
ser.pack(padx=20, pady=10)
ser = tk.Button(server, text='Linux', command=go_server,padx=20)
ser.pack(padx=20, pady=10)


server.pack(padx = 20, pady=(0,20))





x.mainloop()
