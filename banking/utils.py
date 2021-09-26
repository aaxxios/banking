import logging
import os
import subprocess
import termcolor


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s  >>%(levelname)-8s<< %(message)s',
                    datefmt='%m-%d %H:%M')


def warn(msg):
    logging.warn(termcolor.colored(msg, 'yellow'))


def info(msg):
    logging.info(termcolor.colored(msg, 'green'))


def refresh():
    if os.name == 'nt':
        subprocess.call('cls', shell=True)
    else:
        subprocess.call('clear', shell=True)
