import Network
import socket
import os

sync = {'type': 'synchronize'}

id = len(os.listdir('C:\\Users\\USER\\PycharmProjects\\Blockchain-master\\chain'))

sock = socket.socket()
host = socket.gethostname()
ip = socket.gethostbyname(host)

sync.update({'chain': id})
sync.update({'ip': ip})

net = Network.Network()

net.send_message(sync)
