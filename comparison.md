## python-urx (https://github.com/SintefManufacturing/python-urx)

requirements:
-python3

note: Does not work with eurodam wifi.

installation:
-pip install urx
-git clone https://github.com/SintefManufacturing/python-urx.git

issues:
-test_move gives the error:  "File "test_movep.py", line 15, in <module> rob.movep(pose, acc=a, vel=v, radius=r, wait=False) TypeError: movep() got an unexpected keyword argument 'radius'"
soultion: After deleting the argument radius it works.

-spnav_control.py gives the error: "Traceback (most recent call last): File "spnav_control.py", line 3, in <module> import spnav ModuleNotFoundError: No module named 'spnav'"
solution: pip install spnav, but then it gives the error: "Traceback (most recent call last):
  File "spnav_control.py", line 3, in <module>
    import spnav
  File "/home/esi-emil/.local/lib/python3.7/site-packages/spnav/__init__.py", line 7, in <module>
    pythonapi.PyCObject_AsVoidPtr.restype = c_void_p
  File "/usr/lib/python3.7/ctypes/__init__.py", line 377, in __getattr__
    func = self.__getitem__(name)
  File "/usr/lib/python3.7/ctypes/__init__.py", line 382, in __getitem__
    func = self._FuncPtr((name_or_ordinal, self))
AttributeError: python3: undefined symbol: PyCObject_AsVoidPtr"
could not solve this error.

-matrices.py starts moving but then gives error: "Traceback (most recent call last):
  File "matrices.py", line 20, in <module>
    rob.translate((l, 0, 0), acc=a, vel=v)
  File "/home/esi-emil/.local/lib/python3.7/site-packages/urx/urrobot.py", line 429, in translate
    return self.movex(command, p, vel=vel, acc=acc, wait=wait)
  File "/home/esi-emil/.local/lib/python3.7/site-packages/urx/robot.py", line 180, in movex
    return self.set_pose(t, acc, vel, wait=wait, command=command, threshold=threshold)
  File "/home/esi-emil/.local/lib/python3.7/site-packages/urx/robot.py", line 105, in set_pose
    pose = URRobot.movex(self, command, t.pose_vector, acc=acc, vel=vel, wait=wait, threshold=threshold)
  File "/home/esi-emil/.local/lib/python3.7/site-packages/urx/urrobot.py", line 316, in movex
    self._wait_for_move(tpose[:6], threshold=threshold)
  File "/home/esi-emil/.local/lib/python3.7/site-packages/urx/urrobot.py", line 217, in _wait_for_move
    raise RobotException("Robot stopped")
urx.urrobot.RobotException: Robot stopped"
could not solve this error.

-get_robot gives: "WARNING:ursecmon:tried 11 times to find a packet in data, advertised packet size: -2, type: 3
WARNING:ursecmon:Data length: 68
WARNING:ursecmon:tried 11 times to find a packet in data, advertised packet size: -2, type: 3"
solution: could not solve it.




## ur-rtde 1.4.3 (https://gitlab.com/sdurobotics/ur_rtde/-/tree/master)

-A C++ interface for controlling and receiving data from a UR robot using the
Real-Time Data Exchange (RTDE)
interface of the robot. The interface can also by used with python, through the provided python bindings.

Key Features:

-Uses the Real-Time Data Exchange (RTDE) of the robot.
-Available on multiple platforms (Linux, Windows, macOS)
-Can be used from C++ and Python.
-Relies only on STL datatypes and can be used with various robot frameworks.
-Switchable register range (FieldBus / PLC [0..23] or external clients range [24..47])
-Has async move capability.
-Can be used with 500Hz.


Compatible Robots

-All CB-Series from CB3/CB3.1 software 3.3
-All e-Series

installing for Python3: 

-pip3 install --user ur_rtde
note: Make sure your pip version >=19.3, otherwise the install might fail. Also you may need to install git,cmake and wheel.

Issues:
-Servoj_example and speedj_example is risky for the robot making it hitting itself, I used a lower velocity,accaleration, longer sleep time to be more safe. Using Emergency button is crucial for testing this script.
-move_until_contact.py is dont`t work and I get a "tool-contact is not supported in this machine" error on the control panel of UR-10.



## XML-RPC

-XML-RPC is a Remote Procedure Call method that uses XML to transfer data between programs over sockets.

Pros: 
-Can work with almost any language such as Python, Java, C++ and C.

Cons: 
-Requires a connection setup between remote program/server and UR Controller instead of just sending queries from remote program.
-A built in program should be installed within UR Controller which restricts flexible usage of robot arm.(?)

Some attention points:

-It is important that connections to the remote program are built-up in the BeforeStart sequence, since it takes a relatively long time to build up the connection compared to performing the function call. When the “camera” is not used it causes no overhead.

-XML-RPC function calls are transfered to remote programs. Depending on the computing power & network speed the reaction time for the get_next_pose might vary.

-When the program stops, the XML-RPC connection will be automatically cleaned up.

-It is recommended to use other ports than occupied ports and frequently used ports such as '8080' to avoid conflicts.



