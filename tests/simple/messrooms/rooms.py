import aiogram
import asyncio

from roombot import RoomsContainer
from roombot import HandlersTypes
from roombot import RoomsManager
from roombot import User

rc = RoomsContainer()


@rc.add_room("admins_room", HandlersTypes.on_join_universal, permissions=["admin"])
async def res(rb: RoomsManager, bot: aiogram.Bot, user: User):
    room2_text = "Room2"
    room2_button = aiogram.types.KeyboardButton(room2_text)
    await bot.send_message(user.telegram_id, "Hello. Im admin room. You cant use it as simple user",
                           reply_markup=aiogram.types.ReplyKeyboardMarkup().add(room2_button))


# @rc.add_room("admins_room", HandlersTypes.on_join_message, content_type=["text"], permissions=["admin"])
@rc.add_room("admins_room", HandlersTypes.message, content_type=["text"], permissions=["admin"])
async def res(mess: aiogram.types.Message, rb: RoomsManager):
    room2_text = "Room2"
    room2_button = aiogram.types.KeyboardButton(room2_text)
    if mess.text == room2_text:
        await rb.actions_with_user.go_to_room(mess.from_user.id, "room2")
        return
    await mess.answer("Hello. Im admin room. You cant use it as simple user",
                      reply_markup=aiogram.types.ReplyKeyboardMarkup().add(room2_button))


# Вы можете использовать on_join вместе с message
@rc.add_room("room2", HandlersTypes.callback, content_type=["text"])
async def anya(callback: aiogram.types.CallbackQuery, rb: RoomsManager):
    data = callback.data.split(":")
    if len(data) == 2 and data[0] == "goto" and data[1] == "admins_room":
        if not await rb.actions_with_user.go_to_room(callback.from_user.id, "admins_room"):
            await callback.answer("You are not admin")
        else:
            await callback.answer("Goooood")


@rc.add_room("room2", HandlersTypes.on_join_message, content_type=["text"])
@rc.add_room("room2", HandlersTypes.message, content_type=["text"])
async def res(mess: aiogram.types.Message, rb: RoomsManager):
    admins_room_text = "AdminRoom"
    start_text = "StartRoom"
    get_admin_access = "GetAdminAccess"
    admins_room_kb = aiogram.types.KeyboardButton(admins_room_text)
    admins_room_button = aiogram.types.InlineKeyboardButton(admins_room_text, callback_data="goto:admins_room")
    start_button = aiogram.types.KeyboardButton(start_text)
    get_admin_access_button = aiogram.types.KeyboardButton(get_admin_access)
    if mess.text == start_text:
        await rb.actions_with_user.go_to_room(mess.from_user.id, "start")
        return
    if mess.text == admins_room_text:
        if not await rb.actions_with_user.go_to_room(mess.from_user.id, "admins_room"):
            await mess.answer("Have no permissions")
        return
    if mess.text == get_admin_access:
        if await rb.actions_with_user.get_permissions(mess.from_user.id) != "admin":
            await rb.actions_with_user.set_permissions(mess.from_user.id, "admin")
            await mess.answer("Gets permissions")
        else:
            await mess.answer("Already have this permissions")
        return
    await mess.answer("Menu", reply_markup=aiogram.types.InlineKeyboardMarkup().add(admins_room_button))
    await mess.answer("Im room2 room",
                      reply_markup=aiogram.types.ReplyKeyboardMarkup().add(admins_room_kb).add(start_button).add(get_admin_access_button))


def an(message: aiogram.types.Message):
    return True
    if message.text in ["lol", "Room2"]:
        return True
    return False


@rc.add_room("start", HandlersTypes.on_join_message, content_type=["text"])
@rc.add_room("start", HandlersTypes.message, content_type=["text"], room_filter=an)
async def fun(mess: aiogram.types.Message, rb: RoomsManager):
    room2_text = "Room2"
    room2_button = aiogram.types.KeyboardButton(room2_text)
    if mess.text == room2_text:
        await rb.actions_with_user.go_to_room(mess.from_user.id, "room2")
        return
    await mess.answer("Im start room", reply_markup=aiogram.types.ReplyKeyboardMarkup().add(room2_button))
