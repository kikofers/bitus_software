from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json
import sys
import random

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
        mainit_aktivo_seriju(len(seriju_saraksts)-1)
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
        default_darbinieku_saraksts[vards]["iekļauts"] =  jauns_statuss
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

"""
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
"""

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

""" Globālie mainīgie, kas darbina kodu. """
# Nodibina sēriju sarakstu, kā arī sēriju indeksu.
seriju_saraksts = []
aktiva_serija = None

# Nodibina default pozīciju un darbinieku sarakstus, kuri tiks iekopēti jaunās sērijās.
default_poziciju_saraksts = {
    "Pozīcija 1": { "laiks": 0.66, "gabali": random.randint(1, 10) },
    "Pozīcija 2": { "laiks": 1.33, "gabali": random.randint(1, 10) },
    "Pozīcija 3": { "laiks": 0.5, "gabali": random.randint(1, 10) },
    "Pozīcija 4": { "laiks": 0.33, "gabali": random.randint(1, 10) },
    "Pozīcija 5": { "laiks": 1.33, "gabali": random.randint(1, 10) },
    "Pozīcija 6": { "laiks": 1, "gabali": random.randint(1, 10) },
    "Pozīcija 7": { "laiks": 0.8, "gabali": random.randint(1, 10) },
    "Pozīcija 8": { "laiks": 2, "gabali": random.randint(1, 10) },
    "Pozīcija 9": { "laiks": 0.66, "gabali": random.randint(1, 10) }
}

default_darbinieku_saraksts = {
    "Māris": { "efektivitāte": 1.2, "iekļauts": False },
    "Uldis": { "efektivitāte": 1.2, "iekļauts": False },
    "Juris": { "efektivitāte": 1.2, "iekļauts": False },
    "Sandis": { "efektivitāte": 0.3, "iekļauts": False },
    "Ervīns": { "efektivitāte": 0.1, "iekļauts": False },
    "Jānis": { "efektivitāte": 0.1, "iekļauts": False },
    "Aigars": { "efektivitāte": 0.3, "iekļauts": False },
    "Ingus": { "efektivitāte": 1.0, "iekļauts": True },
    "Alvis": { "efektivitāte": 0.8, "iekļauts": False },
    "Maksims": { "efektivitāte": 0.1, "iekļauts": False }
}

# Aprēķiniem nepieciešamie mainīgie.
krasotavas_kludas_koeficients = 0.03
kvalitates_parbaudes_koeficients = 0.03
arejie_faktori = 0

# Aprēķina cik sērijā ir daudz darba, mērot stundās.
def aprekinat_darba_laiku():
    if aktiva_serija is not None:
        current_series = seriju_saraksts[aktiva_serija - 1]
        total_time = 0
        for pozicija, info in current_series["poziciju_saraksts"].items():
            total_time += info["laiks"] * info["gabali"]
        return total_time
    else:
        return None

# Aprēķina cik ilgi aizņems laiks, lai izpildītu sēriju, ņemot vērā tikai tos darbiniekus, kuri ir iekļauti.
def aprekinat_izpildes_laiku():
    if aktiva_serija is not None:
        current_series = seriju_saraksts[aktiva_serija - 1]

        kopejais_laiks = aprekinat_darba_laiku()
        kopeja_efektivitate = 0

        for darbinieks in current_series["darbinieku_saraksts"].values():
            if darbinieks["iekļauts"]:
                kopeja_efektivitate += darbinieks["efektivitāte"]
        
        kopejais_laiks += kopejais_laiks * krasotavas_kludas_koeficients
        kopejais_laiks += kopejais_laiks * kvalitates_parbaudes_koeficients
        kopejais_laiks += arejie_faktori

        # print("Kopējā darbinieku efektivitāte:", round(kopeja_efektivitate, 1))

        kopejais_laiks /= kopeja_efektivitate
        # print(f"Sēriju izpildes laiks: {round(kopejais_laiks, 1)}h.")
        # print(f"Vajadzēs {round(kopejais_laiks / 8, 1)}d.")
        return kopejais_laiks

    else:
        return None

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tētim programma")
        self.setGeometry(100, 100, 600, 400)

        self.UiComponents()

        self.update_serijas_nosaukumu()
        self.update_pozicijas_datus()
        self.update_darbinieku_datus()
        
        self.show()

    def UiComponents(self):
        Series_font = QFont("Asap Medium", 24, QFont.DemiBold)
        Position_font = QFont("Asap Medium", 13, QFont.Medium)
        header_font = QFont("Asap Medium", 13, QFont.Bold)

        self.serijas_nosaukums = QLabel("", self)
        self.serijas_nosaukums.setFont(Series_font)
        self.serijas_nosaukums.setGeometry(10, 3, 250, 60)

        jauna_serija_poga = QPushButton("Jauna sērija", self)
        jauna_serija_poga.setGeometry(1765, 3, 150, 60)
        jauna_serija_poga.clicked.connect(self.start_new_series)

        atgriezties_poga = QPushButton("Pēdējā sērija", self)
        atgriezties_poga.setGeometry(1600, 3, 150, 60)
        atgriezties_poga.clicked.connect(self.return_to_latest_series)

        nakamas_poga = QPushButton("Nākamā sērija", self)
        nakamas_poga.setGeometry(1435, 3, 150, 60)
        nakamas_poga.clicked.connect(self.next_series)

        ieprieksejas_poga = QPushButton("Iepriekšējā sērija", self)
        ieprieksejas_poga.setGeometry(1270, 3, 150, 60)
        ieprieksejas_poga.clicked.connect(self.previous_series)

        self.tabula_pozicijas = QTableWidget(self)
        self.tabula_pozicijas.setRowCount(len(default_poziciju_saraksts))
        self.tabula_pozicijas.setColumnCount(3)
        self.tabula_pozicijas.setGeometry(10, 70, 542, 453)
        self.tabula_pozicijas.setHorizontalHeaderLabels(["Pozīcija", "Gabalu skaits", "Mainīt skaitu"])
        self.tabula_pozicijas.horizontalHeader().setFont(header_font)
        self.tabula_pozicijas.setColumnWidth(0, 170)
        self.tabula_pozicijas.setColumnWidth(1, 190)
        self.tabula_pozicijas.setColumnWidth(2, 180)
        self.tabula_pozicijas.verticalHeader().setVisible(False)
        self.tabula_pozicijas.setFont(Position_font)
        
        self.tabula_darbinieku = QTableWidget(self)
        self.tabula_darbinieku.setRowCount(len(default_darbinieku_saraksts))
        self.tabula_darbinieku.setColumnCount(4)
        self.tabula_darbinieku.setGeometry(560, 70, 698, 453)
        self.tabula_darbinieku.setHorizontalHeaderLabels(["Darbinieks", "Efektivitāte", "Mainīt efekt.", "Iekļauts"])
        self.tabula_darbinieku.horizontalHeader().setFont(header_font)
        self.tabula_darbinieku.setColumnWidth(1, 180)
        self.tabula_darbinieku.setColumnWidth(2, 190)
        self.tabula_darbinieku.setColumnWidth(3, 150)
        self.tabula_darbinieku.verticalHeader().setVisible(False)
        self.tabula_darbinieku.setFont(Position_font)

        self.showMaximized()

    def update_darbinieku_datus(self):
        if aktiva_serija is not None:
            current_series = seriju_saraksts[aktiva_serija - 1]
            
            # Save the current scroll position
            scroll_position = self.tabula_darbinieku.verticalScrollBar().value()
            
            self.tabula_darbinieku.clear()
            self.tabula_darbinieku.setRowCount(len(current_series["darbinieku_saraksts"]))
            self.tabula_darbinieku.setHorizontalHeaderLabels(["Darbinieks", "Efektivitāte", "Mainīt efekt.", "Iekļauts"])  # Reset headers

            for i, (darbinieks, info) in enumerate(current_series["darbinieku_saraksts"].items()):
                # Darbinieka kolonna.
                item_darbinieks = QTableWidgetItem(darbinieks)
                item_darbinieks.setTextAlignment(Qt.AlignCenter)
                self.tabula_darbinieku.setItem(i, 0, item_darbinieks)

                # Efektivitātes kolonna.
                item_efektivitate = QTableWidgetItem(f"{info['efektivitāte']:.1f}")
                item_efektivitate.setTextAlignment(Qt.AlignCenter)
                self.tabula_darbinieku.setItem(i, 1, item_efektivitate)

                # Create the "+" button
                plus_button = QPushButton("+")
                plus_button.setFixedSize(35, 35)  # Set button size
                plus_button.setStyleSheet("padding: 0; margin: 0;")
                plus_button.clicked.connect(lambda checked, worker=darbinieks: self.update_efficiency(worker, 0.1))

                # Create the "+" button
                minus_button = QPushButton("-")
                minus_button.setFixedSize(35, 35)  # Set button size
                minus_button.setStyleSheet("padding: 0; margin: 0;")
                minus_button.clicked.connect(lambda checked, worker=darbinieks: self.update_efficiency(worker, -0.1))

                # Create a widget container to hold the buttons
                button_widget = QWidget()
                button_layout = QHBoxLayout()
                button_layout.addWidget(plus_button)
                button_layout.addWidget(minus_button)
                button_layout.setAlignment(Qt.AlignCenter)
                button_layout.setContentsMargins(0, 0, 0, 0)
                button_widget.setLayout(button_layout)

                # Add the button widget to the table
                self.tabula_darbinieku.setCellWidget(i, 2, button_widget)

                # Checkbox for "Iekļauts" status
                checkbox = QCheckBox()
                checkbox.setChecked(info["iekļauts"])  # Set initial state
                checkbox.stateChanged.connect(lambda state, worker=darbinieks: self.update_ieklausanu(worker, state))

                # Add the checkbox in a widget container to center it in the cell
                widget = QWidget()
                layout = QHBoxLayout()
                layout.addWidget(checkbox)
                layout.setAlignment(Qt.AlignCenter)
                widget.setLayout(layout)
                self.tabula_darbinieku.setCellWidget(i, 3, widget)
            
            # Restore the scroll position
            self.tabula_darbinieku.verticalScrollBar().setValue(scroll_position)

    def update_efficiency(self, worker, change):
        current_series = seriju_saraksts[aktiva_serija - 1]
        if worker in current_series["darbinieku_saraksts"]:
            current_series["darbinieku_saraksts"][worker]["efektivitāte"] += change
            # Ensure gabali doesn't go below zero
            current_series["darbinieku_saraksts"][worker]["efektivitāte"] = max(0, current_series["darbinieku_saraksts"][worker]["efektivitāte"])
            # print([worker, current_series["darbinieku_saraksts"][worker]["efektivitāte"]])
            self.update_darbinieku_datus()
            saglabat_datus()

    def update_ieklausanu(self, worker, state):
        current_series = seriju_saraksts[aktiva_serija - 1]
        current_series["darbinieku_saraksts"][worker]["iekļauts"] = bool(state)
        saglabat_datus()

    def update_pozicijas_datus(self):
        if aktiva_serija is not None:
            active_positions = seriju_saraksts[aktiva_serija - 1]["poziciju_saraksts"]
            self.tabula_pozicijas.clear()
            self.tabula_pozicijas.setRowCount(len(active_positions))
            self.tabula_pozicijas.setHorizontalHeaderLabels(["Pozīcija", "Gabalu skaits", "Mainīt efekt.", "Mainīt skaitu"])  # Reset headers

            for i, (pozicija, info) in enumerate(active_positions.items()):
                item_pozicija = QTableWidgetItem(pozicija)
                item_gabali = QTableWidgetItem(str(info["gabali"]))

                item_pozicija.setTextAlignment(Qt.AlignCenter)
                item_gabali.setTextAlignment(Qt.AlignCenter)

                self.tabula_pozicijas.setItem(i, 0, item_pozicija)
                self.tabula_pozicijas.setItem(i, 1, item_gabali)

                # Create the "+" button
                plus_button = QPushButton("+")
                plus_button.setFixedSize(35, 35)  # Set button size
                plus_button.setStyleSheet("padding: 0; margin: 0;")
                plus_button.clicked.connect(lambda checked, position=pozicija: self.update_gabali(position, 1))

                # Create the "-" button
                minus_button = QPushButton("-")
                minus_button.setFixedSize(35, 35)  # Set button size
                minus_button.setStyleSheet("padding: 0; margin: 0;")
                minus_button.clicked.connect(lambda checked, position=pozicija: self.update_gabali(position, -1))

                # Create a widget container to hold the buttons
                button_widget = QWidget()
                button_layout = QHBoxLayout()
                button_layout.addWidget(plus_button)
                button_layout.addWidget(minus_button)
                button_layout.setAlignment(Qt.AlignCenter)
                button_layout.setContentsMargins(0, 0, 0, 0)
                button_widget.setLayout(button_layout)

                # Add the button widget to the table
                self.tabula_pozicijas.setCellWidget(i, 2, button_widget)
                
    def update_gabali(self, position, change):
        current_series = seriju_saraksts[aktiva_serija - 1]
        if position in current_series["poziciju_saraksts"]:
            current_series["poziciju_saraksts"][position]["gabali"] += change
            # Ensure gabali doesn't go below zero
            current_series["poziciju_saraksts"][position]["gabali"] = max(0, current_series["poziciju_saraksts"][position]["gabali"])
            self.update_pozicijas_datus()
            saglabat_datus()

    def update_serijas_nosaukumu(self):
        colors = ["black", "blue", "green", "red"]
        selected_color = colors[(aktiva_serija - 1) % 4] if aktiva_serija else "orange"
        self.serijas_nosaukums.setText(f"Sērija {aktiva_serija if aktiva_serija else 'Nav'}")
        self.serijas_nosaukums.setStyleSheet(f"color: {selected_color};")
        self.serijas_nosaukums.show()

    def start_new_series(self):
        jauna_serija()
        self.update_serijas_nosaukumu()
        self.update_pozicijas_datus()
        self.update_darbinieku_datus()

    def return_to_latest_series(self):
        if aktiva_serija is None:
            return None
        else:
            if aktiva_serija == len(seriju_saraksts):
                return None
            else:
                mainit_aktivo_seriju(len(seriju_saraksts)-1)
                self.update_serijas_nosaukumu()
                self.update_pozicijas_datus()
                self.update_darbinieku_datus()

    def next_series(self):
        if aktiva_serija is None:
            return None
        else:
            mainit_aktivo_seriju(aktiva_serija)
            self.update_serijas_nosaukumu()
            self.update_pozicijas_datus()
            self.update_darbinieku_datus()

    def previous_series(self):
        if aktiva_serija is None:
            return None
        else:
            mainit_aktivo_seriju(aktiva_serija - 2)
            self.update_serijas_nosaukumu()
            self.update_pozicijas_datus()
            self.update_darbinieku_datus()

# Running the application
ieladet_datus()
app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())



# print("Alvis dienā normu izdara 9. pozīcijai: ", int(0.8*8/0.66))	
# print("Ingus dienā normu izdara 9. pozīcijai: ", int(1.0*8/0.66))
# print("Māris dienā normu izdara 9. pozīcijai: ", int(1.2*8/0.66))

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