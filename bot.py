import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# Bot configuration
API_ID = 6789000
API_HASH = "your_api_hash"
BOT_TOKEN = "8826931471:AAHwnW62SLT31D_sjEeuzMx75SYB9LfC_A8"
ADMIN_ID = 7983981652

# Ban list store korar set
banned_users = set()

app = Client(
    "telegram_inbox_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.private & filters.command("start"))
async def start_command(client: Client, message: Message):
    user = message.from_user
    user_name = user.first_name if user and user.first_name else "Friend"
    
    welcome_text = (
        f"✨ **Welcome, {user_name}!**\n\n"
        f"Ami Dhruv-er private inbox bot. Apni ekhane amake direct message ba query pathate paren, seta soraSori tar kache chole jabe.\n\n"
        f"📩 Shudhu ekhane apnar message likhe pathiye din!"
    )
    await message.reply_text(welcome_text)

@app.on_message(filters.private & filters.command("owner"))
async def send_owner_info(client: Client, message: Message):
    await message.reply_text("👑 Bot Owner ID: `7983981652`\n(Apni ekhane apnar username o add kore dite paren)")

@app.on_message(filters.private & filters.command("ban") & filters.user(ADMIN_ID))
async def ban_user(client: Client, message: Message):
    try:
        if message.reply_to_message and message.reply_to_message.forward_from:
            target_id = message.reply_to_message.forward_from.id
        else:
            args = message.text.split()
            if len(args) < 2:
                await message.reply_text("⚠️ Byabohar: /ban [user_id] ba karo message-e reply kore /ban din.")
                return
            target_id = int(args[1])
        
        banned_users.add(target_id)
        await message.reply_text(f"🚫 User (`{target_id}`) ke successfully ban kora hoyeche.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@app.on_message(filters.private & filters.command("unban") & filters.user(ADMIN_ID))
async def unban_user(client: Client, message: Message):
    try:
        args = message.text.split()
        if len(args) < 2:
            await message.reply_text("⚠️ Byabohar: /unban [user_id]")
            return
        target_id = int(args[1])
        
        if target_id in banned_users:
            banned_users.remove(target_id)
            await message.reply_text(f"✅ User (`{target_id}`) ke unban kora hoyeche.")
        else:
            await message.reply_text("ℹ️ Ei user-ti ban list-e nei.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@app.on_message(filters.private & ~filters.user(ADMIN_ID))
async def handle_direct_messages(client: Client, message: Message):
    user = message.from_user
    if user and user.id in banned_users:
        return  # Jodi ban thake, message ignore hobe
        
    user_name = user.first_name if user and user.first_name else "User"
    user_mention = user.mention if user else "User"
    
    # 1. Forward message to admin
    await message.forward(ADMIN_ID)
    
    # 2. Send info to admin
    await client.send_message(
        ADMIN_ID,
        f"📩 **New Inbox Message**\nFrom: {user_mention} (ID: `{user.id}`)"
    )
    
    # 3. Send automated reply to user
    await message.reply_text(f"Hello {user_name}, your message has been sent to Dhruv.")

@app.on_message(filters.private & filters.user(ADMIN_ID) & filters.reply)
async def handle_admin_reply(client: Client, message: Message):
    replied_to = message.reply_to_message
    if replied_to and replied_to.forward_from:
        target_user_id = replied_to.forward_from.id
        await client.send_message(target_user_id, message.text)
        await message.reply_text("✅ Reply sent to the user.")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
