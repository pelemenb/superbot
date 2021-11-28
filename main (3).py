import vk_api
import time
from vk_api.longpoll import VkLongPoll, VkEventType

from cities import Cities

vk_session = vk_api.VkApi(token="981e658682601cf8f30bcaa1f3b78f6e024526e60b801788320322792091173160c7f718df09796632ecb)
longpoll = VkLongPoll(vk_session)


correct_cities = ['Новосибирск', 'Красноярск', 'Курск', 'Кемерово', 'Оренбунг', 'Гамбург']
players_in_game = []
active_games = []


def send_message(id, message):
    vk_session.method("messages.send", {"user_id": id,
                                        "message": message,
                                        "random_id": 0})


def is_message(event):
    return event.type == VkEventType.MESSAGE_NEW and event.to_me


def is_play_game(event):
    game_command = ['начали', "let's go", 'города']
    return event.text.lower() in game_command


 def kill_game(game):
     user_ids = game.user_ids
     active_games.pop(active_games.index(game))
     players_in_game.remove(user_ids[0])
     players_in_game.remove(user_ids[1])


def is_player_step(self, user_id):
    return user_id == self.user_ids[self.current_step]


def main():
    user_in_queue = None
    for event in longpoll.listen():
        if is_message(event):
            if is_play_game(event):
                if user_in_queue is None:
                    send_message(event.user_id, 'Вы встали в очередь на игру в города!')
                    user_in_queue = event.user_id
                elif event.user_id != user_in_queue:
                    send_message(user_in_queue, 'Мы нашли вам оппонента')
                    send_message(event.user_id, 'Оппонент уже ожидает вас!')
                    active_games.append(Cities(user_in_queue, event.user_id))
                    players_in_game.append(user_in_queue)
                    players_in_game.append(event.user_id)
                    first_user = active_games[-1].user_ids[active_games[-1].current_step]
                    send_message(first_user, 'Вы ходите первый! Назовите город на любую букву.')
                    user_in_queue = None
            elif event.user_id in players_in_game:
                bad = False
                igra = ''
                for game in active_games:
                    if event.user_id in game.user_ids:
                        if game.user_ids.index(event.user_id) != game.current_step:
                            bad = True
                            break
                        else:
                            igra = game
                if bad:
                    send_message(event.user_id, 'Сейчас не ваш ход!')
                    continue
                if not igra.is_correct_first_char(event.text[0].upper()):
                    send_message(event.user_id, 'Вы назвали город не на ту букву и проиграли! Игра окончена!')
                    send_message(igra.user_ids[1 - igra.current_step], 'Вы победили!')
                    kill_game(igra)
                city = event.text
                user1 = igra.user_ids[0]
                user2 = igra.user_ids[1]
                if user != event.user_id:
                    user1, user2 = user2 , user1
                if not igra.is_unused_city(city):
                    send_message(user1, 'Ты проиграл потуму что назвал город который уже был')
                    send_message(user2, 'Вы победили')
                    kill_game(igra)

                do_step(igra)
                send_message(user2, f'Твой ход ходи на букуву:{igra.last_char}.\n'
                                    f'был назван город:{igra.used_cities[-1]}')
def do_step(user_id, city):
    igra.current_step = 1 - igra.current_step
    igra.change_last_char(city)
    igra.used_cities.append(city.lower())


main()