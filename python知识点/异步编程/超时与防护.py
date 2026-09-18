import asyncio

async def slow_operation():
    await asyncio.sleep(5)
    return "操作完成"

async def main():
    try:
        # 为协程设置两秒超时
        result = await asyncio.wait_for(slow_operation(), timeout=2.0)
        print(result)
    except asyncio.TimeoutError:
        print("操作超时！")

    task = asyncio.create_task(slow_operation())
    shielded_task = asyncio.shield(task)

if __name__ == "__main__":
    asyncio.run(main())