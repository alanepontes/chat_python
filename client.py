#!/usr/bin/env python
# coding: utf-8
# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

from __future__ import unicode_literals
import socket, select, string, sys, re


def get_name_user():
    regex = re.compile(r'([a-zA-Z0-9 _]+)', flags = re.IGNORECASE)
    nick_name = raw_input('>')
    while regex.match(nick_name) is None:
        print 'O nome de usuário não é válido, utilize alfabeto, numero ou _'
        nick_name = raw_input('>')
    return nick_name

def prompt(user_name) :
    sys.stdout.write('<'+user_name+'>')
    sys.stdout.flush()

if __name__ == "__main__":

    if(len(sys.argv) < 3) :
        print 'Uso : python client.py host port'
        sys.exit()

    user_name = get_name_user()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try :
        s.connect((host, port))
        s.send(user_name)
    except :
        print 'Não foi capaz de conectar'
        sys.exit()

    print 'Você entrou na sala. Diga oi!'
    prompt(user_name)

    while 1:
        socket_list = [sys.stdin, s]

        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            if sock == s:
                data = sock.recv(64)
                if not data :
                    print '\nServidor desconectado.'
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    prompt(user_name)

            else :
                msg = sys.stdin.readline()
                while(len(msg) > 64):
                    print 'Voce ultrapassou o limite de 64 caracteres, diminua sua mensagem'
                    msg = sys.stdin.readline()
                s.send("nick_name:"+user_name+" |message:"+msg)
                prompt(user_name)