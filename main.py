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
from docopt import docopt
import os
import signal
import subprocess
from config import VENV, PATH


def start_program(program_file):
    try:
        # Start the program as a subprocess
        proc = subprocess.Popen([f"{PATH}/{program_file}"])
        print(f"Started {program_file} with PID {proc.pid}")
    except Exception as e:
        print(f"Failed to start {program_file}: {e}")


def stop_program(pid):
    try:
        # Send a termination signal to the process with the given PID
        os.kill(pid, signal.SIGTERM)
        print(f"Stopped process with PID {pid}")
    except Exception as e:
        print(f"Failed to stop process with PID {pid}: {e}")


if __name__ == '__main__':
    arguments = docopt(__doc__, version='AP Control')
    if arguments['list']:
        pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
        for pid in pids:
            cmd = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read().decode('utf-8')
            for cm in cmd:
                if cm in ['gps.py', 'imu.py', 'zmq.py']:
                    print(pid, cm)

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
        for pid in pids:
            try:
                cmd = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read().decode('utf-8')

                if program_file in cmd:
                    stop_program(int(pid))
            except IOError:  # proc has already terminated
                continue
