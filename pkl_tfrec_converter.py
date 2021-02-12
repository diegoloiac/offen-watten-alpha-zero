import argparse
from core.utils.utils import deserialize
import numpy as np
import tensorflow as tf


def _float_feature(value):
    """Returns a float_list from a float / double."""
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))


def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy()   # BytesList won't unpack a string from an EagerTensor.
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def serialize_example(obs, pi, game_result):
    """
    Creates a tf.train.Example message ready to be written to a file.
    """
    # Create a dictionary mapping the feature name to the tf.train.Example-compatible
    # data type.
    feature = {
        'observation': _bytes_feature(obs),
        'pi': _bytes_feature(pi),
        'game_result': _float_feature(game_result),
    }

    # Create a Features message using tf.train.Example.

    example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
    return example_proto.SerializeToString()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--path", dest="path", help="Path where the pkl file is saved. Required.")

    options = parser.parse_args()

    if not options.path or not options.path.endswith('.pkl'):
        parser.error('Missing argument or file extension not valid. Path is required.')

    path = options.path

    print('Deserializing pkl memory')
    pkl_memory = deserialize(path)

    observations, pi_s, game_results = list(zip(*pkl_memory))

    observations = np.asarray(observations)
    pi_s = np.asarray(pi_s)
    game_results = np.asarray(game_results).astype(np.float64)

    examples = (observations, pi_s, game_results)

    n_examples = len(observations)
    print(f'Number of examples: {n_examples}')

    print('Converting observations and pi_s to byte string')

    byte_observations = []
    for i in range(len(observations)):
        byte_observations.append(observations[i].tobytes())
    byte_pi_s = []
    for i in range(len(pi_s)):
        byte_pi_s.append(pi_s[i].tobytes())

    converted_examples = (byte_observations, byte_pi_s, game_results)

    tfrecord_path = path[:-3] + 'tfrecord'

    print(f'Serializing and writing examples to {tfrecord_path}')
    with tf.io.TFRecordWriter(tfrecord_path) as writer:
        for i in range(n_examples):
            example = serialize_example(byte_observations[i], byte_pi_s[i], game_results[i])
            writer.write(example)
