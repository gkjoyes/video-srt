import toml
import csv


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


def read_csv(file_path='data/subtitle.csv'):
    """
    read_csv will read subtitle csv file
    and convert that data into a specific format for
    compatibility with moviepy library.
    """

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


if __name__ == '__main__':
    conf_file = "conf/conf.toml"
    conf = read_conf(conf_file)
    subtitles = read_csv(conf['data']['subtitle'])
    print(subtitles)
