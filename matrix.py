from PIL import Image, ImageDraw
import os, sys
import numpy
import _matrix
from matplotlib import cm
import argparse
import logging
import uuid
from random import SystemRandom

def get_options():
    parser = argparse.ArgumentParser(description='Visual cryptography.')
    parser.add_argument('--message', '-m',  required = True, metavar = "MESSAGE_IMAGE_FILE_PATH", help='message image')
    parser.add_argument('--secret',  '-s',  metavar = "SECRET_IMAGE_FILE_PATH",    default = "secret",   help='secret image (will be created if it does not exist)')
    parser.add_argument('--ciphered', '-c', metavar = "CIPHERED_IMAGE_FILE_PATH", default = "ciphered", help='ciphered image (to be generated)')
    parser.add_argument('--resize',  '-r', metavar = "WIDTH,HEIGHT", help='resize message image (defaults to message image size)')
    parser.add_argument('--prepared_message', '-p',  metavar = "PREPARED_MESSAGE_IMAGE_FILE_PATH",  help='if present, the prepared message image is saved to this path')
    parser.add_argument('--display', '-d', action='store_true')
    parser.add_argument('--format', '-f', metavar = "OUTPUT FORMAT (JPEG or PNG)", default = 'PNG', help='output format')
    args = parser.parse_args()
    if args.resize:
        try:
            width, height = [int(i.strip()) for i in args.resize.strip().split(",")]
            args.resize = (width, height)
        except:
            parser.error("Invalid format for resize option.")
        else:
            if width <= 0:
                parser.error("Resize width should be > 0.")
            if height <= 0:
                parser.error("Resize height should be > 0.")
    return args

def save_display(s,c,m,f):
    img = Image.open(s)
    background = Image.open(c)
    background.paste(img, (0, 0), img)
    background.save(m,f)

logging.basicConfig(level=logging.INFO)
args = get_options()

infile = args.message
if not os.path.isfile(infile):
	print("That file does not exist.")
	exit()

# try to open image file
try:
    img = Image.open(infile)
except IOError as e:
    logging.fatal("Fatal error: I/O error while loading message image '%s' (%s)" % (args.message, str(e)))
    sys.exit(1)

#f, e = os.path.splitext(infile)
uuid = uuid.uuid1()
logging.info('UUID: %s' % (uuid))
if args.resize:
    img = img.resize(args.resize, Image.ANTIALIAS)
img=img.convert('1')#convert image to 1 bit
pix = numpy.array(img)
_m1 = _matrix.Matrix(pix)

# prepare two empty matrix
width=img.size[0]*2
height=img.size[1]*2
out_image_A = Image.new('1', (width, height))
out_image_B = Image.new('1', (width, height))
a = numpy.array(out_image_A)
b = numpy.array(out_image_B)
_m2 = _matrix.Matrix(a)
_m3 = _matrix.Matrix(b)

f = args.format.lower()
if not f == 'jpeg' and not f == 'png':
    logging.fatal("Not support format type: '%s' , only supprt jpeg or png" % (f))
    sys.exit(1)
s = args.secret+'.'+f
c = args.ciphered+'.'+f

if args.prepared_message:
    _m2 = _matrix.Matrix(numpy.array(Image.open(args.prepared_message).convert('1')))
    res = _matrix.generate_cipher(_m1,_m2,_m3,int(width/2),int(height/2))
    d = numpy.asarray(_matrix.to_matrix(res))
    ttt = Image.fromarray(d)
    ttt.save(c, f.upper())
else:
    res = _matrix.generate(_m1,_m2,_m3,int(width/2),int(height/2))
    d = numpy.asarray(_matrix.to_matrix(res[0]))
    ttt = Image.fromarray(d)
    ttt.save(s, f.upper())
    d = numpy.asarray(_matrix.to_matrix(res[1]))
    ttt = Image.fromarray(d)
    ttt.save(c, f.upper())

if args.display:
    save_display(s, c, str(uuid)+"_vlidation."+f, f.upper())
print("Done.")
