from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

from AloneX import pbot
from AloneX.db.imposterdb import (
    impo_off,
    impo_on,
    check_pretender,
    add_userdata,
    get_userdata,
    usr_data,
)
from AloneX.helpers.decorator import protected_ids, user_admin_cache


async def is_user_admin(chat_id: int, user_id: int):
    if user_id in protected_ids:
        return True
    key = (chat_id, user_id, "a")
    cached = user_admin_cache.get(key)
    if cached is not None:
        return cached
    try:
        member = await pbot.get_chat_member(chat_id, user_id)
        ok = member.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        )
        user_admin_cache[key] = ok
        return ok
    except Exception:
        return False


@pbot.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=69)
async def chk_usr(_, message: Message):
    if message.sender_chat or not await check_pretender(message.chat.id):
        return
    if not message.from_user:
        return

    if not await usr_data(message.from_user.id):
        return await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )

    usernamebefore, first_name, lastname_before = await get_userdata(message.from_user.id)
    msg = ""

    if (
        usernamebefore != message.from_user.username
        or first_name != message.from_user.first_name
        or lastname_before != message.from_user.last_name
    ):
        msg += f"""**🔓 PRETENDER DETECTED 🔓**

👤 User: {message.from_user.mention}
🆔 ID: `{message.from_user.id}`

"""

    if usernamebefore != message.from_user.username:
        msg += f"**Username Changed**\nFrom: {usernamebefore or 'NO USERNAME'}\nTo: {message.from_user.username or 'NO USERNAME'}\n\n"

    if first_name != message.from_user.first_name:
        msg += f"**First Name Changed**\nFrom: {first_name}\nTo: {message.from_user.first_name}\n\n"

    if lastname_before != message.from_user.last_name:
        msg += f"**Last Name Changed**\nFrom: {lastname_before or 'NO LAST NAME'}\nTo: {message.from_user.last_name or 'NO LAST NAME'}\n\n"

    if msg:
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
        await message.reply_photo(
            "https://telegra.ph/file/58afe55fee5ae99d6901b.jpg",
            caption=msg,
        )


@pbot.on_message(filters.group & filters.command("imposter"))
async def set_mataa(_, message: Message):
    if not message.from_user:
        return

    if not await is_user_admin(message.chat.id, message.from_user.id):
        return await message.reply_text("❌ You must be an admin.")

    if len(message.command) == 1:
        return await message.reply_text(
            "Usage: /imposter enable | disable"
        )

    arg = message.command[1].lower()

    if arg == "enable":
        already = await impo_on(message.chat.id)
        if already:
            await message.reply_text("Pretender mode is already enabled.")
        else:
            await message.reply_text("Pretender mode enabled successfully.")

    elif arg == "disable":
        enabled = await impo_off(message.chat.id)
        if not enabled:
            await message.reply_text("Pretender mode is already disabled.")
        else:
            await message.reply_text("Pretender mode disabled successfully.")
    else:
        await message.reply_text("Usage: /imposter enable | disable")
      
