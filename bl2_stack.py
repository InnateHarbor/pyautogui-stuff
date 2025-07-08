import pyautogui
import keyboard
import time
import sys
import win32api, win32con

def refill_ammo():
    # go to ammo machine
    pyautogui.keyDown("s")
    time.sleep(0.5)
    pyautogui.keyUp("s")
    pyautogui.keyDown("a")
    time.sleep(0.75)
    pyautogui.keyUp("a")
    pyautogui.keyDown("s")
    time.sleep(1.5)
    pyautogui.keyUp("s")

    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -1650, 0, 0, 0)

    pyautogui.keyDown("w")
    time.sleep(2)
    pyautogui.keyUp("w")

    # refill ammo
    if pyautogui.locateOnScreen("e_shop.png", confidence=0.8) != None:
        pyautogui.press("e")
        time.sleep(1)
        pyautogui.press("down", 3)
        pyautogui.press("enter", 10)
        pyautogui.press("esc")
        time.sleep(1)

    # go back to range
    pyautogui.keyDown("s")
    time.sleep(2)
    pyautogui.keyUp("s")

    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1650, 0, 0, 0)

    pyautogui.keyDown("w")
    time.sleep(1.5)
    pyautogui.keyUp("w")
    pyautogui.keyDown("d")
    time.sleep(0.75)
    pyautogui.keyUp("d")
    pyautogui.keyDown("w")
    time.sleep(0.5)
    pyautogui.keyUp("w")



# START OF MAIN
print("stacking now")

time.sleep(5)

while(True):
    # fire
    pyautogui.mouseDown(button="left")

    # check if out of ammo
    if pyautogui.locateOnScreen("out_of_ammo.png", confidence=0.5) != None:
        print("out_of_ammo")
        refill_ammo()

    # failsafe
    if keyboard.is_pressed("esc"):
        print("stopped")
        sys.exit(0)