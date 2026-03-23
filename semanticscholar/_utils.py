import asyncio
import concurrent.futures


def _run_async(coro):
    """Run an async coroutine from synchronous code, even if an event
    loop is already running (e.g. Jupyter notebooks)."""
    try:
        asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(asyncio.run, coro)
            return future.result()
    except RuntimeError:
        return asyncio.run(coro)
