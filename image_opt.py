import Image, ImageFile
import os, argparse

ImageFile.MAXBLOCK = 2**20

parser = argparse.ArgumentParser(description="Test")
parser.add_argument('directory', type=str, help='directory to use')
parser.add_argument('-q', '--quality', help='zip quality', type=int, default=85)
args = parser.parse_args()

if os.path.isdir(args.directory) and os.access(args.directory, os.R_OK):
    DIRECTORY = args.directory

else:
    raise Exception("{0} is not a readable dir".format(args.directory)) 


total_efficiency = 0

def size_format(size):
    return str(int(size) / 1000) + "Kb"

def efficiency_format(efficiency, type = 0):
    bold = '\033[1m' if type == 1 else ""        
    color = '\033[92m' if efficiency > 500 else '\033[91m'

    return color + bold + size_format(efficiency) + '\033[0m'        


def optimize_image(filename, filetype):
    global total_efficiency
    old_size = os.stat(filename).st_size
    image = Image.open(filename)          
    image.save(filename, optimize=True, quality=args.quality)
    new_size = os.stat(filename).st_size
    efficiency =  old_size - new_size
    total_efficiency += efficiency   
    if efficiency > 500 :
        color = '\033[92m'
    else:
        color = '\033[91m'        

    print """ %(file)s optimized from %(old_size)s to %(new_size)s, efficiency - """ % {'file': filename, 'old_size': size_format(old_size), 'new_size': size_format(new_size)} + efficiency_format(efficiency)
       


for root, subdirs, files in os.walk(DIRECTORY):
    for file in files:
        filetype = os.path.splitext(file)[1].lower()
        if filetype in ('.jpg', '.jpeg', '.png'):
            filename = os.path.join(root, file)
            optimize_image(filename, 1)

print "Total efficiency is " + efficiency_format(total_efficiency, 1) 
