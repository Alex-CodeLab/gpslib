""" Control

Usage:
  main.py start [gps|imu|zmq]
  main.py stop [gps|imu|zmq]

  main.py (-h | --help)
  main.py --version

Options:
  -h --help     Show this screen.

"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='AP Control')
    print(arguments)
