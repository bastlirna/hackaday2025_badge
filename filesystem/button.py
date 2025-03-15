from machine import Pin

class Button:
    
    def __init__(self, pin, active_low=True):
        self._pin = pin
        self._active_low = active_low
        self.value = pin.value()
        self.last_state = self.value
        
    def update(self):
        self.last_value = self.value
        self.value = self._pin.value()
        if 
        self.pressed = 

    def is_pressed(self):
        if self._active_low:
            return not self._pin.value()
        else:
            return self._pin.value()

    def was_pressed(self
