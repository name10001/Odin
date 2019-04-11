#!/usr/bin/env python3
from random import randint
import schedule
from time import time, sleep
from flask import *
from threading import Thread

import flask_server as fs
from waiting_room import WaitingRoom

games = {}


@fs.app.route('/')
def index():
    return render_template("index.html", message=None)


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
def new_game():
    """
    makes a new game and then redirects user to it
    :return: None
    """
    game_id = make_unique_game_id()
    games[game_id] = WaitingRoom(game_id)
    return redirect('/' + game_id)


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
        return render_template("index.html", message="Game not found")


@fs.socket_io.on('waiting room')
def waiting_room(game_id):
    if game_id in games:
        return games[game_id].joined_waiting_room()


@fs.socket_io.on('start game')
def waiting_room(game_id):
    if game_id in games:
        games[game_id].start()


@fs.socket_io.on('initial game connection')
def initial_game_connection(game_id):
    if game_id in games:
        if games[game_id].is_running():
            games[game_id].get_game().initial_connection()


@fs.socket_io.on('game message')
def game_message(game_id, message, data):
    if game_id in games:
        if games[game_id].is_running():
            games[game_id].get_game().message(message, data)


def clear_old_games():
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


schedule.every().hour.do(clear_old_games)

if __name__ == '__main__':
    t = Thread(target=run_schedule)
    t.start()
    fs.socket_io.run(fs.app, debug=False, host='0.0.0.0', port=80)
