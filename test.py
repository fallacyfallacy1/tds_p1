# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "faker",
#     "httpx",
#     "numpy",
#     "pillow",
#     "python-dateutil",
# ]
# ///


async def read(path: str):
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(f"http://localhost:8000/read?path={path}")
        if response.status_code != 200:
            raise Exception(f"Cannot read {path}")
        return response.text


async def run():
    print(await read("/data/format.md"))


run()
