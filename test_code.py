'''
These are test modules for the code on the pi, soon I will add the entire code from the pi on here once I go back to my garage to ctrl-c-ctrl-v here
'''

#Code to account for not placing a glass on the platform and ordering a drink

class NoGlassError(Exception):
    pass

try:
    stepper.blink(0.0003, 0.0003, n=6000, background=False)
    if not lightsen.active:
        raise NoGlassError
    else:
        stepper.blink(0.0003, 0.0003)
        wait(lambda: lightsen.active, timeout_seconds=10)
        stepper.off()

        '''
        here is where the rest of the existing code goes to complete the pour_drink function
        '''
except NoGlassError:
    direction.off()
    stepper.blink(0.0003, 0.0003)
    button.wait_for_press()
    stepper.off()
    redLED.blink(0.5, 0.5, n=5)