class GameStateManager:
    def __init__(self):
        self.map = Map()
        self.player = Player()
        self._round_phase = ""
        self._bomb = None
    
    def apply_round_phase(self, phase: str):
        if self._round_phase != phase:
            self._round_phase = phase
    
    def apply_bomb(self, bomb_state: str):
        if self._bomb != bomb_state:
            self._bomb = bomb_state

class Team:
    def __init__(self):
        self._score = None
        self._name = None
        self._consecutive_losses = None
        self._remaining_timeouts = None
        self._matches_won = None
    
    def apply_score(self, score: int):
        if self._score != score:
            self._score = score
    
    def apply_name(self, name: str):
        if self._name != name:
            self._name = name
    
    def apply_consecutive_losses(self, losses: int):
        if self._consecutive_losses != losses:
            self._consecutive_losses = losses
    
    def apply_timeouts_remaining(self, timeouts: int):
        if self._remaining_timeouts != timeouts:
            self._remaining_timeouts = timeouts
    
    def apply_matches_won_this_series(self, wins: int):
        if self._matches_won != wins:
            self._matches_won = wins

class Map:
    def __init__(self):
        self._round_wins = []

        self._mode = None
        self._name = None
        self._phase = None
        self._round = None

        self.team_ct = Team()
        self.team_t  = Team()

        self._num_matches_to_win_series = -1
        self._current_spectators = -1
        self._souveniers_total = -1
    
    def apply_round_win(self, round: int, result: str):
        assert round >= 0

        if round >= len(self._round_wins):
            for _ in range(round - len(self._round_wins) + 1):
                self._round_wins.append(None)
        
        if self._round_wins[round] != result:
            self._round_wins[round] = result
        
    def apply_mode(self, mode: str):
        if self._mode != mode:
            self._mode = mode
    
    def apply_name(self, name: str):
        if self._name != name:
            self._name = name
    
    def apply_phase(self, phase: str):
        if self._phase != phase:
            self._phase = phase
    
    def apply_round(self, round: int):
        if self._round != round:
            self._round = round
    
    def apply_num_matches_to_win_series(self, num_matches: int):
        if self._num_matches_to_win_series != num_matches:
            self._num_matches_to_win_series = num_matches
    
    def apply_current_spectators(self, spectators: int):
        if self._current_spectators != spectators:
            self._current_spectators = spectators
    
    def apply_souveniers_total(self, souveniers: int):
        if self._souveniers_total != souveniers:
            self._souveniers_total = souveniers

class MatchStats:
    def __init__(self):
        self._kills = None
        self._assists = None
        self._deaths = None
        self._mvps = None
        self._score = None
    
    def apply_kills(self, kills: int):
        if self._kills != kills:
            self._kills = kills
    
    def apply_assists(self, assists: int):
        if self._assists != assists:
            self._assists = assists
    
    def apply_deaths(self, deaths: int):
        if self._deaths != deaths:
            self._deaths = deaths
    
    def apply_mvps(self, mvps: int):
        if self._mvps != mvps:
            self._mvps = mvps
    
    def apply_score(self, score: int):
        if self._score != score:
            self._score = score

class PlayerState:
    def __init__(self):
        self._health = None
        self._armor = None
        self._helmet = None
        self._defuse_kit = None
        self._flashed = None
        self._smoked = None
        self._burning = None
        self._money = None
        self._round_kills = None
        self._round_killhs = None
        self._equip_value = None
    
    def apply_health(self, health: int):
        if self._health != health:
            self._health = health
    
    def apply_armor(self, armor: int):
        if self._armor != armor:
            self._armor = armor
    
    def apply_helmet(self, helmet: bool):
        if self._helmet != helmet:
            self._helmet = helmet
    
    def apply_defuse_kit(self, defuse_kit: bool):
        if self._defuse_kit != defuse_kit:
            self._defuse_kit = defuse_kit
    
    def apply_flashed(self, flashed: int):
        if self._flashed != flashed:
            self._flashed = flashed
    
    def apply_smoked(self, smoked: int):
        if self._smoked != smoked:
            self._smoked = smoked
    
    def apply_burning(self, burning: int):
        if self._burning != burning:
            self._burning = burning
    
    def apply_money(self, money: int):
        if self._money != money:
            self._money = money
    
    def apply_round_kills(self, kills: int):
        if self._round_kills != kills:
            self._round_kills = kills
    
    def apply_round_killhs(self, killhs: int):
        if self._round_killhs != killhs:
            self._round_killhs = killhs
    
    def apply_equip_value(self, value: int):
        if self._equip_value != value:
            self._equip_value = value

class Weapon:
    def __init__(self):
        self._name = None
        self._paintkit = None
        self._type = None
        self._ammo_clip = None
        self._ammo_clip_max = None
        self._ammo_reserve = None
        self._state = None
    
    def apply_name(self, name: str):
        if self._name != name:
            self._name = name
    
    def apply_paintkit(self, paintkit: str):
        if self._paintkit != paintkit:
            self._paintkit = paintkit
    
    def apply_type(self, type: str):
        if self._type != type:
            self._type = type
    
    def apply_ammo_clip(self, ammo_clip: int):
        if self._ammo_clip != ammo_clip:
            self._ammo_clip = ammo_clip
    
    def apply_ammo_clip_max(self, ammo_clip_max: int):
        if self._ammo_clip_max != ammo_clip_max:
            self._ammo_clip_max = ammo_clip_max
    
    def apply_ammo_clip(self, ammo_reserve: int):
        if self._ammo_reserve != ammo_reserve:
            self._ammo_reserve = ammo_reserve
    
    def apply_state(self, state: str):
        if self._state != state:
            self._state = state

class Player:
    def __init__(self):
        self.match_stats = None
        self.player_state = None
        self._weapon_0 = None
        self._weapon_1 = None
        self._weapon_2 = None
        self._weapon_3 = None
        self._weapon_4 = None
        self._weapon_5 = None
        self._weapon_6 = None
        self._weapon_7 = None
        self._weapon_8 = None
    
    def get_weapon(self, weapon: str) -> Weapon:
        if weapon == "weapon_0":
            return self._weapon_0
        elif weapon == "weapon_1":
            return self._weapon_1
        elif weapon == "weapon_2":
            return self._weapon_2
        elif weapon == "weapon_3":
            return self._weapon_3
        elif weapon == "weapon_4":
            return self._weapon_4
        elif weapon == "weapon_5":
            return self._weapon_5
        elif weapon == "weapon_6":
            return self._weapon_6
        elif weapon == "weapon_7":
            return self._weapon_7
        elif weapon == "weapon_8":
            return self._weapon_8
        else:
            raise Exception(f"invalid weapon id: '{weapon}'")