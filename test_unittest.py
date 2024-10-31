import unittest

from tetim_programma import (
    mainit_laiku, mainit_efektivitati, mainit_ieklausanu, pievienot_darbinieku, dzest_darbinieku,
    jauna_serija, mainit_aktivo_seriju, SERIJA_mainit_gabalus, SERIJA_mainit_laiku,
    SERIJA_mainit_efektivitati, SERIJA_mainit_ieklaušanu, SERIJA_pievienot_darbinieku, SERIJA_dzest_darbinieku,
    default_poziciju_saraksts, default_darbinieku_saraksts, seriju_saraksts
)

class TestTetimProgramma(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global seriju_saraksts, aktiva_serija
        seriju_saraksts = []
        aktiva_serija = None
        jauna_serija()  # Create the first series
        jauna_serija()  # Create the second series

    def setUp(self):
        # Reset the active series before each test
        global aktiva_serija
        aktiva_serija = seriju_saraksts[0]  # Set the first series as active

    def test_mainit_laiku(self):
        mainit_laiku("Pozīcija 1", 15)
        self.assertEqual(default_poziciju_saraksts["Pozīcija 1"]["laiks"], 15)

    def test_mainit_efektivitati(self):
        mainit_efektivitati("Māris Zariņš", 2.5)
        self.assertEqual(default_darbinieku_saraksts["Māris Zariņš"]["efektivitāte"], 2.5)

    def test_mainit_ieklausanu(self):
        mainit_ieklausanu("Māris Zariņš", False)
        self.assertFalse(default_darbinieku_saraksts["Māris Zariņš"]["iekļauts"])

    def test_pievienot_darbinieku(self):
        pievienot_darbinieku("Jauns Darbinieks", 1.2)
        self.assertIn("Jauns Darbinieks", default_darbinieku_saraksts)
        self.assertEqual(default_darbinieku_saraksts["Jauns Darbinieks"]["efektivitāte"], 1.2)

    def test_dzest_darbinieku(self):
        dzest_darbinieku("Māris Zariņš")
        self.assertNotIn("Māris Zariņš", default_darbinieku_saraksts)

    def test_SERIJA_mainit_gabalus(self):
        SERIJA_mainit_gabalus("Pozīcija 1", 10)
        self.assertEqual(seriju_saraksts[0]["poziciju_saraksts"]["Pozīcija 1"]["gabali"], 10)

    def test_SERIJA_mainit_laiku(self):
        SERIJA_mainit_laiku("Pozīcija 1", 20)
        self.assertEqual(seriju_saraksts[0]["poziciju_saraksts"]["Pozīcija 1"]["laiks"], 20)

    def test_SERIJA_mainit_efektivitati(self):
        SERIJA_mainit_efektivitati("Māris Zariņš", 3.0)
        self.assertEqual(seriju_saraksts[0]["darbinieku_saraksts"]["Māris Zariņš"]["efektivitāte"], 3.0)

    def test_SERIJA_mainit_ieklaušanu(self):
        SERIJA_mainit_ieklaušanu("Māris Zariņš", False)
        self.assertFalse(seriju_saraksts[0]["darbinieku_saraksts"]["Māris Zariņš"]["iekļauts"])

    def test_SERIJA_pievienot_darbinieku(self):
        SERIJA_pievienot_darbinieku("Jauns Darbinieks", 1.5)
        self.assertIn("Jauns Darbinieks", seriju_saraksts[0]["darbinieku_saraksts"])
        self.assertEqual(seriju_saraksts[0]["darbinieku_saraksts"]["Jauns Darbinieks"]["efektivitāte"], 1.5)

    def test_SERIJA_dzest_darbinieku(self):
        SERIJA_dzest_darbinieku("Māris Zariņš")
        self.assertNotIn("Māris Zariņš", seriju_saraksts[0]["darbinieku_saraksts"])

if __name__ == '__main__':
    unittest.main()