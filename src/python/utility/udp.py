import pymel.core as pm
import socket

UDP_IP="127.0.0.1"
UDP_PORT=9300

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind( (UDP_IP, UDP_PORT) )

if not pm.objExists('info'):
    loc = pm.spaceLocator(n='info')
else:
    loc = pm.PyNode('info')
# end if create info loc 

print('#### start processing ####')

while True:
    # receive data and filter out position
    data = sock.recv(1024)
    pm.refresh()
    if not data:
        continue
    # end if no data
    if data == 'q':
        sock.close()
        print('#### end processing ####')
        break
    # end if break out and close socket
    position = [float(ds) for ds in data.split(';')]
    position.append(0.0)
    loc.t.set(position)
# end while receive data till hitting q key


# 
# 
# #T.13 - 47
# #Python to Maya script test
# 
# # establish library for udp connection
# import socket
# 
# counter = 0
# 
# #set IP + port for the receiver
# UDP_IP="localhost"
# UDP_PORT=5005
# 
# sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
# #bind receiver to the adress
# sock.bind( (UDP_IP,UDP_PORT) )
# 
# #while true read. buffer size is 1024 bytes. message is set in data.
# while True:
#     print('starting to read..')
#     data, addr = sock.recvfrom(1024)
#     print("received message:", data)
#     if data != 0:
#         counter += 1
#         print("bytes received:", len(data))
#         print(counter)
#         
#         
# 
# print(counter)