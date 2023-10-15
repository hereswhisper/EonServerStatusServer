import asyncio
import websockets
import os
import time
import json
import ssl

DATA_FILE = 'server_status.txt'

async def read_file_and_send(ws, path):
    last_modification = 0
    while True:
        current_modification = os.path.getmtime(path)
        if current_modification != last_modification:
            with open(path, 'r') as file:
                content = json.load(file)
                print(f"Sending data: {json.dumps(content)}")  # Diagnostic print
                await ws.send(json.dumps(content))
                last_modification = current_modification
        await asyncio.sleep(1)

async def server(websocket, path):
    print("Client connected.")  # Diagnostic print
    await read_file_and_send(websocket, DATA_FILE)

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct paths to the certificate and private key
certificate_path = os.path.join(current_directory, 'certificate.pem')
private_key_path = os.path.join(current_directory, 'private.pem')

# SSL context setup
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certificate_path, private_key_path)

start_server = websockets.serve(server, "0.0.0.0", 443, ssl=ssl_context)

print("Secure WebSocket server started. Awaiting connections...")  # Initial print to show server has started
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
