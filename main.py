from gui.window import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

# TODO: izlēmu, ka priekš ātrdarbības es izveidošu lokālu datu kopiju, kurā saglabāšu
#       nolasītos datus no datubāzes. Tādējādi, ja lietotājs veic izmaiņas, es varu
#       veikt tās lokāli, un paralēli atjaunot datubāzi, nevis katru reizi nolasīt datus.
#       Lokālie dati tiks attēloti tabulās.
#
#       Ir arī updatota cenu tabula datubāzē.
#
#       Principā nāksies pilnīgi katru tabulu no datubāzes saglabāt lokāli, lai programma ir ātra.
#
#       Jāizlasa ko DeepSeek AI teiks par to tabulu refresh. Un tad principā skatoties pēc test.py
#       faila varēšu saprast ko darīt tālāk.

""" Funkcijas, kuras aprēķina darba laiku un izpildes laiku.
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
"""

""" UI prasības:
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())