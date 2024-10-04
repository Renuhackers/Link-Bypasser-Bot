from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BotCommand,
    Message,
    CallbackQuery,
)
from pyrogram.errors import UserNotParticipant
from os import remove
from threading import Thread
from json import load, dump
from re import search
from time import time
import os
from texts import HELP_TEXT
import bypasser
import freewall

# Define your channels and admin chat ID here
channel_1 = "RenusHackingArmy"
channel_2 = "RenusBotsChannel"
join_photo_url = "https://t.me/MediaXStore/9"  # URL of the photo to be sent
admin_chat_id = 2068329336  # Replace with your admin chat ID

# Bot configurations
bot_token = "7247999366:AAFvIWUmUlmaGwfj_5i3u4q0gf2g_DfEx9o"
api_hash = "0ca4154111e7b0f99e9929710faa3f25"
api_id = "25105744"
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Save new user chat ID and notify admin
def save_and_notify_user(chat_id, user, bot):
    file_path = "url-bypass-users.txt"
    
    # Ensure the file exists, create if not
    if not os.path.exists(file_path):
        open(file_path, 'w').close()

    # Read existing users from the file
    with open(file_path, "r") as file:
        users = file.read()

    # If user is new, save the chat ID and notify the admin
    if str(chat_id) not in users:
        # Save the new user chat ID
        with open(file_path, "a") as file:
            file.write(f"{chat_id}\n")

        # Fetch the total number of users from the file
        with open(file_path, "r") as file:
            total_users = len(file.readlines())

        # Notify the admin with formatted message
        app.send_message(
    chat_id=admin_chat_id, 
    text=f"#NewUser started bot:\nName: {user.first_name}\nID: {chat_id}\nTotal: {total_users}"
)
        
        # Function to check if a user is a member of a channel
def is_member(client, user_id, channel):
    try:
        client.get_chat_member(channel, user_id)
        return True
    except UserNotParticipant:
        return False

# Start command
@app.on_message(filters.command(["start"]))
def send_start(client: Client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    save_and_notify_user(user_id, message.from_user, client)
    # Send welcome message if the user is verified
    welcome_text = f"**» ʜᴇʟʟᴏ {user_name}!\n\n" \
                   "» ɪ ᴀᴍ ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ᴀᴅs + ᴅʀɪᴠᴇ ʙʏᴘᴀss ʙᴏᴛ\n\n" \
                   "» ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ʜᴇʀᴇ ɪ ᴡɪʟʟ ʙʏᴘᴀss ᴀʟʟ ᴛʜᴇ ᴀᴅs ʟɪɴᴋ !!\n\n" \
                   "» ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ʏᴏᴜʀ ʟɪɴᴋ & ᴇɴᴊᴏʏ\n\n" \
                   "» ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : [ʀᴇɴᴜs ʜᴀᴄᴋᴇʀ 🦋](https://t.me/RenusRobot)**"

    client.send_photo(
        chat_id=user_id,
        photo="https://t.me/MediaXStore/8",  # Replace with your welcome image URL
        caption=welcome_text,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("✘ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs ✘", url="https://t.me/{context.bot.username}?startgroup=true")],
                [InlineKeyboardButton("✘ ᴜᴘᴅᴀᴛᴇs ✘", url=f"https://t.me/RenusHackingArmy"),
                 InlineKeyboardButton("✘ sᴜᴘᴘᴏʀᴛ ✘", url=f"https://t.me/RenusBotsGroup")],
                [InlineKeyboardButton("⌬ ʀᴇǫᴜᴇsᴛ ᴀ ᴡᴇʙsɪᴛᴇ ᴛᴏ ʙʏᴘᴀss ⌬", url="https://t.me/RenusRobot")],
                [InlineKeyboardButton("〄 ʜᴇʟᴘ 〄", callback_data="help"),
                 InlineKeyboardButton("〄 ᴀʙᴏᴜᴛ 〄", callback_data="about")],
            ]
        )
    )

# Callback query handler for inline buttons
@app.on_callback_query()
def callback_handler(client: Client, query: CallbackQuery):
    data = query.data

    if data == "help":
        query.message.edit_text(
            text="*__⊹ ʜᴏᴡ ᴛᴏ ᴜsᴇ ʙʏᴘᴀss ʙᴏᴛ ⊹__*\n\n"

"`» Send me any ads link or drive links`"
"`» This bot will send the bypassed link`"
"`» This bot also supports groups`"
"`» Add me to your groups as admin to make the bot more powerful!`"
"`» For more information: RenusArmy`"

"__‼️ Warning__"
"`» Do not overload the bot`"
"`» If bot not working and issues`"
"♚ Contact ♚ - Renus Hacker",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Home", callback_data="home"),
                     InlineKeyboardButton("Close", callback_data="close")],
                ]
            )
        )
    elif data == "about":
        query.message.edit_text(
            text="┏━━━━【 ᴍʀxʙʏᴘᴀss ᴀʙᴏᴜᴛ 】━━━━✗\n"
                 "┃ » Name: MRxBypass Bot\n"
                 "┃ » Owner: MR X Mirror\n"
                 "┃ » Version: MR X 2.1\n"
                 "┃ » Language: Python 3\n"
                 "┃ » Framework: Pyrogram\n"
                 "┃ » Database: Mongo DB\n"
                 "┃ » Hosted on: MR X Server\n"
                 "┃ » Developer: MR X Mirror\n"
                 "┃ » My best friend: This Person\n"
                 "┗━━━━━━━━━━━━━━━━━━━✗",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Home", callback_data="home"),
                     InlineKeyboardButton("Close", callback_data="close")],
                    [InlineKeyboardButton("Contact", url="https://t.me/RenusHacker")],
                ]
            )
        )
    elif data == "home":
        user_id = query.from_user.id
        user_name = query.from_user.first_name
        # Redirect to home
        welcome_text = f"**» Hello {user_name}!\n\n" \
                       "» I am a powerful ads + drive bypass bot.\n\n" \
                       "» Send me your link & enjoy!\n\n" \
                       "» Maintained by: Renus Hacker 🦋**"

        query.message.edit_text(
            text=welcome_text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("✘ Add me to your Groups ✘", url="https://t.me/YOUR_BOT_USERNAME?startgroup=true")],
                    [InlineKeyboardButton("✘ Updates ✘", url=f"https://t.me/{channel_1}"),
                     InlineKeyboardButton("✘ Support ✘", url=f"https://t.me/RenusBotsGroup")],
                    [InlineKeyboardButton("⌬ Request a website to bypass ⌬", url="https://t.me/RenusRobot")],
                    [InlineKeyboardButton("〄 Help 〄", callback_data="help"),
                     InlineKeyboardButton("〄 About 〄", callback_data="about")],
                ]
            )
        )
    elif data == "close":
        query.message.delete()

def check_membership(client: Client, user_id: int):
    # Check if the user is a member of both channels
    if not (is_member(client, user_id, channel_1) and is_member(client, user_id, channel_2)):
        client.send_photo(
            chat_id=user_id,
            photo=join_photo_url,
            caption="**⚠️ ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ! ⚠️\n\n✘ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs.\n\n✘ ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴍᴇ,\n\n✘ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴs,\n\n✘ ᴛʜᴇɴ ᴄʟɪᴄᴋ /start**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Join Channel 1", url=f"https://t.me/{channel_1}")], 
                    [InlineKeyboardButton("Join Channel 2", url=f"https://t.me/{channel_2}")],
                ]
            )
        )
        return False
    return True

# links
# Handle incoming messages
@app.on_message(filters.text)
def receive(client: Client, message: Message):
    user_id = message.from_user.id
    save_and_notify_user(user_id, message.from_user, client)
    if check_membership(client, user_id):
        bypass = Thread(target=lambda: loopthread(message), daemon=True)
        bypass.start()
    # If not a member, access denied message has already been sent in check_membership function

# doc thread
def docthread(message: Message):
    msg: Message = app.send_message(
        message.chat.id, "🔎 __bypassing...__", reply_to_message_id=message.id
    )
    print("sent DLC file")
    file = app.download_media(message)
    dlccont = open(file, "r").read()
    links = bypasser.getlinks(dlccont)
    app.edit_message_text(
        message.chat.id, msg.id, f"__{links}__", disable_web_page_preview=True
    )
    remove(file)

# files
@app.on_message([filters.document, filters.photo, filters.video])
def docfile(
    client: Client,
    message: Message,
):

    try:
        if message.document.file_name.endswith("dlc"):
           
            bypass = Thread(target=lambda: docthread(message), daemon=True)
            bypass.start()
            return
    except:
        pass

    bypass = Thread(target=lambda: loopthread(message, True), daemon=True)
    bypass.start()

# handle index
def handleIndex(ele: str, message: Message, msg: Message):
    result = bypasser.scrapeIndex(ele)
    try:
        app.delete_messages(message.chat.id, msg.id)
    except:
        pass
    for page in result:
        app.send_message(
            message.chat.id,
            page,
            reply_to_message_id=message.id,
            disable_web_page_preview=True,
        )

# loop thread
def loopthread(message: Message, otherss=False):
    urls = []
    if otherss:
        texts = message.caption
    else:
        texts = message.text

    if texts in [None, ""]:
        return
    for ele in texts.split():
        if "http://" in ele or "https://" in ele:
            urls.append(ele)
    if len(urls) == 0:
        return

    if bypasser.ispresent(bypasser.ddl.ddllist, urls[0]):
        msg: Message = app.send_message(
            message.chat.id, "⚡ __generating...__", reply_to_message_id=message.id
        )
    elif freewall.pass_paywall(urls[0], check=True):
        msg: Message = app.send_message(
            message.chat.id, "🕴️ __jumping the wall...__", reply_to_message_id=message.id
        )
    else:
        if "https://olamovies" in urls[0] or "https://psa.wf/" in urls[0]:
            msg: Message = app.send_message(
                message.chat.id,
                "⏳ __this might take some time...__",
                reply_to_message_id=message.id,
            )
        else:
            msg: Message = app.send_message(
                message.chat.id, "🔎 __bypassing...__", reply_to_message_id=message.id
            )

    strt = time()
    links = ""
    temp = None

    for ele in urls:
        if search(r"https?:\/\/(?:[\w.-]+)?\.\w+\/\d+:", ele):
            handleIndex(ele, message, msg)
            return
        elif bypasser.ispresent(bypasser.ddl.ddllist, ele):
            try:
                temp = bypasser.ddl.direct_link_generator(ele)
            except Exception as e:
                temp = "**Error**: " + str(e)
        elif freewall.pass_paywall(ele, check=True):
            freefile = freewall.pass_paywall(ele)
            if freefile:
                try:
                    app.send_document(
                        message.chat.id, freefile, reply_to_message_id=message.id
                    )
                    remove(freefile)
                    app.delete_messages(message.chat.id, [msg.id])
                    return
                except:
                    pass
            else:
                app.send_message(
                    message.chat.id, "__Failed to Jump__", reply_to_message_id=message.id
                )
        else:
            try:
                temp = bypasser.shortners(ele)
            except Exception as e:
                temp = "**Error**: " + str(e)

        print("bypassed:", temp)
        if temp is not None:
            links = links + temp + "\n"

    end = time()
    print("Took " + "{:.2f}".format(end - strt) + "sec")

    if otherss:
        try:
            app.send_photo(
                message.chat.id,
                message.photo.file_id,
                f"__{links}__",
                reply_to_message_id=message.id,
            )
            app.delete_messages(message.chat.id, [msg.id])
            return
        except:
            pass

    try:
        final = []
        tmp = ""
        for ele in links.split("\n"):
            tmp += ele + "\n"
            if len(tmp) > 4000:
                final.append(tmp)
                tmp = ""
        final.append(tmp)
        app.delete_messages(message.chat.id, msg.id)
        tmsgid = message.id
        for ele in final:
            tmsg = app.send_message(
                message.chat.id,
                f"__{ele}__",
                reply_to_message_id=tmsgid,
                disable_web_page_preview=True,
            )
            tmsgid = tmsg.id
    except Exception as e:
        app.send_message(
            message.chat.id,
            f"__Failed to Bypass: {e}__",
            reply_to_message_id=message.id,
        )

# server loop
print("Bot Starting")
app.run()
