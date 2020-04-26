import src.courier_controller as courier_control
import keyboard
import time

#################
""" CONSTANTS """
#################
IP_ADDRESS = "192.168.227.20"
PORT       = 1883
SPEED      = 80   # 80% speed
TOPIC      = "/drive"


##################
""" CODE START """
##################
if __name__ == '__main__':
    try:
        print("Starting robot controller!")
        controller = courier_control.CourierController("TinyBotController", IP_ADDRESS, PORT)       
        
        while True:
            payload = None
            # Drive the right motor forward at 80% speed
            if keyboard.is_pressed('1'):
                payload = "{}{}".format('r', SPEED)

            # Drive the left motor forward at 80% speed
            elif keyboard.is_pressed('2'):
                payload = "{}{}".format('l', SPEED)
            
            # Stop both motors
            elif keyboard.is_pressed('3'):
                payload = "{}{}".format('b', 0)
            
            # Exit loop
            elif keyboard.is_pressed('q'):
                break
            
            # Send command to robot only if we have one prepared
            if payload != None:
                controller.send(payload, TOPIC)   
                time.sleep(0.2)
    
    except KeyboardInterrupt:
        print("CTRL+C detected")
        # More cleanup here!
    finally:
        print("Controller disconnected")