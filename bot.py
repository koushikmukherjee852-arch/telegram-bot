import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# Bot configuration
API_ID = 6789000
API_HASH = "your_api_hash"
BOT_TOKEN = "8826931471:AAHwnW62SLT31D_sjEeuzMx75SYB9LfC_A8"
ADMIN_ID = 7983981652

app = Client(
    "telegram_inbox_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.private & ~filters.user(ADMIN_ID))
async def handle_direct_messages(client: Client, message: Message):
    user = message.from_user
    user_name = user.first_name if user and user.first_name else "User"
    user_mention = user.mention if user else "User"
    
    # 1. Forward the message to the admin
    await message.forward(ADMIN_ID)
    
    # 2. Send info to admin
    await client.send_message(
        ADMIN_ID,
        f"📩 **New Inbox Message**\nFrom: {user_mention} (ID: `{user.id}`)"
    )
    
    # 3. Send automated reply to the user
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
    
