"""RoomieButton Manager."""
import os
import tempfile
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
        # self.heartbeat_dict = hb.Beatdict()

        # udp_thread = Thread(
        #     target=self.heartbeat_listen,
        #     daemon=True,
        #     name="mnger-heartbeat"
        # )
        # udp_thread.start()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mng_sock:
            mng_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            mng_sock.bind((self.host, self.port))
            mng_sock.listen()
            while True:
                conn = mng_sock.accept()[0]
                self.run_tcp(conn)
                time.sleep(0.1)

    def run_tcp(self, conn: socket.socket):
        """Listens for messages."""
        with conn:
            while True:
                data = conn.recv(4096)
                if not data:    # Connection closed
                    break
                try:
                    self.handle_message(
                        json.loads(data.decode("utf-8"))
                    )
                except json.JSONDecodeError:
                    continue

    # def heartbeat_listen(self):
    #     """Daemon thread listening for UDP heartbeat messages."""
    #     LOGGER.info("Starting heartbeat listener")
    #     with socket.socket(
    #         socket.AF_INET,
    #         socket.SOCK_DGRAM
    #     ) as rec_socket:
    #         rec_socket.setsockopt(
    #             socket.SOL_SOCKET,
    #             socket.SO_REUSEADDR,
    #             1
    #         )
    #         rec_socket.bind((self.host, self.port))
    #         rec_socket.settimeout(0.1)
    #         while True:
    #             try:
    #                 data = rec_socket.recv(4096)
    #             except socket.timeout:
    #                 continue
    #             # deal with data sent by worker
    #             try:
    #                 msg = json.loads(data.decode("utf-8"))
    #             except ValueError:
    #                 continue
    #             if data:
    #                 self.heartbeat_dict.update(
    #                     f"{msg['worker_host']}:{msg['worker_port']}"
    #                 )
    #             silent = self.heartbeat_dict.extract_silent(10)
    #             for worker in silent:
    #                 self.workers[worker] = "dead"
    #                 LOGGER.info("DEAD %s", worker)

    def handle_message(self, msg):
        """Handle a message from a device."""
        LOGGER.info("Received message: %s", msg)



@click.command()
@click.option("--host", "host", default="localhost")
@click.option("--port", "port", default=6000)
@click.option("--logfile", "logfile", default=None)
@click.option("--loglevel", "loglevel", default="info")
def main(host, port, logfile, loglevel, shared_dir):
    """Run Manager."""
    tempfile.tempdir = shared_dir
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
