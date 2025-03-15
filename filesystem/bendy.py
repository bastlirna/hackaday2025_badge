from machine import I2C
from i2c_slave import I2cSlave

class Bendy(I2cSlave):
    
    C_I2C_ADDRESS = 0x2C
    
    C_STATUS_REG = 0x00
    C_MODE_REG = 0x01
    C_LED_COLOR_REG = 0x02
    C_CHIP_RESET_REG = 0x05
    
    C_MODE_CYCLE = 0
    C_MODE_COLOR_WIPE = 1
    C_MODE_THEATER_CHASE = 2
    C_MODE_RAINBOW = 3
    C_MODE_RAINBOW_CYCLE = 4
    C_MODE_THEATER_CHASE_RAINBOW = 5
    
    def __init__(self, i2c_bus):
        super().__init__(i2c_bus, self.C_I2C_ADDRESS)

    def get_status(self):
        return self.read(self.C_STATUS_REG)

    def set_mode(self, mode):
        self.write(self.C_MODE_REG, bytearray([mode]))        
