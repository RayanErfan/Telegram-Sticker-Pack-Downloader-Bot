
---

# 🧩 Telegram Sticker Pack Downloader Bot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Telethon](https://img.shields.io/badge/Telethon-Library-orange)](https://github.com/LonamiWebs/Telethon)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://t.me)

A **powerful Telegram bot** built with **Telethon** that lets users **download entire sticker packs** (including static, animated, and video stickers) from Telegram.
The bot automatically downloads all stickers from any pack, compresses them into a **ZIP archive**, and sends it back to the user.

---

## 🚀 Features

* 🎨 **Full pack downloads** — grab every sticker from a Telegram sticker pack
* ⚡ **Supports all types**:

  * Static stickers (`.webp`)
  * Animated stickers (`.tgs`)
  * Video stickers (`.webm`)
* 🗜️ **Automatic ZIP creation**
* 🧹 **Temporary file cleanup** after every task
* 🔁 **Progress updates** in chat
* 🛠️ **Simple commands**: `/start`, `/help`, `/ping`

---

## 🧠 How It Works

1. User sends a link like:

   ```
   t.me/addstickers/CoolDogs
   ```
2. Bot extracts the pack name and fetches the sticker list via the Telegram API.
3. Downloads all stickers locally.
4. Creates a `.zip` file (e.g. `CoolDogs.zip`).
5. Sends it to the user, then cleans up.

---

## 💬 Example Interaction

**User:**

```
t.me/addstickers/FunnyCats
```

**Bot:**

```
📦 Downloading 45 stickers...
✅ Pack ready! Sending FunnyCats.zip
```

---

## 🧰 Commands

| Command  | Description                 |
| -------- | --------------------------- |
| `/start` | Start and get instructions  |
| `/help`  | Show command list and usage |
| `/ping`  | Check if bot is alive       |

---

## ⚙️ Setup Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/RayanErfan/telegram-sticker-downloader.git
cd telegram-sticker-downloader
```

### 2️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 3️⃣ Add Environment Variables

Create a `.env` file in the project root:

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_BOT_TOKEN=your_bot_token
```

### 4️⃣ Run the Bot

```bash
python bot.py
```

---

## 🧩 Project Structure

```
.
├── bot.py                 # Main bot logic
├── stickers/              # Temporary sticker folder
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
```

---

## 🧾 Logging

The bot uses Python’s built-in `logging` module to display:

* Start / stop events
* Sticker pack download progress
* Any runtime errors

Logs are printed to stdout for easy monitoring (ideal for VPS or Docker).

---

## 🪪 License

Released under the **MIT License** — feel free to use, modify, and distribute with proper credit.

---

## ⭐ Support & Contribution

If you like this project:

* Star ⭐ the repo
* Open issues for bug reports or ideas
* Pull requests welcome!

---
