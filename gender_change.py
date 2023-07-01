import asyncio
import struct

from wizwalker import ClientHandler, utils

path = input("What is your Wizard101 path? (Example: C:\Kingsisle Entertainment\Wizard101)\n")
utils.override_wiz_install_location(rf'{path}')

target_gender = False

"""
This script will change every wizard in your game into the chosen gender.
"""

MODELINFOPATTERN = rb"\x44\x8B\x88\xB4\x00\x00\x00\x44" \
                   rb"\x8B\x90\xB0\x00\x00\x00\x48\x8B" \
                   rb"\x0E\x48\x8B\x11\x48\x8B\xC2\x48" \
                   rb"\x3B\xD1\x74\x17\x4C\x8B\x40\x10" \
                   rb"\x45\x39\x48\x48\x74\x19"


async def main(gender):
    try:
        target_gender = gender
        if target_gender:
            async with ClientHandler() as ch:
                clients = ch.get_new_clients()
        
                # address should be the same for all clients
                model_info_race = await clients[0].hook_handler.pattern_scan(
                    MODELINFOPATTERN,
                    module="WizardGraphicalClient.exe",
                )
                model_info_gender = model_info_race + 7
        
                packed_gender = struct.pack("<I", target_gender)
                packed_gender_bytes = b"\x41\xBA" + packed_gender + b"\x90"
        
                for client in clients:
                    print(f"{packed_gender_bytes=}")
                    await client.hook_handler.write_bytes(model_info_gender, packed_gender_bytes)
        else:
            target_gender = input("Please choose a gender: (Type M or F)\n")
            if target_gender.lower() == "f":
                target_gender = 0
            elif target_gender.lower() == "m":
                target_gender = 1
            else:
                print("Not a valid gender input.")
                exit()
            async with ClientHandler() as ch:
                clients = ch.get_new_clients()
        
                # address should be the same for all clients
                model_info_race = await clients[0].hook_handler.pattern_scan(
                    MODELINFOPATTERN,
                    module="WizardGraphicalClient.exe",
                )
                model_info_gender = model_info_race + 7
        
                packed_gender = struct.pack("<I", target_gender)
                packed_gender_bytes = b"\x41\xBA" + packed_gender + b"\x90"
        
                for client in clients:
                    print(f"{packed_gender_bytes=}")
                    await client.hook_handler.write_bytes(model_info_gender, packed_gender_bytes)
    except Exception as e:
        if "root.wad not found" in f'{e}':
            print(f"Invalid Wizard101 path.")
        elif "list index out of range" in f'{e}':
            print(f"Make sure Wizard101 is open.") 
        else:
            print(f"An error occured: {e}") 
        exit()


if __name__ == "__main__":
    asyncio.run(main(target_gender))

