#!/usr/bin/env python3
import uno_config
from player import Player
from random import randint
import flask_server as fs
import schedule
from flask import *
from waiting_room import WaitingRoom

games = {}


@fs.app.route('/')
def index():
    return render_template("index.html")


def make_unique_game_id():
    """
    generates an unique id for a game that consisting of 4 random numbers each 3 digit
    :return: The generated ID as a string
    """
    # I wish python had a do while loop
    def generate():
        new_game_id = '{:05d}'
        return new_game_id.format(randint(10000, 100000))

    # generates an ID if its not unique, generate another
    game_id = generate()
    while game_id in games:
        game_id = generate()

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
        return redirect('/')


@fs.socket_io.on('connect')
def user_connected():
    pass


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
    pass


schedule.every().hour.do(clear_old_games)

if __name__ == '__main__':
    fs.socket_io.run(fs.app, debug=True, host='0.0.0.0', port=80)
