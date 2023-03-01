from machine import Pin, PWM
import network
import time
import random

led = machine.Pin(14, machine.Pin.OUT)
led.off()
switch = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)

class Servo:
    # these values work for the TowerPro MG90s
    __servo_pwm_freq = 50
    __min_u10_duty = 26 - 0  # offset for correction
    __max_u10_duty = 123 - 0  # offset for correction
    min_angle = 0
    max_angle = 180
    current_angle = 0.001


    def __init__(self, pin):
        self.__initialise(pin)


    def update_settings(self, servo_pwm_freq, min_u10_duty, max_u10_duty, min_angle, max_angle, pin):
        self.__servo_pwm_freq = servo_pwm_freq
        self.__min_u10_duty = min_u10_duty
        self.__max_u10_duty = max_u10_duty
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.__initialise(pin)


    def move(self, angle):
        if angle == self.current_angle:
            return
        elif self.current_angle > angle:
            while self.current_angle > angle:
                self.current_angle -= 1
                duty_u10 = self.__angle_to_u10_duty(self.current_angle)
                self.__motor.duty(duty_u10)
                time.sleep(0.02)
        elif self.current_angle < angle:
            while self.current_angle < angle:
                self.current_angle += 1
                duty_u10 = self.__angle_to_u10_duty(self.current_angle)
                self.__motor.duty(duty_u10)
                time.sleep(0.02)

    def __angle_to_u10_duty(self, angle):
        return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u10_duty


    def __initialise(self, pin):
        self.current_angle = -0.001
        self.__angle_conversion_factor = (self.__max_u10_duty - self.__min_u10_duty) / (self.max_angle - self.min_angle)
        self.__motor = PWM(Pin(pin))
        self.__motor.freq(self.__servo_pwm_freq)

if __name__ == "__main__":
    motor = Servo(pin=12)

    # TO CHECK IF WORK ?
    # LINES TO DEACTIVATE WIFI CONNECTION TO POWER REDUCTION
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(False)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    while True:
        if not switch.value():
            led.on()
            motor.move(45)
            t = random.getrandbits(3)
            t = 1 if t == 0 else t
            time.sleep(t)
            motor.move(55)
            t = random.getrandbits(3)
            t = 1 if t == 0 else t
            time.sleep(t)
        else:
            led.off()
            motor.move(50)
            time.sleep(3)
