from abc import ABC, abstractmethod

class AbsChromosome(ABC):
    @abstractmethod
    def __init__(self, info):
        pass

    @abstractmethod
    def crossover(self, mate, context):
        pass
    
    @abstractmethod
    def mutate(self):
        pass
        
    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def get_name(self):
        # Name should be camelCase
        pass

    @abstractmethod
    def render(self):
        pass
