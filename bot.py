import os
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Bot tokens for multiple bots
bot_tokens = [
    'YOUR_BOT_1_TOKEN',  # First bot token (for scraping)
    'YOUR_BOT_2_TOKEN'   # Second bot token (for uploading)
]

# Local directory to save media
download_dir = './downloads/'

# Function to download media from a bot
def download_media(update, context):
    # Checking if message contains media (photo or video)
    if update.message.photo or update.message.video:
        # Get the file from message
        file = update.message.photo[-1].get_file() if update.message.photo else update.message.video.get_file()
        # Create a file path based on message ID
        file_path = os.path.join(download_dir, f"{update.message.message_id}.jpg" if update.message.photo else f"{update.message.message_id}.mp4")
        # Download the file
        file.download(file_path)
        update.message.reply_text(f"Media downloaded to {file_path}")
    else:
        update.message.reply_text("No media found in the message.")

# Function to handle the /start command
def start(update, context):
    bot = update.message.bot
    update.message.reply_text(f"Hello from {bot.name}, I am here to assist you!")

# Function to upload media to another bot
def upload_media_to_another_bot(bot_token, media_file):
    bot = Bot(token=bot_token)
    # Send media to second bot
    bot.send_document(chat_id=bot.get_me().id, document=media_file)
    print(f"Media uploaded to Bot 2: {media_file}")

# Function to set up and handle multiple bots
def set_up_multiple_bots():
    # Setup first bot (for scraping)
    for bot_token in bot_tokens:
        bot = Bot(token=bot_token)
        updater = Updater(bot_token, use_context=True)
        dispatcher = updater.dispatcher

        # Handle /start command
        dispatcher.add_handler(CommandHandler('start', start))
        
        # Handle media download
        dispatcher.add_handler(MessageHandler(Filters.photo | Filters.video, download_media))

        # Start polling for the bot
        updater.start_polling()

# Main function to initiate the bots and handle media scraping and uploading
def main():
    set_up_multiple_bots()

    # After scraping, upload media to another bot (Example)
    media_file = "./downloads/some_image.jpg"  # Example media file (this should come from the downloaded media)
    upload_media_to_another_bot(bot_tokens[1], media_file)  # Upload to second bot

if __name__ == "__main__":
    # Make sure download folder exists
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # Start the program
    main()
