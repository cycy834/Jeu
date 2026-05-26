import asyncio
import threading

from src.Joaquim.network.client import NetworkClient


class NetworkRuntime:
    def __init__(self, uri, player_name, player_sprite=''):
        self.uri           = uri
        self.player_name   = player_name
        self.player_sprite = player_sprite
        self.loop   = None
        self.client = None
        self.thread = None

    def start(self):
        def runner():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

            self.client = NetworkClient(self.uri, self.player_name, self.player_sprite)

            async def setup():
                try:
                    await self.client.connect_to_server()
                    self.loop.create_task(self.client.receive_loop())
                except Exception:
                    pass

            self.loop.run_until_complete(setup())
            self.loop.run_forever()

        self.thread = threading.Thread(target=runner, daemon=True)
        self.thread.start()

    def send_position(self, x, y, room):
        if self.loop and self.client and self.client.connected:
            asyncio.run_coroutine_threadsafe(
                self.client.send_position(x, y, room),
                self.loop
            )

    def send_puzzle_solved(self, puzzle_id, digit_index, digit):
        if self.loop and self.client and self.client.connected:
            asyncio.run_coroutine_threadsafe(
                self.client.send_puzzle_solved(puzzle_id, digit_index, digit),
                self.loop
            )

    def send_player_caught(self, reason="Attrapé par une IA"):
        if self.loop and self.client and self.client.connected:
            asyncio.run_coroutine_threadsafe(
                self.client.send_player_caught(reason),
                self.loop
            )

    def send_team_lose_life(self, caught_player_id):
        if self.loop and self.client and self.client.connected:
            asyncio.run_coroutine_threadsafe(
                self.client.send_team_lose_life(caught_player_id),
                self.loop
            )
