from os import listdir
from prompt_toolkit.shortcuts import input_dialog, message_dialog, radiolist_dialog
from prompt_toolkit.styles import Style

from main import menu
from personage import PersonagePlayer1, PersonagePlayer2
from utils import MovementValidator, HitValidator, RoundValidator, input_dialog_multiple_line, JsonValidator


class Game:
    def __init__(self):
        self.player1 = PersonagePlayer1()
        self.player2 = PersonagePlayer2()
        self.json_game = {"player1": {}, "player2": {}}
        self.start_game = True
        self.draw = 0
        self.winner = None
        self.history = ''

    def set_winner(self, player):
        self.winner = player
        example_style = Style.from_dict({
            'dialog': 'bg:#88ff88',
            'dialog frame.label': 'bg:#ffffff #000000',
            'dialog.body': 'bg:#000000 #00ff00',
            'dialog shadow': 'bg:#00aa00',
            })
        message_dialog(
            title='!Hay un Ganador!',
            text=f'¡Felicidades {player.name} has ganado! tienes {player.life} de vida restante.',
            ok_text='Continuar',
            style=example_style).run()

    def case_where_player1_will_attack_first(self, index):
        movements_player1 = self.json_game.get('player1')['movimientos'][index]
        hits_player1 = self.json_game.get('player1')['golpes'][index]
        damage, name_attack = self.player1.attack_combination(movements_player1, hits_player1)
        self.player2.life -= damage
        story = self.get_story(movements_player1, name_attack, damage)
        self.history += f'{self.player1.name} {story}\n'

        message_dialog(
            title='',
            text=f'{self.history}',
            ok_text='Continuar').run()
        if self.player2.life < 1:
            self.set_winner(self.player1)
        else:
            movements_player2 = self.json_game.get('player2')['movimientos'][index]
            hits_player2 = self.json_game.get('player2')['golpes'][index]
            damage, name_attack = self.player2.attack_combination(movements_player2, hits_player2)
            self.player1.life -= damage
            story = self.get_story(movements_player2, name_attack, damage)
            self.history += f'{self.player2.name} {story}\n'
            message_dialog(
                title='',
                text=f'{self.history}',
                ok_text='Continuar').run()
            if self.player1.life < 1:
                self.set_winner(self.player2)

    def case_where_player2_will_attack_first(self, index):
        movements_player2 = self.json_game.get('player2')['movimientos'][index]
        hits_player2 = self.json_game.get('player2')['golpes'][index]
        damage, name_attack = self.player2.attack_combination(movements_player2, hits_player2)
        self.player1.life -= damage
        story = self.get_story(movements_player2, name_attack, damage)
        self.history += f'{self.player2.name} {story}\n'
        message_dialog(
            title='',
            text=f'{self.history}',
            ok_text='Continuar').run()
        if self.player1.life < 1:
            self.set_winner(self.player2)
        else:
            movements_player1 = self.json_game.get('player1')['movimientos'][index]
            hits_player1 = self.json_game.get('player1')['golpes'][index]
            damage, name_attack = self.player1.attack_combination(movements_player1, hits_player1)
            self.player2.life -= damage
            story = self.get_story(movements_player1, name_attack, damage)
            self.history += f'{self.player1.name} {story}\n'

            message_dialog(
                title='',
                text=f'{self.history}',
                ok_text='Continuar').run()
            if self.player2.life < 1:
                self.set_winner(self.player1)

    def check_who_starts_first(self):
        player1_json = self.json_game.get('player1')
        player2_json = self.json_game.get('player2')
        if self.start_game:
            if player1_json.get('num_combinaciones') < player2_json.get('num_combinaciones'):
                return self.case_where_player1_will_attack_first
            else:
                return self.case_where_player2_will_attack_first
        if self.draw == 1:
            if player1_json.get('num_movimientos') < player2_json.get('num_movimientos'):
                return self.case_where_player1_will_attack_first
            else:
                return self.case_where_player2_will_attack_first
        if self.draw == 2:
            if player1_json.get('num_golpes') < player2_json.get('num_golpes'):
                return self.case_where_player1_will_attack_first
            else:
                return self.case_where_player2_will_attack_first
        if self.draw > 2:
            return self.case_where_player1_will_attack_first

    def input_player(self, num_round, num_player):
        data_json = {'movimientos': [], 'golpes': []}
        for i_round in range(1, int(num_round) + 1):
            print(f"Ronda: {i_round}:")
            movements = input_dialog(
                title=f'Turno de jugador {num_player}',
                text=f'Ingresa los movimientos para la ronda {i_round}:',
                password=False,
                validator=MovementValidator(), default='').run()
            if movements is None:
                movements = ''
            hits = input_dialog(
                title=f'Turno de jugador {num_player}',
                text=f'Ingresa el ataque para la ronda {i_round}:',
                password=False, validator=HitValidator(), default='').run()
            if hits is None:
                hits = ''
            data_json['movimientos'].append(movements.upper())

            data_json['golpes'].append(hits.upper())

        self.json_game[f'player{num_player}'] = data_json
        return data_json

    def battle(self):
        result = radiolist_dialog(
            title="Peleas guardadas",
            text="Seleccione una opción presionando Enter y luego presiones TAB y Enter",
            values=[
                ('create', 'Crear pelea'),
                ('simulation', 'Simular pelea guardada'),
                ('menu', 'Regresar al menú principal'),
                ]
            ).run()
        if result == 'create':
            self.battle_create()
        elif result == 'simulation':
            self.battle_simulation()
        elif result == 'menu':
            menu(False)
        else:
            self.battle()
        self.get_statistics()
        message_dialog(
            title='',
            text=f'¡Comienza el combate entre Jugador 1 {self.player1.name} y Jugador 2 {self.player2.name}!',
            ok_text='Continuar').run()
        num_round = len(self.json_game.get('player1').get('movimientos', []))

        while self.player1.life > 0 and self.player2.life > 0:

            function_game = self.check_who_starts_first()
            for n_round in range(0, int(num_round)):
                if not self.winner:
                    function_game(n_round)
                break
            self.start_game = False
            self.draw += 1

    def battle_simulation(self):
        import json
        list_options = [('json', 'Ingresar json')]
        files = listdir('data')
        for file in files:
            if file.endswith(".json"):
                list_options.append((f'data/{file}', file))

        result = radiolist_dialog(
            title="Peleas guardadas",
            text="Seleccione una opción presionando Enter y luego presiones TAB y Enter",
            values=list_options
            ).run()
        if result == 'json':
            text_json = self.get_json_text()
            json_game = json.loads(text_json)
        else:
            if result is None:
                self.battle()
            file = open(result, mode='r')
            json_game = json.load(file)
        self.json_game = json_game
        return json_game

    def battle_create(self):
        num_round = input_dialog(
            title='',
            text='Ingresa la cantidad de rondas a jugar',
            password=False,
            validator=RoundValidator()).run()
        if num_round is None:
            self.battle()
        self.input_player(num_round, 1)
        self.input_player(num_round, 2)

    def get_statistics(self):
        for key, value in self.json_game.items():
            self.json_game[key]['num_movimientos'] = 0
            self.json_game[key]['num_golpes'] = 0
            self.json_game[key]['num_combinaciones'] = 0
            player_json = self.json_game[key]
            list_movements = player_json.get('movimientos', [])
            list_hits = player_json.get('golpes', [])
            for index, movement in enumerate(list_movements):
                qty_movement = len(movement)
                # Hago una validacion por si en el json ingresan mas de 5
                if qty_movement > 5:
                    self.json_game[key]['movimientos'][index] = movement[0:5]
                    qty_movement = 5
                self.json_game[key]['num_movimientos'] += qty_movement

            for index, hit in enumerate(list_hits):
                qty_hit = len(hit)
                # Hago una validacion por si en el json ingresan mas de 1
                if qty_hit > 1:
                    self.json_game[key]['golpes'][index] = hit[0:1]
                    qty_hit = 1
                self.json_game[key]['num_golpes'] += qty_hit
            self.json_game[key]['num_combinaciones'] = self.json_game[key]['num_golpes'] + self.json_game[key][
                'num_movimientos']

    def get_story(self, movement, name_attack, damage=None):
        if len(name_attack) > 0:
            if damage > 1:
                return f'a usado el ataque especial {name_attack}, haciendo un daño al oponente de {damage}'
            else:
                if len(movement):
                    return f'se mueve y conecta con {name_attack}'
                return f"ha atacado con {name_attack}"
        else:
            if len(movement):
                return 'se mueve'
            else:
                return 'se queda quieto'

    def get_json_text(self):

        json_text = input_dialog_multiple_line(
            title=f'Json',
            text=f'Ingresa el texto del json y luego pulsa TAB y Enter',
            validator=JsonValidator()).run()
        return json_text
