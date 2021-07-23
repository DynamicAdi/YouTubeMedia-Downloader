import os
import time
from telethon import TelegramClient 
from telethon import events 
from telethon.tl.types import DocumentAttributeAudio
from config import *
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
# Config #
API_ID = config.API_ID
API_HASH = config.API_HASH
TOKEN = config.TOKEN

psycho = TelegramClient('ytvideo', API_ID, API_HASH).start(bot_token=TOKEN)
# startup # above #


@psycho.on(events.NewMessage(pattern="^/yt(audio|video)"))
async def download_video(v_url):
    """ For .ytdl command, download media from YouTube and many other sites. """
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()
    lmao = await v_url.reply("`Preparing to download...`")
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "256",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        video = False
        song = True
    elif type == "video":
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        song = False
        video = True
    try:
        await lmao.edit("`Fetching data, please wait..`")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await lmao.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await lmao.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await lmao.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await lmao.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await lmao.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await lmao.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await lmao.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await lmao.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await lmao.edit(f"{str(type(e)): {str(e)}}")
        return
    time.time()
    if song:
        await lmao.edit(
            f"`Preparing to upload song:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(ytdl_data["duration"]),
                    title=str(ytdl_data["title"]),
                    performer=str(ytdl_data["uploader"]),
                )
            ],
        )
        os.remove(f"{ytdl_data['id']}.mp3")
    elif video:
        await lmao.edit(
            f"`Preparing to upload video:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp4",
            supports_streaming=True,
            caption=ytdl_data["title"],
        )
        os.remove(f"{ytdl_data['id']}.mp4")
     
# Start up lines 
START = """
HI[👀](https://telegra.ph/file/a0f8de2ef7c7778e5c509.jpg)
Welcome✨ This is  YouTube Downloader
•I can download Video with YT links🤩
•I can Download Audio too with YT links 

Check Help for more.

"""

# Help lines
HELP = """
HEY This is Help menu for Me
|| use `/ytaudio`<Link> FOR AUDIO ||
|| use `/ytvideo`<Link> For VIDEO ||
•Report bugs&issue at Support 🙃•

"""

# ABOUT lines 
ABOUT = """
WELCOME ✨
This is about me:
→ Name:- Afiya YouTube Media Downloader 
→ Library:- Telethon 
→ Class:- Python3 

"""
@psycho.on(events.NewMessage(pattern="/start"))
async def start(event):
      await event.reply(START, buttons=[
        [
          Button.url("updates Channel", url="t.me/Psycho_Bots"),
          Button.url("Support", url="t.me/Psychobots_chat")
          ],
          [
            Button.inline("help", data="hlp"),
            Button.inline("About", data="abt")]
           ])
       
     
   
@psycho.on(events.callbackquery.CallbackQuery(data="hlp"))
async def hlp(event):
      await event.edit(HELP, buttons=[
        [
          Button.inline("Back🧚", data="bc")],
          ])
        
     
   
@psycho.on(events.callbackquery.CallbackQuery(data="abt"))
async def abt(event):
      await event.edit(ABOUT, buttons=[
        [
          Button.inline("Back🧚", data="bc")],
          ])
          
@psycho.on(events.callbackquery.CallbackQuery(data="bc"))
async def bc(event):
      await event.edit(START, buttons=[
        [
          Button.url("updates Channel", url="t.me/Psycho_Bots"),
          Button.url("Support", url="t.me/Psychobots_chat")
          ],
          [
            Button.inline("help", data="hlp"),
            Button.inline("About", data="abt")]
           ])
           
         
       
      
# © BY @Alone_loverboy
# For Own PsychoBots 
# Telethon
# Python3 
# Kanger = Gay 
