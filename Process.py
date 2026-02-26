class Process:
    _memoria = -1
    _instrucciones = -1
    _estado = ""

    def __init__(self, memoria:int, instrucciones:int):
        self.memoria = memoria
        self.instrucciones = instrucciones