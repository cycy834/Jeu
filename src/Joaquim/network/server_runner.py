import asyncio
import socket
import threading

_thread = None
PORT = 8765


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'


def start():
    """Lance le serveur WebSocket dans un thread daemon. Appelable plusieurs fois (idempotent)."""
    global _thread

    from src.Joaquim.network import server as srv
    from src.Joaquim.network.shared_state import GameState

    # Toujours remettre l'état à zéro (nouvelle partie)
    srv.game_state = GameState()
    srv.connections = {}

    if _thread and _thread.is_alive():
        return

    def _run():
        asyncio.run(srv.main())

    _thread = threading.Thread(target=_run, daemon=True)
    _thread.start()


def is_running():
    return _thread is not None and _thread.is_alive()
