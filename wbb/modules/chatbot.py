"""
MIT License

Copyright (c) 2021 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from pyrogram import filters

from wbb import (BOT_ID, SUDOERS, app, arq)
from wbb.core.decorators.errors import capture_err
from wbb.utils.filter_groups import chatbot_group

__MODULE__ = "ChatBot"
__HELP__ = """
/chatbot [ON|OFF] To Enable Or Disable ChatBot In Your Chat.
.chatbot [ON|OFF] To Do The Same For Userbot."""

active_chats_bot = []
active_chats_ubot = []


# Enabled | Disable Chatbot


@app.on_message(filters.command("chatbot") & ~filters.edited)
@capture_err
async def chatbot_status(_, message):
    global active_chats_bot
    if len(message.command) != 2:
        await message.reply_text("**Usage**\n/chatbot [ON|OFF]")
        return
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id

    if status == "ON" or status == "on" or status == "On":
        if chat_id not in active_chats_bot:
            active_chats_bot.append(chat_id)
            text = (
                "Chatbot Enabled Reply To Any Message "
                + "Of Mine To Get A Reply"
            )
            await message.reply_text(text)
            return
        await message.reply_text("ChatBot Is Already Enabled.")
        return

    elif status == "OFF" or status == "off" or status == "Off":
        if chat_id in active_chats_bot:
            active_chats_bot.remove(chat_id)
            await message.reply_text("Chatbot Disabled!")
            return
        await message.reply_text("ChatBot Is Already Disabled.")
        return

    else:
        await message.reply_text("**Usage**\n/chatbot [ON|OFF]")


async def lunaQuery(query: str, user_id: int):
    luna = await arq.luna(query, user_id)
    return luna.result


@app.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded,
    group=chatbot_group,
)
@capture_err
async def chatbot_talk(_, message):
    if message.chat.id not in active_chats_bot:
        return
    if not message.reply_to_message:
        return
    if message.reply_to_message.from_user.id != BOT_ID:
        return
    query = message.text
    await app2.send_chat_action(message.chat.id, "typing")
    response = await lunaQuery(
        query, message.from_user.id if message.from_user else 0
    )
    await app2.send_chat_action(message.chat.id, "cancel")
    await message.reply_text(response)
