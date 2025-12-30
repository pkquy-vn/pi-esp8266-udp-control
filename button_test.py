from gpiozero import Button
from signal import pause

button = Button(17, pull_up=True)

def on_press():
    print("Button pressed!")

button.when_pressed = on_press
print("Waiting for button press on GPIO17...")
pause()

