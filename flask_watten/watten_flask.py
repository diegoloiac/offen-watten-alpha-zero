from flask import Flask, request
import flask
from flask_restful import Resource, Api, marshal_with, fields
import uuid

from flask_watten.model.response import WattenResponse
from flask_watten.watten_engine import WattenEngine
from games.watten.WattenGame import WattenGame

app = Flask(__name__)
api = Api(app, prefix="/api/rest")

# map containing running games
running_games = {"TEST_GAME_ID": WattenGame()}

response_fields = {
    'message': fields.String,
    'body': WattenResponse
}

watten_engine = WattenEngine()


class FlaskWattenGame(Resource):

    @marshal_with(response_fields)
    def put(self):
        """ Starts a new game """
        game_id = str(uuid.uuid4())

        request_body = request.get_json(force=True)
        player_distributes_cards = request_body['player_distributes_cards']

        new_game = WattenGame()
        starting_state = new_game.get_player_visible_state(0)
        states = None
        if player_distributes_cards:
            new_game.trueboard.current_player = -1
            new_game.trueboard.distributing_cards_player = 1

            starting_state = new_game.get_player_visible_state(0)  # override starting state
            states = watten_engine.make_move_against_ai(new_game)

        running_games[game_id] = new_game
        res = WattenResponse(message="Game started successfully",
                             body={
                                 'game_id': game_id,
                                 'starting_state': starting_state,
                                 'states': states
                             })

        return res

    @marshal_with(response_fields)
    def delete(self, game_id):
        """ Delete a running game """
        try:
            running_games[game_id]
        except KeyError:
            return WattenResponse(message="Game with id [%s] does not exist" % game_id)
        del running_games[game_id]

        return WattenResponse(message="Game with id [%s] deleted successfully" % game_id)


class FlaskWattenActions(Resource):

    @marshal_with(response_fields)
    def get(self, game_id):
        """ Get list of valid moves """
        try:
            running_game = running_games[game_id]
        except KeyError:
            return WattenResponse(message="Game with id [%s] does not exist" % game_id)
        valid_moves = watten_engine.get_valid_moves(running_game)
        return WattenResponse(message="List of available moves", body={'valid_moves': valid_moves})

    @marshal_with(response_fields)
    def post(self, game_id):
        """ Make a move """
        try:
            running_game = running_games[game_id]
        except KeyError:
            return WattenResponse(message="Game with id [%s] does not exist" % game_id)
        request_body = request.get_json(force=True)
        move = request_body['move']
        # game_result, next_player = running_game.make_move(move)
        states_and_moves = watten_engine.make_move_against_ai(running_game, move)
        return WattenResponse(message="AI played its moves", body=states_and_moves)


api.add_resource(FlaskWattenGame, '/game', '/game/<string:game_id>')
api.add_resource(FlaskWattenActions, '/moves/<string:game_id>')

if __name__ == '__main__':
    app.run(debug=True)
