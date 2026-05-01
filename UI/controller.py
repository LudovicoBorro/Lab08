import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        self._view._txtOut.controls.clear()

        val_nerc = self._view._ddNerc.value
        max_anni = self._view._txtYears.value
        max_ore = self._view._txtHours.value

        self._check_txt(max_anni, max_ore, val_nerc)

        max_anni = int(max_anni)
        max_ore = int(max_ore)

        # Richiamo il metodo del modello per risultato algoritmo ricorsivo
        self._model.worstCase(self._idMap.get(val_nerc), max_anni, max_ore)

    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v

    def _check_txt(self, max_anni, max_ore, val_nerc):
        if max_anni is None:
            self._view.create_alert("Inserire un valore per gli anni massimi!")
            return

        if max_ore is None:
            self._view.create_alert("Inserire un valore per le ore massime!")
            return

        if val_nerc is None:
            self._view.create_alert("Inserire un valore nel campo nerc!")
            return

        try:
            max_anni_int = int(max_anni)
        except ValueError:
            self._view.create_alert("Attenzione! Inserire un numero valido per gli anni massimi!")
            return

        try:
            max_ore_int = int(max_ore)
        except ValueError:
            self._view.create_alert("Attenzione! Inserire un numero valido per le ore massime!")
            return