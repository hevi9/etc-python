import asyncio


async def atask(secs):
    print("sleeping %ds" % secs)
    await asyncio.sleep(secs)
    print("wake up after %ds" % secs)

tasks = [atask(i) for i in range(10)]
tasks = asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(tasks)
loop.close()

