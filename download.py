# %%
from ftplib import FTP
from os import getcwd
from pathlib import Path
import time
import sys

CURR_DIR = Path(getcwd())
with open("download.log", mode='w', encoding='utf-8') as f:
    f.write("")


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
        server_list = []
        for line in content[3:]:
            arr = line.replace('\n', '').split(',')
            conf = dict()
            conf['name'] = arr[0].strip()
            conf['host'] = arr[1].strip()
            conf['user'] = arr[2].strip()
            conf['passwd'] = arr[3].strip()
            server_list.append(conf)
    return dest, server_list

# %%


def dl_(dest, ftp):
    ftp.cwd('lamp_sample')
    for directory in ftp.nlst():
        start_time = time.time()
        local_dir = Path.joinpath(dest, server_config['name'], directory)
        if not local_dir.is_dir():
            local_dir.mkdir(parents=True)
        ftp.cwd(directory)

        filenames = ftp.nlst()
        for i, filename in enumerate(filenames):
            local_file = Path.joinpath(local_dir, filename)
            if local_file.is_file():
                print(
                    f"skipped: {server_config['name']}/{directory} {i+1}/{len(filenames)}")
                sys.stdout.flush()
                continue
            print(
                f"retriving: {server_config['name']}/{directory} {i+1}/{len(filenames)}")
            sys.stdout.flush()

            with open(local_file, mode='wb') as f:
                ftp.retrbinary('RETR ' + filename, f.write)
        ftp.cwd('..')
        with open("download.log", encoding="utf8", mode="a") as f:
            f.write("function cost {:.3f} seconds\n".format(
                time.time() - start_time))


def dl(dest, server_config):
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)

    with FTP(host=server_config['host']) as ftp:
        ftp.login(user=server_config['user'], passwd=server_config['passwd'])
        dl_(dest=dest, ftp=ftp)

# %%


if __name__ == '__main__':
    dest, server_list = read_config()
    for server_config in server_list:
        dl(dest, server_config)
