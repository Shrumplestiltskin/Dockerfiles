#!/usr/bin/python3
import docker
from sys import argv, exit

client = docker.from_env()

if __name__ == '__main__':
    if len(argv) < 2:
        print('Script takes unseal key as arg')
        exit(0)

    for x in client.containers.list():
        if 'vault' in x.attrs['Config']['Image']:
            x.exec_run('vault operator unseal %s' % argv[1])
            vault_status = x.exec_run('vault status')
            print(vault_status[1].decode('utf-8'), sep='\n')
