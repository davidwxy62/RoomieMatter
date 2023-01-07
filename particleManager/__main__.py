"""RoomieButton Manager."""
"""INSECURE: This is a proof of concept. Do not use in production."""
import logging
import json
import socket
import threading
from particleManager import config
from particleManager import db

# Configure logging
LOGGER = logging.getLogger(__name__)

class Manager:

    def __init__(self, host, port):
        """Construct a Manager and start listening for messages."""
        self.host = host
        self.port = int(port)

        self.buttons = {}   # { username : host }

        LOGGER.info("Manager started")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mng_sock:
            mng_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            mng_sock.bind((self.host, self.port))
            mng_sock.listen()
            while True:
                conn = mng_sock.accept()[0]
                self.run_tcp(conn)


    def run_tcp(self, conn: socket.socket):
        """Listens for messages."""
        with conn:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                try:
                    self.handle_message(
                        json.loads(data.decode("utf-8")),
                        conn.getpeername()[0]
                    )
                except json.JSONDecodeError:
                    LOGGER.info("Data from %s caused JSONDecodeError", conn.getpeername())
                    LOGGER.info("Data: %s", data)
                    continue
                except KeyError:
                    LOGGER.info("Data from %s caused KeyError", conn.getpeername())
                    LOGGER.info("Data: %s", data)
                    continue
                except UnicodeDecodeError:
                    LOGGER.info("Data from %s caused UnicodeDecodeError", conn.getpeername())
                    LOGGER.info("Data: %s", data)
                    continue


    def handle_message(self, msg, host):
        """Handle a message from a device."""
        if msg["event"] == "register_device":
            ack = {}
            if db.username_pwd_match_db(msg["username"], msg["password"]):
                self.buttons[msg["username"]] = host
                LOGGER.info("Successfully registered %s:%s", host, msg["username"])
                ack['status'] = 'success'
            else:
                LOGGER.info("Invalid credentials from %s", host)
                ack['status'] = 'error'
            threading.Thread(target=self.send_message, args=(ack, host)).start()

        elif msg["event"] == "particle_status_change":
            ack = {}
            if not db.username_pwd_match_db(msg["username"], msg["password"]):
                LOGGER.info("Invalid credentials from %s", host)
                ack['status'] = 'error'
                threading.Thread(target=self.send_message, args=(ack, host)).start()
                return
            if msg["username"] not in self.buttons:
                self.buttons[msg["username"]] = host
                LOGGER.info("Registered %s", host)
            if msg["new_status"] != db.get_status_db(msg["username"]):
                db.change_status_db(msg["username"])
                LOGGER.info("%s is now %s", msg["username"], msg["new_status"])
            ack['status'] = 'success'
            threading.Thread(target=self.send_message, args=(ack, host)).start()

        elif msg["event"] == "server_status_change":
            if not db.username_hashed_pwd_match_db(msg["username"], msg["hashed_password"]):
                LOGGER.info("Invalid credentials from %s", host)
                return
            if msg["username"] not in self.buttons:
                LOGGER.info("Unregistered device %s", host)
                return
            notice = {
                "event": "server_status_change",
                "username": msg["username"],
                "new_status": msg["new_status"]
            }
            LOGGER.info("Sending notice to %s", self.buttons[msg["username"]])
            threading.Thread(target=self.send_message, args=(notice, self.buttons[msg["username"]])).start()

        else:
            LOGGER.info("Invalid message from %s", host)
            LOGGER.info(msg)

            
            
    def send_message(self, msg, host):
        """Send a message to a device."""
        with socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            ) as outbound_sock:
                outbound_sock.settimeout(1)
                try:
                    outbound_sock.connect((host, 27))
                    outbound_sock.sendall(
                        json.dumps(msg).encode("utf-8")
                    )
                except ConnectionRefusedError:
                    return
                except socket.timeout:
                    return


def main():
    """Run Manager."""
    host = config.SERVER_HOST
    port = config.SERVER_PORT
    logfile = config.LOG_FILE
    loglevel = config.LOG_LEVEL
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


