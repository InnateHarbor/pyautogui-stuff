import pyautogui
import keyboard

print("starting fishing")

# manually right-click first

while True:
    try:
        fish = pyautogui.locateOnScreen("fishing_bobber.png", confidence=0.8)
        if fish:
            print("found something")
            pyautogui.click(button="right", clicks=2, interval=2)
        
    except:
        do = 0

    # failsafe
    if keyboard.is_pressed("esc"):
        break

print("stopping fishing")