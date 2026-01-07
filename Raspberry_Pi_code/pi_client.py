from gpiozero import Button, LED
import socket
import select
import time

ESP_IP = "192.168.12.131"
ESP_PORT = 5005
PI_LISTEN_PORT = 5006

BUTTON_GPIO = 17
WHITE_GPIO = 16

RED_GPIO = 20
GREEN_GPIO = 21
BLUE_GPIO = 26

LOW_MAX = 850
MED_MAX = 1000

btn = Button(BUTTON_GPIO, pull_up=True, bounce_time=0.06)
white = LED(WHITE_GPIO)
red = LED(RED_GPIO)
green = LED(GREEN_GPIO)
blue = LED(BLUE_GPIO)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PI_LISTEN_PORT))
sock.setblocking(False)

IDLE = 0
ACTIVE = 1
ERROR = 2

state = IDLE
last_rx = 0.0
flash_next = 0.0
flash_on = False

def rgb_off():
    red.off()
    green.off()
    blue.off()

def all_off():
    white.off()
    rgb_off()

def set_rgb_by_value(v: int):
    if v <= LOW_MAX:
        red.on(); green.off(); blue.off()
    elif v <= MED_MAX:
        red.on(); green.on(); blue.off()
    else:
        red.on(); green.on(); blue.on()

def send_msg(msg: str):
    sock.sendto(msg.encode("utf-8"), (ESP_IP, ESP_PORT))

def go_idle():
    global state
    state = IDLE
    all_off()

def go_active():
    global state, last_rx, flash_next, flash_on
    state = ACTIVE
    last_rx = time.monotonic()
    flash_on = False
    white.on()
    rgb_off()
    send_msg("START")

def go_error():
    global state, flash_next, flash_on
    state = ERROR
    rgb_off()
    flash_on = False
    flash_next = time.monotonic()

def on_button_press():
    global state
    if state == IDLE:
        go_active()
    else:
        send_msg("STOP")
        go_idle()

btn.when_pressed = on_button_press

go_idle()

while True:
    now = time.monotonic()

    if state == ACTIVE:
        if now - last_rx >= 10.0:
            go_error()

    if state == ERROR:
        if now >= flash_next:
            flash_on = not flash_on
            (white.on() if flash_on else white.off())
            flash_next = now + 0.5

    r, _, _ = select.select([sock], [], [], 0.05)
    if r:
        data, _addr = sock.recvfrom(1024)
        msg = data.decode("utf-8", errors="ignore").strip()

        if state == ACTIVE:
            last_rx = time.monotonic()
            try:
                v = int(msg)
                set_rgb_by_value(v)
            except ValueError:
                pass
