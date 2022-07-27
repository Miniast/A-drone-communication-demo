"""
Date: 05.28,2022.
Creator: Astrolopha
"""
# 客户端client.py

import socket
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
from cutoff import *
from random import randint
import utils

app = Flask(__name__)
CORS(app)

my_socket = None
drone_info = {}

server_ip = "127.0.0.1"
server_port = "8080"


def result_process(data):
    return jsonify({'code': 200, 'result': data, 'message': 'ok', 'type': 'success'})


def get_newid():
    return chr(ord('A') + randint(0, 25)) + str(randint(1, 32))


@app.route("/")
def run():
    return "hallo world"


@app.route("/register", methods=['GET'])
def register():
    newid = get_newid()
    drone_info['id'] = newid
    drone_info['records'] = []
    return result_process(drone_info['id'])


@app.route("/drone_info", methods=['GET', 'POST'])
def getDroneInfo():
    return result_process(drone_info)


@app.route("/drone_record", methods=['POST'])
def getDroneRecords():
    return result_process(drone_info['records'])


@app.route("/send_message", methods=['POST'])
def handle_send_message():
    data = request.get_data()
    print(data)
    return result_process("Yes")


def close_socket():
    utils.send(my_socket, {'type': 'close'})
    my_socket.shutdown(2)
    my_socket.close()


def register():
    global my_socket, drone_info
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.settimeout(5)
    my_socket.connect((server_ip, int(server_port)))

    server_response = utils.recv(my_socket)
    drone_info['id'] = server_response['id']
    drone_info['records'] = []

    t = threading.Thread(target=recv_message, args=())
    t.setDaemon(True)
    t.start()


def recv_message():
    global my_socket
    while True:
        data = utils.recv(my_socket)
        if data['type'] == 'send_message':
            dataset = 'markSet' + str(data['data'])
            data = data['raw_data']
            if data == eval(dataset):
                print("Message send and check successfully: {0} from Server to {1}".format(dataset,
                                                                                           drone_info['id']))
                drone_info['records'].append(data)
            else:
                print("Message damaged.")
            print("Transmission {0} from Server to {1}.".format(dataset, drone_info['id']))


def send_message(dataset):
    global my_socket
    msg = 'markSet' + str(dataset)
    data = eval(msg)
    utils.send(my_socket, {'type': 'send_message', 'id': drone_info['id'], 'data': msg, 'raw_data': data})


if __name__ == '__main__':
    register()
    while True:
        dataset = input("Select the markSet(1 ~ 25): ")
        send_message(dataset)
    # app.run()
