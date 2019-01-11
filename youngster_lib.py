import re
import os


class Reader:

    @staticmethod
    def extract_dir_logs(dir_path):
        logs = []
        for file in os.listdir(dir_path):
            file_absolute_path = dir_path + file
            arq = open(file_absolute_path, 'r+', encoding="utf-8")
            file_content = arq.read()
            arq.close()
            m = re.search('<script type="text/plain" class="battle-log-data">.*?</script>', file_content, re.DOTALL)
            logs.append(m.group(0))
        return logs

    def get_current_action(self, log_line, battle):
        line_info = log_line.split('|')
        if re.match(r'\|turn\|', log_line):
            battle.current_turn = line_info[2]
        elif re.match(r'\|switch\|p1', log_line):
            battle.p1_switch(line_info[3])
        elif re.match(r'\|switch\|p2', log_line):
            battle.p2_switch(line_info[3])
        elif re.match(r'\|move\|p1', log_line):
            battle.p1_move(line_info[3])
        elif re.match(r'\|move\|p2', log_line):
            battle.p2_move(line_info[3])
        elif re.match(r'\|faint\|p1', log_line):
            battle.faint_flag_p1 = True
        elif re.match(r'\|faint\|p2', log_line):
            battle.faint_flag_p2 = True
        elif re.match(r'\|poke\|p1', log_line):
            battle.assign_poke(1, line_info[3])
        elif re.match(r'\|poke\|p2', log_line):
            battle.assign_poke(2, line_info[3])

        # PLAYER 1 STATUS AND STATUS HEALS

        elif re.match(r'\|-status\|p1', log_line):    # status infliction
            battle.change_status(line_info[3], 'p1')
            print(line_info[3])
        elif re.match(r'\|-heal\|p1', log_line):    # attack boost
            pass

        # PLAYER 2 STATUS AND STATUS HEALS

        elif re.match(r'\|-status\|p2', log_line):    # attack boost
            battle.change_status(line_info[3], 'p2')
        elif re.match(r'\|-heal\|p1.*', log_line):
            pass

        # PLAYER 1 BOOSTS
        elif re.match(r'\|-boost\|p1.*\|atk\|', log_line):    # attack boost
            battle.p1_boosts.boost('attack', int(line_info[4]))
        elif re.match(r'\|-unboost\|p1.*\|atk\|', log_line):  # attack unboost
            battle.p1_boosts.unboost('attack', int(line_info[4]))
        elif re.match(r'\|-boost\|p1.*\|def\|', log_line):    # defense boost
            battle.p1_boosts.boost('defense', int(line_info[4]))
        elif re.match(r'\|-unboost\|p1.*\|def\|', log_line):  # defense unboost
            battle.p1_boosts.unboost('defense', int(line_info[4]))
        elif re.match(r'\|-boost\|p1.*\|spa\|', log_line):    # special attack boost
            battle.p1_boosts.boost('specialAttack', int(line_info[4]))
        elif re.match(r'\|-unboost\|p1.*\|spa\|', log_line):  # special attack unboost
            battle.p1_boosts.unboost('specialAttack', int(line_info[4]))
        elif re.match(r'\|-boost\|p1.*\|spd\|', log_line):    # special defense boost
            battle.p1_boosts.boost('specialDefense', int(line_info[4]))
        elif re.match(r'\|-unboost\|p1.*\|spd\|', log_line):  # special defense unboost
            battle.p1_boosts.unboost('specialDefense', int(line_info[4]))
        elif re.match(r'\|-boost\|p1.*\|spe\|', log_line):    # speed boost
            battle.p1_boosts.boost('speed', int(line_info[4]))
        elif re.match(r'\|-unboost\|p1.*\|spe\|', log_line):  # speed unboost
            battle.p1_boosts.unboost('speed', int(line_info[4]))

    # PLAYER 2 BOOSTS

        elif re.match(r'\|-boost\|p2.*\|atk\|', log_line):      # attack boost
            battle.p2_boosts.boost('attack', int(line_info[4]))
        elif re.match(r'\|-unboost\|p2.*\|atk\|', log_line):    # attack unboost
            battle.p2_boosts.unboost('attack', int(line_info[4]))
        elif re.match(r'\|-boost\|p2.*\|def\|', log_line):      # defense boost
            battle.p2_boosts.boost('defense', int(line_info[4]))
        elif re.match(r'\|-unboost\|p2.*\|def\|', log_line):    # defense unboost
            battle.p2_boosts.unboost('defense', int(line_info[4]))
        elif re.match(r'\|-boost\|p2.*\|spa\|', log_line):      # special attack boost
            battle.p2_boosts.boost('specialAttack', int(line_info[4]))
        elif re.match(r'\|-unboost\|p2.*\|spa\|', log_line):    # special attack unboost
            battle.p2_boosts.unboost('specialAttack', int(line_info[4]))
        elif re.match(r'\|-boost\|p2.*\|spd\|', log_line):      # special defense boost
            battle.p2_boosts.boost('specialDefense', int(line_info[4]))
        elif re.match(r'\|-unboost\|p2.*\|spd\|', log_line):    # special defense unboost
            battle.p2_boosts.unboost('specialDefense', int(line_info[4]))
        elif re.match(r'\|-boost\|p2.*\|spe\|', log_line):      # speed boost
            battle.p2_boosts.boost('speed', int(line_info[4]))
        elif re.match(r'\|-unboost\|p2.*\|spe\|', log_line):    # speed unboost
            battle.p2_boosts.unboost('speed', int(line_info[4]))


class Writer:

    def record_battle(self, battle_log, db_file_path):

        battle = Battle()
        reader = Reader()
        db_arq = open(db_file_path, 'a+', encoding="utf-8")

        for line in battle_log:
            reader.get_current_action(line, battle)

        db_arq.write(battle.battle_buffer)


class Battle:
    def __init__(self):

        # core attributes of the battle snapshot

        self.pokemon_one = ''
        self.pokemon_two = ''
        self.p1_action = ''
        self.p2_action = ''
        self.current_turn = ''
        self.description = ''
        self.battle_buffer = ''
        self.p1_team = []
        self.p2_team = []

        # shifting flags

        self.faint_flag_p1 = False
        self.faint_flag_p2 = False
        self.u_turn_flag_p1 = False
        self.u_turn_flag_p2 = False

        # stats (boosts and unboosts)

        self.p1_boosts = StatsBoost()
        self.p2_boosts = StatsBoost()

        # status

        self.p1_status = 'none'
        self.p2_status = 'none'

    def assign_poke(self, player, poke):
        self.p1_team.append(poke) if player == 1 else self.p2_team.append(poke)

    def p1_switch(self, pokemon):

        if self.pokemon_one == '':
            self.p1_action = 'lead_switch'
        elif self.current_turn and self.faint_flag_p1 is True:
            self.p1_action = 'faint_switch'
            self.faint_flag_p1 = False
        elif self.u_turn_flag_p1 is True:
            self.p1_action = 'move_switch'
        else:
            self.p1_action = 'switch'
        self.description = pokemon
        self.p1_boosts.clear_boosts()
        self.battle_buffer += self.return_p1_snapshot()
        self.pokemon_one = pokemon

    def p2_switch(self, pokemon):

        if self.pokemon_two == '':
            self.p2_action = 'lead_switch'
        elif self.current_turn and self.faint_flag_p2 is True:
            self.p2_action = 'faint_switch'
            self.faint_flag_p2 = False
        elif self.u_turn_flag_p2 is True:
            self.p2_action = 'move_switch'
        else:
            self.p2_action = 'switch'
        self.description = pokemon
        self.p2_boosts.clear_boosts()
        self.battle_buffer += self.return_p2_snapshot()
        self.pokemon_two = pokemon

    def p1_move(self, movement):
        self.p1_action = 'move'
        self.description = movement
        self.battle_buffer += self.return_p1_snapshot()
        self.u_turn_flag_p1 = True if movement == "U-turn" else False

    def p2_move(self, movement):
        self.p2_action = 'move'
        self.description = movement
        self.battle_buffer += self.return_p2_snapshot()
        self.u_turn_flag_p2 = True if movement == "U-turn" else False

    def return_p1_snapshot(self):
        return self.current_turn + '|p1|' + self.pokemon_one + '|' + self.pokemon_two + '|' + self.p1_action + '|' + self.description + \
                '|' + str(self.p1_boosts.attack) + \
                '|' + str(self.p1_boosts.defense) + \
                '|' + str(self.p1_boosts.specialAttack) + \
                '|' + str(self.p1_boosts.specialDefense) + \
                '|' + str(self.p1_boosts.speed) + \
                '|' + self.p1_status + '\n'

    def return_p2_snapshot(self):
        return self.current_turn + '|p2|' + self.pokemon_two + '|' + self.pokemon_one + '|' + self.p2_action + '|' + self.description + \
               '|' + str(self.p2_boosts.attack) + \
               '|' + str(self.p2_boosts.defense) + \
               '|' + str(self.p2_boosts.specialAttack) + \
               '|' + str(self.p2_boosts.specialDefense) + \
               '|' + str(self.p2_boosts.speed) + \
               '|' + self.p2_status + '\n'

    def change_status(self, status, player):
        if player == 'p1':
            self.p1_status = status
        else:
            self.p2_status = status


class StatsBoost:

    # Hp ain't boostable

    def __init__(self):
        self.attack = 0
        self.defense = 0
        self.specialAttack = 0
        self.specialDefense = 0
        self.speed = 0

    def clear_boosts(self):
        self.__dict__ = {attr: 0 for attr, value in self.__dict__.items()}

    def boost(self, stat, times):
        self.__dict__.update({stat: self.__dict__[stat] + times})

    def unboost(self, stat, times):
        self.__dict__.update({stat: self.__dict__[stat] - times})
