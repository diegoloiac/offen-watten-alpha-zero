import argparse
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

from core.EnvironmentSelector import EnvironmentSelector


def throw_error(message):
    print(message)
    sys.exit(1)


def train(agent_profile, agent_path, out_agent_path, memory_folder=None, game_memory=None, epochs=1):
    physical_devices = tf.config.list_physical_devices('GPU')
    print(physical_devices)
    for gpu in physical_devices:
        tf.config.experimental.set_memory_growth(gpu, True)

    env_selector = EnvironmentSelector()

    agent = env_selector.get_agent(agent_profile)

    if agent_path:
        agent.load(agent_path)

    if not memory_folder:
        print("Error: You must specify a memory folder in which you have all the tfrecord files!")
        throw_error("Error: You must specify a memory folder in which you have all the tfrecord files!")

    print("Initiate training...")

    paths = []
    for file in os.listdir(memory_folder):
        paths.append(memory_folder + '/' + file)

    agent.train(paths, epochs=epochs)

    print("Training finished!")

    agent.save(out_agent_path)

    print("Model saved!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--agent", dest="agent_profile",
                        help="Agent profile from EnvironmentSelector. Required.")
    parser.add_argument("--memory_path", dest="memory_path",
                        help="Agent profile from EnvironmentSelector. Required.")
    parser.add_argument("--out_agent_path", dest="out_agent_path",
                        help="Path to the generated agent's model. Required.")

    parser.add_argument("--agent_path", dest="agent_path",
                        help="Path to the agent's model.")

    parser.add_argument("--epochs", dest="epochs", type=int,
                        default=1,
                        help="Epochs to train")

    options = parser.parse_args()

    if not options.agent_profile:
        parser.error('Agent profile must be selected')

    if not options.memory_path:
        parser.error('Memory path must be selected')

    if not options.out_agent_path:
        parser.error('Out Agent model path must be selected')

    train(options.agent_profile, options.agent_path,
          options.out_agent_path, memory_folder=options.memory_path,
          epochs=options.epochs)
