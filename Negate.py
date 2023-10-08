import io
import os
from threading import Thread
import ffmpeg
from get_video_data import get_video_data
from thumbnails import gen_thumbs


class Negate(Thread):
    def __init__(self, bot, video_path, bm):

        Thread.__init__(self)
        self.bot = bot
        self.video_path = video_path
        self.bm = bm
        org_filename = video_path.split('\\')[-1]
        self.out_filename = f'negate-{org_filename}'

    def run(self):
        self.bot.edit_message_text(self.bm.chat.id, self.bm.id, f'Download complete'
                                                                f'\n\nProcess started')
        try:
            process = (
                ffmpeg
                .input(self.video_path)
                .filter('negate')
                .output(self.out_filename)
                .run(capture_stdout=True, capture_stderr=True)
            )
            stderr = process[1].decode('utf-8')
            self.bot.edit_message_text(self.bm.chat.id, self.bm.id, 'Process finished'
                                                                    '\n\nUploading')

            caption = self.out_filename.split('.')[0]
            data = get_video_data(self.out_filename)

            if data['size'] < 10485760:  # 10 MB MINIMUM TO SET THUMBNAILS ON TELEGRAM
                bvm = self.bot.send_video(self.bm.chat.id, self.out_filename,
                                          caption=caption,
                                          duration=data['duration'],
                                          width=data['width'],
                                          height=data['height'],
                                          file_name=self.out_filename)

            else:
                thumbs = gen_thumbs(self.out_filename, data)
                if thumbs is not None:
                    bvm = self.bot.send_video(self.bm.chat.id, self.out_filename,
                                              caption=caption,
                                              duration=data['duration'],
                                              width=data['width'],
                                              height=data['height'],
                                              thumb=io.BytesIO(thumbs),
                                              file_name=self.out_filename)

                else:
                    bvm = self.bot.send_video(self.bm.chat.id, self.out_filename,
                                              caption=caption,
                                              duration=data['duration'],
                                              width=data['width'],
                                              height=data['height'],
                                              file_name=self.out_filename)

            if bvm is not None:
                os.remove(self.out_filename)

        except ffmpeg.Error as e:
            stderr = e.stderr.decode('utf-8')
            self.bot.edit_message_text(self.bm.chat.id, self.bm.id, 'Process failed')
            self.bot.send_message(self.bm.chat.id, stderr)

        os.remove(self.video_path)
