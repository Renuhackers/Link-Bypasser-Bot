from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BotCommand,
    Message,
)
from pyrogram.errors import UserNotParticipant
from os import remove
from threading import Thread
from json import load, dump
from re import search

from texts import HELP_TEXT
import bypasser
import freewall
from time import time

# Define your channels and admin chat ID here
channel_1 = "RenusHackingArmy"
channel_2 = "RenusBotsChannel"
join_photo_url = "https://t.me/MediaXStore/9"  # URL of the photo to be sent
admin_chat_id = 2068329336  # Replace with your admin chat ID

# Bot configurations
bot_token = "6447129150:AAG8XSHZeqKOkdFusBTuJhl93AecMsDey00"
api_hash = "0ca4154111e7b0f99e9929710faa3f25"
api_id = "25105744"
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Load or create users.json
try:
    with open("users.json", "r") as f:
        users = load(f)
except FileNotFoundError:
    users = {}

# Function to save users
def save_users():
    with open("users.json", "w") as f:
        dump(users, f)

# Function to handle new users
def handle_new_user(user):
    if str(user.id) not in users:
        users[str(user.id)] = {
            "name": user.first_name,
            "username": user.username,
            "chat_id": user.id
        }
        save_users()
        # Send notification to admin
        app.send_message(
            admin_chat_id,
            f"New user started the bot:\n\nName: {user.first_name}\nUsername: {user.username}\nChat ID: {user.id}"
        )

# Function to check if a user is a member of a channel
def is_member(client, user_id, channel):
    try:
        client.get_chat_member(channel, user_id)
        return True
    except UserNotParticipant:
        return False

with app:
    app.set_bot_commands(
        [
            BotCommand("start", "Welcome Message"),
            BotCommand("help", "List of All Supported Sites"),
        ]
    )

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
        if temp != None:
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

# start command
@app.on_message(filters.command(["start"]))
def send_start(
    client: Client,
    message: Message,
):
    user_id = message.from_user.id

    # Handle new user
    handle_new_user(message.from_user)

    # Check if the user is a member of the required channels
    if not (is_member(client, user_id, channel_1) and is_member(client, user_id, channel_2)):
        client.send_photo(
            message.chat.id,
            join_photo_url,
            caption="*⚠️ ᴀᴄᴄᴇss ᴅᴇɴɪᴇᴅ! ⚠️\n\n✘ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs.\n\n✘ ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴍᴇ,\n\n✘ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴs,\n\n✘ ᴛʜᴇɴ ᴄʟɪᴄᴋ /start*",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Join Channel 1", url=f"https://t.me/{channel_1[1:]}")
                    ],
                    [
                        InlineKeyboardButton("Join Channel 2", url=f"https://t.me/{channel_2[1:]}")
                    ]
                ]
            ),
            reply_to_message_id=message.id
        )
        return

    # If the user is a member of both channels, send the welcome message
    client.send_message(
        message.chat.id,
        f"👋 Hi **{message.from_user.mention}**, I am Link Bypasser Bot. Just send me any supported links, and I will get you the results.\nCheckout /help to Read More.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🌐 Source Code", url="https://github.com/bipinkrish/Link-Bypasser-Bot")
                ],
                [
                    InlineKeyboardButton("Replit", url="https://replit.com/@bipinkrish/Link-Bypasser#app.py")
                ],
            ]
        ),
        reply_to_message_id=message.id,
   
    )

# help command
@app.on_message(filters.command(["help"]))
def send_help(
    client: Client,
    message: Message,
):
    app.send_message(
        message.chat.id,
        HELP_TEXT,
        reply_to_message_id=message.id,
        disable_web_page_preview=True,
    )

# links
@app.on_message(filters.text)
def receive(
    client: Client,
    message: Message,
):
    bypass = Thread(target=lambda: loopthread(message), daemon=True)
    bypass.start()

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

# server loop
print("Bot Starting")
app.run()
