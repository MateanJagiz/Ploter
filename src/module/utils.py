import RPi.GPIO as GPIO
from time import sleep
import configparser

config = configparser.ConfigParser()
config.read('config.ini')  

time_step_arm = config.getfloat('device', 'time_step_arm')
time_step_trollay = config.getfloat('device', 'time_step_trollay')
time_wait_1_active_pixel = config.getfloat('device', 'time_wait_1_active_pixel')
time_wait_n_active_pixel = config.getfloat('device', 'time_wait_n_active_pixel')
trolley_steps_on_move = config.getint('device', 'trolley_steps_on_move')
arm_steps_on_move = config.getint('device', 'arm_steps_on_move')

    # ===== Ustawienia GPIO =====

GPIO.cleanup()
sleep(0.1)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

    # ====== Krańcówki======

limit_switch_ARM_begin  = 26
limit_switch_ARM_end    = 6
limit_switch_bed_begin  = 5
limit_switch_bed_end    = 19

GPIO.setup(limit_switch_ARM_begin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(limit_switch_ARM_end, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(limit_switch_bed_begin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(limit_switch_bed_end, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def limit_switch_check():
    for pin in [limit_switch_ARM_begin, limit_switch_ARM_end, limit_switch_bed_begin, limit_switch_bed_end]:
        if GPIO.input(pin) == 0:
            return True  
    return False  

    # ======  silnik stół (TROLLEY)  ======

ENA_TRO = 7
DIR_TRO = 8
PUL_TRO = 24

GPIO.setup(ENA_TRO, GPIO.OUT)
GPIO.setup(DIR_TRO, GPIO.OUT)
GPIO.setup(PUL_TRO, GPIO.OUT)

def step_troll():
    for i in range(trolley_steps_on_move):
        GPIO.output(PUL_TRO, GPIO.HIGH)
        sleep(time_step_trollay)
        GPIO.output(PUL_TRO, GPIO.LOW)
        sleep(time_step_trollay)



    # ======  silnik ramię (ARM)  ======

PUL_ARM = 16
DIR_ARM = 20
ENA_ARM = 21

GPIO.setup(ENA_ARM, GPIO.OUT)
GPIO.setup(DIR_ARM, GPIO.OUT)
GPIO.setup(PUL_ARM, GPIO.OUT)

def step_arm():
    for i in range(arm_steps_on_move):
        GPIO.output(PUL_ARM, GPIO.HIGH)
        sleep(time_step_arm)
        GPIO.output(PUL_ARM, GPIO.LOW)
        sleep(time_step_arm)


    # ======  LASER TTL ======

GPIO.setup(13, GPIO.OUT)

def laser_off():
    GPIO.output(13, GPIO.LOW)
    print("===> LASER OFF")

def laser_on():
    GPIO.output(13, GPIO.HIGH)
    print("===> LASER ON")

def safe_mode():
    GPIO.output(ENA_ARM, GPIO.HIGH)
    GPIO.output(ENA_TRO, GPIO.HIGH)
    laser_off()

def default_position():
    GPIO.output(ENA_TRO, GPIO.LOW)
    GPIO.output(DIR_TRO, GPIO.HIGH)
    while limit_switch_check() == False:
        step_troll()
    GPIO.output(DIR_TRO, GPIO.LOW)
    for i in range(50):
        step_troll()

    GPIO.output(ENA_ARM, GPIO.LOW)
    GPIO.output(DIR_ARM, GPIO.LOW)
    while limit_switch_check() == False:
        step_arm()
    GPIO.output(DIR_ARM, GPIO.HIGH)
    for i in range(50):
        step_arm()

def new_line(): # silnik wózka robi jeden krok ruch postępujący (np. 2 kroki)
    GPIO.output(ENA_TRO, GPIO.LOW)
    GPIO.output(DIR_TRO, GPIO.LOW)
    if limit_switch_check() == False:
        step_troll()

def cd_left(): # silnik ramienia zmienia kierunek na lewo
    GPIO.output(DIR_ARM, GPIO.HIGH)

def cd_right(): # silnik ramienia zmienia kierunek na prawo
    GPIO.output(DIR_ARM, GPIO.LOW)

def end(): # powrót do pozycji defaultowej.
    laser_off()
    default_position()
    safe_mode()

def empty_step(): # wyłącza laser i szybko omija ten punkt
    laser_off()
    step_arm()

def active_step():
    step_arm()
    sleep(0.05)

def first_pixel():
    step_arm()
    laser_on()
    sleep(0.2)
