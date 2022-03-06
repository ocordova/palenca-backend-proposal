import asyncio
import inspect
from typing import Any

import factory


# https://github.com/FactoryBoy/factory_boy/issues/679#issuecomment-673960170
class TortoiseModelFactory(factory.Factory):
    """Asynchronous factory for creating tortoise model."""

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def maker_coroutine():
            for key, value in kwargs.items():
                if inspect.isawaitable(value):
                    kwargs[key] = await value
            return await model_class.create(*args, **kwargs)

        return asyncio.create_task(maker_coroutine())

    @classmethod
    async def create_batch(cls, size, **kwargs):  # pylint: disable=W0236
        return [await cls.create(**kwargs) for _ in range(size)]
