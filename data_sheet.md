# Mirobot Sheet

- X = [-110,160] ("Turn the base")
- Y = [-35,70] ("Move link 1")
- Z = [-120,60] ("Move link 2")
- Roll = [-180,180] ("End-effector roll")
- Pitch = [-200,30] ("End-effector pitch")
- Yaw = [-360,360] ("End-effector yaw")

- go_to_axis(x, y, z, a=roll, b=pitch, c=yaw)


Basiskoordinatensystem:
z hoch runter
x vor zurück von 0 bis 

go_to_axis is better for free movement of end effector as the robot does not try to keep the same end position. 

## Ideas:

Since (I can't fully confirm though) the state of the robot (axes) can not be requested, make a robot class holding its current full state. (already one there, just have to update to new SDK)

Nevermind: arm.get_status() does this. Still good to have representation though I guess