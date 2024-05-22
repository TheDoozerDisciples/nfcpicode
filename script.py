import board
import busio
from digitalio import DigitalInOut
import webbrowser
import pyautogui


from adafruit_pn532.i2c import PN532_I2C

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)


UID_LIST = {str(bytearray(b'\x93\x17\xbb\x02')): "White Tag", 
            str(bytearray(b'\xb1z\xe2\r')): "Blue Tag",
            str(None): "Homepage"}


URL_LIST = {}

reset_pin = DigitalInOut(board.D6)

req_pin = DigitalInOut(board.D12)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)


ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

def switch_to_page(cell_part):
    if cell_part == None:
        pyautogui.hotkey('ctrl', 'w')
        pyautogui.press('f11')
        return
    else:
        url = URL_LIST[cell_part]
        pyautogui.hotkey('ctrl', 'w')
        webbrowser.open(url)
        pyautogui.press('f11')



print("Waiting for RFID/NFC card...")

previous_cell_part = UID_LIST[str(None)]
increment = 0

switch_to_page(None)
while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    
    if str(uid) in UID_LIST.keys():
        cell_part = UID_LIST[str(uid)]
    else:
        print("UNKNOWN UID: ", uid)

    if cell_part != previous_cell_part:
        if increment >= 4:
            previous_cell_part = cell_part
            switch_to_page(cell_part)
        else:
            increment += 1
    else:
        continue


    # # Try again if no card is available.
    # if uid is None:
    #     continue
    # if str(uid) in UID_LIST.keys():
    #     print(UID_LIST[str(uid)])
    # print("Found card with UID:", [hex(i) for i in uid])
    # print(uid)