global HOMELOCATION
HOMELOCATION = {"x": 00.55, "y": -490 , "z":1026, "base":0.00,"shoulder":-90,"elbow":0.00,"wrist1":-90.00,"wrist2":0.00,"wrist3":0.00}


def listfun():
    list1 = []
    global HOMELOCATION
    for key, value in  HOMELOCATION.items():
        list1.append(value)
    print(list1)
    jointPoslist = []
    for i in range (6):
        jointPoslist.append(list1[i+3])
    print(jointPoslist)

    # global HOMELOCATION
    # keys_list[6] = list(HOMELOCATION)
    # print(keys_list)
    # key = keys_list[0]



#     global HOMELOCATION
#     homeJoints = []

#     for i in range (5):
#         homeJoints[i] = list(HOMELOCATION.values()).index(3)
#     print(homeJoints)

listfun()