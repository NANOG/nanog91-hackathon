#!/usr/bin/env python3

import argparse
import hashlib
import os
import sys
import pynautobot
# import colorama
from colorama import Fore, Back, Style
from pprint import pprint

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
    query1 = """
{
  prefixes(
    namespace: "hackathon-template-scenario"
    prefix: ["10.10.0.4/31", "10.10.1.4/31", "2001:db8:10:10::4/127", "2001:db8:10:10:1::4/127"]
  ) {
    prefix
    type
  }
}
"""

    query2 = """
{
  devices(name: "leaf3") {
    name
    interfaces(name: ["Ethernet2", "Ethernet3", "Loopback0", "Management0"]) {
      name
      connected_interface {
        device {
          name
        }
        name
      }
      ip_addresses {
        ip_version
        address
        parent {
          namespace {
            name
          }
          prefix
        }
      }
    }
  }
}
"""
    response1 = nb.graphql.query(query=query1)
    if verbose:
        print(f"return code={response1.status_code}")
        pprint(response1.json)
    prefixes = response1.json['data']['prefixes']

    response2 = nb.graphql.query(query=query2)
    if verbose:
        print(f"return code={response2.status_code}")
        pprint(response2.json)
    interfaces = response2.json['data']['devices'][0]['interfaces']
    return(score_hash(prefixes, interfaces))


def score_2_1(nb, verbose=False):
    print("Challenge 2.1 requires a value printed by your script.")
    print("See the challenge description for details.")
    return None

def score_2_2(nb, verbose=False):
    query2 = """
{
  devices(name: "test-switch") {
    name
    role {
      name
    }
    device_type {
      manufacturer {
        name
      }
      model
      part_number
      u_height
    }
  }
}
"""
    response = nb.graphql.query(query=query2)
    if verbose:
        print(f"return code={response.status_code}")
        print(response.json)
    devices = response.json['data']['devices']
    if len(devices) != 1:
        print("Unable to find device 'test-switch'.")
        return None
    return score_hash(devices[0])
 

def score_2_4(nb, verbose=False):
    dev = nb.dcim.device_types.get(model="vEOS")
    if dev is None:
        return score_hash("Success for 2.4!")
    else:
        print("vEOS device type still exists.")
        return None


def score_2_5(nb, verbose=False):
    query1 = """
{
  devices(name: "leaf5") {
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
    query2 = """
{
  prefixes(
    namespace: "hackathon-template-scenario"
    prefix: ["10.10.0.8/31", "10.10.1.8/31", "2001:db8:10:10::8/127", "2001:db8:10:10:1::8/127"]
  ) {
    prefix
    type
  }
}
"""
    response1 = nb.graphql.query(query=query1)
    if verbose:
        print(f"return code={response1.status_code}")
        print(response1.json)
    leaf5 = response1.json['data']['devices'][0]

    response2 = nb.graphql.query(query=query2)
    if verbose:
        print(f"return code={response2.status_code}")
        print(response2.json)
    prefixes = response2.json['data']['prefixes']
    return score_hash(leaf5, prefixes)

RO_TOKEN = "1dc0438033a3b624e2ddc92995d7d4cd1bdee69a"
RW_TOKEN = "2126afe0cf4cfd8eeb8048a669df9fab2e97c24f"

challenges = {
    "1.1": { "token": RO_TOKEN, "scorer": score_1_1 },
    "1.2": { "token": None,     "scorer": score_1_2 },
    "1.3": { "token": RW_TOKEN, "scorer": score_1_3 },
    "1.4": { "token": RW_TOKEN, "scorer": score_1_4 },
    "1.5": { "token": RW_TOKEN, "scorer": score_1_5 },
    "2.1": { "token": None,     "scorer": score_2_1 },
    "2.2": { "token": RW_TOKEN, "scorer": score_2_2 },
    "2.3": { "token": RW_TOKEN, "scorer": score_2_2 },  # Same as 2.2!
    "2.4": { "token": RW_TOKEN, "scorer": score_2_4 },
    "2.5": { "token": RW_TOKEN, "scorer": score_2_5 },
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("challenge", help="Challenge number")
    ap.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = ap.parse_args()

    if args.challenge not in challenges:
        print(f"Challenge {args.challenge} not implemented")
        return 1

    nbserver = os.environ.get("NB_URL", "http://localhost:80")
    c = challenges[args.challenge]
    if "token" in c and c["token"]:
        try:
            nb = pynautobot.api(
                url=nbserver,
                token=c["token"],
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
