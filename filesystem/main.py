from machine import I2C, Pin
import time
import ssd1327_2
import uqr

counter = 0

display = ssd1327_2.WS_OLED_128X128(i2c1)

def display_qr(data):
    qr = uqr.QRCode()
    qr.add_data(data)
    qr.make()

    matrix = qr.modules
    qr_size = len(matrix)

    scale = display.width // qr_size
    offset_x = (display.width - (qr_size * scale)) // 2
    offset_y = (display.height - (qr_size * scale)) // 2

    display.fill(0)

    for y in range(qr_size):
        for x in range(qr_size):
            color = 15 if matrix[y][x] else 0
            for i in range(scale):
                for j in range(scale):
                    display.pixel(offset_x + x * scale + i, offset_y + y * scale + j, color)

    display.show()


def draw_picture():
    
    #display = ssd1327_2.WS_OLED_128X128(i2c1)  # Grove OLED Display

    display.fill(0)
    x = (display.width - 69) // 2
    y = (display.height - 69) // 2
    display.framebuf.fill_rect(x+0,  y+0,  69, 69, 15)
    display.framebuf.fill_rect(x+15, y+15, 3,  54, 0)
    display.framebuf.fill_rect(x+33, y+0,  3,  54, 0)
    display.framebuf.fill_rect(x+51, y+15, 3,  54, 0)
    display.framebuf.fill_rect(x+60, y+56, 4,  7,  0)
    display.show()

image = 0
images = 3

def draw_image():
    try:
        if image == 0:
            draw_picture()
        elif image == 1:
            display_qr("https://github.com/bastlirna/hackaday2025_badge")
        elif image == 2:
            display_qr("https://macgyver.siliconhill.cz")
    except: 
        print("Display failed")

draw_image()

## do a quick spiral to test
if petal_bus:
    for j in range(8):
        which_leds = (1 << (j+1)) - 1 
        for i in range(1,9):
            print(which_leds)
            petal_bus.writeto_mem(PETAL_ADDRESS, i, bytes([which_leds]))
            time.sleep_ms(30)
            petal_bus.writeto_mem(PETAL_ADDRESS, i, bytes([which_leds]))
    # and clear
    for i in range(1,9):
        petal_bus.writeto_mem(PETAL_ADDRESS, i, bytes([0]))

if etch_sao_sketch_device:
    etch_sao_sketch_device.shake() # clear display

buttonA_last_state = buttonA.value()
buttonA_pressed = False
buttonA_released = False
buttonB_last_state = buttonB.value()
buttonB_pressed = False
buttonB_released = False
buttonC_last_state = buttonC.value()
buttonC_pressed = False
buttonC_released = False

bendy_mode = 0

rotation_last_state = etch_sao_sketch_device.rotation
facing_up = True
facing_up_last = facing_up
turned = False

while True:
    
    buttonA_state = buttonA.value()
    if not buttonA_state and buttonA_last_state:
        buttonA_pressed = True
    else:
        buttonA_pressed = False
    if buttonA_state and not buttonA_last_state:
        buttonA_released = True
    else:
        buttonA_released = False
    buttonA_last_state = buttonA_state

    buttonB_state = buttonB.value()
    if not buttonB_state and buttonB_last_state:
        buttonB_pressed = True
    else:
        buttonB_pressed = False
    if buttonB_state and not buttonB_last_state:
        buttonB_released = True
    else:
        buttonB_released = False
    buttonB_last_state = buttonB_state

    buttonC_state = buttonC.value()
    if not buttonC_state and buttonC_last_state:
        buttonC_pressed = True
    else:
        buttonC_pressed = False
    if buttonC_state and not buttonC_last_state:
        buttonC_released = True
    else:
        buttonC_released = False
    buttonC_last_state = buttonC_state
    
    rotation = etch_sao_sketch_device.rotation
    rotation_last = rotation
    roll = rotation[0]
    pitch = rotation[1]
    if roll > -80 and roll < 80:
        facing_up = False
    if roll < -100 or roll > 100:
        facing_up = True
    if facing_up_last and not facing_up:
        turned = True
        print("Turned")
        image = (image + 1) % images
        draw_image()
    else:
        turned = False
    facing_up_last = facing_up

    ## display button status on RGB
    if petal_bus:
        if not buttonA.value():
            petal_bus.writeto_mem(PETAL_ADDRESS, 2, bytes([0x80]))
        else:
            petal_bus.writeto_mem(PETAL_ADDRESS, 2, bytes([0x00]))

        if not buttonB.value():
            petal_bus.writeto_mem(PETAL_ADDRESS, 3, bytes([0x80]))
        else:
            petal_bus.writeto_mem(PETAL_ADDRESS, 3, bytes([0x00]))

        if not buttonC.value():
            petal_bus.writeto_mem(PETAL_ADDRESS, 4, bytes([0x80]))
        else:
            petal_bus.writeto_mem(PETAL_ADDRESS, 4, bytes([0x00]))

    ## see what's going on with the touch wheel
    if touchwheel_bus:
        tw = touchwheel_read(touchwheel_bus)

    ## display touchwheel on petal
    if petal_bus and touchwheel_bus:
        if tw > 0:
            tw = (128 - tw) % 256 
            petal = int(tw/32) + 1
        else: 
            petal = 999
        for i in range(1,9):
            if i == petal:
                petal_bus.writeto_mem(0, i, bytes([0x7F]))
            else:
                petal_bus.writeto_mem(0, i, bytes([0x00]))

    if etch_sao_sketch_device:
        etch_left = etch_sao_sketch_device.left
        etch_right = etch_sao_sketch_device.right
        print (etch_left, etch_right)
        print(rotation)
        etch_sao_sketch_device.draw_pixel(etch_left, etch_right, 1)
        etch_sao_sketch_device.draw_display()

    if bendy_device:
        if buttonA_pressed:
            bendy_mode = (bendy_mode + 1) % 6
            bendy_device.set_mode(bendy_mode)
            print("Bendy mode ++")
        if buttonB_pressed:
            bendy_mode = (bendy_mode + 6 - 1) % 6
            bendy_device.set_mode(bendy_mode)
            print("Bendy mode --")
    
    time.sleep_ms(100)
    bootLED.off()






