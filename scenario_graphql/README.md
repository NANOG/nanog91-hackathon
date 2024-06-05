# GRAPHQL Challenge

This is a series of challenges utilizing Nautobot's GraphQL API.

GraphQL is a powerful query language for APIs that allows for descriptive and
efficient data queries. Utilizing JSON-formatted queries over HTTP, it allows 
clients to ask for specific data elements and attributes, and to make complex 
queries that span multiple tables (much like SQL JOINs, but utilizing heirarchial
JSON structures to make these easier to work with).

Nautobot's GraphQL API can be queried via its own web UI in Nautobot. See 
https://demo.nautobot.com/graphql.


The query language follows the same keys that are exposed by Nautobot's REST API. However,
under GraphQL, only the requested keys are returned in the reply:

![](images/2024-06-02-15-28-08.png)

Where a JSON query normally returns object IDs for associated elements which must be queried separately, the GraphQL
implementation allows for a query that can include elements from those references objects.

![](images/2024-06-02-15-26-34.png)


GraphQL queries can be filtered by values in any of the object's fields, such as name, tags, role, or similar. 

![](images/2024-06-02-15-30-28.png)

## API Access

The included gql_query python module provides a class and a reference implementation of a GQL query; use this for
your experimentation. Note that the model is async, which requires that it be called using async methods.


**CHALLENGE 1:**
Write a GraphQL query that returns the names and id values of all devices that are in the site named "MCI1".
These should be the only values returned by the query. Extraneous data will not be accepted as part of the solution.
Submit the results of the query to CTFd.

**CHALLENGE 2:**

Write a QraphQL query that returns data about a device named "spine1". The return data should consist of:
- device id
- device name
- The IPv4 and IPv6 addresses/masks assigned to the "Ethernet1" interface.

Note: The above data points should be the *only* data returned by the query. Submit the results of the query to CTFd.

**CHALLENGE 3:**

Write a GraphQL query that for the device named "leaf1", returns the following data:
- The IPv4 and IPv6 addresses of each connected device for interfaces with the "interface-fabric" tag assigned.
- The hostname and bgp_asn custom field value for the connected device.

Note: The above data points should be the *only* data returned by the query. Submit the results of the query to CTFd.

**CHALLENGE 4:**

Given the included jinja2 template, write a python script that usese GraphQL to query the above data for the device named "leaf1", then renders a BGP configuration section via jinja2.
Submit the resulting configuration file to CTFd.

## Development Environment
Note that this repo uses [[Poetry](https://python-poetry.org/)] to manage dependencies. Follow [[instructions](https://python-poetry.org/docs/#installing-with-pipx)] to install, then run the following to activate a venv with needed dependencies (ensure you are in this directory)

```
# Ensure you are in the correct directory
ls -l | grep pyproject.toml
# install dependencies
poetry install
# Activate venv with needed dependencies
poetry shell
```

To add new modules to the virtual environment, run `poetry add <module_name>` using the same module name you would use in a `pip install` command.
