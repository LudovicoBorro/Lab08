import copy

from database.DAO import DAO
from model.powerOutages import Event
from datetime import datetime

class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self._eventi_sorted = None
        self._n_chiamate = 0
        self._n_soluzioni = 0
        self._soluzioni = []
        self._num_ore = 0

    def worstCase(self, nerc, maxY, maxH):
        self.loadEvents(nerc)
        self._eventi_sorted = sorted(self._listEvents, key=lambda x: x.date_event_began)
        self._n_chiamate = 0
        self._n_soluzioni = 0
        self._num_ore = 0
        self._soluzioni = []
        self.ricorsione([], maxY, maxH, 0)

    def ricorsione(self, parziale, maxY, maxH, pos):
        self._n_chiamate += 1
        # Condizione di terminazione
        if self._num_ore > maxH:
            if self._is_valid(parziale, maxY):
                parziale_copy = copy.deepcopy(parziale[0:len(parziale)]) # Escludo l'ultimo elemento che mi ha fatto superare il limite massimo di ore
                self._soluzioni.append(parziale_copy)
                self._n_soluzioni += 1
                print(f"Soluzione parziale: {parziale_copy}, con numero di ore: {self._num_ore}")
                self._num_ore = 0
        # Condizione di ricorsione:
        else:
            for i in range(len(self._eventi_sorted)):
                evento = self._eventi_sorted[pos]
                print(f"Evento: {evento} -- Pos: {pos}")
                parziale.append(evento)
                self._num_ore += (evento.date_event_finished - evento.date_event_began).total_seconds() / 3600
                self.ricorsione(parziale, maxY, maxH, pos+1)
                parziale.pop()

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    @property
    def listNerc(self):
        return self._listNerc

    def _is_valid(self, parziale, maxY):
        eventi_sorted_begin = sorted(parziale, key=lambda x: x.date_event_began)
        eventi_sorted_end = sorted(parziale, key=lambda x: x.date_event_finished, reverse=True)
        min_event = eventi_sorted_begin[0]
        max_event = eventi_sorted_end[0]
        delta_years = max_event.date_event_finished.year - min_event.date_event_began.year
        if delta_years > maxY:
            return False
        return True