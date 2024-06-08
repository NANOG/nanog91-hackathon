# NANOG 91 Challenges

## Introduction

This challenge is an introduction to network modeling using [Nautbot](https://networktocode.com/nautobot/).

The first part is an introduction to Nautobot and using its web interface to read and write data.

The second part is an introduction to using the Nautbot REST API to read and write data.  (Nautobot also has a GraphQL API interface, which will be explored in a separate challenge.)

You are encouraged to review the [Nautobot documentation](https://docs.nautobot.com/projects/core/en/stable/) for detailed instructions on using its web interface and REST API.

These challenges build upon each other, so they should be done in order.  If at any time your Nautbot instance data gets corrupted beyond repair, you can start fresh with the command:
```
sudo containerlab deploy -c
```
This will remove all of your previous work, so if you do this you will need to repeat the steps in the challenges.  (You will retain credit for any challenges you have already completed, so you won't need to reenter the flags.)

## Notes
- Unspecified parameter values are not checked by the scorer.  You may experiment and set them however you like.

## Part 1: Data Model and Web Interface

This section focuses on an introduction to Nautobot's data model and using its web interface to perform common functions.  No programming knowledge is needed.

### Challenge 1.1: Start Nautobot
- Note the public IP address of your team's containerlab host.  You will need this in order to use the web browser.
- Log into your containerlab host.
- Ensure that no other containerlab instances are running, then start up your nautobot instance:
```
cd /opt/clab/scenario_nautobot
sudo containerlab destroy --all
sudo containerlab deploy
```
- While waiting for nautobot to initialize, set up your python environment:
```
poetry install
poetry shell
```
- Browse to http://_ipaddress_:80.  You should see the Nautobot login screen.  If not, wait a few minutes and try again.
- Run the scoring script and copy/paste the output code as the flag below:
```
score 1.1
```

### Challenge 1.2: Nautobot Basics
- Log in with username `nanog91` and password `hackathon`
- Find the device named `leaf2`
- Enter the device's serial number as the flag for this challenge.

### Challenge 1.3: Create an API Token
- Add a read/write API token with the key `2126afe0cf4cfd8eeb8048a669df9fab2e97c24f`
- Run the scoring script and copy/paste the output code as the flag below:
```
score 1.3
```
### Challenge 1.4: Create Devices
- In the location `MCI1`, add a rack named `MCI1-R02` with status `Active`.
- Create two new devices `leaf3` and `leaf4`.  Both should have role `switch_leaf`, device type `Arista cEOS`, location `MCI1`, rack `MCI1-R02`. and status `Active`.  See the table below for additional parameters.

| name  | serial     | position | bgp_asn |
| ----  | ------     | -------- | ------- |
| leaf3 | CEOS000012 | U1       | 65012   |
| leaf4 | CEOS000013 | U2       | 65013   |

- Run the scoring script and copy/paste the output code as the flag below:
```
score 1.4
```

### Challenge 1.5: IP Addressing and Connections
Note: In this challenge, all prefixes and addresses must be
in the `hackathon-template-scenario` namespace.

- Add some prefixes for the links to `leaf3`:

| Prefix | Type |
| ------  | ---- | 
| 10.10.0.4/31 |  network |
| 10.10.1.4/31 |  network |
| 2001:db8:10:10::4/127 |  network |
| 2001:db8:10:10:1::4/127 | network |


- Set the following interfaces and connnections on device `leaf3`:

| interface | IPv4 addr    | IPv6 addr               | Connected to |
| --------- | ---------    | ---------               | ------------ |
| Ethernet2 | 10.10.0.5/31 | 2001:db8:10:10::5/127   | spine1:Ethernet3 |
| Ethernet3 | 10.10.1.5/31 | 2001:db8:10:10:1::5/127 | spine2:Ethernet3 |
| Loopback0 | 192.168.0.5/32 | 2001:db8:0:1:1::5/128 | (none) |
| Management0 | 172.22.0.8/24 | (none) | (none) |

- Run the scoring script and copy/paste the output code as the flag below:
```
score 1.5
```
## Part 2: API Queries

This section focuses using Nautobot's REST API to manipulate data.
Some progamming knowledge is helpful.
Examples are given in Python, but feel free to use another language or toolset.
Just don't use the web interface like in the previous section, that would be cheating!
(It is fine to check your work in the web interface, however.)

You can explore the API structure by clicking the "API" button at the bottom right of any Nautobot web page.
Documentation for the _pynautobot_ python toolkit is available [here](https://docs.nautobot.com/projects/pynautobot/en/latest/) with more advanced information [here](https://docs.nautobot.com/projects/pynautobot/en/cs-mkdocs-tweaks/dev/advanced/).

### Challenge 2.1: API Read Operations
- Write a script to use the API to count the number of devices with
device model `cEOS`.
- Enter the resulting integer value as the flag below.

### Challenge 2.2: API Create Operations
- Using the API:
  - Create a new device type with model `vEOS`, manufacturer `Arista`, part number `veos`, and height `2`.
  - Create a new device named `test-switch` with role `switch_spine`, and device type `vEOS`. (The remaining mandatory values may be set as you wish.)
 
- Run the scoring script and copy/paste the output code as the flag below:
```
score 2.2
```

### Challenge 2.3: API Update Operations
- Using the API, modify the height for device type `vEOS` to `1`.
- Run the scoring script and copy/paste the output code as the flag below:
```
score 2.3
```

### Challenge 2.4: API Delete Operations
- Using the API, delete the device type `vEOS`.
Note that this may fail due to dependencies, you might also need to find
and remove any objects which depend on this device type.
- Run the scoring script and copy/paste the output code as the flag below:
```
score 2.4
```

### Challenge 2.5: Putting it all Together!
Note: In this challenge, all prefixes and addresses must be
in the `hackathon-template-scenario` namespace.

- Create device `leaf5`.
- Create a new devices `leaf5`, with role `switch_leaf`, device type `Arista cEOS`, location `MCI1`, rack `MCI1-R02`. and status `Active`.  See the table below for additional parameters.

| name  | serial     | position | bgp_asn |
| ----  | ------     | -------- | ------- |
| leaf5 | CEOS000014 | U3       | 65014   |

- Add some prefixes for the links to `leaf5`:

| Prefix | Type |
| ------  | ---- | 
| 10.10.0.8/31 |  network |
| 10.10.1.8/31 |  network |
| 2001:db8:10:10::8/127 |  network |
| 2001:db8:10:10:1::8/127 | network |


- Set the following interfaces and connnections on device `leaf5`:

| interface | IPv4 addr    | IPv6 addr               | Connected to |
| --------- | ---------    | ---------               | ------------ |
| Ethernet2 | 10.10.0.9/31 | 2001:db8:10:10::9/127   | spine1:Ethernet4 |
| Ethernet3 | 10.10.1.9/31 | 2001:db8:10:10:1::9/127 | spine2:Ethernet4 |
| Loopback0 | 192.168.0.9/32 | 2001:db8:0:1:1::9/128 | (none) |
| Management0 | 172.22.0.10/24 | (none) | (none) |

- Run the scoring script and copy/paste the output code as the flag below:
```
score 2.5
```