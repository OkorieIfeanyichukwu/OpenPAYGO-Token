import codecs
from datetime import datetime, timedelta
#from encode_token import OPAYGOEncoder
#from shared import OPAYGOShared
#from shared_extended import OPAYGOSharedExtended


class Device:
    def __init__(
    self,
    serial_number,
    key,
    starting_code,
    restricted_digit_mode=False,
    time_divider=1,
    token_count=1,       
    )-> None:   #None not necessary

        self.serial_number = serial_number
        self.key = key
        self.starting_code = starting_code
        self.restricted_digit_mode = restricted_digit_mode
        self.time_divider =time_divider
        self.count = token_count

        self.expiration_date = datetime.now()
        self.payg_enabled = True


    def print_status(self):
        print("DEVICE STATUS")
        print(f"Serial Number: {self.serial_number}")
        print(f"Active: {self.restricted_digit_mode}")
        print(f"Expiration Date: {self.expiration_date}")
        print(f"Current count: {self.count}")
        print(f"PAYG Enabled:{self.payg_enabled}")
        print("\n")




class DeviceServer:
    def __init__(
            self,
            starting_code,
            key,
            starting_count,
            restricted_digit_mode=False,
            time_divider=1,
    )-> None:
        self.starting_code = starting_code
        self.key = key
        self.count = starting_count
        self.restricted_digit_mode = restricted_digit_mode
        self.time_divider =time_divider

        self.payg_enabled = True

    def print_status(self):
        print("SERVER STATUS")
        print(f"Current count: {self.count}")
        print(f"Enabled:{self.payg_enabled}")





















if __name__ == "__main__":
    device_data = {#creating a dictionary
        "serial_number": "ZZZ1",
        "starting_code": 123456789,
        "key": "bc41ec9530f6dac86b1a29ab82edc5fb",
        "restricted_digit_mode": False,
        "time_divider": 1,
        "token_count": 1,
    }

    device= Device(
        serial_number=device_data["serial_number"],
        key=codecs.decode(device_data["key"], "hex"),
        starting_code=device_data["starting_code"],
        restricted_digit_mode=device_data["restricted_digit_mode"],
        time_divider=device_data["time_divider"],
        token_count=device_data["token_count"],
    )
    device_server= DeviceServer(
        starting_code=device_data["starting_code"],
        key=codecs.decode(device_data["key"], "hex"),
        starting_count=device_data["token_count"],
        restricted_digit_mode=device_data["restricted_digit_mode"],
        time_divider=device_data["time_divider"],
    )   
    print("===INITIAL STATUS===")
    device.print_status()
    device_server.print_status()
    print("===END INITIAL STATUS===")
