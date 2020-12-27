from PIL import Image, ImageDraw
import os, sys
import numpy
from matplotlib import cm
import argparse


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

