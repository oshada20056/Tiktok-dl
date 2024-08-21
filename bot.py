
   import requests
   from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

   # Replace with your Bot Token
   BOT_TOKEN = "5782499781:AAHsp52YhPxonTz84FOi-stSMJ-281_jccI"

   def start(update, context):
       update.message.reply_text("Welcome! Send me a TikTok video link to download it.")

   def download_tiktok(update, context):
       url = update.message.text
       if "tiktok.com" in url:
           try:
               # Use a TikTok API (optional) or a TikTok video downloader
               # Example using a public TikTok downloader (replace this with your chosen method)
               response = requests.get(f"https://www.tiktokdownloader.com/download?url={url}")
               response.raise_for_status()  # Raise an exception for bad HTTP requests
               video_url = response.text.split('"')[1]

               # Send the downloaded video to the user
               context.bot.send_video(chat_id=update.effective_chat.id, video=video_url)

           except Exception as e:
               update.message.reply_text(f"Error: {e}")
       else:
           update.message.reply_text("Please provide a valid TikTok video link.")

   def main():
       updater = Updater(BOT_TOKEN, use_context=True)
       dispatcher = updater.dispatcher

       dispatcher.add_handler(CommandHandler("start", start))
       dispatcher.add_handler(MessageHandler(Filters.text, download_tiktok))

       updater.start_polling()
       updater.idle()

   if __name__ == "__main__":
       main()
   
