import time
import asyncio

async def say_after(delay, what):
    """模拟耗时操作的一个简单的异步函数"""
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"程序开始于：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

    # 顺序执行两个协程，await用于挂起当前协程，等待一个可等待对象完成
    await say_after(1, "你好")
    await say_after(2, "世界")

    print(f"程序结束于：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

if __name__ == "__main__":
    asyncio.run(main())