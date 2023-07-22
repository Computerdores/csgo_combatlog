# reference: https://github.com/mdarvanaghi/CSGO-GSI/blob/master/gsi_server.py

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from GamestateManager import *

class GSIServer(HTTPServer):
    def __init__(self, server_address: tuple[str, int], RequestHandler: BaseHTTPRequestHandler, token: str = None):
        super().__init__(server_address, RequestHandler)
        self.token = token
        self.gamestate_manager = GameStateManager()

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')
        payload = json.loads(body)

        self.parse_payload(payload, self.server.gamestate_manager)
        if len(payload.keys()) > 0:
            print(f"bomb: {self.server.gamestate_manager._bomb}")
        
    def parse_payload(self, payload: dict, gamestate_manager: GameStateManager):
        if "round" in payload:
            if "phase" in payload["round"]:
                gamestate_manager.apply_round_phase(payload["round"]["phase"])
            if "bomb" in payload["round"]:
                gamestate_manager.apply_bomb(payload["round"]["bomb"])
            else:
                gamestate_manager.apply_bomb(None)

        if "map" in payload:
            self.parse_map(payload["map"], gamestate_manager)
        if "player" in payload:
            self.parse_player(payload["player"], gamestate_manager)
    
    def parse_map(self, map_data: dict, gamestate_manager: GameStateManager):
        if "round_wins" in map_data:
            for k in map_data["round_wins"].keys():
                gamestate_manager.map.apply_round_win(int(k), map_data["round_wins"][k])
        
        if "mode" in map_data:
            gamestate_manager.map.apply_mode(map_data["mode"])
        if "name" in map_data:
            gamestate_manager.map.apply_name(map_data["name"])
        if "phase" in map_data:
            gamestate_manager.map.apply_phase(map_data["phase"])
        if "round" in map_data:
            gamestate_manager.map.apply_round(map_data["round"])

        if "team_ct" in map_data:
            RequestHandler._apply_team(map_data["team_ct"], gamestate_manager.map.team_ct)
        if "team_t" in map_data:
            RequestHandler._apply_team(map_data["team_t"], gamestate_manager.map.team_t)

        if "num_matches_to_win_series" in map_data:
            gamestate_manager.map.apply_num_matches_to_win_series(map_data["num_matches_to_win_series"])
        if "current_spectators" in map_data:
            gamestate_manager.map.apply_current_spectators(map_data["current_spectators"])
        if "souvenirs_total" in map_data:
            gamestate_manager.map.apply_souveniers_total(map_data["souvenirs_total"])

    def parse_player(self, player_data: dict, gamestate_manager: GameStateManager):
        pass # TODO: parse everything

    def _apply_team(team_data: dict, team: Team):
        if "score" in team_data:
            team.apply_score(team_data["score"])
        if "name" in team_data:
            team.apply_name(team_data["name"])
        if "consecutive_round_losses" in team_data:
            team.apply_consecutive_losses(team_data["consecutive_round_losses"])
        if "timeouts_remaining" in team_data:
            team.apply_timeouts_remaining(team_data["timeouts_remaining"])
        if "matches_won_this_series" in team_data:
            team.apply_matches_won_this_series(team_data["matches_won_this_series"])


if __name__ == "__main__":
    server = GSIServer(("127.0.0.1", 5996), RequestHandler, "42069")
    server.serve_forever()
    server.server_close()