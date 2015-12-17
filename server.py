#!/usr/bin/env python
# coding: utf-8
# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

from __future__ import unicode_literals
import socket, select, re

def get_data_client (input_):
    data = {"nick_name":re.search('nick_name:([a-zA-Z0-9 _]+)\|', input_).group(1),"message":re.search('message:([a-zÀ-ÿA-Z0-9 ?!,.\-\_&]+)', input_).group(1) }
    return data


def broadcast_data (sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                socket.close()
                CONNECTION_LIST.remove(socket)

def send_message_yourself(sock, message):
    try :
        sock.send(message)
    except :
        sock.close()
        CONNECTION_LIST.remove(sock)


if __name__ == "__main__":

    CONNECTION_LIST = []
    RECV_BUFFER = 64
    PORT = 9000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(5)

    CONNECTION_LIST.append(server_socket)

    print "Servidor do chat iniciado na porta: " + str(PORT)

    while 1:
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])


        for sock in read_sockets:
            nick_name = ''
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                nick_name = sockfd.recv(RECV_BUFFER)
                print nick_name + " - (%s, %s) conectado" % addr

                broadcast_data(sockfd, nick_name + " - entrou na sala\n")

            else:
                try:
                    data = sock.recv(RECV_BUFFER)

                    if data:
                        if(len(CONNECTION_LIST) < 3):
                            send_message_yourself(sock, "\r" + '<Servidor> - Espere um pouco - Apenas voce esta logado!\n')
                        else:
                            dict_data = get_data_client(data)
                            broadcast_data(sock, "\r" + '<' + str(dict_data['nick_name']) + '> ' + dict_data['message'].encode('utf-8')+"\n")
                except:
                    broadcast_data(sock, nick_name + " - (%s, %s) está offline" % addr)
                    print nick_name + " - (%s, %s) está offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.close()