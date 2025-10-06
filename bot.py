import os
import httpx
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_API_KEY = os.getenv("RENDER_API_KEY")
OWNER_ID = int(os.getenv("OWNER_ID", "736279262"))

# ✅ Add your Render projects here
PROJECTS = {
    "file-streamer": "srv-cpudugmehbks73efe7a0",
    "video-bot": "srv-cabc123xyz456def789",
    "website-deploy": "srv-cdef987uvw654zyx321"
}

app = Client("render_deploy_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def trigger_render_deploy(service_id: str) -> str:
    """Trigger render redeploy"""
    url = f"https://api.render.com/deploy/{service_id}?key={RENDER_API_KEY}"
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.post(url)
            if r.status_code in [200, 201, 202]:
                return f"✅ Deploy started for `{service_id}` (HTTP {r.status_code})"
            else:
                return f"⚠️ Failed to deploy `{service_id}` (HTTP {r.status_code})\nResponse: {r.text}"
        except Exception as e:
            return f"❌ Error: {e}"

# /start command
@app.on_message(filters.command("start") & filters.user(OWNER_ID))
async def start(_, message):
    await message.reply_text(
        "👋 Hello! This bot can redeploy your Render projects.\n\nUse /redeploy to choose a project."
    )

# /redeploy command — show list
@app.on_message(filters.command("redeploy") & filters.user(OWNER_ID))
async def redeploy_list(_, message):
    buttons = []
    for name, srv_id in PROJECTS.items():
        buttons.append([InlineKeyboardButton(f"🚀 {name}", callback_data=f"deploy:{srv_id}:{name}")])

    await message.reply_text(
        "Select a project to redeploy 👇",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Callback when button pressed
@app.on_callback_query(filters.user(OWNER_ID))
async def deploy_callback(_, query):
    data = query.data
    if not data.startswith("deploy:"):
        return

    parts = data.split(":")
    if len(parts) < 3:
        await query.answer("Invalid data.", show_alert=True)
        return

    service_id, project_name = parts[1], parts[2]
    await query.message.edit_text(f"⏳ Redeploying *{project_name}* ...", parse_mode="markdown")

    result = await trigger_render_deploy(service_id)
    await query.message.edit_text(result, parse_mode="markdown")

# Block others
@app.on_message(~filters.user(OWNER_ID))
async def block_others(_, message):
    await message.reply_text("🚫 You are not authorized to use this bot.")

if __name__ == "__main__":
    print("🤖 Bot started...")
    app.run()
