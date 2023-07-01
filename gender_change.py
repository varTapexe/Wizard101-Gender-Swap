import asyncio
import struct

from wizwalker import ClientHandler, utils

utils.override_wiz_install_location(r'E:\Kingsisle Entertainment\Wizard101')

# Male: 1
# Female: 0
# Other???: 3
target_gender = 3

"""
This script will change every single player, pet, and mount into the selected gender.
"""

MODELINFOPATTERN = rb"\x44\x8B\x88\xB4\x00\x00\x00\x44" \
                   rb"\x8B\x90\xB0\x00\x00\x00\x48\x8B" \
                   rb"\x0E\x48\x8B\x11\x48\x8B\xC2\x48" \
                   rb"\x3B\xD1\x74\x17\x4C\x8B\x40\x10" \
                   rb"\x45\x39\x48\x48\x74\x19"


async def main():
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


if __name__ == "__main__":
    asyncio.run(main())

