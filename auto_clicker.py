import pyautogui
import keyboard
import time

toggle_on = False
pyautogui.PAUSE = 0.075

print("starting program")

while True:
    if keyboard.is_pressed("c"):
        toggle_on = True
        print("starting auto-clicking")

    while toggle_on:
        pyautogui.click()

        if keyboard.is_pressed("c"):
            toggle_on = False
            print("stopping auto-clicking")
            time.sleep(1)

        if keyboard.is_pressed("esc"):
            break
    
    if keyboard.is_pressed("esc"):
            break

print("stopping program")