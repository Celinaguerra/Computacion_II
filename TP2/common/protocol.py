import asyncio
import socket
from .serialization import serialize, deserialize

async def async_send_msg(writer: asyncio.StreamWriter, data: dict):
    msg_bytes = serialize(data)
    msg_len = len(msg_bytes)
    
    # Enviar 4 bytes de longitud
    writer.write(msg_len.to_bytes(4, 'big'))
    # Enviar payload
    writer.write(msg_bytes)
    await writer.drain()

async def async_recv_msg(reader: asyncio.StreamReader) -> dict:
    try:
        # Leer 4 bytes de longitud
        len_bytes = await reader.readexactly(4)
        msg_len = int.from_bytes(len_bytes, 'big')
        
        # Leer payload
        data_bytes = await reader.readexactly(msg_len)
        return deserialize(data_bytes)
    except asyncio.IncompleteReadError:
        print("Error de protocolo: Conexión cerrada inesperadamente por el peer.")
        return {"error": "Conexión cerrada abruptamente"}


def sync_send_msg(sock: socket.socket, data: dict):
    msg_bytes = serialize(data)
    msg_len = len(msg_bytes)
    
    # Enviar 4 bytes de longitud + payload
    sock.sendall(msg_len.to_bytes(4, 'big') + msg_bytes)

def _recv_all(sock: socket.socket, n: int) -> bytes:
    chunks = []
    bytes_recd = 0
    while bytes_recd < n:
        chunk = sock.recv(min(n - bytes_recd, 4096))
        if chunk == b'':
            raise ConnectionError("Socket cerrado antes de recibir todos los datos")
        chunks.append(chunk)
        bytes_recd += len(chunk)
    return b''.join(chunks)

def sync_recv_msg(sock: socket.socket) -> dict:
    try:
        # Leer 4 bytes de longitud
        len_bytes = _recv_all(sock, 4)
        msg_len = int.from_bytes(len_bytes, 'big')
        
        # Leer payload
        data_bytes = _recv_all(sock, msg_len)
        return deserialize(data_bytes)
    except ConnectionError:
        print("Error de protocolo: Conexión cerrada inesperadamente por el peer.")
        return {"error": "Conexión cerrada abruptamente"}