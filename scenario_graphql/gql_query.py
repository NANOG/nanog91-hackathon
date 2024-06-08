#!/usr/bin/env python3

import asyncio
from aiohttp import ClientSession
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import logging
logging.basicConfig(level=logging.ERROR)
import pprint
import os
import sys

# Demo Nautobot instance for the hackathon
GQL_ENDPOINT = "http://n91-nautobot.hackathon.nanog.org:8080/api/graphql/"
CSRF_TOKEN_ENDPOINT = "http://n91-nautobot.hackathon.nanog.org:8080/api/"

"""
API token string can be found on the Admin page in Nautobot.
Ether fill in the constant below, or set NB_API_TOKEN environment variable.
"""
# NB_API_TOKEN:str = "changeme"
# Comment below out if you're filling in the key above
NB_API_TOKEN: None = None


class GqlQuery:
    """Run GraphQL query."""
    
    def __init__(self, gql_endpoint: str,
                 api_token: str,
                 with_csrf: bool,
                 csrf_endpoint: str = None):
        self.gql_endpoint = gql_endpoint
        self.api_token = api_token
        self.with_csrf = with_csrf
        self.csrf_token_endpoint = csrf_endpoint
    
    async def _fetch_csrf_token(self, session: ClientSession, url: str) -> str:
        """
        Because GQL Queries are POST requests, some servers will require
        a CSRF token.
        """
        # Need to include text/html header, otherwise cookie is not generated
        async with session.head(url, headers={"Accept":"text/html"}) as response:
            # Extract the CSRF token from the cookies
            csrf_token = response.cookies.get('csrftoken').value
            print(f"DEBUG: csrf_token = {csrf_token}")
            return csrf_token

    async def fetch_data(self, query_str) -> dict:
        """Execute the GraphQL query."""
        # Set default token header
        headers: dict[str] = {"Authorization": f"Token {self.api_token}"}
        cookies: dict[str] = {}

        async with ClientSession() as session:

            if self.with_csrf:
                # Fetch the CSRF token
                csrf_token = self._fetch_csrf_token(session, self.csrf_token_endpoint)
                # Then set 
                headers["X-CSRFToken"] = csrf_token
                cookies["csrftoken"] = csrf_token

            # Define the transport with a Nautobot server URL and token authentication
            transport = AIOHTTPTransport(url=self.gql_endpoint,
                                        headers=headers,
                                        cookies=cookies,
                                        )

            # GQL Query
            async with Client(transport=transport, fetch_schema_from_transport=False) as gql_session:
                # Execute the query on the transport
                result = await gql_session.execute(gql(query_str))

            return result

async def main():
    """Putting in this docstring so I don't get fined. Main, obv."""
    
    # API Token is either defined above, or set as an environmet var
    if NB_API_TOKEN:
        nb_api_token: str = NB_API_TOKEN
    else:
        nb_api_token: str = os.environ.get('NB_API_TOKEN')
        if not nb_api_token:
            logging.fatal("Must define NB_API_TOKEN!")
            sys.exit(1)
    # CSRF seems to be required by Nautobot when I stand up an instance on localhost; however,
    # this doesn't seem to be needed connecting from an external host. Which seems very strange.
    # Either way, you can update the arg if it's needed.        
    g = GqlQuery(gql_endpoint=GQL_ENDPOINT,
                 api_token=nb_api_token,
                 with_csrf=False)
    # Sample query
    data = await g.fetch_data('{locations(name: "MCI1"){name facility}}')
    pprint.pprint(data)

if __name__ == "__main__":
    asyncio.run(main())
