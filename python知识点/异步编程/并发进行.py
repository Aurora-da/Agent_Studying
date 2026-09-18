import time
import asyncio

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    return f"{what} 完成"

async def main():
    print(f"程序开始于：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

    # 创建两个 Task， 它们会被事件循环并发调度，在这里它们两个已经开始运行了
    task1 = asyncio.create_task(say_after(1, "你好"))
    task2 = asyncio.create_task(say_after(2, "世界"))

    # 等待两个 Task 完成， 并获取结果
    result1 = await task1
    result2 = await task2

    print(f"结果：{result1}, {result2}")
    print(f"程序结束于：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

if __name__ == "__main__":
    asyncio.run(main())