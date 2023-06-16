""" Control

Usage:
  main.py list
  main.py start [gps|imu|zmq]
  main.py stop [gps|imu|zmq]

  main.py (-h | --help)
  main.py --version

Options:
  -h --help     Show this screen.

"""
import logging
import os
import signal
import subprocess

from docopt import docopt

from config import PATH
logging.basicConfig(filename='/var/log/gps_control.log', level=logging.INFO)


def start_program(prog_file):
    try:
        # Start the program as a subprocess
        with subprocess.Popen([f"{PATH}/{prog_file}"]) as proc:
            print(f"Started {prog_file} with PID {proc.pid}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start {prog_file}: {e}")
        logging.exception(e)

def stop_program(pid):
    try:
        # Send a termination signal to the process with the given PID
        os.kill(pid, signal.SIGTERM)
        print(f"Stopped process with PID {pid}")
    except ProcessLookupError as e:
        print(f"Failed to stop process with PID {pid}: {e}")


if __name__ == '__main__':
    arguments = docopt(__doc__, version='AP Control')
    program_file = None
    if arguments['list']:
        pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
        for pid_ in pids:
            with open(os.path.join('/proc', pid_, 'cmdline'), 'rb') as file:
                cmd = file.read().decode('utf-8')
                for cm in cmd:
                    if cm in {'gps.py', 'imu.py', 'zmq.py'}:
                        print(pid_, cm)

    if arguments['gps']:
        program_file = 'gps.py'
    if arguments['imu']:
        program_file = 'imu.py'
    if arguments['zmq']:
        program_file = 'zeromq.py'

    if arguments['start']:
        start_program(program_file)

    if arguments['stop']:
        pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
        for pid_ in pids:
            try:
                with open(os.path.join('/proc', pid_, 'cmdline'), 'rb') as file:
                    cmd = file.read().decode('utf-8')

                if program_file in cmd:
                    stop_program(int(pid_))
            except IOError:  # proc has already terminated
                continue
