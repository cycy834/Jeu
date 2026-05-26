import json
from websockets.asyncio.client import connect

from src.Joaquim.network.protocol import (
    JOIN,
    MOVE,
    PUZZLE_SOLVED,
    PLAYER_CAUGHT,
    TEAM_LOSE_LIFE,
    WELCOME,
    STATE,
    CODE_UPDATE,
    LEVEL_RESTART,
    LEVEL_COMPLETE,
)


class NetworkClient:
    def __init__(self, uri, player_name, player_sprite=''):
        self.uri = uri
        self.player_name   = player_name
        self.player_sprite = player_sprite
        self.websocket = None
        self.player_id = None
        self.connected = False

        self.players_state = {}
        self.level_state = {
            "level_id": "niveau_1",
            "code_digits": [None, None, None, None],
            "solved_puzzles": [],
            "alert_triggered": False,
            "level_failed": False,
        }

        self.last_event = None

    async def connect_to_server(self):
        self.websocket = await connect(self.uri)
        self.connected = True

        welcome = json.loads(await self.websocket.recv())
        if welcome["type"] == WELCOME:
            self.player_id = welcome["player_id"]

        await self.send({
            "type":   JOIN,
            "name":   self.player_name,
            "sprite": self.player_sprite,
        })

    async def send(self, data):
        if self.connected and self.websocket:
            await self.websocket.send(json.dumps(data))

    async def send_position(self, x, y, room):
        await self.send({
            "type": MOVE,
            "x": x,
            "y": y,
            "room": room
        })

    async def send_puzzle_solved(self, puzzle_id, digit_index, digit):
        await self.send({
            "type": PUZZLE_SOLVED,
            "puzzle_id": puzzle_id,
            "digit_index": digit_index,
            "digit": digit
        })

    async def send_player_caught(self, reason="Attrape par une IA"):
        await self.send({
            "type": PLAYER_CAUGHT,
            "reason": reason
        })

    async def send_team_lose_life(self, caught_player_id):
        await self.send({
            "type": TEAM_LOSE_LIFE,
            "caught_player_id": caught_player_id,
        })

    async def receive_loop(self):
        try:
            async for raw in self.websocket:
                data = json.loads(raw)
                msg_type = data.get("type")

                if msg_type == STATE:
                    self.players_state = data["players"]
                    self.level_state = data["level"]

                elif msg_type in (CODE_UPDATE, LEVEL_RESTART, LEVEL_COMPLETE):
                    self.last_event = data

                elif msg_type == TEAM_LOSE_LIFE:
                    if data.get('caught_player_id') != self.player_id:
                        self.last_event = data

        except Exception as e:
            print("Deconnecte du serveur :", e)
            self.connected = False
