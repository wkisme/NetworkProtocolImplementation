from ftplib import FTP

def ftp_client():
    ftp = FTP('localhost')  # connect to host, default port
    ftp.login(user='wangkuo', passwd='147637')  # user anonymous, passwd anonymous@

    ftp.cwd('PycharmProjects')  # change into "debian" directory
    a = ftp.retrlines('LIST')  # list directory contents
    print(a)
    ftp.retrbinary('RETR readme', open('README', 'wb').write)

    ftp.quit()
    return a

if __name__ == '__main__':
    ftp_client()




