from gpiozero import Button, LED
from signal import pause
import socket

ESP_IP = "192.168.12.131"
ESP_PORT = 5005

button = Button(17, pull_up=True)
white_led = LED(16)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_udp(msg):
    sock.sendto(msg.encode("utf-8"), (ESP_IP, ESP_PORT))
    print(msg, flush=True)

def on_press():
    white_led.on()
    send_udp("START")

def on_release():
    white_led.off()
    send_udp("STOP")

button.when_pressed = on_press
button.when_released = on_release

pause()
