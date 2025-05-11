
import asyncio

connected_clients = {}
clients_lock = asyncio.Lock()
