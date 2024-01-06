from .game import *
from django.template import loader
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse


# checks to see if a clicked button is available
def button_click(request, buttonNumber):
    game_data = request.session.get('game_instance')
    game_instance = Game.from_json(game_data)
    # buttonNumber starts at 1, get the index which starts at 0 by subtracting 1
    squareIndex = buttonNumber - 1
    if game_instance.board[squareIndex // 3][squareIndex % 3] != 0:
        return JsonResponse({'result': 'taken'})
    return JsonResponse({'result': 'open'})


# initializes a new game; loads Game object
def init_game(request):
    game_instance = Game()
    request.session['game_instance'] = game_instance.to_json()
    context = {'game': game_instance}
    template = loader.get_template('game.html')
    return HttpResponse(template.render(context, request))


# loads the landing page
def land(request):
    return render(request, 'index.html')


# gets players from a locally stored json file
def get_players_data(request):
    with open(r'C:\Users\matt\PycharmProjects\hoopsTacToe\hoopsTacToeApp\players.json') as f:
        players_data = json.load(f)
    return JsonResponse(players_data, safe=False)


# checks game over by checking all possible winning combinations
def check_game_over(request):
    game_data = request.session.get('game_instance')
    game_instance = Game.from_json(game_data)
    board = game_instance.board
    possWins = [board[0],  # top row
                board[1],  # middle row
                board[2],  # bottom row
                [board[0][0], board[1][0], board[2][0]],  # left column
                [board[0][1], board[1][1], board[2][1]],  # middle column
                [board[0][2], board[1][2], board[2][2]],  # right column
                [board[0][0], board[1][1], board[2][2]],  # diagonal (\)
                [board[0][2], board[1][1], board[2][0]]]  # diagonal (/)
    # loop through each possible win and check to see if a player has won
    for i in range(len(possWins)):
        won = True
        for j in range(len(possWins[i]) - 1):
            if possWins[i][j] == 0 or possWins[i][j] != possWins[i][j + 1]:
                won = False
        if won:
            return JsonResponse({'game_over': 'true', 'winner': str(possWins[i][0])})
    return JsonResponse({'game_over': 'false', 'winner': None})


# helper function for check_player, updates the game state to reflect the input from one of the players
def updateCorrectSquare(request, game_instance, square):
    turn = game_instance.turn
    # squares start at one, we want the index to start at 0
    squareIndex = square - 1
    if turn == 1:
        game_instance.board[squareIndex // 3][squareIndex % 3] = 1
    else:
        assert (turn == 2)
        game_instance.board[squareIndex // 3][squareIndex % 3] = 2
    # update the turn
    updateTurn(request, game_instance)
    request.session['game_instance'] = game_instance.to_json()
    return JsonResponse({'result': 'success'})


# updates the turn after a guess is made
def updateTurn(request, game_instance):
    if game_instance.turn == 1:
        game_instance.turn = 2
    else:
        assert (game_instance.turn == 2)
        game_instance.turn = 1
    # update the game state
    request.session['game_instance'] = game_instance.to_json()
    game_data = request.session.get('game_instance')
    game_instance = Game.from_json(game_data)
    print(game_instance.turn)
    return JsonResponse({'result': 'success'})


# queries the database to see if a guessed player is a valid answer for the square
def check_player(request):
    game_data = request.session.get('game_instance')
    game_instance = Game.from_json(game_data)
    square = request.GET.get('square')
    player = request.GET.get('player')
    # makes sure that game_instance exists, throws error otherwise
    valid = False
    if game_instance:
        # guess for square 1
        if square == '1':
            # player is in the answer set, and correct
            print(game_instance.square1Answers)
            if (player,) in game_instance.square1Answers:
                valid = True
        # same logic for remaining squares
        if square == '2':
            print(game_instance.square2Answers)
            if (player,) in game_instance.square2Answers:
                valid = True
        if square == '3':
            print(game_instance.square3Answers)
            if (player,) in game_instance.square3Answers:
                valid = True
        if square == '4':
            print(game_instance.square4Answers)
            if (player,) in game_instance.square4Answers:
                valid = True
        if square == '5':
            print(game_instance.square5Answers)
            if (player,) in game_instance.square5Answers:
                valid = True
        if square == '6':
            print(game_instance.square6Answers)
            if (player,) in game_instance.square6Answers:
                valid = True
        if square == '7':
            print(game_instance.square7Answers)
            if (player,) in game_instance.square7Answers:
                valid = True
        if square == '8':
            print(game_instance.square8Answers)
            if (player,) in game_instance.square8Answers:
                valid = True
        if square == '9':
            print(game_instance.square9Answers)
            if (player,) in game_instance.square9Answers:
                valid = True
        # return false if the player isn't found in its corresponding answer set
        if valid:
            updateCorrectSquare(request, game_instance, int(square))
            return JsonResponse({'result': {'valid': 'true', 'turn': str(game_instance.turn)}})
        else:
            updateTurn(request, game_instance)
            return JsonResponse({'result': {'valid': 'false', 'turn': str(game_instance.turn)}})
    else:
        return JsonResponse({'result': 'error', 'message': 'Game instance not found in session'})
