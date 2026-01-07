from gpiozero import Button
import socket
from signal import pause

# ===== UDP CONFIG =====
UDP_IP = "127.0.0.1"  
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ===== BUTTON CONFIG =====
button = Button(17, pull_up=True)

active = False  # status: Idle / Active

def on_button_pressed():
    global active

    if not active:
        message = "START"
        active = True
    else:
        message = "STOP"
        active = False

    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
    print(f"Button pressed → Sent UDP: {message}")

button.when_pressed = on_button_pressed

print("Button UDP sender running. Press button to send START / STOP.")
pause()
