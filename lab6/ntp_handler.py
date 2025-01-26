from sys import prefix

import ntplib
from datetime import datetime, timedelta, timezone
import argparse

def get_ntp_time(gmt_offset):
    """
    Fetch the exact time from an NTP server and adjust it based on the GMT offset.

    :param gmt_offset: The GMT offset as a string (e.g., "GMT+3" or "GMT-7").
    :return: The adjusted time as a string.
    """
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org', version=3)
        utc_time = datetime.fromtimestamp(response.tx_time, tz=timezone.utc)

        sign = 1 if gmt_offset.startswith("GMT+") else -1
        offset_hours = int(gmt_offset[4:])

        local_time = utc_time + timedelta(hours=sign * offset_hours)
        return local_time.strftime("%Y-%m-%d %H:%M:%S")

    except Exception as e:
        return f"Error fetching time: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch the exact time for a given GMT offset using NTP.")
    parser.add_argument("gmt_offset", type=str, help="Your GMT offset (e.g., GMT+3 or GMT-7).")

    args = parser.parse_args()

    gmt_offset = args.gmt_offset.strip()
    if (
        not (gmt_offset.startswith("GMT+") or gmt_offset.startswith("GMT-"))
        or not gmt_offset[4:].isdigit()
        or int(gmt_offset[4:]) > 11
        or int(gmt_offset[4:]) < 0
    ):
        print("Invalid GMT offset format. Please use the format 'GMT+X' or 'GMT-X' where X is 0-11.")
    else:
        exact_time = get_ntp_time(gmt_offset)
        print(f"The exact time for {gmt_offset} is: {exact_time}")