import RPi.GPIO as GPIO
from time import sleep
import configparser

config = configparser.ConfigParser()
config.read('config.ini')  

GPIO.cleanup()
sleep(0.1)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

limit_switch_ARM_begin  = 26
limit_switch_ARM_end    = 6
limit_switch_bed_begin  = 5
limit_switch_bed_end    = 19



class Motor:
    def __init__(self) -> None:
        self.ENA_TRO = 7
        self.DIR_TRO = 8
        self.PUL_TRO = 24
        GPIO.setup(self.ENA_TRO, GPIO.OUT)
        GPIO.setup(self.DIR_TRO, GPIO.OUT)
        GPIO.setup(self.PUL_TRO, GPIO.OUT)

        self.PUL_ARM = 16
        self.DIR_ARM = 20
        self.ENA_ARM = 21
        GPIO.setup(self.ENA_ARM, GPIO.OUT)
        GPIO.setup(self.DIR_ARM, GPIO.OUT)
        GPIO.setup(self.PUL_ARM, GPIO.OUT)
 
        self.time_step_arm = config.getfloat('device', 'time_step_arm')
        self.time_step_trollay = config.getfloat('device', 'time_step_trollay')
        self.time_wait_1_active_pixel = config.getfloat('device', 'time_wait_1_active_pixel')
        self.time_wait_n_active_pixel = config.getfloat('device', 'time_wait_n_active_pixel')
        self.trolley_steps_on_move = config.getint('device', 'trolley_steps_on_move')
        self.arm_steps_on_move = config.getint('device', 'arm_steps_on_move')

        GPIO.setup(limit_switch_ARM_begin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(limit_switch_ARM_end, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(limit_switch_bed_begin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(limit_switch_bed_end, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    def limit_switch_check(self):
        for pin in [limit_switch_ARM_begin, limit_switch_ARM_end, limit_switch_bed_begin, limit_switch_bed_end]:
            if GPIO.input(pin) == 0:
                return True  
        return False  
 
    def step_troll(self):
        for i in range(self.trolley_steps_on_move):
            GPIO.output(self.PUL_TRO, GPIO.HIGH)
            sleep(self.time_step_trollay)
            GPIO.output(self.PUL_TRO, GPIO.LOW)
            sleep(self.time_step_trollay)

    def step_arm(self):
        for i in range(self.arm_steps_on_move):
            GPIO.output(self.PUL_ARM, GPIO.HIGH)
            sleep(self.time_step_arm)
            GPIO.output(self.PUL_ARM, GPIO.LOW)
            sleep(self.time_step_arm)

class Laser:
    def __init__(self) -> None:
        self.time_on = 0
        self.time_off = 0
        self.laser_pin = 13
        self.pwm_percent = 100
        self.on_off_flag = False
        GPIO.setup(self.laser_pin, GPIO.OUT)
        GPIO.output(self.laser_pin, GPIO.LOW)

    def laser_set_PWM(self, percent):
        self.time_on = percent/10000 #0.0005
        self.time_off = 0.001 - self.time_on

    def off(self):
        GPIO.output(self.laser_pin, GPIO.LOW)

    def on(self):
        #do pwm trzba uzyc pin pwm inaczej nie ma sensu
        GPIO.output(self.laser_pin, GPIO.HIGH)


class Ploter:
    def __init__(self) -> None:
        self.laser = Laser()
        self.motor = Motor()

    def safe_mode(self):
        GPIO.output(self.motor.ENA_ARM, GPIO.HIGH)
        GPIO.output(self.motor.ENA_TRO, GPIO.HIGH)
        self.laser.off()
    
    def default_position(self):
        self.laser.off()
        GPIO.output(self.motor.ENA_TRO, GPIO.LOW)
        GPIO.output(self.motor.DIR_TRO, GPIO.HIGH)
        while self.motor.limit_switch_check() == False:
            self.motor.step_troll()
        GPIO.output(self.motor.DIR_TRO, GPIO.LOW)
        for i in range(50):
            self.motor.step_troll()
    
        GPIO.output(self.motor.ENA_ARM, GPIO.LOW)
        GPIO.output(self.motor.DIR_ARM, GPIO.LOW)
        while self.motor.limit_switch_check() == False:
            self.motor.step_arm()
        GPIO.output(self.motor.DIR_ARM, GPIO.HIGH)
        for i in range(50):
            self.motor.step_arm()
    
    def new_line(self): # silnik wózka robi jeden krok ruch postępujący (np. 2 kroki)
        GPIO.output(self.motor.ENA_TRO, GPIO.LOW)
        GPIO.output(self.motor.DIR_TRO, GPIO.LOW)
        if self.motor.limit_switch_check() == False:
            self.motor.step_troll()
    
    def cd_left(self): # silnik ramienia zmienia kierunek na lewo
        GPIO.output(self.motor.DIR_ARM, GPIO.HIGH)
    
    def cd_right(self): # silnik ramienia zmienia kierunek na prawo
        GPIO.output(self.motor.DIR_ARM, GPIO.LOW)
    
    def end(self): # powrót do pozycji defaultowej.
        self.laser.off()
        self.default_position()
        self.safe_mode()
    
    def empty_step(self): # wyłącza laser i szybko omija ten punkt
        self.laser.off()
        self.motor.step_arm()
    
    def active_step(self):
        self.motor.step_arm()
        sleep(self.motor.time_wait_n_active_pixel)
    
    def first_pixel(self):
        self.motor.step_arm()
        self.laser.on()
        sleep(self.motor.time_wait_1_active_pixel)

