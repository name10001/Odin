#!/usr/bin/env python3
from random import randint
import schedule
from time import time, sleep
from flask import *
from threading import Thread
from socket import gethostbyname, gethostname
import settings

import flask_server as fs
from waiting_room import WaitingRoom

games = {}
sessions = {}

@fs.app.route('/')
def index():
    return render_template("index.html", message=None, theme=settings.get_theme())


def make_unique_game_id():
    """
    generates an unique id for a game that consisting of 1 random numbers each 5 digit
    :return: The generated ID as a string
    """
    # generates an ID if its not unique, generate another
    game_id = '{:05d}'.format(randint(10000, 100000))
    while game_id in games:
        game_id = '{:05d}'.format(randint(10000, 100000))

    return game_id


@fs.app.route('/new_game')
@fs.app.route('/new_game/')
def new_game():
    """
    makes a new game and then redirects user to it
    :return: None
    """
    game_id = make_unique_game_id()
    games[game_id] = WaitingRoom(game_id)

    fs.socket_io.start_background_task(clear_inactive_players, games[game_id])

    return redirect('/' + game_id)

@fs.app.route('/help')
@fs.app.route('/help/')
def help_screen():
    """
    shows the help screen
    :return: None
    """

    return render_template("help.html", theme=settings.get_theme())


@fs.app.route('/<game_id>', methods=['GET', 'POST'])
@fs.app.route('/<game_id>/', methods=['GET', 'POST'])
def render_game(game_id):
    """
    renders the given game
    :param game_id:
    :return:
    """
    if game_id in games:
        return games[game_id].render()
    else:
        return render_template("index.html", message="Game not found", theme=settings.get_theme())


@fs.socket_io.on('waiting room message')
def waiting_room(game_id, message, data):
    if game_id in games:
        return games[game_id].message(message, data)


@fs.socket_io.on('game message')
def game_message(game_id, message, data):
    if game_id in games:
        if games[game_id].is_running():
            games[game_id].get_game().message(message, data)


@fs.socket_io.on('disconnect')
def disconnected():
    del sessions[request.sid]


@fs.socket_io.on('connect')
def connected():
    sessions[request.sid] = 0


def clear_inactive_players(game):
    while game.game_id in games:
        for player_id in game.get_sessions().copy():
            sid = game.get_sessions()[player_id]['sid']

            if sid in sessions:
                game.get_sessions()[player_id]['timeout'] = 0
            else:
                game.get_sessions()[player_id]['timeout'] += 1

                kick = settings.session_inactivity_kick - \
                    game.get_sessions()[player_id]['timeout']

                if kick <= 0:
                    print("PLAYER KICKED", player_id)
                    game.kick_player(player_id)

        fs.socket_io.sleep(1)


def clear_inactive_games():
    """
    removes all the games that have not been modified in over an hour
    :return: None
    """
    current_time = time()
    to_remove = []
    for game_id in games:
        game = games[game_id]
        # if game has not be interacted with in 1 hour, delete it
        if current_time - game.get_last_modified() > 3600:
            print("REMOVING GAME", game.get_id())
            to_remove.append(game_id)
    for game_id in to_remove:
        games.pop(game_id)


def run_schedule():
    while 1:
        schedule.run_pending()
        sleep(1)


schedule.every().hour.do(clear_inactive_games)

if __name__ == '__main__':
    print("Game is now running")
    print("Open a web browser and open one of the following:")
    if settings.port == 80:
        print("\thttp:/" + gethostname() + "/")
        print("\thttp:/" + gethostbyname(gethostname()) + "/")
    else:
        print("\thttp:/" + gethostname() + ":" + str(settings.port) + "/")
        print("\thttp:/" + gethostbyname(gethostname()) +
              ":" + str(settings.port) + "/")

    t1 = Thread(target=run_schedule)
    t1.start()

    fs.socket_io.run(fs.app, debug=False,
                     port=settings.port, host=settings.host)
