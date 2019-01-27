import toml


def read_conf(file="conf/conf.toml"):
    try:
        with open(file) as configfile:
            confstr = configfile.read()
        return toml.loads(confstr)
    except Exception as e:
        print('Conf File not found. Check the path variable and filename: ', str(e))


if __name__ == '__main__':
    conf_file = "conf/conf.toml"
    conf = read_conf(conf_file)
    print(conf)
