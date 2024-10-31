import json
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox

""" Globālie mainīgie un funkcijas, kas darbina kodu. """
# Nodibina sēriju sarakstu, kā arī sēriju indeksu.
seriju_saraksts = []
serijas_indekss = None

# Nodibina default pozīciju un darbinieku sarakstus, kuri tiks iekopēti jaunās sērijās.
default_poziciju_saraksts = {
    "Pozīcija 1": { "laiks": 0.66, "gabali": 0 },
    "Pozīcija 2": { "laiks": 1.33, "gabali": 0 },
    "Pozīcija 3": { "laiks": 0.5, "gabali": 0 },
    "Pozīcija 4": { "laiks": 0.33, "gabali": 0 },
    "Pozīcija 5": { "laiks": 1.33, "gabali": 0 },
    "Pozīcija 6": { "laiks": 1, "gabali": 0 },
    "Pozīcija 7": { "laiks": 0.8, "gabali": 0 },
    "Pozīcija 8": { "laiks": 2, "gabali": 0 },
    "Pozīcija 9": { "laiks": 0.66, "gabali": 0 }
}

default_darbinieku_saraksts = {
    "Māris": { "efektivitāte": 1.2, "iekļauts": True },
    "Uldis": { "efektivitāte": 1.2, "iekļauts": True },
    "Juris": { "efektivitāte": 1.2, "iekļauts": True },
    "Sandis": { "efektivitāte": 0.3, "iekļauts": True },
    "Ervīns": { "efektivitāte": 0.1, "iekļauts": True },
    "Jānis": { "efektivitāte": 0.1, "iekļauts": True },
    "Aigars": { "efektivitāte": 0.3, "iekļauts": True },
    "Ingus": { "efektivitāte": 1.0, "iekļauts": True },
    "Alvis": { "efektivitāte": 0.8, "iekļauts": True },
    "Maksims": { "efektivitāte": 0.1, "iekļauts": True }
}

# print("Ingus dienā normu izdara 9. pozīcijai: ", int(1.0*8/0.66))

# Galvenās funkcijas, kuras saglabā un nolasa datus no faila.
def saglabat_datus():
    with open('serijas_data.json', 'w', encoding='utf-8') as f:
        json.dump(seriju_saraksts, f, ensure_ascii=False, indent=4)
    print("Dati saglabāti failā.")

# Ielādē datus no faila.
def ieladet_datus():
    global seriju_saraksts
    try:
        with open('serijas_data.json', 'r', encoding='utf-8') as f:
            seriju_saraksts = json.load(f)
        print("Veiksmīgi nolasīti dati no faila.")
    except FileNotFoundError:
        print("Sērijas datu fails netika atrasts. Tiks izveidots jauns fails.")

""" Funkcijas, kas maina default sarakstus!!! """
# Funkcija maina "laiks" vērtību norādītajai pozīcijai, default pozīciju sarakstā.
def mainit_laiku(pozicija, jaunais_laiks):
    if pozicija in default_poziciju_saraksts:
        default_poziciju_saraksts[pozicija]["laiks"] = jaunais_laiks
        print(f"Pozīcijas '{pozicija}' laiks tika mainīts uz {jaunais_laiks}.")
    else:
        print(f"Pozīcija '{pozicija}' netika atrasta sarakstā.")

# Funkcija maina esoša darbinieka efektivitāti, izmantojot viņa vārdu un jauno efektivitāti, default darbinieku sarakstā.
def mainit_efektivitati(vards, jauna_efektivitate):
    if vards in default_darbinieku_saraksts:
        default_darbinieku_saraksts[vards]["efektivitāte"] = jauna_efektivitate
        print(f"Darbinieka '{vards}' efektivitāte mainīta uz {jauna_efektivitate}.")
    else:
        print(f"Darbinieks '{vards}' nav atrasts sarakstā.")

# Funkcija maina esoša darbinieka iekļaušanas statusu, izmantojot viņa vārdu un jauno statusu, default darbinieku sarakstā.
def mainit_ieklausanu(vards, jauns_statuss):
    if vards in default_darbinieku_saraksts:
        default_darbinieku_saraksts[vards]["iekļauts"] = jauns_statuss
        print(f"Darbinieka '{vards}' iekļaušanas statuss mainīts uz {jauns_statuss}.")
    else:
        print(f"Darbinieks '{vards}' nav atrasts sarakstā.")

# Funkcija pievieno jaunu darbinieku ar norādīto vārdu un efektivitāti, default darbinieku sarakstā.
def pievienot_darbinieku(vards, efektivitate):
    if vards not in default_darbinieku_saraksts:
        default_darbinieku_saraksts[vards] = {
            "efektivitāte": efektivitate,
            "iekļauts": True
        }
        print(f"Darbinieks '{vards}' pievienots ar efektivitāti {efektivitate}.")
    else:
        print(f"Darbinieks '{vards}' jau eksistē sarakstā.")

# Funkcija dzēš norādīto darbinieku no default darbinieku saraksta.
def dzest_darbinieku(vards):
    if vards in default_darbinieku_saraksts:
        del default_darbinieku_saraksts[vards]
        print(f"Darbinieks '{vards}' tika izdzēsts no saraksta.")
    else:
        print(f"Darbinieks '{vards}' netika atrasts sarakstā.")

""" Funkcijas saistībā ar sērijām: """
# Izveido jaunu sēriju, ņemot informāciju no default sarakstiem.
def jauna_serija():
    global aktiva_serija

    # Uztaisa sarakstu kopijas priekš jaunās sērijas, lai neizmainītu default sarakstus.
    poziciju_saraksts = { poz: vals.copy() for poz, vals in default_poziciju_saraksts.items() }
    darbinieku_saraksts = { name: info.copy() for name, info in default_darbinieku_saraksts.items() }

    # Pievieno jauno sēriju kopējam sēriju sarakstam.
    seriju_saraksts.append({
        "poziciju_saraksts": poziciju_saraksts,
        "darbinieku_saraksts": darbinieku_saraksts
    })

    # Iegūst jaunās sērijas indeksu.
    aktiva_serija = len(seriju_saraksts)
    print(f"Uzsākta jauna sērija, tās indekss: {aktiva_serija}.")

    # Save the series data to a file
    saglabat_datus()

# Funkcija, kas maina aktīvo sēriju, pamatojoties uz indeksu.
def mainit_aktivo_seriju(indekss):
    global aktiva_serija
    if 0 <= indekss < len(seriju_saraksts):
        aktiva_serija = indekss + 1  # Sēriju indeksēšana sākas no 0
        print(f"Aktīvā sērija mainīta uz {aktiva_serija}.")
    else:
        print("Norādīts nederīgs sērijas indekss.")

""" Funkcijas saistībā ar pozīciju saraksta mainīšanu konkrētā sērijā: """
# Maina gabalu skaitu noteiktā pozīcijā, aktīvajā sērijā.
def SERIJA_mainit_gabalus(pozicija, jaunie_gabali):
    if aktiva_serija is not None:
        current_series = seriju_saraksts[aktiva_serija - 1]
        if pozicija in current_series["poziciju_saraksts"]:
            current_series["poziciju_saraksts"][pozicija]["gabali"] = jaunie_gabali
            print(f"Uzdevumu skaits pozīcijā '{pozicija}' mainīts uz {jaunie_gabali}.")
        else:
            print(f"Pozīcija '{pozicija}' netika atrasta aktīvajā sērijā.")
    else:
        print("Nav aktīvas sērijas.")

# Funkcija, kas maina pozīcijas laiku noteiktā sērijā.
def SERIJA_mainit_laiku(pozicija, jaunais_laiks):
    if aktiva_serija is not None:
        current_series = seriju_saraksts[aktiva_serija - 1]
        if pozicija in current_series["poziciju_saraksts"]:
            current_series["poziciju_saraksts"][pozicija]["laiks"] = jaunais_laiks
            print(f"Pozīcijas '{pozicija}' laiks mainīts uz {jaunais_laiks}.")
        else:
            print(f"Pozīcija '{pozicija}' netika atrasta aktīvajā sērijā.")
    else :
        print("Nav aktīvas sērijas.")

""" Funkcijas saistībā ar darbinieku saraksta mainīšanu konkrētajā sērijā:"""
# Funkcija, kas maina darbinieka efektivitāti noteiktā sērijā.
def SERIJA_mainit_efektivitati(darbinieks, jauna_efektivitate):
    if aktiva_serija is not None:
        current_series = seriju_saraksts[aktiva_serija - 1]
        if darbinieks in current_series["darbinieku_saraksts"]:
            current_series["darbinieku_saraksts"][darbinieks]["efektivitāte"] = jauna_efektivitate
            print(f"Darbinieka '{darbinieks}' efektivitāte mainīta uz {jauna_efektivitate}.")
        else:
            print(f"Darbinieks '{darbinieks}' netika atrasts aktīvajā sērijā.")
    else:
        print("Nav aktīvas sērijas.")

# Funkcija, kas maina darbinieka iekļaušanu/neiekļaušanu noteiktā sērijā.
def SERIJA_mainit_ieklaušanu(darbinieks, ieklauts):
    if aktiva_serija is not None:
        current_series = seriju_saraksts[aktiva_serija - 1]
        if darbinieks in current_series["darbinieku_saraksts"]:
            current_series["darbinieku_saraksts"][darbinieks]["iekļauts"] = ieklauts
            print(f"Darbinieka '{darbinieks}' iekļaušana mainīta uz {ieklauts}.")
        else:
            print(f"Darbinieks '{darbinieks}' netika atrasts aktīvajā sērijā.")

# Funkcija, kas pievieno darbinieku noteiktā sērijā.
def SERIJA_pievienot_darbinieku(darbinieks, efektivitate):
    if aktiva_serija is not None:
        current_series = seriju_saraksts[aktiva_serija - 1]
        if darbinieks not in current_series["darbinieku_saraksts"]:
            current_series["darbinieku_saraksts"][darbinieks] = {
                "efektivitāte": efektivitate,
                "iekļauts": True
            }
            print(f"Darbinieks '{darbinieks}' pievienots ar efektivitāti {efektivitate}.")
        else:
            print(f"Darbinieks '{darbinieks}' jau eksistē aktīvajā sērijā.")
    else:
        print("Nav aktīvas sērijas.")

# Funkcija, kas dzēš darbinieku no noteiktās sērijas.
def SERIJA_dzest_darbinieku(darbinieks):
    if aktiva_serija is not None:
        current_series = seriju_saraksts[aktiva_serija - 1]
        if darbinieks in current_series["darbinieku_saraksts"]:
            del current_series["darbinieku_saraksts"][darbinieks]
            print(f"Darbinieks '{darbinieks}' tika izdzēsts no aktīvās sērijas.")
        else:
            print(f"Darbinieks '{darbinieks}' netika atrasts aktīvajā sērijā.")
    else:
        print("Nav aktīvas sērijas.")

"""
1. Tā lapiņa arī parādas blakus uz ekrāna.
2. Diagrammā:
2.1 Sarkanā krāsā [2, 5, 6, 8.]
2.2 Dzeltenā krāsā [1, 7, 9.]
2.3. Zaļā krāsa [3, 4.].

3. Printēšanas funkciju, kurā izprintē to diagrammu un apkopojumu.

Apkopojumā:
 * vienību skaits,
 * loga vērtņu skaits (pats savadīs),
 * durvju vērtņu skaits (pats savadīs),
 * rāmju savienošana (pats savadīs),
 * durvju kopējais skaits (pats savadīs),
 * visus tos rezultātus,
 * brīva vieta komentāriem,
"""

# Ielādē sēriju datus no failiem, kad programma tiek palaista.
# ieladet_datus()
# jauna_serija()
# SERIJA_mainit_gabalus("Pozīcija 1", 5)
# SERIJA_mainit_laiku("Pozīcija 1", 10)
# SERIJA_mainit_efektivitati("Māris Zariņš", 2.0)
# SERIJA_mainit_ieklaušanu("Māris Zariņš", False)
# SERIJA_pievienot_darbinieku("Jānis", 1.5)
# SERIJA_dzest_darbinieku("Uldis")
# 
# saglabat_datus()


""" ChatGPT GUI:
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Button to create a new series
        self.new_series_btn = QPushButton('Izveidot jaunu sēriju', self)
        self.new_series_btn.clicked.connect(self.create_new_series)
        layout.addWidget(self.new_series_btn)

        # ComboBox to select active series
        self.series_selector = QComboBox(self)
        self.series_selector.addItems([str(i+1) for i in range(len(seriju_saraksts))])
        self.series_selector.currentIndexChanged.connect(self.change_active_series)
        layout.addWidget(QLabel('Izvēlēties aktīvo sēriju:'))
        layout.addWidget(self.series_selector)

        # Input for changing pieces in a position
        self.position_input = QLineEdit(self)
        self.pieces_input = QSpinBox(self)
        self.change_pieces_btn = QPushButton('Mainīt gabalu skaitu', self)
        self.change_pieces_btn.clicked.connect(self.change_pieces)
        layout.addWidget(QLabel('Pozīcija:'))
        layout.addWidget(self.position_input)
        layout.addWidget(QLabel('Jaunie gabali:'))
        layout.addWidget(self.pieces_input)
        layout.addWidget(self.change_pieces_btn)

        # Input for changing time in a position
        self.time_input = QSpinBox(self)
        self.change_time_btn = QPushButton('Mainīt pozīcijas laiku', self)
        self.change_time_btn.clicked.connect(self.change_time)
        layout.addWidget(QLabel('Jaunais laiks:'))
        layout.addWidget(self.time_input)
        layout.addWidget(self.change_time_btn)

        # Input for changing employee efficiency
        self.employee_input = QLineEdit(self)
        self.efficiency_input = QDoubleSpinBox(self)
        self.efficiency_input.setRange(0, 10)
        self.change_efficiency_btn = QPushButton('Mainīt darbinieka efektivitāti', self)
        self.change_efficiency_btn.clicked.connect(self.change_efficiency)
        layout.addWidget(QLabel('Darbinieks:'))
        layout.addWidget(self.employee_input)
        layout.addWidget(QLabel('Jaunā efektivitāte:'))
        layout.addWidget(self.efficiency_input)
        layout.addWidget(self.change_efficiency_btn)

        # Input for changing employee inclusion
        self.inclusion_checkbox = QCheckBox('Iekļauts', self)
        self.change_inclusion_btn = QPushButton('Mainīt darbinieka iekļaušanu', self)
        self.change_inclusion_btn.clicked.connect(self.change_inclusion)
        layout.addWidget(self.inclusion_checkbox)
        layout.addWidget(self.change_inclusion_btn)

        self.setLayout(layout)
        self.setWindowTitle('Sēriju pārvaldība')
        self.show()

    def create_new_series(self):
        jauna_serija()
        self.series_selector.addItem(str(len(seriju_saraksts)))
        print("Jauna sērija izveidota.")

    def change_active_series(self):
        index = self.series_selector.currentIndex()
        mainit_aktivo_seriju(index)
        print(f"Aktīvā sērija mainīta uz {index + 1}.")

    def change_pieces(self):
        pozicija = self.position_input.text()
        jaunie_gabali = self.pieces_input.value()
        mainit_gabalus(pozicija, jaunie_gabali)

    def change_time(self):
        pozicija = self.position_input.text()
        jaunais_laiks = self.time_input.value()
        mainit_pozicijas_laiku(pozicija, jaunais_laiks)

    def change_efficiency(self):
        darbinieks = self.employee_input.text()
        jauna_efektivitate = self.efficiency_input.value()
        mainit_darbinieku_efektivitati(darbinieks, jauna_efektivitate)

    def change_inclusion(self):
        darbinieks = self.employee_input.text()
        ieklauts = self.inclusion_checkbox.isChecked()
        mainit_darbinieka_ieklaušanu(darbinieks, ieklauts)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
"""