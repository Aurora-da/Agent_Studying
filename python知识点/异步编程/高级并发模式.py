import asyncio

async def fetch_data(id, delay):
    print(f"任务{id}开始")
    await asyncio.sleep(delay)
    print(f"任务{id}结束")
    return {"id": id, "data": f"来自任务{id}"}

async def main():
    # 并发进行三个任务，并等待所有完成
    results = await asyncio.gather(
        fetch_data(1, 2),
        fetch_data(2, 1),
        fetch_data(3, 3),
    )
    print("所有的任务结果", results)

if __name__ == "__main__":
    asyncio.run(main())