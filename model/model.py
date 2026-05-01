import copy
from time import time
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
        self._soluzioni = set()

    def worstCase(self, nerc, maxY, maxH):
        self.loadEvents(nerc)
        self._eventi_sorted = sorted(self._listEvents, key=lambda x: x.date_event_began)
        self._n_chiamate = 0
        self._n_soluzioni = 0
        self._soluzioni = set()
        start_time = time()
        self.ricorsione([], maxY, maxH, 0, 0, set())
        end_time = time()
        print(f"Numero chiamate: {self._n_chiamate}")
        print(f"Numero soluzioni: {self._n_soluzioni}")
        print(f"Elapsed time: {end_time - start_time}")
        return

    def ricorsione(self, parziale, maxY, maxH, pos, num_ore, visited):
        self._n_chiamate += 1
        if num_ore > maxH:
            sol = parziale[0:len(parziale) - 1]
            last_ev = parziale[-1]
            ore_last_event = (last_ev.date_event_finished - last_ev.date_event_began).total_seconds() / 3600
            if not tuple(sol) in self._soluzioni and len(sol) > 0 and self._is_valid(sol, maxY):
                self._soluzioni.add(tuple(copy.deepcopy(sol)))
                self._n_soluzioni += 1
                print(f"Soluzione parziale: {sol}, ore: {num_ore - ore_last_event}")
            return
        else:
            for i in range(pos, len(self._eventi_sorted)):    # Itero solo sugli eventi rimanenti
                evento = self._eventi_sorted[i]
                ore_evento = (evento.date_event_finished - evento.date_event_began).total_seconds() / 3600
                if evento not in visited:
                    parziale.append(evento)
                    visited.add(evento)
                    self.ricorsione(parziale, maxY, maxH, i+1, num_ore + ore_evento, visited)
                    visited.remove(evento)
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

    def get_best_solution(self, nerc, maxY, maxH):
        best_sol = None
        best_clients = 0
        best_hours = 0

        self.worstCase(nerc, maxY, maxH)

        for sol in self._soluzioni:
            clienti_coinvolti = 0
            hours = 0
            for event in sol:
                clienti_coinvolti += event.customers_affected
                hours += (event.date_event_finished - event.date_event_began).total_seconds() / 3600
            if clienti_coinvolti > best_clients:
                best_clients = clienti_coinvolti
                best_sol = copy.deepcopy(sol)
                best_hours = hours

        return {"sol": best_sol, "clients": best_clients, "hours": best_hours}
