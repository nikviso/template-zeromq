#!/usr/bin/env python3

import os
import zmq
import json
import configparser
import argparse
import base64
from lib.AESCipher import *


def args_parse():
    """
    Arguments parsing:
    -c [/path/to/file]- configuration file path (default - current directory, file config.ini)
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', default='config.ini')
    args = parser.parse_args()

    return args


def config_parser(config_file):
    """
    Configuration file parsing.
    Returns dictionary with configuration parameters:
    'key_file' - AES key file path,
    'server_ip' - IP address for ZMQ routing server binding,
    'server_port' - Port number for ZMQ routing server binding,
    'pidfile' - PID file path,
    'loggerconf_file' - Logger configuration file path. 
    """
    
    config = configparser.ConfigParser()
    config.read(config_file)
    cinfig_dict = {'key_file': config.get('auth_file','key_file'),
                   'server_ip': config.get('ip_address_port','server_ip'),
                   'server_port': config.get('ip_address_port','server_port'),
                   'pidfile': config.get('pid_file','pidfile'),
                   'loggerconf_file': config.get('logger_config_file','loggerconf_file')
                  }
    
    return cinfig_dict


def main(config_params):

    # Getting AES key
    key_file = open(config_params['key_file'],"r")
    key = base64.b64decode(key_file.read())
    key_file.close()
    request_timeout = 2000 # timeout in milliseconds

    AESobj = AESCipher(key)
    context = zmq.Context()
    url_server = "tcp://" + config_params['server_ip'] + ":" + config_params['server_port']

    # Socket to talk to server
    print("Connecting to server…")
    socket = context.socket(zmq.REQ)
    # Set ØMQ socket options API link http://api.zeromq.org/master:zmq-setsockopt
    # socket.setsockopt(zmq.SNDBUF, 8192)
    # Get ØMQ socket options API link http://api.zeromq.org/master:zmq-getsockopt
    # print(socket.getsockopt(zmq.SNDBUF)) 
    socket.setsockopt(zmq.LINGER, 0)  
    socket.setsockopt(zmq.RCVTIMEO, request_timeout)
    socket.connect(url_server)
    
    print("Sending request…" )
    json_reqest = json.dumps({'request': 'getdata_2','user': 'username','password': '67890'})
    socket.send(AESobj.encrypt(json_reqest))
    
    try:
        replay_message = socket.recv()
    except zmq.error.ZMQError as s:
        print(s)
    else:
        message = AESobj.decrypt(replay_message)
        print("Received reply: %s " % message)
    finally:
        socket.close()
        context.term()

    
if __name__ == "__main__":
    config_params = config_parser(args_parse().c)
    # pid = str(os.getpid())
    # open(config_params['pidfile'], 'w').write(pid)

    main(config_params)    
