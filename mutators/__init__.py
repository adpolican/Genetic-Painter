import mutators.solidtriangles

class MutatorNameError:
    pass

mutator_map = {'solid_triangles': mutators.solidtriangles}

def get_mutator(name):
    try:
        return mutator_map[name]
    except:
        raise MutatorNameError('Invalid mutator name')
