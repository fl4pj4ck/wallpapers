import os, configparser, ctypes, random, argparse, sys, datetime, time, shutil
from send2trash import send2trash
from PIL import Image

config_path = os.path.dirname(os.path.realpath(sys.argv[0]))
config_file = os.path.join(config_path, 'wallpapers.ini')
log_file    = os.path.join(config_path, 'wallpapers.log')

# removes first line of the log (current)
#  returns second line of the log, which is previous image
def unlog():
    with open(log_file, "r") as f:
        content = f.read().splitlines(True)
    with open(log_file, "w") as f:
        f.writelines(content[1:])
    return content[0]

# logs a line on top of logfile
def log(entry = "---------------------------------"):
    with open(log_file, "r+") as f:
        content = f.read()
        f.seek(0)
        f.write(entry + '\n' + content)

# not_seen(path)
# returns True if file not seen previously
# + creates log file if doesn't exist
def not_seen(config, path):
    if os.path.isfile(log_file):
        if path in open(log_file).read():
            return False
    else:
        log()
    return True

# get_config(config, setting)
# returns value of setting for a given config object
def get_config(config, setting):
    # read source folder from wallpapers.cfg
    config.read(config_file)
    return str((config.get('DEFAULT', setting))).lower()

# set_config(config, name, setting)
# sets value to setting for a given config object
def set_config(config, name, setting):
    config['DEFAULT'][name] = setting
    with open(config_file, 'w') as configfile:    
        config.write(configfile)

# set_wallpaper(config, new_wallpaper)
# setting new wallpaper to one at location new_wallpaper
# + update las seen in config
def set_wallpaper(config, new_wallpaper):
    if os.path.isfile(new_wallpaper):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, new_wallpaper , 0)
        # update config file with the location of current wallpaper
        if get_config(config, 'last') != new_wallpaper:
            log(new_wallpaper)
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
        while True:
            new_wallpaper = os.path.join(wallpaper_location, random.choice(backgrounds))
            if not_seen(config, new_wallpaper) and os.stat(new_wallpaper).st_size>0:
                set_wallpaper(config, new_wallpaper)
                return

# previous_wallpaper()
# set a wallpaper to one before
def previous_wallpaper(config):
    unlog()
    set_wallpaper(config, unlog())

# delete_wallpaper():
# get current background path from _ini_ and delete
# + manually call next_wallpaper()
def delete_wallpaper(config):
    wallpaper_location = get_config(config, 'last')
    if os.path.isfile(wallpaper_location):
        send2trash(wallpaper_location)
        unlog()
        next_wallpaper(config)

# set_path():
# update wallpapers folder in _ini_
# + manually call next_wallpaper() 
def set_folder(config, new_path):
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
        if not os.path.isfile(get_config(config, 'last')):
            set_config(config, 'last', '')
        if not os.path.isfile(get_config(config, 'safe')):
            set_config(config, 'safe', '')            

# load_safe(config)
# loads "safe" wallpaper specified in config
def load_safe(config):
    set_wallpaper(config, get_config(config, 'safe'))

# flips image either horizontally or vertically
def flip(config, axis):
    last = get_config(config, 'last')
    if os.path.isfile(last):
        current_image = Image.open(last)
        new_image = current_image.transpose(method=axis)
        send2trash(last)
        new_image.save(last)
        set_wallpaper(config, last)

# run_main()
# where the magic happens
def run_main():
    config = configparser.ConfigParser()
    check_config(config)
    # Initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-D", "--delete", action="store_true")
    parser.add_argument("-S", "--safe", action="store_true")             
    parser.add_argument("-F", "--folder", type=str)
    parser.add_argument("-H", "--hor", action="store_true")
    parser.add_argument("-V", "--ver", action="store_true")
    parser.add_argument("-P", "--previous", action="store_true")
    # Read arguments from the command line
    args = parser.parse_args()
    if args.delete:
        delete_wallpaper(config)
    elif args.folder:
        set_folder(config, args.folder)
    elif args.safe:
        load_safe(config)
    elif args.previous:
        previous_wallpaper(config)
    elif args.hor:
        flip(config, Image.FLIP_LEFT_RIGHT)
    elif args.ver:
        flip(config, Image.FLIP_TOP_BOTTOM)
    else:
        next_wallpaper(config)

##########################################################################################
if __name__ == "__main__":
    run_main()
##########################################################################################