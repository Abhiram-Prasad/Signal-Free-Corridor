import socket
import googlemaps
import urllib
import re
import json
from firebase import firebase

siglatitude=[12.923820,12.923051, 12.918555, 12.924393]
#siglatitude=[12.924552,12.923051, 12.918555]
#siglongitude=[77.498910, 77.501417, 77.500992]
siglongitude=[77.500555, 77.501417, 77.500992, 77.499876]
sigflag=[0]*len(siglatitude)
sigconnect=-1
lastdist=-1
k=0
listd=[]
signalorder = []

def distance(source,destination):
        gmaps = googlemaps.Client(key='AIzaSyCJvgqpMM6ErMdUMsJCYNCdUWFFbshFEOA')
        directions_result = gmaps.directions(source, destination, mode="transit",departure_time="now",units="metric")
        for map1 in directions_result:
            overall_stats = map1['legs']
            for dimensions in overall_stats:
                distance = dimensions['distance']
                dist=distance['value']
        return dist
                        
firebase = firebase.FirebaseApplication('https://codebeats-824ea.firebaseio.com/')

destlat=firebase.get('/dest_lat',None)
destlong = firebase.get('/dest_lng', None)
des=str(destlat)+","+str(destlong)

curlat=firebase.get('/lat',None)
curlong = firebase.get('/lng', None)
src=str(curlat)+","+str(curlong)

src = "12.923765,77.501039"
des = "12.926010, 77.499560"

#preprocessing
str1="https://roads.googleapis.com/v1/snapToRoads?path="+src+"|"+des+"&interpolate=true&key=AIzaSyA49vGtIQcknpKABOx43uWruW2i1fqSUYU"
z = urllib.urlopen(str1).read()

actual=distance(src,des)

for itr in range(len(siglatitude)):
        load = distance(src,str(siglatitude[itr])+","+str(siglongitude[itr]))+distance(str(siglatitude[itr])+","+str(siglongitude[itr]),des)
        if abs(load - actual)<=5:
                signalorder.append(itr)

print signalorder
lastcoor=str(curlat)+","+str(curlong)
 
while True:
    
    #connect to app and receive coordinates
    if(k==2):
            break
    amblat=firebase.get('/lat',None)
    amblon = firebase.get('/lng', None)
    source=str(amblat)+","+str(amblon)
    if(source==lastcoor):
        continue
    lastcoor=source
    
    #processing
    #calculate distance from signal
    siglat=siglatitude[signalorder[k]]
    siglon=siglongitude[signalorder[k]]
    source=''
    destination=''
    source=str(amblat)+","+str(amblon)
    print source
    destination=str(siglat)+","+str(siglon)
    gmaps = googlemaps.Client(key='AIzaSyCJvgqpMM6ErMdUMsJCYNCdUWFFbshFEOA')
    directions_result = gmaps.directions(source, destination, mode="transit",departure_time="now",units="metric")
    for map1 in directions_result:
        overall_stats = map1['legs']
        for dimensions in overall_stats:
            distance = dimensions['distance']
            dist=distance['value']
    if(sigconnect==-1):
        if(dist<100 and sigflag[k]==0):
            sigconnect=signalorder[k]
            d1 = -1
            
        if(sigconnect!=-1):
                #turn green
                if(k==1):
                        UDP_IP1 = "192.168.1.102"
                        UDP_PORT1 = 7777
                        m="1"
                        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto(m, (UDP_IP1, UDP_PORT1))
                        print "Sent 1"

                        UDP_IP = "192.168.1.101"
                        UDP_PORT = 8888
                        MESSAGE = "0"
                        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

                else:
                        UDP_IP = "192.168.1.101"
                        UDP_PORT = 8888
                        MESSAGE = "1"
                        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                        print "Sent 1"

                        UDP_IP1 = "192.168.1.102"
                        UDP_PORT1 = 7777
                        m="0"
                        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto(m, (UDP_IP1, UDP_PORT1))
                        print "Sent 0"

                listd.append(dist)

        else:
                if(k==1):
                        UDP_IP1 = "192.168.1.102"
                        UDP_PORT1 = 7777
                        m="0"
                        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto(m, (UDP_IP1, UDP_PORT1))
                        print "Sent 0"

                        UDP_IP = "192.168.1.101"
                        UDP_PORT = 8888
                        MESSAGE = "0"
                        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

                else:
                        UDP_IP = "192.168.1.101"
                        UDP_PORT = 8888
                        MESSAGE = "0"
                        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                        print "Sent 0"            

                        UDP_IP1 = "192.168.1.102"
                        UDP_PORT1 = 7777
                        m="0"
                        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto(m, (UDP_IP1, UDP_PORT1))
                        print "Sent 0"
     
        print dist
                

    else:
        #calculate distance from signal
        siglat=siglatitude[signalorder[k]]
        siglon=siglongitude[signalorder[k]]
        source=''
        destination=''
        source=str(amblat)+","+str(amblon)
        destination=str(siglat)+","+str(siglon)
        gmaps = googlemaps.Client(key='AIzaSyCJvgqpMM6ErMdUMsJCYNCdUWFFbshFEOA')
        directions_result = gmaps.directions(source, destination, mode="transit",departure_time="now",units="metric")
        for map1 in directions_result:
            overall_stats = map1['legs']
            for dimensions in overall_stats:
                distance = dimensions['distance']
                dist=distance['value']
        listd.append(dist)
        print dist

        #continue green
##        UDP_IP = "192.168.1.104"
##        UDP_PORT = 8888
##        MESSAGE = "1"
##        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
##        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
##        print "Send 1"
           
        if(len(listd)>=3):
            if d1<0:
                d1 = sum(listd)/3
                listd = []
                #continue green
                if(k==1):
                        UDP_IP1 = "192.168.1.102"
                        UDP_PORT1 = 7777
                        m="1"
                        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto(m, (UDP_IP1, UDP_PORT1))
                        print "Sent 1"

                        UDP_IP = "192.168.1.101"
                        UDP_PORT = 8888
                        MESSAGE = "0"
                        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

                else:
                        UDP_IP = "192.168.1.101"
                        UDP_PORT = 8888
                        MESSAGE = "1"
                        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                        print "Send 1"

                        UDP_IP1 = "192.168.1.102"
                        UDP_PORT1 = 7777
                        m="0"
                        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        sock.sendto(m, (UDP_IP1, UDP_PORT1))
                        print "Sent 0"

            else:
                d2 = sum(listd)/3
                if d2>d1 or  dist>100:
                        #turn red
                        if(k==1):
                                UDP_IP1 = "192.168.1.102"
                                UDP_PORT1 = 7777
                                m="0"
                                sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                                sock.sendto(m, (UDP_IP1, UDP_PORT1))
                                print "Sent 0"
                                sigconnect=-1
                                k+=1

                                UDP_IP = "192.168.1.101"
                                UDP_PORT = 8888
                                MESSAGE = "0"
                                sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

                        else:
                                UDP_IP = "192.168.1.101"
                                UDP_PORT = 8888
                                MESSAGE = "0"
                                sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                                sigflag[sigconnect]=1
                                sigconnect=-1
                                k+=1
                                print "Send 0"

                                UDP_IP1 = "192.168.1.102"
                                UDP_PORT1 = 7777
                                m="0"
                                sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                                sock.sendto(m, (UDP_IP1, UDP_PORT1))
                                print "Sent 0"

                else:
                        #continue green
                        if(k==1):
                                UDP_IP1 = "192.168.1.102"
                                UDP_PORT1 = 7777
                                m="0"
                                sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                                sock.sendto(m, (UDP_IP1, UDP_PORT1))
                                print "Sent 0"

                                UDP_IP = "192.168.1.101"
                                UDP_PORT = 8888
                                MESSAGE = "0"
                                sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

                        else:
                                UDP_IP = "192.168.1.104"
                                UDP_PORT = 8888
                                MESSAGE = "1"
                                sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                                print "Send 1"

                                UDP_IP1 = "192.168.1.102"
                                UDP_PORT1 = 7777
                                m="0"
                                sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                                sock.sendto(m, (UDP_IP1, UDP_PORT1))
                                print "Sent 0"

                d1 = d2
                listd = []         
