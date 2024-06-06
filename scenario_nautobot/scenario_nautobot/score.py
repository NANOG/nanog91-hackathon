#!/usr/bin/env python3

import argparse
import hashlib
import sys
import pynautobot
# import colorama
from colorama import Fore, Back, Style

def score_hash(*values):
    string = '|'.join(str(v) for v in values)
    # print(f"string={string}")
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

def score_1_1(nb, verbose=False):
    dev = nb.dcim.devices.get(name="leaf1")
    return score_hash(dev.serial)

def score_1_2(nb, verbose=False):
    print("Challenge 1.2 requires a value from the Nautobot web interface.")
    print("See the challenge description for details.")
    return None

def score_1_3(nb, verbose=False):
    dev = nb.dcim.devices.get(name="leaf2")
    # print(f"serial={dev.serial}")
    dev.asset_tag = "24601"
    try:
        dev.save()
    except Exception as e:
        print(f"Failed to update device: {e}")
        print("Hint: Make sure your token has \"Write enabled\" set.")
        sys.exit(1)
    return score_hash(dev.serial)


def score_1_4(nb, verbose=False):
    query = """
{
  devices(name: ["leaf3", "leaf4"]) {
    name
    serial
    role {
      name
    }
    device_type {
      model
    }
    status {
      name
    }
    location {
      name
    }
    rack {
      name
    }
    position
    _custom_field_data
  }
}
"""
    response = nb.graphql.query(query=query)
    if verbose:
        print(f"return code={response.status_code}")
        print(response.json)
    devices = response.json['data']['devices']
    device = {}
    for dev in devices:
        device[dev['name']] = dev
    if verbose:
        print(f"device={device}")

    if 'leaf3' not in device or 'leaf4' not in device:
        print("Unable to find one or both new devices.")
        return None
    
    return score_hash(device['leaf3'], device['leaf4'])


def score_1_5(nb, verbose=False):
    return(score_hash("leaf4"))


RO_TOKEN = "1dc0438033a3b624e2ddc92995d7d4cd1bdee69a"
RW_TOKEN = "2126afe0cf4cfd8eeb8048a669df9fab2e97c24f"

challenges = {
    "1.1": { "token": RO_TOKEN, "scorer": score_1_1 },
    "1.2": { "token": None,     "scorer": score_1_2 },
    "1.3": { "token": RW_TOKEN, "scorer": score_1_3 },
    "1.4": { "token": RW_TOKEN, "scorer": score_1_4 },
    "1.5": { "token": RW_TOKEN, "scorer": score_1_5 },
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("challenge", help="Challenge number")
    ap.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = ap.parse_args()

    if args.challenge not in challenges:
        print(f"Challenge {args.challenge} not implemented")
        return 1

    c = challenges[args.challenge]
    if "token" in c and c["token"]:
        try:
            nb = pynautobot.api(
                url="http://hackathon.twincreeks.net:8003",
                token=c["token"],
                # token="2126afe0cf4cfd8eeb8048a669df9fab2e97c24f",
                # token="b648cf8a0a0c7e50fd62110e414e672cb61bdcdd",
            )
        except Exception as e:
            print(f"Failed to connect to Nautobot: {e}")
            return 1
    else:
        nb = None

    flag = c["scorer"](nb, verbose=args.verbose)
    if flag:
        print(f"Enter the following code as your flag for challenge {args.challenge}:")
        print(Style.BRIGHT + flag + Style.RESET_ALL)
    else:
        print(f"No flag for challenge {args.challenge}.")
        print("Check your work or see the instructions.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
