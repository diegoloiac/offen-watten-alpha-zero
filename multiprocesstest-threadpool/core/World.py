import numpy as np
import itertools
import logging
from tqdm import tqdm
from core.EnvironmentSelector import EnvironmentSelector
import tensorflow as tf

from core.agents.HumanAgent import HumanAgent
from core.agents.AgentRandom import AgentRandom
from versions.asymmetric_sub_watten.AsymmetricSubWattenGame import AsymmetricSubWattenGame
from versions.blind_watten.BlindWattenGame import BlindWattenGame
from versions.hand_watten.HandWattenGame import HandWattenGame
from concurrent.futures import ThreadPoolExecutor


class World:
    """
    An World class where any agents can be play and generate experience
    """

    def __init__(self, add_randomness=False):
        self.RESULT_DRAW = -1
        self.add_randomness = add_randomness

    def execute_game(self, max_game_steps_n=None, allow_exploration=False,
                     verbose=False, show_every_turn=False, exploration_decay_steps=None, need_reset=True):

        episode_exp = []
        augmented_exp = []

        game = HandWattenGame()

        if need_reset:
            game.reset()


        Env = EnvironmentSelector()

        agent = EnvironmentSelector.build_train_agent_ffnn(Env)


        agents = []
        for idx in range(game.get_players_num()):
            agents.append(agent.clone())
            agents[idx].name += str(idx)

        # create cnn game if needed
        cnn_game = None
        if agents[1].name == 'evaluate_cnn':
            cnn_game = HandWattenGame(cnn=True)
            cnn_game.trueboard.init_world_to_state(game.trueboard.current_player, game.trueboard.distributing_cards_player,
                                                   game.trueboard.player_A_hand, game.trueboard.player_B_hand,
                                                   game.trueboard.played_cards, game.trueboard.current_game_player_A_score,
                                                   game.trueboard.current_game_player_B_score, game.trueboard.current_game_prize,
                                                   game.trueboard.is_last_move_raise, game.trueboard.is_last_move_accepted_raise,
                                                   game.trueboard.is_last_hand_raise_valid, game.trueboard.first_card_deck,
                                                   game.trueboard.last_card_deck, game.trueboard.rank,
                                                   game.trueboard.suit, game.trueboard.started_raising)

        game_results = []
        for idx, agent in enumerate(agents):
            if allow_exploration:
                agent.set_exploration_enabled(True)
            else:
                agent.set_exploration_enabled(False)
            agent.prepare_to_game()
            game_results.append(self.RESULT_DRAW)

        cur_player = game.get_cur_player()

        loop_range = itertools.count()

        if verbose:
            loop_range = tqdm(loop_range)

        for episodeStep in loop_range:
            if max_game_steps_n is not None and episodeStep > max_game_steps_n:
                episode_exp = []
                break

            # if show_every_turn:
            #     print("\n", game.get_display_str())

            observation = game.get_observation(cur_player)

            cur_turn_agent = agents[cur_player]

            if exploration_decay_steps and episodeStep >= exploration_decay_steps:
                cur_turn_agent.set_exploration_enabled(False)

            # Make cnn prediction if needed
            if cur_player == 1 and cur_turn_agent.name == 'evaluate_cnn':
                cnn_game.trueboard.init_world_to_state(game.trueboard.current_player, game.trueboard.distributing_cards_player,
                                                       game.trueboard.player_A_hand, game.trueboard.player_B_hand,
                                                       game.trueboard.played_cards, game.trueboard.current_game_player_A_score,
                                                       game.trueboard.current_game_player_B_score, game.trueboard.current_game_prize,
                                                       game.trueboard.is_last_move_raise, game.trueboard.is_last_move_accepted_raise,
                                                       game.trueboard.is_last_hand_raise_valid, game.trueboard.first_card_deck,
                                                       game.trueboard.last_card_deck, game.trueboard.rank,
                                                       game.trueboard.suit, game.trueboard.started_raising)
                actions_prob, observation_value = cur_turn_agent.predict(cnn_game, cur_player)
            else:
                actions_prob, observation_value = cur_turn_agent.predict(game, cur_player)

            episode_exp.append([observation, cur_player, actions_prob])

            # if using NNet agent need to mask the invalid moves
            # mask it anyway so that the class doesn't depend on AgentNNet
            if type(actions_prob) == list:
                actions_prob = np.array(actions_prob, dtype=float)

            # mask invalid moves
            valid_moves = game.get_valid_moves(cur_player)
            old_actions_prob = actions_prob
            actions_prob = actions_prob*valid_moves

            # WATTEN DETERMINISTIC RAISING
            # remove raising from output nn
            if (type(game) == HandWattenGame or type(game) == BlindWattenGame) and type(cur_turn_agent) != HumanAgent and type(cur_turn_agent) != AgentRandom:
                # Convert tensor when dealing with IA
                if tf.is_tensor(observation_value):
                    observation_value = observation_value.numpy()
                    actions_prob = actions_prob.numpy()

                # last move was a raise
                if valid_moves[47] == 1 and valid_moves[48] == 1:
                    # decide whether to fold or not fold
                    if game.decide_about_accepting_raise(observation_value, game.get_number_of_tricks_played()):
                        # player decided not to fold, deciding now whether to accept or raise
                        if valid_moves[46] == 1 and game.decide_about_raising(observation_value, game.get_number_of_tricks_played()):
                            actions_prob = np.zeros(50)
                            actions_prob[46] = 1
                        else:
                            actions_prob = np.zeros(50)
                            actions_prob[48] = 1
                    else:
                        actions_prob = np.zeros(50)
                        actions_prob[47] = 1

                # normal situation in which I can raise
                elif valid_moves[46] == 1:
                    # decide what to do
                    if game.decide_about_raising(observation_value, game.get_number_of_tricks_played()):
                        actions_prob = np.zeros(50)
                        actions_prob[46] = 1
                    else:
                        actions_prob[46] = 0
                        if np.sum(actions_prob) == 0:
                            actions_prob = valid_moves
                            actions_prob[46] = 0
                        actions_prob = np.true_divide(actions_prob, np.sum(actions_prob))
                else:
                    mult = np.ones(len(valid_moves))
                    mult[46:] = 0
                    actions_prob = np.multiply(actions_prob, mult)
                    if np.sum(actions_prob) == 0:
                        actions_prob = valid_moves
                    actions_prob = np.true_divide(actions_prob, np.sum(actions_prob))
                    if self.add_randomness:
                        choose_random = np.choice([False, True], p=[0.9, 0.1])
                        if choose_random:
                            action = np.random.choice(len(valid_moves), p=valid_moves)
                            actions_prob = np.zeros(50)
                            actions_prob[action] = 1

            if not allow_exploration:
                bestA = np.argmax(actions_prob)
                actions_prob = [0] * len(actions_prob)
                actions_prob[bestA] = 1

            action = np.random.choice(len(actions_prob), p=actions_prob)

            try:
                _, cur_player = game.make_move(action)
            except Exception as e:
                print("ERROR")
                print(game.trueboard.moves_series)
                print(game.trueboard.starting_state)
                logging.exception("error")
                raise e

            cur_turn_agent.on_turn_finished(game)

            if game.is_ended():
                if not game.is_draw():
                    results = []
                    for idx, agent in enumerate(agents):
                        game_results[idx] = game.get_score(idx)
                        results.append(game_results[idx])
                        # if 46 not in game.trueboard.moves_series:
                        #     game.trueboard.display()

                        # if verbose:
                        #     print("\n", agent.get_name(), " scored ", game_results[idx], "\n")
                    action_size = game.get_action_size()
                    if action_size == 50:
                        if results[0] == results[1]:
                            raise Exception("Watten game cannot end in a draw")
                    # game.get_display_str()
                else:
                    for idx, agent in enumerate(agents):
                        game_results[idx] = self.RESULT_DRAW
                    raise Exception("Watten game cannot end in a draw")
                break

        # if verbose:
        #     print("\n\nFinal observation on step %d.\n%s\n" % (
        #        loop_range, game.get_display_str()))

        for idx, [cur_observation, cur_player, cur_pi] in enumerate(episode_exp):
            augmented_exp.append((cur_observation, cur_pi, game_results[cur_player]))

        return augmented_exp, game_results

    def execute_games(self, agents, game, num_games, max_game_steps_n=None, allow_exploration=False,
                      verbose=False, show_every_turn=False, exploration_decay_steps=None):
        games_experience = []
        games_results = [0] * len(agents)
        won = [0] * len(agents)

        for idx in range(len(agents)):
            games_results[idx] = 0
            won[idx] = 0

        loop_range = range(num_games)

        # if verbose:
        loop_range = tqdm(loop_range)

        for id_loop in loop_range:
            futures = []
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures.append(executor.submit(self.execute_game(
                                                              max_game_steps_n,
                                                              allow_exploration,verbose,
                                                              show_every_turn,
                                                              exploration_decay_steps)))


                game_experience, game_results = futures[0]

                for idx, result in enumerate(game_results):
                    if result > 0:
                        won[idx] += 1

                if len(game_experience) > 0:
                    games_experience.extend(game_experience)

                for idx in range(len(agents)):
                    games_results[idx] += game_results[idx]

        if verbose:
            for idx, agent in enumerate(agents):
                print(f"--- {agent.get_name()}: {games_results[idx]} ---  {won[idx]}")

        return games_experience, games_results

    def generate_self_play(self, agent, game, num_games,
                           max_game_steps_n=None, allow_exploration=True,
                           verbose=False, show_every_turn=False,
                           exploration_decay_steps=None):
        agents = []
        for idx in range(game.get_players_num()):
            agents.append(agent.clone())
            agents[idx].name += str(idx)

        # add randomness to player with more cards in asymmetric_sub_watten
        if type(game) == AsymmetricSubWattenGame:
            print(agent.exp_rate)
            agents[1].exp_rate = 7

        games_experience, _ = self.execute_games(agents, game, num_games,
                                                 max_game_steps_n=max_game_steps_n, allow_exploration=allow_exploration,
                                                 verbose=verbose, show_every_turn=show_every_turn,
                                                 exploration_decay_steps=exploration_decay_steps)
        return games_experience
