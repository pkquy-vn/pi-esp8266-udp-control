#!/usr/bin/env python3
from gpiozero import Button
from signal import pause
import socket
import time

# ===== CHANGE THESE =====
ESP_IP = "192.168.12.131"   # IP printed on ESP Serial Monitor
ESP_PORT = 5005             # Must match UDP_PORT on ESP
# ========================

BUTTON_GPIO = 17            # BCM numbering (GPIO17 = physical pin 11)
BOUNCE_TIME = 0.08          # 80 ms debounce (helps with noisy button)

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Create button with internal pull-up
button = Button(BUTTON_GPIO, pull_up=True, bounce_time=BOUNCE_TIME)

active = False  # False = IDLE, True = ACTIVE


def send_udp(msg: str) -> None:
    """Send a UDP message to the ESP and print confirmation."""
    data = msg.encode("utf-8")
    sock.sendto(data, (ESP_IP, ESP_PORT))
    print(f"[UDP] Sent -> {ESP_IP}:{ESP_PORT} : {msg}", flush=True)


def on_pressed() -> None:
    """Toggle START/STOP on each press."""
    global active

    # This line proves the button event fired
    print("[BTN] Press detected", flush=True)

    if not active:
        active = True
        send_udp("START")
        print("[STATE] ACTIVE", flush=True)
    else:
        active = False
        send_udp("STOP")
        print("[STATE] IDLE", flush=True)


def on_released() -> None:
    # Optional: helpful to see release events too
    print("[BTN] Released", flush=True)


if __name__ == "__main__":
    print("Pi UDP Button Sender (GPIO17 -> GND, pull-up enabled)", flush=True)
    print(f"Target ESP: {ESP_IP}:{ESP_PORT}", flush=True)
    print("Press the button to toggle START/STOP.\n", flush=True)

    # Bind events
    button.when_pressed = on_pressed
    button.when_released = on_released

    # Prove UDP works even without button (you should see this on ESP Serial)
    time.sleep(0.2)
    send_udp("HELLO_FROM_PI")

    pause()
