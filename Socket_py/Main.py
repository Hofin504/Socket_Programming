from function_common import *
import mailsmtp 
import mailpop3 
import base64 
import os 
import shutil 

path_mailbox = "D:/Gmail/"

def content_choose1(list_mail, list_file, subject_mail, content_mail) :
    print("Day la thong tin soan email: (neu khong dien vui long nhan enter de bo qua)")
    
    # nhap thong in to,cc,bcc
    list_mail["to"] = input("To: ").replace(","," ").split()
    list_mail["cc"] = input("CC: ").replace(","," ").split()
    list_mail["bcc"] = input("BCC: ").replace(","," ").split()
    
    # nhap thong subject va content
    subject_mail = input("Subject: ")
    content_mail = input("Content: ")

    # nhap thong tin file 
    if (input("Co gui file (1.co, 2.khong): ") == "1") : 
        n = int(input("So luong file can gui: "))
        for i in range(1,n + 1): 
            print("Cho biet duong dan file thu ",end = "")
            list_file.append(input(f"{i}: ")) 

    return list_mail, list_file, subject_mail, content_mail  

def check_in_list(Listarray, key): 
    for i in Listarray: 
        if i == key: return True 
    return False

def creater_FilterFolder_mail():
    list_folder = []
    Filter = readinfo_json("Filter")
    for i in range(0,len(Filter)):
        folder_path = path_mailbox + Filter[i][list(Filter[i].keys())[1]]
        list_folder.append(Filter[i][list(Filter[i].keys())[1]])
        os.makedirs(folder_path, mode=0o777, exist_ok = True)
        os.makedirs(folder_path + "/Read", mode=0o777, exist_ok = True)
        os.makedirs(folder_path + "/UnRead", mode=0o777, exist_ok = True)
    
    folder_path = path_mailbox + "Inbox"
    list_folder.append("Inbox")
    os.makedirs(folder_path, mode=0o777, exist_ok = True)
    os.makedirs(folder_path + "/Read", mode=0o777, exist_ok = True)
    os.makedirs(folder_path + "/UnRead", mode=0o777, exist_ok = True)

    return list_folder

def mail_in_folder(): 
    Filter = readinfo_json("Filter")
    list_file_in_folder = []
    for i in range(0,len(Filter)):
        folder_path = path_mailbox + Filter[i][list(Filter[i].keys())[1]]
        for i in os.listdir(folder_path + "/Read"): list_file_in_folder.append(i) 
        for i in os.listdir(folder_path + "/UnRead"): list_file_in_folder.append(i) 
    
    folder_path = path_mailbox + "Inbox"
    for i in os.listdir(folder_path + "/Read"): list_file_in_folder.append(i) 
    for i in os.listdir(folder_path + "/UnRead"): list_file_in_folder.append(i)  

    return list_file_in_folder

def Filter_mail(s, list_folder, number_mail, namemail):
    content_file, From, subject, content, list_file = mailpop3.readinfo_mail(s, number_mail) 
    Filter = readinfo_json("Filter")
    if check_in_list(Filter[0]["From"], From): 
        with open(path_mailbox + Filter[0]["From-to"] + "/UnRead/" + namemail, "w") as f: 
            f.write(content_file)
    elif check_in_list(Filter[1]["Subject"], subject): 
            with open(path_mailbox + Filter[0]["Subject-to"] + "/UnRead/" + namemail, "w") as f: 
                 f.write(content_file)
    elif check_in_list(Filter[2]["Content"], content): 
            with open(path_mailbox + Filter[0]["Content-to"] + "/UnRead/" + namemail, "w") as f: 
                 f.write(content_file)
    elif check_in_list(Filter[3]["Spam"], subject) or check_in_list(Filter[3]["Spam"], content): 
            with open(path_mailbox + Filter[0]["Spam-to"] + "/UnRead/" + namemail, "w") as f: 
                 f.write(content_file)
    else:
            with open(path_mailbox + "Inbox/UnRead/" + namemail,"w") as f:
                f.write(content_file)


def downloadFile(File,path):
    filename,file_data=File
    path+=f'\\{filename}'
    #print(file_data.encode())
    with open(path, 'wb') as attachment_file:
        attachment_file.write(base64.b64decode(file_data))

def read_content(file_path): 
    with open(file_path,"r") as f: 
        boundary = readinfo_json("boundary")
        content_file = con = f.read() 
        From = con[con.find("From:") + 6: con.find("Subject") - 2]
        con = con.split(f"{boundary}\n\n")
        tmp = con[1]
        subject_mail = tmp[tmp.find("Subject:") + 9: ]
        subject_mail = subject_mail.split("\n\n")[0]
        con[2] = con[2].split("\n\n")

        content_mail = con[2][2]
    
        list_file = []
        for i in range(3,len(con) - 1):
            New = con[i].split("\n\n")
            cont = ""
            file_name = New[0][New[0].find('name=') + 5: ]
            for i in range(2,len(New)) : cont += New[i]
            list_file.append((file_name,cont)) 
        return content_file, From, subject_mail, content_mail, list_file

def content_choose2(s, number_of_mail, list_namemail, list_folder): 
    print("Day la danh sach cac mail trong folder cua ban: ")
    for i in range(0,len(list_folder)): print(f"{i + 1}. {list_folder[i]}")
    choose = input("Ban muon xem mail trong folder nao: ")
    if (choose == ""): return
    choose = int(choose)
    print("Day la danh sach trong " + list_folder[choose - 1] + " folder")

    list_fileof_Folder = os.listdir(path_mailbox + list_folder[choose - 1] + "/UnRead/")
    c = 0
    list_fileFolder = []
    T = []
    for i in list_fileof_Folder: 
        content_file, From, subject_mail, content_mail, list_file = read_content(path_mailbox + list_folder[choose - 1] + "/UnRead/" + i)
        T.append((path_mailbox + list_folder[choose - 1],"/UnRead/", i))
        list_fileFolder.append([From,subject_mail,content_mail,list_file])
        c = c + 1
        print(f"{c}. (chua doc) <{From}> <{subject_mail}>")
    list_fileof_Folder = os.listdir(path_mailbox + list_folder[choose - 1] + "/Read/")
    for i in list_fileof_Folder: 
        content_file, From, subject_mail, content_mail, list_file = read_content(path_mailbox + list_folder[choose - 1] + "/Read/" + i)
        c = c + 1
        list_fileFolder.append([From,subject_mail,content_mail,list_file])
        T.append((path_mailbox + list_folder[choose - 1],"/Read/", i))
        print(f"{c}. <{From}> <{subject_mail}>")

    pos = input("Ban doc mail thu may: ")
    if (pos == ""): return 
    pos = int(pos)

    From, subject, content, list_file = list_fileFolder[pos - 1]
    print(f"noi dung mail cua mail thu {pos} la: {content}")
    if (len(list_file) != 0):
        yn = input("Trong file co attached file, ban co muon save file khong (1.co, 2.khong): ")
        if (yn == "1"):
            path = input("cho biet duong dan muon luu: ")
            for i in list_file: 
                downloadFile(i, path)
    shutil.move(T[pos - 1][0] + T[pos - 1][1] + T[pos - 1][2],T[pos - 1][0] + "/Read/" + T[pos - 1][2])
    

def MENU() :
    print("Vui long chon Menu: ")
    print("1. De gui email")
    print("2. De xem danh sach cac email da nhan")
    print("3. Thoat")
    choose = input("Ban chon: ")
    if (choose == "3"): return
    if (choose == "1"): 
        list_mail = {"to": [], "cc": [], "bcc": []}
        list_file = []
        subject_mail = content_mail = ""
        list_mail, list_file, subject_mail, content_mail = content_choose1(list_mail, list_file, subject_mail, content_mail)
        mailsmtp.client_mail(list_mail,list_file,subject_mail,content_mail)
    else:
        pop3_username = input("username: ");
        pop3_password = input("password: ");
        
        global path_mailbox
        path_mailbox += pop3_username + "/";
        
        list_folder = creater_FilterFolder_mail()
        list_mail_in_folder = mail_in_folder()
        
        s, number_of_mail, list_namemail = mailpop3.received_mailserver(pop3_username,pop3_password)
        
        for i in range(0,len(list_namemail)):
            if check_in_list(list_mail_in_folder, list_namemail[i]): continue # neu loc roi thi bo qua 
            Filter_mail(s, list_folder, i + 1, list_namemail[i])
        s.send("QUIT\r\n".encode())

        content_choose2(s, number_of_mail, list_namemail, list_folder)
    MENU()

if __name__ == "__main__":
    MENU()