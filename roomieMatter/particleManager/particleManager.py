"""RoomieButton Manager."""
import os
import logging
import sys
import json
import time
import socket
from threading import Thread
import click
# import mapreduce.utils as ut
# import mapreduce.manager.heartbeat_dict as hb

# Configure logging
LOGGER = logging.getLogger(__name__)

class Manager:

    def __init__(self, host, port):
        """Construct a Manager and start listening for messages."""
        self.host = host
        self.port = int(port)

        self.buttons = {}   # {<host>:<port> : state}

        LOGGER.info("Manager started")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mng_sock:
            mng_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            mng_sock.bind((self.host, self.port))
            mng_sock.listen()
            while True:
                LOGGER.info("Manager listening for connections...")
                conn = mng_sock.accept()[0]
                LOGGER.info("Connection accepted from %s", conn.getpeername())
                self.run_tcp(conn)


    def run_tcp(self, conn: socket.socket):
        """Listens for messages."""
        with conn:
            while True:
                data = conn.recv(4096)
                if not data:    # Connection closed
                    break
                LOGGER.info(f"Heard something on {self.port}")
                LOGGER.info(f"Data received: {data}")
                try:
                    self.handle_message(
                        json.loads(data.decode("utf-8"))
                    )
                except json.JSONDecodeError:
                    continue


    def handle_message(self, msg):
        """Handle a message from a device."""
        LOGGER.info(f"Valid JSON: {msg}")



@click.command()
@click.option("--host", "host", default="localhost")
@click.option("--port", "port", default=6000)
@click.option("--logfile", "logfile", default=None)
@click.option("--loglevel", "loglevel", default="info")
def main(host, port, logfile, loglevel):
    """Run Manager."""
    formatter = logging.Formatter(
        f"Manager {host}:{port} [%(levelname)s] %(message)s"
    )
    if logfile:
        handler = logging.FileHandler(logfile)
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(loglevel.upper())
    Manager(host, port)


if __name__ == "__main__":
    main()
