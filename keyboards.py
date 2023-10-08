from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboards(keyboard):

    if keyboard == 'video_main':
        btn1 = InlineKeyboardButton('INVERT COLOURS', callback_data='video_invert')
        btn2 = InlineKeyboardButton('TRIM VIDEO', callback_data='video_trim')
        btn3 = InlineKeyboardButton('MERGE VIDEOS', callback_data='video_merge')
        btn4 = InlineKeyboardButton('CLOSE', callback_data='close')
        buttons = [[btn1], [btn2], [btn3], [btn4]]
        kb = InlineKeyboardMarkup(buttons)
        return kb

# buttons = [
#     [btn1],
#     [btn2, btn3]
# ]
