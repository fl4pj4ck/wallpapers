import os, configparser, ctypes, random, argparse, sys
from send2trash import send2trash

config_path = os.path.dirname(os.path.realpath(sys.argv[0]))
config_file = os.path.join(config_path, 'wallpapers.ini')

def get_config(config, setting):
    # read source folder from wallpapers.cfg
    config.read(config_file)
    return(config.get('DEFAULT', setting))    

def set_config(config, name, setting):
    config['DEFAULT'][name] = setting
    with open(config_file, 'w') as configfile:    
        config.write(configfile)

def set_wallpaper(config, new_wallpaper):
    if os.path.isfile(new_wallpaper):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, new_wallpaper , 0)
        # update config file with the location of current wallpaper
        set_config(config, 'last', new_wallpaper)

# next_wallpaper(): 
# pick a new wallpaper from _folder_ and set it as current background
# + update _ini_ file with its path
def next_wallpaper(config):
    wallpaper_location = get_config(config, 'folder')
    # get file list, only .jpg and .jpeg
    files = os.listdir(wallpaper_location)
    backgrounds = [file for file in files if file.endswith(( '.jpg', '.jpeg', '.png'))]
    if backgrounds:
        # set new wallpaper
        new_wallpaper = os.path.join(wallpaper_location, random.choice(backgrounds))
        set_wallpaper(config, new_wallpaper)


# delete_wallpaper():
# get current background path from _ini_ and delete
# + manually call next_wallpaper()
def delete_wallpaper(config):
    wallpaper_location = get_config(config, 'last')
    if os.path.isfile(wallpaper_location):
        send2trash(wallpaper_location)
    next_wallpaper(config)

# set_path():
# update wallpapers folder in _ini_
# + manually call next_wallpaper() 
def set_path(config, new_path):
    if os.path.isdir(new_path):
        set_config(config, 'folder', new_path)
        next_wallpaper(config)

# check_config():
# look up _ini_ file and if it doesn't exist - create
# + if no folder reference - create using getcwd()
def check_config(config):
    if not os.path.isfile(config_file):
        set_config(config, 'folder', config_path)
        set_config(config, 'last', '')
        set_config(config, 'safe', '')
    else:
        if not os.path.isdir(get_config(config, 'folder')):
            set_config(config, 'folder', config_path)
        if not os.path.isdir(get_config(config, 'last')):
            set_config(config, 'last', '')
        if not os.path.isdir(get_config(config, 'safe')):
            set_config(config, 'safe', '')            

def load_safe(config):
    if os.path.isfile(get_config(config, 'safe')):
        set_wallpaper(config, get_config(config, 'safe'))
        set_config(config, 'last', '')

# run_main()
# where the magic happens
def run_main():
    config = configparser.ConfigParser()
    check_config(config)
    # Initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-D", "--delete", action="store_true")
    parser.add_argument("-S", "--safe", action="store_true")
    parser.add_argument("-P", "--path", type=str)
    # Read arguments from the command line
    args = parser.parse_args()
    if args.delete:
        delete_wallpaper(config)
    elif args.path:
        set_path(config, args.path)
    elif args.safe:
        load_safe(config)
    else:
        next_wallpaper(config)

if __name__ == "__main__":
    run_main()