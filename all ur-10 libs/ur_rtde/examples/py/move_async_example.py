from rtde_control import RTDEControlInterface as RTDEControl
from rtde_receive import RTDEReceiveInterface as RTDEReceive
import time

global DEFAULTSPEED
DEFAULTSPEED = 0.2
DEFAULTACCELERATION = 0.2
global HOMELOCATION
HOMELOCATION = {"x": 00.55, "y": -490 , "z":1026, "base":0.00,"shoulder":-90,"elbow":0.00,"wrist1":-90.00,"wrist2":0.00,"wrist3":0.00}

rtde_c = RTDEControl("172.16.1.222")
rtde_r = RTDEReceive("172.16.1.222")
init_q = rtde_r.getActualQ() # output is around 1/57.29 the degree value on screen
TCPpose = rtde_r.getActualTCPPose() # x and y is 1/1000 what is on the screen, z is different: 1/1000 + 0.4
# z comparisons: 0.681 output but 281 on screen, 0.400 when 0.35(almost 0) on screen, 0.501 when 101 on screen
# TCPpose[0]= TCPpose[0]*1000
# TCPpose[1]= TCPpose[1]*1000
# TCPpose[2]= (TCPpose[2]-0.4)*1000
print(init_q)
print(TCPpose)


# Target in the robot base
new_q = init_q[:]
new_q[0] += 0.3745
new_q[2] += 0.4



# Move asynchronously in joint space to new_q, we specify asynchronous behavior by setting the async parameter to
# 'True'. Try to set the async parameter to 'False' to observe a default synchronous movement, which cannot be stopped
# by the stopJ function due to the blocking behaviour.

rtde_c.moveJ(new_q, 0.4, 0.3, False)
#time.sleep(0.9)
# Stop the movement before it reaches new_q
#rtde_c.stopJ(0.5)

# Target in the Z-Axis of the TCP
target = rtde_r.getActualTCPPose()
target[2] += 0.9

# Move asynchronously in cartesian space to target, we specify asynchronous behavior by setting the async parameter to
# 'True'. Try to set the async parameter to 'False' to observe a default synchronous movement, which cannot be stopped
# by the stopL function due to the blocking behaviour.
#rtde_c.moveL(target, 0.5, 0.5, True)
#time.sleep(0.2)
# Stop the movement before it reaches target
#rtde_c.stopL(0.5)

# Move back to initial joint configuration
#rtde_c.moveJ(init_q)

# Stop the RTDE control script
rtde_c.stopScript()
