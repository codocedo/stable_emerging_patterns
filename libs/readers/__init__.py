"""
CONTAINER OF READERS
YOU HAVE A NEW FILE FORMAT?
IMPLEMENTED IT HERE!!!
"""

import subprocess

def get_number_of_objects(fname):
    """
    COUNT THE NUMBER OF LINES IN A FILE USING UNIX'S wc
    http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
    """
    proc = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    result, err = proc.communicate()
    if proc.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])



def read_plain_representations(file_path):
    """
    file_path: path to the context
    READ OBJECT REPRESENTATIONS IN A STREAMING MANNER.
    DO NOT PARSE THINGS
    """
    with open(file_path, 'r') as fin:
        for line in fin:
            yield line.replace('\n', '')


def read_object_representations(file_path, separator=" "):
    """
    PARSE OBJECT REPRESENTATIONS FROM PLAIN CSV
    YIELDS A SET OF INTEGERS
    """
    for line in read_plain_representations(file_path):
        if line != '':
            yield set([int(i) for i in line.split(separator)])



def read_map(filepath):
    """
    READ OBJECT AND ATTRIBUTES MAPS
    ENTRY FILE IS A TEXT WHERE OBJECTS AND ATTRIBUTES ARE LISTED ONE PER LINE
    LINE WITH JUST # IS THE SEPARATOR OF OBJECTS AND ATTRIBUTES
    e.g.
    g1
    g2
    #
    m1
    m2
    """
    lines = file(filepath).read().split('#\n')
    objects = {j:i.strip() for j, i in enumerate(lines[0].split('\n')) if i.strip() != ''}
    attributes = {j:i.strip() for j, i in enumerate(lines[1].split('\n')) if i.strip() != ''}
    return objects, attributes
