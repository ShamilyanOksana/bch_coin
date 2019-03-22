import socket
import json
import Blockchain


class Network:
    bch = Blockchain.BlockChain()

    def get_message(self):
        '''
        Сервер. получает сообщение, отправляет его в модуль Blockchain
        '''
        while True:
            sock = socket.socket()
            # HOST = socket.gethostname()
            sock.bind(('', 9090))
            sock.listen(1)
            conn, address = sock.accept()
            self.add_new_ip(address[0])
            package = conn.recv(32768)
            package = json.loads(package.decode())
            if package:
                self.bch.get_package(package)
            sock.close()

    def send_message(self, data):
        '''
        Клиент, отправляет сообщение в сеть
        '''
        if str(type(data)) == "<class 'str'>":
            data = json.dumps(data, sort_keys=True).encode()
        elif str(type(data)) == "<class 'dict'>":
            data = json.dumps(data, sort_keys=True).encode()
        print(data)
        hostname = socket.gethostname()
        my_ip = socket.gethostbyname(hostname)
        self.add_new_ip(my_ip)
        ip_list = self.get_all_ip()
        for ip in ip_list:
            sock = socket.socket()
            try:
                sock.settimeout(5)
                sock.connect((ip, 9090))
                sock.send(data)
                sock.settimeout(None)
                sock.close()
            except Exception:
                sock.close()

    def add_new_ip(self, ip):
        '''
        Добавление нового ip в список всех ip-адресов
        '''
        try:
            status = 0
            with open('ip.txt', 'r') as ips:
                header = ips.readline()
                for row in ips:
                    if row[:-1] == ip:
                        status = 0
                        break
                    else:
                        status = 1
            if status:
                with open('ip.txt', 'a') as ips:
                    ips.write(ip+'\n')
        except Exception:
            pass

    def get_all_ip(self):
        '''
        Возвращает список всех ip-адресов
        '''
        ip_list = []
        with open('ip.txt', 'r') as ips:
            ips.readline()
            for row in ips:
                ip_list.append(row[:-1])
        return ip_list

    def send_to_user(self, ip, data):
        sock = socket.socket()
        try:
            sock.settimeout(5)
            sock.connect((ip, 9090))
            sock.send(data)
            sock.settimeout(None)
            sock.close()
        except Exception:
            sock.close()