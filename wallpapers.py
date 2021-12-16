import os, configparser, ctypes, random, argparse

config_path = os.getcwd()
config_file = os.path.join(config_path, 'wallpapers.ini')

def next_wallpaper():
    # read source folder from wallpapers.cfg
    config = configparser.ConfigParser()
    config.read(config_file)
    wallpaper_location = config.get('DEFAULT', 'folder')

    # get file list, only .jpg and .jpeg
    files = os.listdir(wallpaper_location)
    backgrounds = [file for file in files if file.endswith(( '.jpg', '.jpeg', '.png'))]

    if backgrounds:
        # set new wallpaper
        new_wallpaper = os.path.join(wallpaper_location, random.choice(backgrounds))
        if os.path.isfile(new_wallpaper):
            ctypes.windll.user32.SystemParametersInfoW(20, 0, new_wallpaper , 0)
            
            # update config file with the location of current wallpaper
            config['DEFAULT']['last'] = new_wallpaper
            with open(config_file, 'w') as configfile:    
                config.write(configfile)

def delete_wallpaper():
    # read source folder from wallpapers.cfg
    config = configparser.ConfigParser()
    config.read(config_file)
    wallpaper_location = config.get('DEFAULT', 'last')

    if os.path.isfile(wallpaper_location):
        os.remove(wallpaper_location)
    
    next_wallpaper()

def set_path(new_path):
    if os.path.isdir(new_path):
        config = configparser.ConfigParser()
        config.read(config_file)
        config['DEFAULT']['folder'] = new_path
        with open(config_file, 'w') as configfile:    
            config.write(configfile)
        next_wallpaper()

def check_config():
    if not os.path.isfile(config_file):
        config = configparser.ConfigParser()
        config['DEFAULT']['folder'] = config_path
        config['DEFAULT']['last'] = ''
        with open(config_file, 'w') as configfile:    
                    config.write(configfile)

def run_main():
    # Initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-D", "--delete", action="store_true")
    parser.add_argument("-P", "--path", type=str)

    # Read arguments from the command line
    args = parser.parse_args()

    # Check for --version or -V
    if args.delete:
        delete_wallpaper()
    elif args.path:
        set_path(args.path)
    else:
        next_wallpaper()

check_config()
run_main()
