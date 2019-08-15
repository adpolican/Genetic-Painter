import mutators.solidtriangles
import mutators.eqtriangles

class MutatorNameError:
    pass

mutator_map = {
   'solidtriangles': mutators.solidtriangles,
   'eqtriangles': mutators.eqtriangles,
              }

def get_mutator(name):
    try:
        return mutator_map[name]
    except:
        raise MutatorNameError('Invalid mutator name')
