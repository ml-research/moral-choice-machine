import itertools, gensim, logging, os


def chunks(l, n):
    """
    splits a list of arbitrary lenght in a list of lists of lenght n while keeping the original order
    :param l:       list that is to split
    :param n:       length of returned sublists
    :return:        list of sublists
    """
    n = max(1, n)
    return list(l[i:i+n] for i in range(0, len(l), n))


def bar(iteration, maxIteration, freq = 50, text=''):
    """
    fancy status update while execution. Call in each iteration of a running function with fixed number of iterations
    :param iteration:           current iteration
    :param maxIteration:        last iteration
    :param freq:                number of outputs
    :param text:                (string) message
    """
    if (iteration != 0) and int(iteration % (maxIteration / freq)) == 0:
        bar = '|'
        for _ in itertools.repeat(None, int(iteration / (maxIteration / freq))):
            bar += '='
        for _ in itertools.repeat(None, freq - int(iteration / (maxIteration / freq))):
            bar += '-'
        bar += '|'
        logging.info(text + bar + str(iteration / (maxIteration / 100)) + '% | Iteration:' + str(iteration) + '/' + str(maxIteration))


def find_all_txt(dir):
    """
    Finds all text files in a directory.
    :param dir:     (string) directory
    :return:        List of files
    """
    all = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".txt"):
                all.append(root + "/" + file)
    return all


def find_all_files(dir):
    """
    Finds all files in a directory.
    :param dir:     (string) directory
    :return:        List of files
    """
    all = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            all.append(root + "/" + file)
    return all


def get_all_model_tags():
    """
    Get tags of all self created models
    :return: list of [tag, path] of CBOW models, list of [tag, path] of Skip-gram models
    """
    CBOW = []
    SG = []

    # CBOW
    for elem in find_all_files('./models/models/CBOW/'):
        CBOW.append([elem[22:], elem])

    # Skip-grams
    for elem in find_all_files('./models/models/SG/'):
        SG.append([elem[20:], elem])

    return CBOW, SG


def low(list):
    """
    Transforms any string included in a list into lowercase
    :param list:        list of strings
    :return:            list of strings (lowercase)
    """
    out = [x.lower() for x in list]
    return out
