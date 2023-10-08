from pyrogram import Client, filters
from pyrogram.errors import RPCError
import os
import math

from Negate import Negate
from keep_alive import keep_alive
from keyboards import keyboards
import common_globals as cg


bot = Client('video_editor',
             api_id=os.environ['API_ID'],
             api_hash=os.environ['API_HASH'],
             bot_token=os.environ['BOT_TOKEN'],
             max_concurrent_transmissions=4)


@bot.on_message(filters.command('start'))
async def start_command(client, msg):
    await msg.reply('Alive')


async def dl_progress(current, total, client, bm):
    def convert_size(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    progress = float(f"{current * 100 / total:.1f}")
    current = convert_size(current)
    total = convert_size(total)

    if progress != 100.0:
        await client.edit_message_text(bm.chat.id, bm.id, f'Downloading {progress}%'
                                                          f'\n{current} / {total}')
    else:
        try:
            await client.edit_message_text(bm.chat.id, bm.id, f'Download complete')
        except RPCError:
            pass


@bot.on_message(filters.video)
async def video_message(client, msg):
    cid = msg.chat.id
    cg.user_job[cid] = msg
    await client.send_message(cid, 'What do you want to do', reply_markup=keyboards('video_main'))


@bot.on_callback_query(filters.regex('video_invert'))
async def callback_query(client, call):
    cid = call.message.chat.id
    mid = call.message.id
    video_msg = cg.user_job[cid]

    bm = await client.edit_message_text(cid, mid, 'Download starting')
    video_path = await video_msg.download(progress=dl_progress, progress_args=(client, bm))
    Negate(client, video_path, bm).start()


try:
    bot.stop()
except ConnectionError:
    pass

keep_alive()
print('BOT STARTING')
bot.run()
