import asyncio
from sfapi_client import AsyncClient
from sfapi_client.compute import Machine
from sfapi_client import Resource

async def fetch_status():
    """Fetch and print the status of the Perlmutter machine."""
    async with AsyncClient() as client:
        status = await client.compute(Machine.perlmutter)
        print("Perlmutter Status:")
        print(status)
        print()

async def fetch_outages():
    """Fetch and print the most recent outages for the Spin resource."""
    async with AsyncClient() as client:
        outages = await client.resources.outages(Resource.spin)
        print("Recent Outages for Spin:")
        if outages:
            for outage in outages:
                print(outage)
        else:
            print("No recent outages found.")
        print()

if __name__ == "__main__":
    asyncio.run(fetch_status())
    # asyncio.run(fetch_outages())
