import pyautogui

image_location = pyautogui.locateCenterOnScreen("edge_logo.png", confidence=0.8)

# must have only one edge window open lol

pyautogui.moveTo(image_location, duration=0.5)
pyautogui.click()

with pyautogui.hold("ctrl"):
    pyautogui.press("t")

pyautogui.write("test in progress... ... ... ... ", interval=0.1)
pyautogui.write("complete!")