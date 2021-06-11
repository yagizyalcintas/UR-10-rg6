import urx
from IPython import embed
import logging

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        #robot = urx.Robot("192.168.1.6")
        robot = urx.Robot("172.16.1.222")
        #robot = urx.Robot("localhost")
        r = robot
        print("Robot object is available as robot or r")
        embed()
    finally:
        robot.close()
