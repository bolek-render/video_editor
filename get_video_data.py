import os
import ffmpeg


def get_video_data(source_file):
    size = os.path.getsize(source_file)
    probe = ffmpeg.probe(source_file)
    duration = int(float(probe['streams'][0]['duration']))
    width = probe['streams'][0]['width']
    height = probe['streams'][0]['height']

    data = {'size': size,
            'duration': duration,
            'width': width,
            'height': height}

    return data
