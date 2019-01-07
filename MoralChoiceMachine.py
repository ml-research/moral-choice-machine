import tensorflow as tf
import tensorflow_hub as hub
from scipy import spatial
from util import *
import numpy as np
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# Set logging output.
tf.logging.set_verbosity(tf.logging.INFO)
# Import the Universal Sentence Encoder's TF Hub module
embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/1")
logging.info('Import done!')

########################################################################################################################


def mcm_overall(template, insert, log=True):
    """
    Moral Choice Machine for an overall bias - takes a list of inserts and a template and calculates the overall bias
    for each insertion
    :param template:    Question template to calculate an overall bias, e.g. gender or moral - list of [q, a1, a2]
                        Questions include '{}' as a place holder for the inserts.
    :param insert:      List of different inserts for the question template.
    :param log:         True for detailed information in logging output. Default: True
    :return:            the overall bias for each insert - list of [insert, bias]
    """
    # logging.info('mcm_overall --- start')
    d = mcm(list([x[0].format(i), x[1], x[2]] for i in insert for x in template), False)

    res = []
    for chunk in chunks(d, n=len(template)):    # n = number of sentences in the template
        biases = [x[0] for x in chunk]          # get only biases
        questions = [x[1] for x in chunk]
        overall_bias = (round(sum(biases), 4))

        res.append([overall_bias, questions])

    j = 0
    for i in insert:
        overall_bias = res[j][0]
        questions = res[j][1]

        res[j] = [overall_bias, i]

        if False in [i in q for q in questions]:
            logging.error('mcm_overall --- wrong value considered for overall bias')

        if log:
            logging.info('mcm_overall --- bias = %.3f' % overall_bias + ' - insert: ' + i + ')')
        j += 1
    # logging.info('mcm_overall --- end')

    return res


def mcm(data, log=True):
    """
    Moral Choice Machine - takes a set of questions with two possible answers and identifies the best by USE rating
    :param data:    list of lists of the form [q, a1, a2]
    :param log:     True for detailed information in logging output. Default: True
    :return:        input list extended by biases - [bias (float), q (string), a1 (sting), a2 (string)]
    """
    # merge strings to single list (to compute all embeddings with a single session)
    merged = []
    for elem in data:
        merged.extend(elem)

    # calculate embeddings and split in lists of the form [q,a,a] again
    embed_list = chunks(get_sen_embedding(merged), 3)
    ret = []

    for i, line in enumerate(data):
        embedding = embed_list[i]

        q_a1_dist = 1 - spatial.distance.cosine(np.array(embedding[0]), np.array(embedding[1]))
        q_a2_dist = 1 - spatial.distance.cosine(np.array(embedding[0]), np.array(embedding[2]))

        bias = q_a2_dist - q_a1_dist

        ret.append([bias, line[0], line[1], line[2]])

        if log:
            if bias > 0:
                logging.info('mcm --- bias = %.3f' % bias + ' - q: ' + line[0] + ' | answer: ' + line[2] + ' ('
                             + str(q_a2_dist) + ') | alternative: ' + line[1] + ' (' + str(q_a1_dist) + ')')
            elif bias < 0:
                logging.info('mcm --- bias = %.3f' % bias + ' - q: ' + line[0] + ' | answer: ' + line[1] + ' ('
                             + str(q_a1_dist) + ') | alternative: ' + line[2] + ' (' + str(q_a2_dist) + ')')
            elif bias == 0:
                logging.info('mcm --- bias = %.3f' % bias + ' - q: ' + line[0] + ' | both answers are equally correct')
    return ret


def get_sen_embedding(messages):
    """
    Generate embeddings for an undefined number of sentences
    :param messages:    list of stings
    :param log:         True for detailed information in logging output. Default: True
    :return:            Numerical presentations of input sentences - list of vectors
    """
    # logging.info('get_sen_embedding --- start')

    ret = []
    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        message_embeddings = session.run(embed(messages))

        for i, message_embedding in enumerate(np.array(message_embeddings).tolist()):
            ret.append(message_embedding)
    # logging.info('get_sen_embedding --- end')
    return ret
