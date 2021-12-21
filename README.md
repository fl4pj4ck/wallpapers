# wallpapers

Small Python3 utility to change Windows wallpapers.

Usage:

wallpapers.py [-P path] [-D]

- no parameter: next wallpaper from selected folder
- [-P path] provide new path from which a new wallpaper will be picked
- [-D] delete current wallpaper and display next

Configuration stored in wallpapers.ini:

    [DEFAULT]
    
    folder = X:\location_for_folder_containing_image files
    
    last = X:\location_for_folder_containing_image files\currently_displayed_wallpaper.png


Distributed under MIT Licencse.

Copyright 2021 https://github.com/fl4pj4ck

Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the 
"Software"), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish, 
distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to 
the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

