from abc import ABC, abstractmethod

class AbsChromosome(ABC):
    @abstractmethod
    def __init__(self, info):
        pass

    @abstractmethod
    def crossover(self, mate):
        pass
    
    @abstractmethod
    def mutate(self, chrom):
        pass
        
    @abstractmethod
    def evaluate(self, chrom):
        pass

    @abstractmethod
    def get_name(self):
        # Name should be camelCase
        pass

    @abstractmethod
    def render(self):
        pass
