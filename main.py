import asyncio

async def ticker(delay, to):
    """Yield numbers from 0 to `to` every `delay` seconds."""
    for i in range(to):
        yield i
        await asyncio.sleep(delay)

async def main():
    async for t in ticker(1, 10):
        print(t)
        # process(t)

if __name__ == "__main__":
    asyncio.run(main())

