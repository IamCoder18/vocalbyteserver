import json
import ssl
import uuid
import websockets
from client import Client


class Server:
    def __init__(self, vad_pipeline, asr_pipeline, host='localhost', port=8765, sampling_rate=16000, samples_width=2, certfile = None, keyfile = None):
        self.vad_pipeline = vad_pipeline
        self.asr_pipeline = asr_pipeline
        self.host = host
        self.port = port
        self.sampling_rate = sampling_rate
        self.samples_width = samples_width
        self.certfile = certfile
        self.keyfile = keyfile
        self.connected_clients = {}

    async def handle_audio(self, client, websocket):
        while True:
            message = await websocket.recv()

            if isinstance(message, bytes):
                client.append_audio_data(message)
            elif isinstance(message, str):
                config = json.loads(message)
                if config.get('type') == 'config':
                    client.update_language(config['language'])
                    continue
            else:
                print(f"Unexpected message type from {client.client_id}")

            client.process_audio(websocket, self.vad_pipeline, self.asr_pipeline)


    async def handle_websocket(self, websocket, path):
        client_id = str(uuid.uuid4())
        client = Client(client_id, self.sampling_rate, self.samples_width)
        self.connected_clients[client_id] = client

        print(f"Client {client_id} connected")

        try:
            await self.handle_audio(client, websocket)
        except websockets.ConnectionClosed as e:
            print(f"Connection with {client_id} closed: {e}")
        finally:
            del self.connected_clients[client_id]

    def start(self):
        # self.certfile = "./localhost.pem"
        # self.keyfile = "./localhost-key.pem"
        # if self.certfile:
        #     ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        #     ssl_context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        #     print(f"WebSocket server ready to accept secure connections on wss://{self.host}:{self.port}")
        #     return websockets.serve(self.handle_websocket, self.host, self.port, ssl=ssl_context)
        # else:
        #     print(f"WebSocket server ready to accept unsecure connections on ws://{self.host}:{self.port}")
        #     return websockets.serve(self.handle_websocket, self.host, self.port)
        print(f"WebSocket server ready!")
        return websockets.serve(self.handle_websocket, self.host, self.port)