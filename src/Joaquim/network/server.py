import asyncio
import json
import uuid
from websockets.asyncio.server import serve

from src.Joaquim.network.shared_state import GameState, PlayerState
from src.Joaquim.network.protocol import (
    JOIN,
    MOVE,
    PUZZLE_SOLVED,
    PLAYER_CAUGHT,
    TEAM_LOSE_LIFE,
    REQUEST_STATE,
    WELCOME,
    STATE,
    CODE_UPDATE,
    LEVEL_RESTART,
    LEVEL_COMPLETE,
)

game_state = GameState()
connections = {}


def serialize_state():
    return {
        "type": STATE,
        "players": {
    	    pid: {
        	"name":   p.name,
        	"x":      p.x,
        	"y":      p.y,
        	"room":   p.room,
        	"caught": p.caught,
        	"sprite": p.sprite,
    }
            for pid, p in game_state.players.items()
        },
        "level": {
            "level_id": game_state.level.level_id,
            "code_digits": game_state.level.code_digits,
            "solved_puzzles": list(game_state.level.solved_puzzles),
            "alert_triggered": game_state.level.alert_triggered,
            "level_failed": game_state.level.level_failed
        }
    }


async def broadcast(data):
    if not connections:
        return

    raw = json.dumps(data)
    dead = []

    for ws in list(connections.keys()):
        try:
            await ws.send(raw)
        except Exception:
            dead.append(ws)

    for ws in dead:
        pid = connections.pop(ws, None)
        if pid and pid in game_state.players:
            del game_state.players[pid]


async def broadcast_state():
    await broadcast(serialize_state())


def reset_current_level():
    game_state.level.code_digits = [None, None, None, None]
    game_state.level.solved_puzzles.clear()
    game_state.level.alert_triggered = False
    game_state.level.level_failed = False

    for player in game_state.players.values():
    	player.x = 100
    	player.y = 100
    	player.room = 1
    	player.caught = False


async def fail_level(reason, caught_player_id=None):
    game_state.level.alert_triggered = True
    game_state.level.level_failed = True

    await broadcast({
        "type": LEVEL_RESTART,
        "reason": reason,
        "caught_player_id": caught_player_id
    })

    reset_current_level()
    await broadcast_state()


async def handle_join(player_id, data):
    game_state.players[player_id].name   = data.get("name",   f"Player_{player_id}")
    game_state.players[player_id].sprite = data.get("sprite", "")


async def handle_move(player_id, data):
    player = game_state.players[player_id]
    player.x = int(data.get("x", player.x))
    player.y = int(data.get("y", player.y))
    player.room = int(data.get("room", player.room))


async def handle_puzzle_solved(player_id, data):
    puzzle_id = data["puzzle_id"]
    digit_index = int(data["digit_index"])
    digit_value = int(data["digit"])

    if puzzle_id in game_state.level.solved_puzzles:
        return

    game_state.level.solved_puzzles.add(puzzle_id)
    game_state.level.code_digits[digit_index] = digit_value

    await broadcast({
        "type": CODE_UPDATE,
        "puzzle_id": puzzle_id,
        "digit_index": digit_index,
        "digit": digit_value,
        "found_by": player_id
    })

    await broadcast_state()

    if all(d is not None for d in game_state.level.code_digits):
        await broadcast({
            "type": LEVEL_COMPLETE,
            "level_id": game_state.level.level_id,
            "final_code": game_state.level.code_digits
        })


async def handle_player_caught(player_id, data):
    if player_id in game_state.players:
        game_state.players[player_id].caught = True

    await fail_level(
        reason=data.get("reason", "Un voleur a été attrapé"),
        caught_player_id=player_id
    )


async def handler(websocket):
    player_id = str(uuid.uuid4())[:8]
    connections[websocket] = player_id
    game_state.players[player_id] = PlayerState(
        player_id=player_id,
        name=f"Player_{player_id}"
    )

    try:
        await websocket.send(json.dumps({
            "type": WELCOME,
            "player_id": player_id
        }))

        await broadcast_state()

        async for raw in websocket:
            data = json.loads(raw)
            msg_type = data.get("type")

            if msg_type == JOIN:
                await handle_join(player_id, data)

            elif msg_type == MOVE:
                await handle_move(player_id, data)

            elif msg_type == PUZZLE_SOLVED:
                await handle_puzzle_solved(player_id, data)

            elif msg_type == PLAYER_CAUGHT:
                await handle_player_caught(player_id, data)

            elif msg_type == TEAM_LOSE_LIFE:
                await broadcast(data)

            elif msg_type == REQUEST_STATE:
                await websocket.send(json.dumps(serialize_state()))

            await broadcast_state()

    except Exception as e:
        print("Erreur client :", e)

    finally:
        pid = connections.pop(websocket, None)
        if pid and pid in game_state.players:
            del game_state.players[pid]
        await broadcast_state()


async def main():
    async with serve(handler, "0.0.0.0", 8765):
        print("Serveur lancé sur ws://0.0.0.0:8765")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
