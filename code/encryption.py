from csv import *
def encrypt(ip):
    ip = str(ip)
    with open('key.csv','r') as u:
        p = reader(u)
        d={}
        for i in p:
            d[i[0]] = i[1]
        encrypted = ''
        u.seek(0)
        s = ''
        for i in ip:
            for j in d:
                if i == j:
                    s += d[j]
        return s

def decrypt(ip):
    with open('key.csv','r') as u:
        p = reader(u)
        d={}
        for i in p:
            d[i[0]] = i[1]
        encrypted = ''
        u.seek(0)
        s = ''
        for i in ip:
            for j in d:
                if i == d[j]:
                    s += j
        return s
