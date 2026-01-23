import RPi.GPIO as GPIO
from time import sleep

    # ===== Ustawienia GPIO =====

GPIO.cleanup()
sleep(1)
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
    for i in range(5):
        GPIO.output(PUL_TRO, GPIO.HIGH)
        sleep(0.0007)
        GPIO.output(PUL_TRO, GPIO.LOW)
        sleep(0.0007)


    # ======  silnik ramię (ARM)  ======

PUL_ARM = 16
DIR_ARM = 20
ENA_ARM = 21

GPIO.setup(ENA_ARM, GPIO.OUT)
GPIO.setup(DIR_ARM, GPIO.OUT)
GPIO.setup(PUL_ARM, GPIO.OUT)

def step_arm():
    for i in range(5):
        GPIO.output(PUL_ARM, GPIO.HIGH)
        sleep(0.0007)
        GPIO.output(PUL_ARM, GPIO.LOW)
        sleep(0.0007)


    # ======  LASER TTL ======

GPIO.setup(13, GPIO.OUT)

def laser_off():
    GPIO.output(13, GPIO.LOW)
    print("===> LASER OFF")

def laser_on():
    GPIO.output(13, GPIO.HIGH)
    print("===> LASER ON")

#GPIO.setup(13, GPIO.OUT)
#GPIO.output(13, GPIO.HIGH)  # Ustaw HIGH
#print(GPIO.input(13))       # 1 (HIGH)
#sleep(3)
#GPIO.output(13, GPIO.LOW)   # Ustaw LOW
#print(GPIO.input(13))       # 0 (LOW)
#sleep(3)

def safe_mode():
    GPIO.output(ENA_ARM, GPIO.HIGH)
    GPIO.output(ENA_TRO, GPIO.HIGH)
    laser_off()

def default_position():
    GPIO.output(ENA_TRO, GPIO.LOW)
    GPIO.output(DIR_TRO, GPIO.HIGH)
    while limit_switch_check() == False:
        GPIO.output(PUL_TRO, GPIO.LOW)
        sleep(0.0009)
        GPIO.output(PUL_TRO, GPIO.HIGH)
        sleep(0.0009)
    GPIO.output(DIR_TRO, GPIO.LOW)
    for i in range(100):
        GPIO.output(PUL_TRO, GPIO.LOW)
        sleep(0.0009)
        GPIO.output(PUL_TRO, GPIO.HIGH)
        sleep(0.0009)
    sleep(1)

    GPIO.output(ENA_ARM, GPIO.LOW)
    GPIO.output(DIR_ARM, GPIO.LOW)
    while limit_switch_check() == False:
        GPIO.output(PUL_ARM, GPIO.LOW)
        sleep(0.0007)
        GPIO.output(PUL_ARM, GPIO.HIGH)
        sleep(0.0007)
    GPIO.output(DIR_ARM, GPIO.HIGH)
    for i in range(100):
        GPIO.output(PUL_ARM, GPIO.LOW)
        sleep(0.0007)
        GPIO.output(PUL_ARM, GPIO.HIGH)
        sleep(0.0007)

def new_line(): # silnik wózka robi jeden krok ruch postępujący (np. 2 kroki)
    GPIO.output(ENA_TRO, GPIO.LOW)
    GPIO.output(DIR_TRO, GPIO.HIGH)
    while limit_switch_check() == False:
        for i in range(5):
            GPIO.output(PUL_TRO, GPIO.LOW)
            sleep(0.0009)
            GPIO.output(PUL_TRO, GPIO.HIGH)
            sleep(0.0009)
        break
    return True

def cd_left(): # silnik ramienia zmienia kierunek na lewo
    GPIO.output(DIR_ARM, GPIO.HIGH)
    return True

def cd_right(): # silnik ramienia zmienia kierunek na prawo
    GPIO.output(DIR_ARM, GPIO.LOW)
    return True

def end(): # powrót do pozycji defaultowej.
    default_position()
    safe_mode()
    return True

def empty_step(): # wyłącza laser i szybko omija ten punkt
    laser_off()
    step_arm()

def active_step():
    sleep(0.01)
    step_arm()

def first_pixel():
    laser_on
    sleep(0.1)
    step_arm()

