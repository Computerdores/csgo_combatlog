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
        #if len(payload.keys()) > 0:
        #    print(f"bomb: {self.server.gamestate_manager._bomb}")
        
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
        if "match_stats" in player_data:
            if "kills" in player_data["match_stats"]:
                gamestate_manager.player.match_stats.apply_kills(player_data["match_stats"]["kills"])
            if "assists" in player_data["match_stats"]:
                gamestate_manager.player.match_stats.apply_assists(player_data["match_stats"]["assists"])
            if "deaths" in player_data["match_stats"]:
                gamestate_manager.player.match_stats.apply_deaths(player_data["match_stats"]["deaths"])
            if "mvps" in player_data["match_stats"]:
                gamestate_manager.player.match_stats.apply_mvps(player_data["match_stats"]["mvps"])
            if "score" in player_data["match_stats"]:
                gamestate_manager.player.match_stats.apply_score(player_data["match_stats"]["score"])


        if "state" in player_data:
            if "health" in player_data["state"]:
                gamestate_manager.player.player_state.apply_health(player_data["state"]["health"])
            if "armor" in player_data["state"]:
                gamestate_manager.player.player_state.apply_armor(player_data["state"]["armor"])
            if "helmet" in player_data["state"]:
                gamestate_manager.player.player_state.apply_helmet(player_data["state"]["helmet"])

            if "defusekit" in player_data["state"]:
                gamestate_manager.player.player_state.apply_defusekit(player_data["state"]["defusekit"])
            else:
                gamestate_manager.player.player_state.apply_defusekit(False)

            if "flashed" in player_data["state"]:
                gamestate_manager.player.player_state.apply_flashed(player_data["state"]["flashed"])
            if "smoked" in player_data["state"]:
                gamestate_manager.player.player_state.apply_smoked(player_data["state"]["smoked"])
            if "burning" in player_data["state"]:
                gamestate_manager.player.player_state.apply_burning(player_data["state"]["burning"])
            if "money" in player_data["state"]:
                gamestate_manager.player.player_state.apply_money(player_data["state"]["money"])
            if "round_kills" in player_data["state"]:
                gamestate_manager.player.player_state.apply_round_kills(player_data["state"]["round_kills"])
            if "round_killhs" in player_data["state"]:
                gamestate_manager.player.player_state.apply_round_killhs(player_data["state"]["round_killhs"])
            if "equip_value" in player_data["state"]:
                gamestate_manager.player.player_state.apply_equip_value(player_data["state"]["equip_value"])


        if "weapons" in player_data:
            for k in player_data["weapons"].keys():
                w = gamestate_manager.player.get_weapon(k)
                w_data = player_data["weapons"][k]

                if "name" in w_data:
                    w.apply_name(w_data["name"])
                else:
                    w.apply_name(None)
                
                if "paintkit" in w_data:
                    w.apply_paintkit(w_data["paintkit"])
                else:
                    w.apply_paintkit(None)
                
                if "type" in w_data:
                    w.apply_type(w_data["type"])
                else:
                    w.apply_type(None)
                
                if "ammo_clip" in w_data:
                    w.apply_ammo_clip(w_data["ammo_clip"])
                else:
                    w.apply_ammo_clip(None)
                
                if "ammo_clip_max" in w_data:
                    w.apply_ammo_clip_max(w_data["ammo_clip_max"])
                else:
                    w.apply_ammo_clip_max(None)
                
                if "ammo_reserve" in w_data:
                    w.apply_ammo_reserve(w_data["ammo_reserve"])
                else:
                    w.apply_ammo_reserve(None)
                
                if "state" in w_data:
                    w.apply_state(w_data["state"])
                else:
                    w.apply_state(None)
    
    def _apply_match_stats(self, match_data: dict, gamestate_manager: GameStateManager):
        pass

    def _apply_player_state(self, state_data: dict, gamestate_manager: GameStateManager):
        pass

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