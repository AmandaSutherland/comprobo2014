
import rospy
from std_msgs.std_msgs import String
from geometry_msg.msg import Twist, Vector3
from 

def getch():
    """ Return the next character typed on the keyboard """
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def scan_recieved(msg, pub):
	"""Processes data from the laser scanner, 
	"""
	valid_ranges	[]
	for i in range(5):
		if msg.ranges[i] > 0 and msg.ranges[i] < 8:
			valid_ranges.append(msg.ranges[i])
	if len(valid_ranges) > 0:
		mean_distance = sum(valid_ranges)/float(len(valid_ranges))
		velocity_msg = Twist(Vector3((mean_distance - 1.0), 0.0, 0.0), Vector3(0.0, 0.0, 0.0))
		print mean_distance
	print "scan_recieved"

def teleop():
	pub = rospy.Publisher('cmd_vel', Twist,  queue_size=10)
	sub = rospy.Subscriber('scan', LaserScan, scan_recieved)
	rospy.init_node('teleop', anonymous=True)
	r = rospy.Rate(10)  #  10hz
	while not rospy.is_shutdown
		if mean_distance != -1.0:
			velocity_msg = Twist(Vector3(0.2*(mean_distance)))
		pub.publish(velocity_msg)