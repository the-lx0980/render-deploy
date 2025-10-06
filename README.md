# 🛰️ Render Projects Auto Monitor Bot

A **fully automated Render project monitor bot** built using **Pyrogram** and **APScheduler**.  
It periodically checks the status of multiple deployed web apps (e.g., on Render, Vercel, etc.),  
auto-redeploys any app that goes down, and posts live status updates in a Telegram **channel message**.

---

## ⚙️ Features

- 🔄 **Automatic Status Check** — runs every X minutes (configurable)
- 🧠 **Auto Redeploy if Down** — calls your Render deploy hook when a project is offline
- 📢 **Channel Update** — keeps one pinned message in your status channel always up-to-date
- 🧹 **No Private Chat Commands** — runs silently, no PM commands or buttons
- ⚡ **Lightweight & Async** — uses `httpx` and `asyncio` for fast non-blocking requests

---

