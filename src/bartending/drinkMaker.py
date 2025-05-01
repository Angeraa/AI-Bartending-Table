from gpiozero import LED, AngularServo, Button, SmoothedInputDevice, CPUTemperature
from gpiozero.pins.pigpio import PiGPIOFactory
import numpy as np
from waiting import wait
import time
from bartending.custom_exceptions import NoGlassError

class DrinkMaker:
    def __init__(self):
        self.factory = PiGPIOFactory()
        self.pumps = []
        self.pin_numbers = [5, 6, 13, 19, 26, 21, 20, 16, 12, 7, 8, 25] #Vermouth Tequila Whiskey Rum WhiteWine RedWine Gin Tonic Pepsi Lime Campari Sec
        self.greenLED = LED(27)
        self.redLED = LED(22)
        self.stepper = LED(23)
        self.direction = LED(24)
        self.direction.on()
        self.lightsen = SmoothedInputDevice(18, pull_up=True, average=np.mean, threshold=0.4, sample_wait=0.1)
        self.lightsen._queue.start()
        self.button = Button(17)
        self.cpu = CPUTemperature()

        self.setup_pumps()
        self.setup_servos()
        self.up_lift()
        self.greenLED.blink(1, 1, 3, False)

    def setup_pumps(self):
        for pin in self.pin_numbers:
            self.pumps.append(LED(pin))

    def setup_servos(self):
        self.servo1 = AngularServo(14, min_pulse_width=0.0008, pin_factory=self.factory)
        self.servo2 = AngularServo(15, min_pulse_width=0.0008, pin_factory=self.factory)
        self.servo1.angle = -90
        self.servo2.angle = 60
        
    def up_lift(self):
        if not self.button.is_pressed:
            self.direction.off()	
            self.stepper.blink(0.00015, 0.00015)
            self.button.wait_for_press()
            self.stepper.off()
        self.direction.on()

    def get_cpu_temperature(self):
        return self.cpu.temperature

    def close(self):
        self.lightsen.close()
        
    def offAllPumps(self):
        for pump in self.pumps:
            pump.off()

    def pump_drink(self, pump_number, pump_volume, is_wine=False): #takes in a list of pumps and volume, and the size of the glass
        dt = 0
        pump_time = []
        
        print("Making a drink")
        
        #servo retracts
        self.servo1.angle = -90
        self.servo2.angle = 60
        
        if is_wine:
            try:
                self.stepper.blink(0.00015, 0.00015, n=19000, background=False)
                print(self.lightsen.is_active)
                if not self.lightsen.is_active:
                    print("No glass detected")
                    raise NoGlassError
                else:
                    print("Glass Detected")
                    self.stepper.blink(0.00015, 0.00015)
                    try:
                        wait(lambda: not self.lightsen.is_active, timeout_seconds=16)
                    except TimeoutExpired:
                        pass
                    time.sleep(1)
                    self.stepper.off()
            except NoGlassError:
                print("error raised")
                self.direction.off()
                self.redLED.blink(0.5, 0.5)
                self.stepper.blink(0.00015, 0.00015)
                self.button.wait_for_press()
                self.stepper.off()
                self.direction.on()
                self.redLED.off()
                return
        else:
            #lower the platform based on the glass
            try:
                self.stepper.blink(0.00015, 0.00015, n=9000, background=False)
                if not self.lightsen.is_active:
                    print("No glass detected")
                    raise NoGlassError
                else:
                    print("Glass Detected")
                    self.stepper.blink(0.00015, 0.00015)
                    try:
                        wait(lambda: not self.lightsen.is_active, timeout_seconds=16)
                    except TimeoutExpired:
                        pass
                    self.stepper.off()
            except NoGlassError:
                print("error raised")
                self.direction.off()
                self.redLED.blink(0.5, 0.5)
                self.stepper.blink(0.00015, 0.00015)
                self.button.wait_for_press()
                self.stepper.off()
                self.direction.on()
                self.redLED.off()
                return
        
        time.sleep(1)
        
        #now move the servo to deploy the nozzles
        self.servo1.angle = 90	
        self.servo2.angle = -80
        
        #turn the volume into time using an approximation
        for i in pump_volume:
            pump_time.append(i/35)
        
        time.sleep(1)
        
        #turn pumps on
        for num in pump_number:
            self.pumps[num].on()
            print(f"Pump {num} is on")
        
        #start loop for tracking the time the pumps are on
        last_time = time.time()
        while True:
            dt += time.time() - last_time
            last_time = time.time()
            for i in range(len(pump_time)):
                if dt > pump_time[i]:
                    self.pumps[pump_number[i]].off()
                    print(f"Pump {pump_number[i]} is off")
            if not self.pumps[pump_number[pump_time.index(max(pump_time))]].is_lit:
                self.offAllPumps()
                break
            time.sleep(0.3)
        
        time.sleep(2)
        
        #servo retracts
        self.servo1.angle = -90
        self.servo2.angle = 60
        
        time.sleep(0.5)
        
        #platform goes back up
        self.up_lift()