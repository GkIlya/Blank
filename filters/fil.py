from aiogram import types

from aiogram.dispatcher.filters import BoundFilter

from config import admins


class Admin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in admins