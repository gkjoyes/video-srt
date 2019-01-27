import toml
import csv
from moviepy import editor
import sys


def read_conf(file="conf/conf.toml"):
    """
    read_conf will read configfile for our project
    """

    try:
        with open(file) as configfile:
            confstr = configfile.read()
        return toml.loads(confstr)
    except Exception as e:
        print('Conf File not found. Check the path variable and filename: ', str(e))
        sys.exit()


def read_csv(file_path='data/subtitle.csv'):
    """
    read_csv will read subtitle csv file
    and convert that data into a specific format for
    compatibility with moviepy library.
    """
    try:
        lines = []
        with open(file_path, newline='') as subtitles:
            subtitle_reader = csv.DictReader(subtitles)
            for txt in subtitle_reader:
                line = []
                start_end = (int(txt['start']), int(txt['end']))
                line.append(start_end)
                line.append(txt['text'])
                lines.append(tuple(line))

        return lines
    except Exception as e:
        print('Subtitle File not found. Check the path variable and filename: ', str(e))
        sys.exit()


def annotate(
        clip,
        subtitle,
        txt_color='white',
        fontsize=20,
        font='',
        loc_x="center",
        loc_y="bottom"):
    """
    Writes a text(subtitle) to the specified position.
    """
    txtclip = editor.TextClip(subtitle, fontsize=fontsize, font=font, color=txt_color)
    cvc = editor.CompositeVideoClip([clip, txtclip.set_pos((loc_x, loc_y))])
    return cvc.set_duration(clip.duration)


def append_subtitle(conf, subtitles):
    try:
        video = editor.VideoFileClip(conf['data']['video'])
        annotated_clips = [annotate(
            video.subclip(from_t, to_t),
            txt,
            conf['subtitle-conf']['txt_color'],
            conf['subtitle-conf']['fontsize'],
            conf['subtitle-conf']['font'],
            conf['subtitle-conf']['position'][0],
            conf['subtitle-conf']['position'][1])
            for (from_t, to_t), txt in subtitles]

        final_clip = editor.concatenate_videoclips(annotated_clips)
        final_clip.write_videofile(conf['data']['output'])
    except Exception as e:
        print("Exception occured during appending subtitle to video: ", str(e))


if __name__ == '__main__':
    conf_file = "conf/conf.toml"
    conf = read_conf(conf_file)
    subtitles = read_csv(conf['data']['subtitle'])
    append_subtitle(conf, subtitles)
