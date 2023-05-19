import random
import string
import uuid
import chess
import re
from django.db import IntegrityError
from chessbunker.settings import WEBSOCKET_SERVER_URL
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .models import Player, Game
from chessbunker.settings import ENVIRONMENT


# ================= User =================


@method_decorator(csrf_exempt, name='dispatch')
class PlayerAPI(View):
    """Player API"""

    def post(self, request):
        """Register a new user and create a new player"""

        try:
            body = json.loads(request.body.decode('utf-8'))

            if 'username' not in body:
                return JsonResponse({"status": 400, "message": "Provide username to request body"}, status=400)

            if 'password' not in body:
                return JsonResponse({"status": 400, "message": "Provide user password to request body"}, status=400)

            if 'email' not in body:
                return JsonResponse({"status": 400, "message": "Provide user email to request body"}, status=400)

            # # Validate email
            if ENVIRONMENT == 'production':
                if re.match(r"[^@]+@[^@]+\.[^@]+", body['email']) == None:
                    return JsonResponse({"status": 400, "message": "Invalid email"}, status=400)

                # # Validate password
                if len(body['password']) < 8 or len(body['password']) > 50:
                    return JsonResponse({"status": 400, "message": "Password must be between 8 and 50 characters"}, status=400)

            user = User.objects.create_user(
                username=body['username'], password=body['password'],
                email=body['email'])

            user.save()

            player = Player(user=user)
            player.save()

            return JsonResponse({"status": 200, "message": "User created successfully"}, status=200)

        except IntegrityError as e:
            return JsonResponse({"status": 400, "message": "User with this credentials already exist"}, status=400)
        except Exception as e:
            return JsonResponse({"status": 500, "message": str(e)}, status=500)

    @method_decorator(login_required)
    def get(self, request):
        """Get user information"""

        return JsonResponse({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "elo": request.user.player.elo,
            "games_played": request.user.player.games_played,
            "games_won": request.user.player.games_won,
            "games_lost": request.user.player.games_lost,
            "games_draw": request.user.player.games_draw
        })

    @method_decorator(login_required)
    def patch(self, request):
        """Update user information"""
        try:
            allowed_user_updates = set(['username', 'email', 'password'])

            body = json.loads(request.body.decode('utf-8'))

            for key in body:
                if key in allowed_user_updates:
                    if key == 'password':
                        request.user.set_password(body[key])
                    else:
                        setattr(request.user, key, body[key])
                else:
                    return JsonResponse({"status": 400, "message": "Invalid key in request body"}, status=400)

            request.user.player.save()
            request.user.save()

            return JsonResponse({"status": 200, "message": "User updated successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"status": 500, "message": str(e)}, status=500)

    @method_decorator(login_required)
    def delete(self, request):
        """Delete user"""
        try:
            request.user.player.delete()
            request.user.delete()
            return JsonResponse({"status": 200, "message": "User deleted successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"status": 500, "message": str(e)}, status=500)


@csrf_exempt
@require_POST
def login_user(request):
    """Login a user"""

    try:
        body = json.loads(request.body.decode('utf-8'))

        if 'username' not in body:
            return JsonResponse({"status": 400, "message": "Provide username to request body"}, status=400)

        if 'password' not in body:
            return JsonResponse({"status": 400, "message": "Provide user password to request body"}, status=400)

        user = authenticate(request, username=body['username'],
                            password=body['password'])

        if user is None:
            return JsonResponse({"status": 401, "message": "Invalid credentials"}, status=401)

        login(request, user)

        return JsonResponse({"status": 200, "message": "User logged in successfully", "user": user.id}, status=200)
    except Exception as e:
        return JsonResponse({"status": 500, "message": str(e)}, status=500)


@csrf_exempt
@require_POST
def logout_user(request):
    """Logout a user"""

    try:
        logout(request)
        return JsonResponse({"status": 200, "message": "User logged out successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"status": 500, "message": str(e)}, status=500)


@csrf_exempt
@require_POST
def ranking(request):
    """Get players with highest elo"""

    body = json.loads(request.body.decode('utf-8'))

    limit = 10
    skip = 0

    if 'limit' in body:
        if body['limit'] <= 0:
            return JsonResponse({"status": 400, "message": "Limit cannot be less or equal 0"}, status=400)

        limit = body['limit']

    if 'skip' in body:
        if body['skip'] < 0:
            return JsonResponse({"status": 400, "message": "Skip cannot be less than 0"}, status=400)

        skip = body['skip']

    player_list = Player.objects.order_by('-elo')[skip*limit:skip*limit+limit]

    json_player_list = [{
        "username": player.user.username,
        "elo": player.elo,
        "games_won": player.games_won,
        "games_lost": player.games_lost
    } for player in player_list]

    return JsonResponse({"ranking": json_player_list, "status": 200, "message": "Ranking downloaded successfully"}, status=200)

# ================= Game =================


@method_decorator(csrf_exempt, name='dispatch')
class GameAPI(View):
    """Game API"""

    @method_decorator(login_required)
    def get(self, request):
        try:
            body = json.loads(request.body.decode('utf-8'))

            if "id" not in body:
                return JsonResponse({"status": 400, "message": "Provide game id"}, status=400)

            game = Game.objects.get(id=body["id"])

            if not game:
                return JsonResponse({"status": 400, "message": "Game not found"}, status=400)

            return JsonResponse({
                "id": game.id,
                "status": game.status,
                "join_code": game.join_code,
                "white": game.white.user.id if game.white else None,
                "black": game.black.user.id if game.black else None,
                "white_timer": game.white_timer,
                "black_timer": game.black_timer,
                "fen": game.fen,
                "event_server_url": game.event_server_url,
                "date": game.date,
            })
        except Exception as e:
            return JsonResponse({"status": 500, "message": str(e)}, status=500)

    @method_decorator(login_required)
    def post(self, request):
        try:
            body = json.loads(request.body.decode('utf-8'))

            # User can join only one game (prod only)
            if ENVIRONMENT == "production":
                user_games = Game.objects.filter(Q(status=Game.Status.IN_PROGRESS) & (
                    Q(white=request.user.player) | Q(black=request.user.player)))

                if user_games:
                    return JsonResponse({"status": 400, "message": "You are already in a game"}, status=400)

            # Join game with code
            if 'join_code' in body and body['join_code'] != "":
                # Join game
                game = Game.objects.get(join_code=body['join_code'])

                if not game:
                    return JsonResponse({"status": 400, "message": "Game not found"}, status=400)

                if game.status != Game.Status.CODE_JOIN:
                    return JsonResponse({"status": 400, "message": "Game is not in matchmaking status"}, status=400)

                setattr(game, 'join_code', None)
                setattr(game, 'status', Game.Status.START)

                if (game.white and game.white == request.user.player) or (game.black and game.black == request.user.player):
                    return JsonResponse({"status": 400, "message": "You are already in this game"}, status=400)

                # Set player 2
                if game.white:
                    setattr(game, 'black', request.user.player)
                else:
                    setattr(game, 'white', request.user.player)

                game.save()

                return JsonResponse({"status": 200, "message": "Game joined successfully", "event_server_url": game.event_server_url, "id": game.id}, status=200)

            # Find a game using matchmaking
            game = Game.objects.filter(
                status=Game.Status.MATCHMAKING, white=request.user.player).first() or Game.objects.filter(status=Game.Status.MATCHMAKING, black=request.user.player).first()

            if game:
                return JsonResponse({"status": 400, "message": "You are already in matchmaking"}, status=400)

            game = Game.objects.filter(
                status=Game.Status.MATCHMAKING).exclude(white=request.user.player, black=request.user.player).order_by('date')

            # Get the game with elo difference less than 100
            best_game = None
            for g in game:
                game_player_elo = g.white.elo if g.white else g.black.elo
                user_elo = request.user.player.elo

                if abs(game_player_elo - user_elo) <= 100:
                    best_game = g
                    break

            game = best_game

            if game:
                if game.white:
                    setattr(game, 'black', request.user.player)
                else:
                    setattr(game, 'white', request.user.player)

                setattr(game, 'status', Game.Status.START)
                game.save()

                return JsonResponse({"status": 200, "message": "Game found successfully", "event_server_url": game.event_server_url, "id": game.id}, status=200)

            # Create a new game

            if 'generate_join_code' in body and body['generate_join_code']:
                join_code = ''.join(random.choices(
                    string.ascii_uppercase + string.digits, k=6))
                status = Game.Status.CODE_JOIN
            else:
                join_code = None
                status = Game.Status.MATCHMAKING

            timer = 900
            if 'timer' in body:
                if body['timer'] <= 0:
                    return JsonResponse({"status": 400, "message": "Timer value cannot be less or equal 0"}, status=400)

                timer = body['timer']

            room_id = str(uuid.uuid4()).replace('-', '')
            side = 'white'
            server_url = f"{WEBSOCKET_SERVER_URL}/{room_id}"

            game = Game(join_code=join_code, status=status,
                        event_server_url=server_url, white_timer=timer, black_timer=timer)
            setattr(game, side, request.user.player)
            game.save()

            return JsonResponse({"status": 200, "message": "Matchmaking started successfully", "event_server_url": server_url, "join_code": join_code, "id": game.id}, status=200)
        except Exception as e:
            return JsonResponse({"status": 500, "message": str(e)}, status=500)

    @method_decorator(login_required)
    def patch(self, request):
        try:
            body = json.loads(request.body.decode('utf-8'))

            if "id" not in body:
                return JsonResponse({"status": 400, "message": "Provide game id"}, status=400)

            if "action" not in body:
                return JsonResponse({"status": 400, "message": "Provide action"}, status=400)

            game = Game.objects.get(id=body["id"])

            if not game:
                return JsonResponse({"status": 400, "message": "Game not found"}, status=400)

            if game.status == Game.Status.ENDED:
                return JsonResponse({"status": 400, "message": "Game is finished"}, status=400)

            if game.white != request.user.player and game.black != request.user.player:
                return JsonResponse({"status": 400, "message": "You are not in this game"}, status=400)

            if game.fen:
                board = chess.Board(game.fen)
            else:
                board = chess.Board()

            if body["action"] == "MOVE":
                # Check if it's the player's turn
                if game.white == request.user.player and board.turn != chess.WHITE:
                    return JsonResponse({"status": 400, "message": "It's not your turn"}, status=400)

                if game.black == request.user.player and board.turn != chess.BLACK:
                    return JsonResponse({"status": 400, "message": "It's not your turn"}, status=400)

                # Check if move is valid
                if "move" not in body:
                    return JsonResponse({"status": 400, "message": "Provide move"}, status=400)

                if not board.is_legal(chess.Move.from_uci(body["move"])):
                    return JsonResponse({"status": 400, "message": "Invalid move"}, status=400)

                # Update board
                board.push(chess.Move.from_uci(body["move"]))
                setattr(game, 'fen', board.fen())
                setattr(game, 'status', Game.Status.IN_PROGRESS)

                # Update timer
                if "timer" in body:
                    if game.white == request.user.player:
                        setattr(game, 'white_timer', body["timer"])
                    else:
                        setattr(game, 'black_timer', body["timer"])
                # Check if game is finished
                if board.is_game_over():
                    if board.is_checkmate():
                        if board.turn == chess.WHITE:
                            setattr(game, 'winner', game.black)
                            winner = game.black
                            loser = game.white
                        else:
                            setattr(game, 'winner', game.white)
                            winner = game.white
                            loser = game.black

                        # Update user stats
                        player = Player.objects.get(id=winner.id)
                        player.games_won += 1
                        player.games_played += 1
                        player.elo += 10
                        player.save()

                        player = Player.objects.get(id=loser.id)
                        player.games_lost += 1
                        player.games_played += 1
                        player.elo -= 10
                        player.save()

                    else:
                        setattr(game, 'winner', None)

                    setattr(game, 'status', Game.Status.ENDED)

                game.save()

            elif body["action"] == "STOP":
                # Set user making the request as the loser
                if game.white == request.user.player:
                    setattr(game, 'winner', game.black)
                    winner = game.black
                    loser = game.white
                else:
                    setattr(game, 'winner', game.white)
                    winner = game.white
                    loser = game.black

                # Update user stats
                player = Player.objects.get(id=winner.id)
                player.games_won += 1
                player.games_played += 1
                player.elo += 10
                player.save()

                player = Player.objects.get(id=loser.id)
                player.games_lost += 1
                player.games_played += 1
                player.elo -= 10
                player.save()

                setattr(game, 'status', Game.Status.ENDED)
                game.save()

            return JsonResponse({"status": 200, "message": "Game updated successfully", "fen": game.fen}, status=200)

        except Exception as e:
            return JsonResponse({"status": 500, "message": str(e)}, status=500)

    @method_decorator(login_required)
    def delete(self, request):
        try:
            body = json.loads(request.body.decode('utf-8'))

            if "id" not in body:
                return JsonResponse({"status": 400, "message": "Provide game id"}, status=400)

            game = Game.objects.get(id=body["id"])

            if not game:
                return JsonResponse({"status": 400, "message": "Game not found"}, status=400)

            if game.status == Game.Status.ENDED:
                return JsonResponse({"status": 400, "message": "Game is finished"}, status=400)

            if game.white != request.user.player and game.black != request.user.player:
                return JsonResponse({"status": 400, "message": "You are not in this game"}, status=400)

            # Leave game

            # If only one player joined, delete the game
            if (game.white == request.user.player and not game.black) or (game.black == request.user.player and not game.white):
                game.delete()
                return JsonResponse({"status": 200, "message": "Game left successfully"}, status=200)

            # If both players joined, set the other player as winner

            if game.white == request.user.player:
                setattr(game, 'winner', game.black)
                winner = game.black
                loser = game.white

            else:
                setattr(game, 'winner', game.white)
                winner = game.white
                loser = game.black

            # Update user stats
            player = Player.objects.get(id=winner.id)
            player.games_won += 1
            player.games_played += 1
            player.elo += 10
            player.save()

            player = Player.objects.get(id=loser.id)
            player.games_lost += 1
            player.games_played += 1
            player.elo -= 10
            player.save()

            setattr(game, 'status', Game.Status.ENDED)
            game.save()

            return JsonResponse({"status": 200, "message": "Game left successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"status": 500, "message": str(e)}, status=500)