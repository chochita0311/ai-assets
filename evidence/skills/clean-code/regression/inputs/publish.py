"""Synthetic asynchronous publisher with caller-owned state and resources."""


async def publish(stopping, clock, deadline, write, mark_complete, release):
    try:
        if stopping() or clock() >= deadline:
            return False
        await write()
        if stopping() or clock() >= deadline:
            return False
        mark_complete()
        return True
    finally:
        await release()
