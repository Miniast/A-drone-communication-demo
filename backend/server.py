"""
Date: 05.28,2022.
Creator: Astrolopha
"""
# 服务器端sever.py

import socket
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
import time
from random import randint
from cutoff import *
import utils

app = Flask(__name__)
CORS(app)

server_ip = "127.0.0.1"
server_port = "8080"
dronesList = []


def result_process(data):
    return jsonify({'code': 200, 'result': data, 'message': 'ok', 'type': 'success'})


def get_newid():
    return chr(ord('A') + randint(0, 25)) + str(randint(1, 32))


def check_newid(newid):
    for drone in dronesList:
        if newid == drone['id']:
            return False
    return True


def find_drone_by_socket(socket_id):
    for drone in dronesList:
        if drone['socket_id'] == socket_id:
            return drone
    return False


@app.route("/")
def run():
    return "Hello World!"


@app.route("/drone_info", methods=['GET', 'POST'])
def getDronesInfo():
    return result_process(dronesList)


@app.route("/drone_record", methods=['POST'])
def get():
    return "hallo world"


@app.route("/send_message", methods=['POST'])
def handle_send_message():
    data = request.get_data()
    return result_process("Yes")


def register():
    while True:
        client, addr = server.accept()
        if find_drone_by_socket(client):
            print("Client already exists.")
            return

        print("New Client arrives.")

        newid = get_newid()
        while not check_newid(newid):
            newid = get_newid()

        new_drone = {
            'socket_id': client,
            'id': newid,
            'records': []
        }
        dronesList.append(new_drone)

        utils.send(client, {
            'type': 'register',
            'response': 'ok',
            'id': new_drone['id']
        })
        print("The new droneId is {0}".format(new_drone['id']))
        r = threading.Thread(target=recv_message, args=(client,))
        r.start()


def recv_message(client):
    while True:
        time.sleep(1)
        try:
            drone = find_drone_by_socket(client)
            if drone:
                data = utils.recv(client)
                if data == '':
                    print("The client has quit.")
                    dronesList.remove(drone)

        except BaseException as error:
            print("A connection has ended.")
            drone = find_drone_by_socket(client)
            dronesList.remove(drone)

        print("Transmission {0} from {1} to Server.".format(data['data'], drone['id']))


def send_message(client, dataset):
    drone = find_drone_by_socket(client)
    utils.send(client, {
        'type': 'send_message',
        'id': drone['id'],
        'data': dataset,
        'raw_data': eval('markSet' + str(dataset))
    })
    for drone in dronesList:
        if drone['socket_id'] == client:
            drone['records'].append(dataset)


if __name__ == '__main__':
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, int(server_port)))
    server.listen(10)
    print("Server start successfully. Waiting for connection...")
    t = threading.Thread(target=register)
    t.setDaemon(True)
    t.start()

    while True:
        if len(dronesList) == 0:
            print("Empty dronesList.")
        else:
            for (index, drone) in enumerate(dronesList):
                print(drone['id'])
        dataset = input("Select the markSet(1 ~ 25): ")
        try:
            dataset = int(dataset)
            if 0 <= dataset <= 25:
                target = input("Select the droneId: ")
                for drone in dronesList:
                    if drone['id'] == target:
                        send_message(drone['socket_id'], dataset)
        except:
            print("Illegal input.")
    # app.run()
