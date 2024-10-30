# telemetry/udp_listener.py

import socket
import json
import time
import logging

# Configure Logging
logging.basicConfig(
    filename='telemetry_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def start_udp_listener(host='0.0.0.0', port=20777):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    logging.info(f"UDP Listener started on {host}:{port}")
    print(f"UDP Listener started on {host}:{port}")

    try:
        while True:
            data, addr = sock.recvfrom(65535)  # Buffer size
            try:
                decoded_data = data.decode('utf-8')
                json_data = json.loads(decoded_data)
                logging.info(json.dumps(json_data))
                print(f"Received data from {addr}: {json_data}")
            except json.JSONDecodeError:
                logging.error(f"Failed to decode JSON from {addr}: {data}")
                print(f"Failed to decode JSON from {addr}")
    except KeyboardInterrupt:
        logging.info("UDP Listener stopped manually.")
        print("\nUDP Listener stopped.")
    finally:
        sock.close()

if __name__ == "__main__":
    start_udp_listener()