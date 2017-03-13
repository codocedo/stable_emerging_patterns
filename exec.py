from __future__ import print_function
import sys
from libs.readers import read_object_representations, get_number_of_objects




def lexo(set_a, set_b):
    """
    LEXICAL COMPARISON BETWEEN TWO SETS OF INTEGERS
    """
    return tuple(sorted(set_a)) <= tuple(sorted(set_b))

class Context(object):
    """
    CONTEXT MANAGER
    """
    def __init__(self, **params):
        if params['filename'] != None:
            print(params['filename'], params.get('separator', ' '), params)
            self.load_ctx(filename=params['filename'])

    def load_ctx(self, filename, separator=' '):
        """
        Formal Context as a list of sets
        """
        # READ THE CONTEXT
        self.ctx = list([B for B in read_object_representations(filename,
                                                                separator=separator)])
        # OBJ COUNTER
        self.glen = len(self.ctx)
        # MAP ATTRIBUTES TO INDICES
        self.mmap = {j:i for i, j in enumerate(sorted(reduce(lambda x, y: x.union(y), self.ctx)))}
        # REGENERATE NEW CONTEXT WITH INDEXED ATTRIBUTES
        self.ctx = [set([self.mmap[i] for i in attributes]) for attributes in self.ctx]
        # ATT COUNTER
        self.mlen = len(self.mmap)

        # INVERTED CONTEXT
        self.ctxi = [set([]) for i in xrange(self.mlen)]

        for object_id, attributes in enumerate(self.ctx):
            for att in attributes:
                self.ctxi[att].add(object_id)


def cbo(extent, intent, current_attribute, ctx, depth=0, **cbo_params):
    """
    extent: SET OF INTEGERS
    intent: SET OF INTEGERS
    current_attribute: indicates the new attribute to add to the intent
    ctx: context manager

    BASIC CLOSE BY ONE ITERATION
    """
    if len(intent) == ctx.mlen or current_attribute >= ctx.mlen:
        return
    cbo_params['print'](extent, intent, depth)
    cache = []
    for j in range(current_attribute, ctx.mlen):
        #print 'J',j,
        if j not in intent:
            new_extent = extent.intersection(ctx.ctxi[j])

            if len(new_extent) > cbo_params['min_sup']*ctx.glen:
                # OBTAIN THE INTENT OF THE NEW EXTENT
                new_intent = reduce(lambda x, y: x.intersection(y),
                                    [ctx.ctx[i] for i in new_extent])
                # CANONICAL TEST
                attributes_j = set(range(j))
                if lexo(intent.intersection(attributes_j),
                        new_intent.intersection(attributes_j)) and new_intent not in cache:
                    cache.append(new_intent)
                    cbo(new_extent, new_intent, j+1, ctx, depth+1, **cbo_params)


def execute_cbo(filepath):
    """
    WRAPPER FOR THE EXECUTION OF CBO
    """
    params = {
        'filename':filepath
    }

    ctx = Context(**params)

    cbo_params = {
        'min_sup':0,
        'print':lambda extent, intent, depth:
                print('\t'*depth, '->',
                      extent,
                      intent,
                     )
    }
    cbo(set(range(ctx.glen)), set([]), -1, ctx, **cbo_params)


if __name__ == "__main__":
    execute_cbo(sys.argv[1])
