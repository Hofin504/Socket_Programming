import socket
import base64
import os
from function_common import * 

def download_mail(s, number_mail):
    s.send(f"RETR {number_mail}\r\n".encode())
    con = s.recv(1024).decode()
    file_size = int(con.split()[1]) 
    file_size -= 1024
    while file_size >= 0: 
        data = s.recv(1024)
        con += data.decode()
        file_size -= 1024
    return con 

def readinfo_mail(s, number_mail) :
    con = download_mail(s, number_mail)
    boundary = readinfo_json("boundary")
    content_file = con 
    From = con[con.find("From:") + 6: con.find("Subject") - 2]

    con = con.split(f"{boundary}\r\n")
    tmp = str(con[1])
    subject_mail = tmp[tmp.find("Subject:") + 9: tmp.find(boundary) - 46]
    con[2] = con[2].split("\r\n")

    content_mail = con[2][2]
    
    list_file = []
    for i in range(3,len(con) - 1):
        New = con[i].split("\r\n")
        cont = ""
        file_name = New[0][New[0].find('name=') + 5: ]
        for i in range(3,len(New)) : cont += New[i]
        list_file.append((file_name,cont))
    return content_file, From, subject_mail, content_mail, list_file
      

def list_email_name(pop_conn):
    pop_conn.sendall(b'UIDL\r\n')
    response=pop_conn.recv(1024).decode().split();
    uidl=[]
    for i in range(2,len(response)-1,2):
        uidl.append(response[i])
    return uidl

def retrieve_email_with_attachment(pop3_host, pop3_port, username, password):
    pop_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    pop_conn.connect((pop3_host, pop3_port))

    response = pop_conn.recv(1024).decode()

    # Send user credentials
    pop_conn.sendall(f'USER {username}\r\n'.encode())
    response = pop_conn.recv(1024).decode()

    pop_conn.sendall(f'PASS {password}\r\n'.encode())
    response = pop_conn.recv(1024).decode()

    pop_conn.sendall(b'LIST\r\n')
    response = pop_conn.recv(1024).decode()

    num_messages = len(response.splitlines())-2

    email_name_list=list_email_name(pop_conn)

    return pop_conn, num_messages, email_name_list

def received_mailserver(pop3_username, pop3_password) : 
     # Set your POP3 server details
     pop3_host = readinfo_json("mailserver")
     pop3_port = readinfo_json("POP3")  # Standard POP3 port

     # # Call the retrieve_email_with_attachment_socket function
     return retrieve_email_with_attachment(pop3_host, pop3_port, pop3_username, pop3_password)
