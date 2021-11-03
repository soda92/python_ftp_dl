from ftplib import FTP
with FTP(host="192.168.1.79") as ftp:
    ftp.login(user="toybrick", passwd="toybrick")
    ftp.cwd("lamp_sample")
    filenames = ftp.nlst()
    print(filenames)
