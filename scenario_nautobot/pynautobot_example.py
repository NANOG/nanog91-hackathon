#!/usr/bin/env python3

import pynautobot
import os

# Set the base URL for the Nautobot API
nb_url = os.environ.get("NB_URL", "http://localhost:80")

nb = pynautobot.api(
    url=nb_url,
    token="2126afe0cf4cfd8eeb8048a669df9fab2e97c24f",
)

# Retrieve all devices with a name containing "spine"
devices = nb.dcim.devices.filter(q="spine")
for d in devices:
    print(f"device {d.name}: model={d.device_type.model}, serial={d.serial}")

print("")
# Find a device named "demo"
demo = nb.dcim.devices.get(name="demo")
if demo:
    print("Found device named 'demo'")
else:
    print("Device named 'demo' not found")

# Create a device named "demo", if it doesn't already exist:
if not demo:
    demo = nb.dcim.devices.create(
        name="demo",
        role="switch_spine",
        device_type={"model": "cEOS"},
        location={"name": "MCI1"},
        status="Active",
        custom_fields={"bgp_asn": "65550"}

    )
    print("Created device named 'demo'")

# Update the device's serial number
demo.serial = "1234567890"
demo.save()
print(f"Updated device named 'demo' with serial number {demo.serial}")

# Delete the device
demo.delete()
print("Deleted device named 'demo'")
