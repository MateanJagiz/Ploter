import RPi.GPIO as GPIO
from time import sleep
   # ======  LASER TTL ======
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)

def laser_off():
    GPIO.output(13, GPIO.LOW)
    print("===> LASER OFF")

def laser_on():
    GPIO.output(13, GPIO.HIGH)
    print("===> LASER ON")

def laser_on_50_proc():
    while True:
        laser_on()
        sleep(0.0001)
        laser_off()
        sleep(0.0001)

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
    GPIO.output(DIR_TRO, GPIO.LOW)
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
    sleep(0.05)
    step_arm()

def first_pixel():
    laser_on()
    sleep(0.2)
    step_arm()

laser_on_50_proc()
