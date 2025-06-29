async def event_generator(callback):
    async for chunk in callback:
        yield f"data: {chunk}"