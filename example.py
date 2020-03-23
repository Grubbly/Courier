import src.courier as courier
import RPi.GPIO as GPIO

##################
""" GPIO SETUP """
##################
right_motor_forward = 19
right_motor_backward = 26

left_motor_forward = 16
left_motor_backward = 20

GPIO.setmode(GPIO.BCM)

GPIO.setup(right_motor_forward, GPIO.OUT)
GPIO.setup(right_motor_backward, GPIO.OUT)
GPIO.setup(left_motor_forward, GPIO.OUT)
GPIO.setup(left_motor_backward, GPIO.OUT)

pwm_r_f = GPIO.PWM(right_motor_forward, 1000)
pwm_r_b = GPIO.PWM(right_motor_backward, 1100)
pwm_l_f = GPIO.PWM(left_motor_forward, 1200)
pwm_l_b = GPIO.PWM(left_motor_backward, 1300)

pwm_r_f.start(0)
pwm_r_b.start(0)
pwm_l_f.start(0)
pwm_l_b.start(0)
print("Finished PWM/GPIO init")


#########################
""" NETWORK CONSTANTS """
#########################
IP_ADDRESS = "192.168.227.23"
PORT = 1883


##################
""" CODE START """
##################
def drive(code):
    print("Drive received code: {}".format(code))

    # First character in code determines which
    # motor will move
    motor = code[0]

    # Last characters in code determines the speed
    # the motor will move
    speed = int(code[1:])    
    
    if motor == 'l':
        pwm_l_f.ChangeDutyCycle(speed)
    elif motor == 'r':
        pwm_r_f.ChangeDutyCycle(speed)
    elif motor == 'b':
        pwm_l_f.ChangeDutyCycle(speed)
        pwm_r_f.ChangeDutyCycle(speed)
    else:
        print("Invalid drive code!")
        return

    print("Driving motor {} at {}% power".format(motor, speed))

if __name__ == '__main__':
    print("Starting robot!")

    # Instantiate a Courier class object and configure
    # it to connect to my robot on the network.
    courier = courier.Courier("TinyBot", IP_ADDRESS, PORT)
    courier.add_topic("/drive", drive)
    courier.run()

