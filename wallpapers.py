import os, configparser, ctypes, random, argparse
from send2trash import send2trash

config_path = os.path.abspath(os.path.dirname(__file__))
config_file = os.path.join(config_path, 'wallpapers.ini')

# next_wallpaper(): 
# pick a new wallpaper from _folder_ and set it as current background
# + update _ini_ file with its path
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

# delete_wallpaper():
# get current background path from _ini_ and delete
# + manually call next_wallpaper()
def delete_wallpaper():
    # read source folder from wallpapers.cfg
    config = configparser.ConfigParser()
    config.read(config_file)
    wallpaper_location = config.get('DEFAULT', 'last')
    if os.path.isfile(wallpaper_location):
        send2trash(wallpaper_location)
    next_wallpaper()

# set_path():
# update wallpapers folder in _ini_
# + manually call next_wallpaper() 
def set_path(new_path):
    if os.path.isdir(new_path):
        config = configparser.ConfigParser()
        config.read(config_file)
        config['DEFAULT']['folder'] = new_path
        with open(config_file, 'w') as configfile:    
            config.write(configfile)
        next_wallpaper()

# check_config():
# look up _ini_ file and if it doesn't exist - create
# + if no folder reference - create using getcwd()
def check_config():
    if not os.path.isfile(config_file):
        config = configparser.ConfigParser()
        config['DEFAULT']['folder'] = config_path
        config['DEFAULT']['last'] = ''
        with open(config_file, 'w') as configfile:    
            config.write(configfile)
    else:
        config = configparser.ConfigParser()
        config.read(config_file)
        wallpaper_folder = config['DEFAULT']['folder']
        if not os.path.isdir(wallpaper_folder):
            config['DEFAULT']['folder'] = config_path
            with open(config_file, 'w') as configfile:    
                config.write(configfile)

# run_main()
# where the magic happens
def run_main():
    check_config()
    # Initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-D", "--delete", action="store_true")
    parser.add_argument("-P", "--path", type=str)
    # Read arguments from the command line
    args = parser.parse_args()
    if args.delete:
        delete_wallpaper()
    elif args.path:
        set_path(args.path)
    else:
        next_wallpaper()

if __name__ == "__main__":
    run_main()