from experta import *

class Weather(Fact):
    pass

class Route(Fact):
    pass

class Contigencies(KnowledgeEngine):
    @Rule(Weather(Type="Frost"))
    def handle_frost(self):
        return "Frost"