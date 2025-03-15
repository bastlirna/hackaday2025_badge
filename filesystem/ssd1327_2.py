"""
MicroPython SSD1327 OLED I2C driver
https://github.com/mcauser/micropython-ssd1327

MIT License
Copyright (c) 2017 Mike Causer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__version__ = '1.1.1'

from micropython import const
import framebuf
import time

# commands
SET_COL_ADDR          = const(0x15)
SET_SCROLL_DEACTIVATE = const(0x2E)
SET_ROW_ADDR          = const(0x75)
SET_CONTRAST          = const(0x81)
SET_SEG_REMAP         = const(0xA0)
SET_DISP_START_LINE   = const(0xA1)
SET_DISP_OFFSET       = const(0xA2)
SET_DISP_MODE         = const(0xA4) # 0xA4 normal, 0xA5 all on, 0xA6 all off, 0xA7 when inverted
SET_MUX_RATIO         = const(0xA8)
SET_FN_SELECT_A       = const(0xAB)
SET_DISP              = const(0xAE) # 0xAE power off, 0xAF power on
SET_PHASE_LEN         = const(0xB1)
SET_DISP_CLK_DIV      = const(0xB3)
SET_SECOND_PRECHARGE  = const(0xB6)
SET_GRAYSCALE_TABLE   = const(0xB8)
SET_GRAYSCALE_LINEAR  = const(0xB9)
SET_PRECHARGE         = const(0xBC)
SET_VCOM_DESEL        = const(0xBE)
SET_FN_SELECT_B       = const(0xD5)
SET_COMMAND_LOCK      = const(0xFD)

# registers
REG_CMD  = const(0x80)
REG_DATA = const(0x40)

class SSD1327:
    def __init__(self, width=128, height=128):
        self.width = width
        self.height = height
        self.buffer = bytearray(self.width * self.height // 2)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.GS4_HMSB)

        self.col_addr = ((128 - self.width) // 4, 63 - ((128 - self.width) // 4))
        # 96x96     (8, 55)
        # 128x128   (0, 63)

        self.row_addr = (0, self.height - 1)
        # 96x96     (0, 95)
        # 128x128   (0, 127)

        self.offset = 128 - self.height
        # 96x96     32
        # 128x128   0

        self.poweron()
        self.init_display()

    def init_displayXX(self):
        for cmd in (
            0x0fd, 0x012,
            0x0a2, 0x000,
            0x0ab, 0x001,
            0x0b9,
            0x0bc, 0x008,
            0x0be, 0x007,
            0x0b6, 0x001,
            0x0d5, 0x062,
            0x0a4): # Display on
            self.write_cmd(cmd)
        self.fill(0)
        self.write_data(self.buffer)

    def init_display(self):
        init_sequence = [
            0xAE,       # Display off
            0x15, 0x00, 0x7F,  # Set column address (0-127)
            0x75, 0x00, 0x7F,  # Set row address (0-127)
            0x81, 0x80,        # Contrast (128 default)
            0xA0, 0x51,        # Set remap (COM and SEG orientation)
            0xA1, 0x00,        # Display start line
            0xA2, 0x00,        # Display offset
            0xA4,              # Normal display mode
            0xA8, 0x7F,        # Multiplex ratio (1/128)
            0xAB, 0x01,        # Enable internal VDD regulator
            0xB1, 0x51,        # Phase length
            0xB3, 0x01,        # Display clock divide ratio/oscillator frequency
            0xB6, 0x01,        # Set second precharge period
            0xB9,              # Set default grayscale lookup table
            0xBC, 0x08,        # Pre-charge voltage level
            0xBE, 0x07,        # VCOMH voltage level
            0xD5, 0x62,        # Function selection B (Enable internal regulator)
            0xFD, 0x12,        # Unlock commands
            0xAF               # Display on
        ]

        for cmd in init_sequence:
            self.write_cmd(cmd)
            time.sleep_ms(1)
            



    def init_display2(self):
        for cmd in (
            SET_COMMAND_LOCK, 0x12, # Unlock
            #SET_DISP, # Display off
            # Resolution and layout
            SET_DISP_START_LINE, 0x00,
            SET_DISP_OFFSET, self.offset, # Set vertical offset by COM from 0~127
            # Set re-map
            # Enable column address re-map
            # Disable nibble re-map
            # Horizontal address increment
            # Enable COM re-map
            # Enable COM split odd even
            SET_SEG_REMAP, 0x51,
            SET_MUX_RATIO, self.height - 1,
            # Timing and driving scheme
            SET_FN_SELECT_A, 0x01, # Enable internal VDD regulator
            SET_PHASE_LEN, 0x51, # Phase 1: 1 DCLK, Phase 2: 5 DCLKs
            SET_DISP_CLK_DIV, 0x01, # Divide ratio: 1, Oscillator Frequency: 0
            SET_PRECHARGE, 0x08, # Set pre-charge voltage level: VCOMH
            SET_VCOM_DESEL, 0x07, # Set VCOMH COM deselect voltage level: 0.86*Vcc
            SET_SECOND_PRECHARGE, 0x01, # Second Pre-charge period: 1 DCLK
            SET_FN_SELECT_B, 0x62, # Enable enternal VSL, Enable second precharge
            # Display
            SET_GRAYSCALE_LINEAR, # Use linear greyscale lookup table
            SET_CONTRAST, 0x7f, # Medium brightness
            SET_DISP_MODE, # Normal, not inverted
            SET_COL_ADDR, self.col_addr[0], self.col_addr[1],
            SET_ROW_ADDR, self.row_addr[0], self.row_addr[1],
            SET_SCROLL_DEACTIVATE,
            SET_DISP | 0x01): # Display on
            self.write_cmd(cmd)
        self.fill(0)
        self.write_data(self.buffer)

    def poweroff(self):
        self.write_cmd(SET_FN_SELECT_A)
        self.write_cmd(0x00) # Disable internal VDD regulator, to save power
        self.write_cmd(SET_DISP)

    def poweron(self):
        self.write_cmd(SET_FN_SELECT_A)
        self.write_cmd(0x01) # Enable internal VDD regulator
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast) # 0-255

    def rotate(self, rotate):
        self.poweroff()
        self.write_cmd(SET_DISP_OFFSET)
        self.write_cmd(self.height if rotate else self.offset)
        self.write_cmd(SET_SEG_REMAP)
        self.write_cmd(0x42 if rotate else 0x51)
        self.poweron()

    def invert(self, invert):
        self.write_cmd(SET_DISP_MODE | (invert & 1) << 1 | (invert & 1)) # 0xA4=Normal, 0xA7=Inverted

    def show(self):
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(self.col_addr[0])
        self.write_cmd(self.col_addr[1])
        self.write_cmd(SET_ROW_ADDR)
        self.write_cmd(self.row_addr[0])
        self.write_cmd(self.row_addr[1])
        self.write_data(self.buffer)

    def fill(self, col):
        self.framebuf.fill(col)

    def pixel(self, x, y, col):
        self.framebuf.pixel(x, y, col)

    def line(self, x1, y1, x2, y2, col):
        self.framebuf.line(x1, y1, x2, y2, col)

    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)
        # software scroll

    def text(self, string, x, y, col=15):
        self.framebuf.text(string, x, y, col)

    def write_cmd(self):
        raise NotImplementedError

    def write_data(self):
        raise NotImplementedError


class SSD1327_I2C(SSD1327):
    def __init__(self, width, height, i2c, addr=0x3c):
        self.i2c = i2c
        self.addr = addr
        self.cmd_arr = bytearray([REG_CMD, 0])  # Co=1, D/C#=0
        self.data_list = [bytes((REG_DATA,)), None]
        super().__init__(width, height)

    def write_cmd(self, cmd):
        self.cmd_arr[1] = cmd
        self.i2c.writeto(self.addr, self.cmd_arr)

    def write_data(self, data_buf):
        self.data_list[1] = data_buf
        self.i2c.writevto(self.addr, self.data_list)


class SEEED_OLED_96X96(SSD1327_I2C):
    def __init__(self, i2c):
        super().__init__(96, 96, i2c)

    def lookup(self, table):
        # GS0 has no pre-charge and current drive
        self.write_cmd(SET_GRAYSCALE_TABLE)
        for i in range(0,15):
            self.write_cmd(table[i])

class WS_OLED_128X128(SSD1327_I2C):
    def __init__(self, i2c, addr=0x3c):
        super().__init__(128, 128, i2c, addr)