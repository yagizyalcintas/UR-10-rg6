from rtde_control import RTDEControlInterface as RTDEControl
from rtde_receive import RTDEReceiveInterface as RTDEReceive
from rtde_io import RTDEIOInterface as RTDEIO
from urTD import get_td
import requests
import socket
import time
import json


from flask import Flask, request, abort,redirect, url_for,flash



from jsonschema import Draft6Validator
from sys import exit


try:
    from PIL import Image
except ImportError:
    exit("This script requires the pillow module\nInstall with: sudo pip install pillow")

# ---------------- CONFIG ----------------
#TD_DIRECTORY_ADDRESS = "http://172.16.1.100:8080"
global DEFAULTSPEED
DEFAULTSPEED = 0.5
global DEFAULTACCELERATION
DEFAULTACCELERATION = 0.5
global HOMELOCATION
HOMELOCATION = {"x": 00.55, "y": -490 , "z":1026, "base":0.00,"shoulder":-90,"elbow":0.00,"wrist1":-90.00,"wrist2":0.00,"wrist3":0.00}


td = 0
app = Flask(__name__)


@app.route("/ur10/")
def thing_description():
    return json.dumps(get_td(ip_addr)), {'Content-Type': 'application/json'}


@app.route("/ur10/properties/homeloc", methods=["GET"])
def homeloc():
    x = json.dumps(HOMELOCATION)
    print(type(json.dumps(HOMELOCATION)))
    print(json.dumps(HOMELOCATION))
    return x , {'Content-Type': 'application/json'}


@app.route("/ur10/properties/curLocation", methods=["GET"])
def curLocation():
    rtde_c = RTDEControl("172.16.1.222")
    rtde_r = RTDEReceive("172.16.1.222")
    TCPpose = rtde_r.getActualTCPPose()
    TCPpose[0]= TCPpose[0]*1000
    TCPpose[1]= TCPpose[1]*1000
    TCPpose[2]= (TCPpose[2]-0.4)*1000
    return json.dumps(TCPpose), {'Content-Type': 'application/json'}

@app.route("/ur10/properties/curJointPos", methods=["GET"])
def curJointPos():
    rtde_c = RTDEControl("172.16.1.222")
    rtde_r = RTDEReceive("172.16.1.222")
    init_q = rtde_r.getActualQ()
    for i in range (6):
        init_q[i]= init_q[i]*57.29
    return json.dumps(init_q), {'Content-Type': 'application/json'}


@app.route("/ur10/properties/moveSpeed", methods=["GET","PUT"])
def speed():
    global DEFAULTSPEED
    if request.method == "PUT":
        if request.is_json:
            print((request.json))
            if type(request.json) == float and 0 <= request.json <= 1:
                DEFAULTSPEED = request.json
                return "new default speed is {}".format(DEFAULTSPEED)
            else:
                abort(400)
        else:
            abort(415)
    else:
        return json.dumps(DEFAULTSPEED), {'Content-Type': 'application/json'}

@app.route("/ur10/properties/moveAcceleration", methods=["GET","PUT"])
def acceleration():
    global DEFAULTACCELERATION
    if request.method == "PUT":
        if request.is_json:
            print((request.json))
            if type(request.json) == float and 0 <= request.json <= 1:
                DEFAULTACCELERATION = request.json
                return "new default acceleration is {}".format(DEFAULTACCELERATION)
            else:
                abort(400)
        else:
            abort(415)
    else:
        return json.dumps(DEFAULTACCELERATION), {'Content-Type': 'application/json'}


@app.route("/ur10/actions/goHome", methods=["POST"])
def goHome():
    rtde_c = RTDEControl("172.16.1.222")
    rtde_r = RTDEReceive("172.16.1.222")
    list1 = []
    global HOMELOCATION
    for key, value in  HOMELOCATION.items():
        list1.append(value)
    print(list1)
    jointPoslist = []
    for i in range (6):
        jointPoslist.append(list1[i+3])
    print(jointPoslist)
    for i in range (6):
        jointPoslist[i]= jointPoslist[i]/57.29
    rtde_c.moveJ(jointPoslist, DEFAULTSPEED, DEFAULTACCELERATION, False)
    return "" ,204


@app.route("/ur10/actions/turnBase", methods=["POST"])
def turnBase():

    if request.is_json:
        # schema = td["actions"]["turnBase"]["input"]
        # valid_input = Draft6Validator(schema).is_valid(request.json)
        degree = request.json["base"]
        
        if type(degree) == float and -360 < degree and degree < 360: #valid_input
            print((type(degree)))
            rtde_c = RTDEControl("172.16.1.222")
            rtde_r = RTDEReceive("172.16.1.222")
            init_q = rtde_r.getActualQ()
            new_q = init_q[:]
            new_q[0] += degree/57.29
            rtde_c.moveJ(new_q, DEFAULTSPEED, DEFAULTACCELERATION, False)
            return "new base degree is: {}".format(new_q[0]) 
        else:
            return "input out of bound"
            abort(400)

    else:
        return "Error 415"
        abort(415)


##################################################3
@app.route("/ur10/actions/turnShoulder", methods=["POST"])
def turnShoulder():

    if request.is_json:
        # schema = td["actions"]["turnBase"]["input"]
        # valid_input = Draft6Validator(schema).is_valid(request.json)
        degree = request.json["shoulder"]
        
        if type(degree) == float and -360 < degree and degree < 360: #valid_input
            print(degree)
            rtde_c = RTDEControl("172.16.1.222")
            rtde_r = RTDEReceive("172.16.1.222")
            init_q = rtde_r.getActualQ()
            new_q = init_q[:]
            new_q[1] += degree/57.29
            rtde_c.moveJ(new_q, DEFAULTSPEED, DEFAULTACCELERATION, False)
            return "new shoulder degree is: {}".format(new_q[1]) 
        else:
            return "input out of bound"
            abort(400)

    else:
        return "Error 415"
        abort(415)


@app.route("/ur10/actions/turnElbow", methods=["POST"])
def turnElbow():

    if request.is_json:
        # schema = td["actions"]["turnBase"]["input"]
        # valid_input = Draft6Validator(schema).is_valid(request.json)
        degree = request.json["elbow"]
        
        if type(degree) == float and -360 < degree and degree < 360: #valid_input
            print((type(degree)))
            rtde_c = RTDEControl("172.16.1.222")
            rtde_r = RTDEReceive("172.16.1.222")
            init_q = rtde_r.getActualQ()
            new_q = init_q[:]
            new_q[2] += degree/57.29
            rtde_c.moveJ(new_q, DEFAULTSPEED, DEFAULTACCELERATION, False)
            return "new elbow degree is: {}".format(new_q[2]) 
        else:
            return "input out of bound"
            abort(400)

    else:
        return "Error 415"
        abort(415)


@app.route("/ur10/actions/turnWrist1", methods=["POST"])
def turnWrist1():

    if request.is_json:
        # schema = td["actions"]["turnBase"]["input"]
        # valid_input = Draft6Validator(schema).is_valid(request.json)
        degree = request.json["wrist1"]
        
        if type(degree) == float and -360 < degree and degree < 360: #valid_input
            print((type(degree)))
            rtde_c = RTDEControl("172.16.1.222")
            rtde_r = RTDEReceive("172.16.1.222")
            init_q = rtde_r.getActualQ()
            new_q = init_q[:]
            new_q[3] += degree/57.29
            rtde_c.moveJ(new_q, DEFAULTSPEED, DEFAULTACCELERATION, False)
            return "new wrist1 degree is: {}".format(new_q[3]) 
        else:
            return "input out of bound"
            abort(400)

    else:
        return "Error 415"
        abort(415)


@app.route("/ur10/actions/turnWrist2", methods=["POST"])
def turnWrist2():

    if request.is_json:
        # schema = td["actions"]["turnBase"]["input"]
        # valid_input = Draft6Validator(schema).is_valid(request.json)
        degree = request.json["wrist2"]
        
        if type(degree) == float and -360 < degree and degree < 360: #valid_input
            print((type(degree)))
            rtde_c = RTDEControl("172.16.1.222")
            rtde_r = RTDEReceive("172.16.1.222")
            init_q = rtde_r.getActualQ()
            new_q = init_q[:]
            new_q[4] += degree/57.29
            rtde_c.moveJ(new_q, DEFAULTSPEED, DEFAULTACCELERATION, False)
            return "new wrist2 degree is: {}".format(new_q[4]) 
        else:
            return "input out of bound"
            abort(400)

    else:
        return "Error 415"
        abort(415)


@app.route("/ur10/actions/turnWrist3", methods=["POST"])
def turnWrist3():

    if request.is_json:
        # schema = td["actions"]["turnBase"]["input"]
        # valid_input = Draft6Validator(schema).is_valid(request.json)
        degree = request.json["wrist3"]
        
        if type(degree) == float and -360 < degree and degree < 360: #valid_input
            print((type(degree)))
            rtde_c = RTDEControl("172.16.1.222")
            rtde_r = RTDEReceive("172.16.1.222")
            init_q = rtde_r.getActualQ()
            new_q = init_q[:]
            new_q[5] += degree/57.29
            rtde_c.moveJ(new_q, DEFAULTSPEED, DEFAULTACCELERATION, False)
            return "new wrist3 degree is: {}".format(new_q[5]) 
        else:
            return "input out of bound"
            abort(400)

    else:
        return "Error 415"
        abort(415)     

#and type(value)== float and -360<value<360
@app.route("/ur10/actions/SetJointDegrees", methods=["POST"])
def SetJointDegrees():

    if request.is_json:
        jointList = [None]*6
        print(request.json)
        print(type(request.json))

        # schema = td["actions"]["turnBase"]["input"]
        # valid_input = Draft6Validator(schema).is_valid(request.json)
        for key in request.json.keys():
            if key == "base" :
                jointList[0] = request.json["base"]/57.29
            elif key == "shoulder":
                jointList[1] = request.json["shoulder"]/57.29
            elif key == "elbow":
                jointList[2] = request.json["elbow"]/57.29
            elif key == "wrist1":
                jointList[3] = request.json["wrist1"]/57.29
            elif key == "wrist2":
                jointList[4] = request.json["wrist2"]/57.29
            elif key == "wrist3":
                jointList[5] = request.json["wrist3"]/57.29

        print(jointList)
        rtde_c = RTDEControl("172.16.1.222")
        rtde_r = RTDEReceive("172.16.1.222")
        init_q = rtde_r.getActualQ()
        print(init_q)

        for i in range (6):
            if not jointList[i] == None:
                init_q[i]=jointList[i]
            else:
                pass  

        new_q = init_q[:]
        print(new_q)
        rtde_c.moveJ(new_q, DEFAULTSPEED, DEFAULTACCELERATION, False)
        return "new joint degree values are: {}".format(new_q)
    else:
        return "Error 415"
        abort(415)  

###################################################333

@app.route("/ur10/actions/goTo", methods=["POST"])
def goTo():
    global DEFAULTACCELERATION
    global DEFAULTSPEED
    if request.is_json:
        GoList = [None]*3
        print(request.json)
        print(type(request.json))

        # schema = td["actions"]["turnBase"]["input"]
        # valid_input = Draft6Validator(schema).is_valid(request.json)
        for key in request.json.keys():
            if key == "x" :
                GoList[0] = request.json["x"]/1000 
            elif key == "y":
                GoList[1] = request.json["y"]/1000 
            elif key == "z":
                GoList[2] = request.json["z"]/1000 + 0.4
            elif key == "s" and 0 < request.json["s"] <= 1:
                DEFAULTSPEED = request.json["s"]
            elif key == "a"and 0 < request.json["a"] <= 1:
                DEFAULTACCELERATION = request.json["a"]


        print(GoList)
        rtde_c = RTDEControl("172.16.1.222")
        rtde_r = RTDEReceive("172.16.1.222")
        TCPpose = rtde_r.getActualTCPPose()
        print(TCPpose)

        for i in range (3):
            if not GoList[i] == None:
                TCPpose[i]=GoList[i]
            else:
                pass  

        new_q = TCPpose[:]
        print(new_q)
        rtde_c.moveL(new_q,DEFAULTSPEED,DEFAULTACCELERATION , False)
        TCPpose = rtde_r.getActualTCPPose()
        TCPpose[0]= TCPpose[0]*1000
        TCPpose[1]= TCPpose[1]*1000
        TCPpose[2]= (TCPpose[2]-0.4)*1000
        return "new position values are: {}".format(TCPpose)
    else:
        return "Error 415"
        abort(415)  


@app.route("/ur10/actions/Move", methods=["POST"])
def Move():
    global DEFAULTACCELERATION
    global DEFAULTSPEED
    if request.is_json:
        GoList = [None]*3
        print(request.json)
        print(type(request.json))

        # schema = td["actions"]["turnBase"]["input"]
        # valid_input = Draft6Validator(schema).is_valid(request.json)
        for key in request.json.keys():
            if key == "x" :
                GoList[0] = request.json["x"]/1000 
            elif key == "y":
                GoList[1] = request.json["y"]/1000 
            elif key == "z":
                GoList[2] = request.json["z"]/1000 + 0.4
            elif key == "s" and 0 < request.json["s"] <= 1:
                DEFAULTSPEED = request.json["s"]
            elif key == "a"and 0 < request.json["a"] <= 1:
                DEFAULTACCELERATION = request.json["a"]


        print(GoList)
        rtde_c = RTDEControl("172.16.1.222")
        rtde_r = RTDEReceive("172.16.1.222")
        TCPpose = rtde_r.getActualTCPPose()
        print(TCPpose)

        for i in range (3):
            if not GoList[i] == None:
                TCPpose[i]+= GoList[i]
            else:
                pass  

        new_q = TCPpose[:]
        print(new_q)
        rtde_c.moveL(new_q,DEFAULTSPEED,DEFAULTACCELERATION , False)
        TCPpose = rtde_r.getActualTCPPose()
        TCPpose[0]= TCPpose[0]*1000
        TCPpose[1]= TCPpose[1]*1000
        TCPpose[2]= (TCPpose[2]-0.4)*1000
        return "new position values are: {}".format(TCPpose)
    else:
        return "Error 415"
        abort(415) 



@app.route("/ur10/actions/gripClose", methods=["POST"])
def gripClose(): 

    rtde_io_ = RTDEIO("172.16.1.222")
    rtde_receive_ = RTDEReceive("172.16.1.222")
    rtde_io_.setStandardDigitalOut(0, False)
    return "", 204

@app.route("/ur10/actions/gripOpen", methods=["POST"])
def gripOpen(): 

    rtde_io_ = RTDEIO("172.16.1.222")
    rtde_receive_ = RTDEReceive("172.16.1.222")
    rtde_io_.setStandardDigitalOut(0, True)
    return "", 204

##################################33


# wait for Wifi to connect
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# while True:
#     try:
#         # connect to router to ensure a successful connection
#         s.connect(('172.16.1.1', 80))
#         ip_addr = s.getsockname()[0] + ":" + str(8080)
#         print(ip_addr)
#         break
#     except OSError:
#         time.sleep(5)




# Run app server
app.run(host='0.0.0.0', port=8080)