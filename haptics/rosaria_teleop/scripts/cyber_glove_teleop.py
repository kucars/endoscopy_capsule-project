#!/usr/bin/env python
import roslib
import rospy
from geometry_msgs.msg import Twist
from evdev import uinput, ecodes as e

import serial
import time
def ask():
  return raw_input('\nInsert a valid command: ' )

def read(old):
  r=c.read(1) #read G
  new=[]
  while 1:
    r=c.read(1)
    if ord(r) == 0:
	if len(new) == 18:	  
	   return new
	else:
	   return old 
    else:
	#print ord(r)
	new.append(ord(r))



if __name__=="__main__":
    
    rospy.init_node('cyber_glove_teleop')
    pub = rospy.Publisher('~cmd_vel', Twist)

    c=serial.Serial('/dev/ttyUSB0')
    c.baudrate=115200
    data=[]
    circular=[]
    f = open('data.txt', 'w')

    while 1:

 	c.write("G")
 	data=read(data)

 	print data
 	t = time.time()
 	#f.write(str(t))
 	#f.write(' ')
 	count = 0
 	for i in data:
		count = count + i
		#f.write(str(i))
		#f.write(' ')
	print data[5]
	#f.write("\n")
	print count

    	control_linear_speed=0.0
	control_angular_speed=0.0
	if count > 2000:
	  #with uinput.UInput() as ui:
	    #ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
	    #ui.write(e.EV_KEY, e.KEY_UP, 1)
	    #ui.syn()
	    control_linear_speed=1.0
	    print 'Forward\n'
	elif data[0] > 120:
	  #with uinput.UInput() as ui:
	    #ui.write(e.EV_KEY, e.KEY_DOWN, 1)
	    #ui.syn()
	    control_linear_speed=-1.0
	    print 'Backward\n'
	elif data[5] > 110:
	  #with uinput.UInput() as ui:
	    #ui.write(e.EV_KEY, e.KEY_RIGHT, 1)
	    #ui.syn()
	    control_angular_speed=1.0
	    print 'Right\n'
	elif data[10] > 110:
	  #with uinput.UInput() as ui:
	    #ui.write(e.EV_KEY, e.KEY_LEFT, 1)
	    #ui.syn()
	    control_angular_speed=-1.0
	    print 'Left\n'
	else:
	  #with uinput.UInput() as ui:
	    #ui.write(e.EV_KEY, e.KEY_SPACE, 1)
	    #ui.syn()
	    print 'nothing'
	#f.close()
        twist = Twist()
        twist.linear.x = control_linear_speed; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = control_angular_speed
        pub.publish(twist)
    c.close()
