from machine import I2C, Pin
import time

counter = 0

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

bendy_mode = 0

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






