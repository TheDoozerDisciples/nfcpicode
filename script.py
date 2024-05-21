import board
import busio
from digitalio import DigitalInOut


from adafruit_pn532.i2c import PN532_I2C

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)

UID_GROUP_ASSIGNMENT = {}
UID_GROUP = {}

UID_LIST = {str(bytearray(b'\x93\x17\xbb\x02')): "White Tag", 
            str(bytearray(b'\xb1z\xe2\r')): "Blue Tag"}

reset_pin = DigitalInOut(board.D6)

req_pin = DigitalInOut(board.D12)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)


ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

def switch_to_page(uid):
    page = UID_LIST[str(uid)]
    # TODO SELENIUM OPENING PAGE


print("Waiting for RFID/NFC card...")

previous_uid = None
increment = 0
uid_group = UID_GROUP[UID_GROUPS_ASSIGNMENT[None]]
while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)

    if previous_uid not in uid_group:
        if increment >= 5:
            previous_uid = uid
            switch_to_page(uid)
        else:
            increment += 1


    # # Try again if no card is available.
    # if uid is None:
    #     continue
    # if str(uid) in UID_LIST.keys():
    #     print(UID_LIST[str(uid)])
    # print("Found card with UID:", [hex(i) for i in uid])
    # print(uid)