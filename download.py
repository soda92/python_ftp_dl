# %%
from ftplib import FTP
from os import getcwd
from pathlib import Path

CURR_DIR = Path(getcwd())


def read_config():
    conf_file = Path.joinpath(CURR_DIR, 'config.txt')
    if not conf_file.is_file():
        conf_file = Path.joinpath(CURR_DIR, 'config.example.txt')
    dest = Path.joinpath(CURR_DIR, 'data')
    server_list = []
    with open(conf_file, mode='r', encoding='utf-8') as f:
        content = f.readlines()
        dest_conf = content[1].replace('\n', '').split('=')[1]
        dest_conf = dest_conf.strip()
        if dest_conf != '':
            dest = dest_conf
        server_list = [line.replace('\n', '').split(',')
                       for line in content[3:]]
    return dest, server_list


# %%
dest, server_list = read_config()
name, ip, username, password = server_list[0]
# %%
ftp = FTP(source_address=(ip, 22), user=username, passwd=password)

# %%


def dl(dest, server):
    dest = Path(dest).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    for name, ip, username, password in server:
        with FTP(host=ip, user=username, passwd=password) as ftp:
            FTP.retrbinary()
