import io
import os
import ffmpeg
from PIL import Image, UnidentifiedImageError


def gen_thumbs(source, data):
    thumbnails_bytes = None

    duration = data['duration']
    width = data['width']
    height = data['height']

    if duration >= 16:
        frame_step = int(duration / 16)
        frames = []
        thumbs = []

        for frame in range(int(frame_step / 2), duration + 1, frame_step):
            frames.append(frame)

        for frame in frames:
            out, _ = (
                ffmpeg
                .input(source, ss=frame)
                .output('pipe:', vframes=1, format='image2', vcodec='png', loglevel="quiet")
                .global_args('-nostdin')
                .run(capture_stdout=True)
            )
            thumbs.append(io.BytesIO(out))

        if len(thumbs) == 16:
            thumbnails = Image.new('RGB', (width * 4, height * 4))
            index = 0

            for x in range(0, height * 4, height):
                for y in range(0, width * 4, width):
                    try:
                        image = Image.open(thumbs[index])
                        thumbnails.paste(image, (y, x))
                    except UnidentifiedImageError:
                        pass

                    index += 1

            thumbs.clear()
            thumbnails_bytes = io.BytesIO()
            thumbnails.save(thumbnails_bytes, format='png')
            thumbnails_bytes = thumbnails_bytes.getvalue()

    return thumbnails_bytes
