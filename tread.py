import threading
import Network
import Mining

net = Network.Network()
t1 = threading.Thread(name='server', target=net.get_message)
t1.start()

m = Mining.Mining()
t2 = threading.Thread(name='maining', target=m.collecting_block, args={2})
t2.start()
