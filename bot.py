from pyrogram import Client, filters
import requests
import re
import os
import math

# Replace these with your own values
api_id = '21204722'
api_hash = '4f5b4bbc15e7f9df9961ac92e8fd219b'
bot_token = '5782499781:AAHsp52YhPxonTz84FOi-stSMJ-281_jccI'

# Initialize Pyrogram Client
app = Client("tiktok_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Function to download TikTok video with progress bar
def download_tiktok_video(url, message):
    video_id = re.search(r'/video/(\d+)', url)
    if not video_id:
        return None

    video_id = video_id.group(1)

    # Replace with a real TikTok video download URL or service
    download_url = f"https://api.tiktokv.com/aweme/v1/play/?video_id={video_id}&line=0&ratio=default&media_type=4&improve_bitrate=0&source=PackSourceEnum_PUBLISH"

    try:
        response = requests.get(download_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        if response.status_code == 200:
            file_name = f"{video_id}.mp4"
            with open(file_name, 'wb') as f:
                downloaded_size = 0
                chunk_size = 1024
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)

                        # Update progress bar
                        progress = math.ceil(downloaded_size / total_size * 100)
                        if progress % 10 == 0:  # Update every 10%
                            app.send_message(
                                chat_id=message.chat.id,
                                text=f"Download progress: {progress}%"
                            )
            return file_name
        else:
            return None
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

# Command handler for downloading TikTok videos
@app.on_message(filters.command("download") & filters.text)
async def download_tiktok(client, message):
    url = message.text.split(maxsplit=1)[-1]

    await message.reply_text("Downloading TikTok video...")

    video_file = download_tiktok_video(url, message)
    if video_file:
        await message.reply_video(video_file, caption="Here is your TikTok video!")
        os.remove(video_file)
    else:
        await message.reply_text("Failed to download the TikTok video. Please check the URL and try again.")

# Run the bot
app.run()
