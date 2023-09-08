#!/bin/python

# Netcat clone as seen in the book 'Blackhat Python by Justin Seitz and Tim Arnold. Thank you!'

import argparse
import shlex
import subprocess
import sys
import textwrap

def execute(cmd):
    cmd = cmd.strip()

    if not cmd:
        return

    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)

    return output.decode()

class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.1 -p 5555 -l -c # command shell
            netcat.py -t 192.168.1.1 -p 5555 -l -u=mytest.txt # upload file
            netcat.py -t 192.168.1.1 -p 5555 -l -e=\'cat /etc/passwd\' # execute command 
            echo 'ABC' | ./netcat.py -t 192.168.1.1 -p 5555 # echo text to server
            netcat.py -t 192.168.1.1 -p 5555 # connect to server
        '''))

    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.1', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')

    args = parser.parse_args()

    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()
