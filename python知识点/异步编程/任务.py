import asyncio

async def worker(name, delay):
    await asyncio.sleep(delay)
    print(f"worker {name} completed")

async def main():
    task1 = asyncio.create_task(worker("A", 3))
    task2 = asyncio.create_task(worker("B", 2))
    await task1
    await task2

if __name__ == "__main__":
    asyncio.run(main())