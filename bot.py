import os
import re
import zipfile
import asyncio
import shutil
from telethon import TelegramClient, events
from telethon.tl.types import InputStickerSetShortName
from telethon.tl.functions.messages import GetStickerSetRequest
import logging

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Get API credentials from environment variables
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Validate essential credentials
if not all([API_ID, API_HASH, BOT_TOKEN]):
    logger.error("Missing required environment variables! Please set TELEGRAM_API_ID, TELEGRAM_API_HASH, and TELEGRAM_BOT_TOKEN")
    exit(1)

try:
    API_ID = int(API_ID)
except ValueError:
    logger.error("TELEGRAM_API_ID must be an integer")
    exit(1)

# Create a directory for temporary files
if not os.path.exists('stickers'):
    os.makedirs('stickers')

# Initialize the client
client = TelegramClient('sticker_downloader_bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(pattern=r'(?i).*(t\.me/addstickers/|https?://t\.me/addstickers/)([a-zA-Z0-9_]+).*'))
async def handle_sticker_pack(event):
    """Handle messages containing sticker pack links"""
    try:
        # Send initial status message
        status_msg = await event.respond("Processing your sticker pack request...")

        # Extract the sticker pack name from the URL
        match = re.search(r'(?:t\.me/addstickers/|https?://t\.me/addstickers/)([a-zA-Z0-9_]+)', event.text)
        if not match:
            await status_msg.edit("Invalid sticker pack link. Please send a valid t.me/addstickers/... link.")
            return

        sticker_set_name = match.group(1)
        await status_msg.edit(f"Found sticker pack: {sticker_set_name}\nDownloading stickers...")

        try:
            # Get the sticker set using the proper function
            sticker_set_input = InputStickerSetShortName(short_name=sticker_set_name)
            sticker_set = await client(GetStickerSetRequest(stickerset=sticker_set_input, hash=0))

            # Check if sticker set exists and has documents
            if not sticker_set or not hasattr(sticker_set, 'documents') or not sticker_set.documents:
                await status_msg.edit("Could not find that sticker pack or it's empty. Please check the link and try again.")
                return

            # Create a unique folder for this pack
            pack_folder = f"stickers/{sticker_set_name}"
            if os.path.exists(pack_folder):
                shutil.rmtree(pack_folder)  # Clear existing folder if it exists
            os.makedirs(pack_folder)

            # Download all stickers
            total_stickers = len(sticker_set.documents)
            await status_msg.edit(f"Downloading {total_stickers} stickers from pack '{sticker_set_name}'...")

            for i, document in enumerate(sticker_set.documents):
                # Determine file extension based on MIME type
                if document.mime_type == 'application/x-tgsticker':
                    file_ext = ".tgs"  # Animated stickers
                elif document.mime_type.startswith('video/'):
                    file_ext = ".webm"  # Video stickers
                else:
                    file_ext = ".webp"  # Regular stickers

                file_path = f"{pack_folder}/{sticker_set_name}_{i+1}{file_ext}"

                try:
                    await client.download_media(document, file_path)

                    # Update progress regularly
                    if (i + 1) % 5 == 0 or i == 0 or i == total_stickers - 1:
                        percentage = ((i + 1) / total_stickers) * 100
                        await status_msg.edit(f"Downloaded {i+1}/{total_stickers} stickers ({percentage:.1f}%)...")
                except Exception as dl_error:
                    logger.warning(f"Failed to download sticker {i+1}: {str(dl_error)}")
                    continue

            # Create ZIP archive
            zip_path = f"stickers/{sticker_set_name}.zip"
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for root, dirs, files in os.walk(pack_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, arcname=os.path.basename(file_path))

            # Send the ZIP file if it exists and has content
            if os.path.exists(zip_path) and os.path.getsize(zip_path) > 0:
                await status_msg.edit(f"Sending sticker pack archive for '{sticker_set_name}'...")
                await client.send_file(
                    event.chat_id,
                    zip_path,
                    caption=f"Sticker pack: {sticker_set_name}\nTotal stickers: {total_stickers}"
                )
                await status_msg.edit("Done! All stickers have been downloaded and sent.")
            else:
                await status_msg.edit("Failed to create the sticker pack archive. No stickers could be downloaded.")

            # Clean up
            try:
                if os.path.exists(pack_folder):
                    shutil.rmtree(pack_folder)
                if os.path.exists(zip_path):
                    os.remove(zip_path)
            except Exception as cleanup_error:
                logger.error(f"Error during cleanup: {cleanup_error}")

        except Exception as pack_error:
            logger.error(f"Error processing sticker set {sticker_set_name}: {str(pack_error)}")
            await status_msg.edit(f"Error processing sticker pack: {str(pack_error)}")

    except Exception as e:
        logger.error(f"Unexpected error in handle_sticker_pack: {e}")
        try:
            await event.respond(f"An unexpected error occurred: {str(e)}")
        except:
            pass

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    """Handle the /start command"""
    await event.respond(
        "👋 Welcome to Sticker Pack Downloader Bot!\n\n"
        "Send me a sticker pack link (t.me/addstickers/...) and I'll download "
        "all stickers from the pack and send them to you as a ZIP archive.\n\n"
        "Example: t.me/addstickers/Animals\n\n"
        "Use /help to see available commands."
    )

@client.on(events.NewMessage(pattern='/help'))
async def help_handler(event):
    """Handle the /help command"""
    await event.respond(
        "📚 **Bot Usage:**\n\n"
        "1. Send a sticker pack link like: t.me/addstickers/packname\n"
        "2. Wait while I download all stickers\n"
        "3. Receive a ZIP file with all stickers from the pack\n\n"
        "**Supported sticker types:**\n"
        "- Regular stickers (.webp)\n"
        "- Animated stickers (.tgs)\n"
        "- Video stickers (.webm)\n\n"
        "**Available commands:**\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/ping - Check if bot is alive"
    )

@client.on(events.NewMessage(pattern='/ping'))
async def ping_handler(event):
    """Simple ping command to check if bot is alive"""
    await event.respond("Pong! Bot is running.")

async def main():
    """Main function to start the bot"""
    try:
        # Connect to Telegram
        await client.start(bot_token=BOT_TOKEN)

        # Print some information
        me = await client.get_me()
        logger.info(f"Bot started as @{me.username}")

        # Run the client until disconnected
        await client.run_until_disconnected()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
    finally:
        # Cleanup on exit
        if client.is_connected():
            await client.disconnect()
        logger.info("Bot has been stopped")

if __name__ == '__main__':
    # Run the main function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
