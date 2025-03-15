class I2cSlave:
    
    def __init__(self, i2c_bus, i2c_address):
        self._i2c = i2c_bus
        self._address = i2c_address

    def read(self, reg_address, nbytes=1):
        return self._i2c.readfrom_mem(self._address, reg_address, nbytes)

    def read_expect(self, reg_address, expected, nbytes=1):
        value = self.read(reg_address, nbytes)
        #value = int.from_bytes(value, "big")
        if value != expected:
            raise RuntimeError("Value doesn't match!")
            # Address: 0x%X, read: 0x%X, expected: 0x%X" % (reg_address, value, expected))

    def write(self, reg_address, data:Bytes):
        self._i2c.writeto_mem(self._address, reg_address, data)

    def write_expect(self, reg_address, data:Bytes):
        self.write(reg_address, data)
        self.read_expect(reg_address, data, len(data))

