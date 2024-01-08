from datetime import datetime, timedelta
from encode_token import OPAYGOEncoder
from decode_token import OPAYGODecoder
from shared import OPAYGOShared
from shared_extended import OPAYGOSharedExtended
import codecs

#OPAYGOEncoder=OPAYGOEncoder()

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
        self.used_counts = []

    def print_status(self):
        print("DEVICE STATUS")
        print(f"Serial Number: {self.serial_number}")
        print(f"Active: {self.is_active()}")
        print(f"Expiration Date: {self.expiration_date}")
        print(f"Current count: {self.count}")
        print(f"PAYG Enabled:{self.payg_enabled}")
        #print(f"key: {self.key}")
        print("\n")

    def is_active(self):
        return self.expiration_date > datetime.now()

    def decode_token(self,token):
        token_value, token_count, token_type = OPAYGODecoder.get_activation_value_count_and_type_from_token(
            token=int(token),             #token was generated as string type
            starting_code=self.starting_code,
            key=self.key,
            last_count=self.count,
            restricted_digit_set= self.restricted_digit_mode,
            used_counts=self.used_counts,
        )

        if not token_value:
            print("Invalid Token")
            return False
        if token_value==-2:
            print("Old Token")
            return False
        
        self.count=token_count
        self.used_counts =OPAYGODecoder.update_used_counts(
            past_used_counts=self.used_counts,
            value=token_value,
            new_count=token_count,
            type=token_type,
        )
        self.update_device_status(token_value, token_type)

    def update_device_status(self,token_value,token_type):
        number_of_days = token_value/self.time_divider
        if token_type == OPAYGOShared.TOKEN_TYPE_SET_TIME:
            self.expiration_date=datetime.now() + timedelta(days=number_of_days)
        else:
            if self.expiration_date<datetime.now():
                self.expiration_date =datetime.now()
            self.expiration_date = self.expiration_date + timedelta(days=number_of_days)

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
        #print(f"key: {self.key}")

    def generate_token(self,value,mode):
        self.count, token = OPAYGOEncoder.generate_standard_token(
            starting_code = self.starting_code,
            key = self.key,
            value = value,
            count= self.count,
            mode=mode,
            restricted_digit_set=self.restricted_digit_mode,
        )
        return token

if __name__ == "__main__":
    device_data = {#creating a dictionary
        "serial_number": "ZZZ1",
        "starting_code": 123456789,
        "key": b"bc41ec9530f6dac86b1a29ab82edc5fb",            #bc41ec95 works for codecs.encode while  bc41ec9530f6dac86b1a29ab82edc5fb works for codecs.decode
        "restricted_digit_mode": False,
        "time_divider": 1,
        "token_count": 1,
    }

    device= Device(
        serial_number=device_data["serial_number"],
        key=codecs.decode(device_data["key"], 'hex'),
        starting_code=device_data["starting_code"],
        restricted_digit_mode=device_data["restricted_digit_mode"],
        time_divider=device_data["time_divider"],
        token_count=device_data["token_count"],
    )
    device_server= DeviceServer(
        starting_code=device_data["starting_code"],
        key=codecs.decode(device_data["key"], 'hex'),
        starting_count=device_data["token_count"],
        restricted_digit_mode=device_data["restricted_digit_mode"],
        time_divider=device_data["time_divider"],
    )   
    print("===INITIAL STATUS===")
    device.print_status()
    device_server.print_status()
    print("===END INITIAL STATUS===")

token = device_server.generate_token(5,OPAYGOShared.TOKEN_TYPE_ADD_TIME)
print(f"TOKEN: {token}  the type: {type(token)}") 

#use token on device
device.decode_token(token=token)


print("===STATUS AFTER DECODING TOKEN===")
device.print_status()
device_server.print_status()
print("===END STATUS===")