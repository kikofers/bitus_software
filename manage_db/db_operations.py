import sqlite3
import time

class DatabaseOperations:
    def __init__(self):
        self.conn = sqlite3.connect('manage_db/db.sqlite3')
        self.cursor = self.conn.cursor()
        self.conn.execute("PRAGMA foreign_keys = ON;")  # Ensure foreign keys are enforced.
        self.create_tables()

    # Creates the tables if they don't exist.
    def create_tables(self):
        # Series table.
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS series (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_date INTEGER NOT NULL
            )
        ''')

        # Positions table (many-to-1 with series).
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS positions (
                position INTEGER NOT NULL,  -- Position number (1-9)
                value INTEGER DEFAULT 0,    -- Part count for the position
                series_id INTEGER NOT NULL, -- Foreign key to series
                PRIMARY KEY (position, series_id),
                FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE
            )
        ''')

        # Positions table (many-to-1 with series).
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS coefficients (
                coefficient_id INTEGER NOT NULL,
                value INTEGER DEFAULT 0,
                series_id INTEGER NOT NULL,
                PRIMARY KEY (coefficient_id, series_id),
                FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE
            )
        ''')

        # Workers table (many-to-1 with series).
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS workers (
                worker_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT,
                efficiency REAL NOT NULL,
                working BOOL DEFAULT 1,
                series_id INTEGER NOT NULL,
                FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE
            )
        ''')

        # Price table for each position.
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prices (
                price_id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                price REAL DEFAULT 0.0,
                count INTEGER DEFAULT 0,
                series_id INTEGER NOT NULL,
                FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE
            )
        ''')

        self.conn.commit()

    # Manage series:
    # Create a new series.
    def create_series(self):
        # Insert into the series table
        self.cursor.execute('''
            INSERT INTO series (start_date) VALUES (?)
        ''', (int(time.time()),))
        series_id = self.cursor.lastrowid

        # Initialize positions with value = 0 for the new series
        for position in range(1, 10):  # Positions 1 through 9
            self.cursor.execute('''
                INSERT INTO positions (position, value, series_id)
                VALUES (?, 0, ?)
            ''', (position, series_id))

        # Copy coefficients from the latest series (if exists)
        self.cursor.execute('''
            INSERT INTO coefficients (coefficient_id, value, series_id)
            SELECT coefficient_id, value, ? FROM coefficients WHERE series_id = ?
        ''', (series_id, self.get_last_series_id()))

        # If no previous series exists, initialize coefficients with default value 0
        if self.cursor.rowcount == 0:  # No rows were copied
            for coefficient_id in range(1, 12):  # Coefficients 1 through 11
                self.cursor.execute('''
                    INSERT INTO coefficients (coefficient_id, value, series_id)
                    VALUES (?, 0, ?)
                ''', (coefficient_id, series_id))

        # Copy workers from the latest series
        self.cursor.execute('''
            INSERT INTO workers (series_id, name, surname, efficiency, working)
            SELECT ?, name, surname, efficiency, working FROM workers WHERE series_id = ?
        ''', (series_id, self.get_last_series_id()))

        # Copy prices from the latest series, but use the default value for count
        self.cursor.execute('''
            INSERT INTO prices (description, price, series_id)
            SELECT description, price, ? FROM prices WHERE series_id = ?
        ''', (series_id, self.get_last_series_id()))

        self.conn.commit()

    # Get the latest series id.
    def get_last_series_id(self):
        self.cursor.execute('''
            SELECT id FROM series ORDER BY id DESC LIMIT 1
        ''')
        result = self.cursor.fetchone()
        if result is None:
            return 0
        return result[0]



    # Manage workers:
    # Add a worker to the worker table.
    def add_series_worker(self, series_id, name, surname, efficiency):
        query = "INSERT INTO workers (series_id, name, surname, efficiency) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (series_id, name, surname, efficiency))
        self.conn.commit()

    # Delete a worker by given ID.
    def delete_worker(self, worker_id):
        query = "DELETE FROM workers WHERE id = ?"
        self.cursor.execute(query, (worker_id,))
        self.conn.commit()

    # Edit a worker's efficiency.
    def edit_worker(self, worker_id, efficiency):
        query = "UPDATE workers SET efficiency = ? WHERE id = ?"
        self.cursor.execute(query, (efficiency, worker_id))
        self.conn.commit()

    # Reverse the working status of a worker.
    def toggle_working(self, worker_id):
        query = "UPDATE workers SET working = NOT working WHERE id = ?"
        self.cursor.execute(query, (worker_id,))
        self.conn.commit()



    # Manage positions:
    # Add 1 to a position's value.
    def add_one(self, position, series_id):
        query = "UPDATE positions SET value = value + 1 WHERE position = ? AND series_id = ?"
        self.cursor.execute(query, (position, series_id))
        self.conn.commit()

    # Remove 1 from a position's value.
    def remove_one(self, position, series_id):
        query = "UPDATE positions SET value = value - 1 WHERE position = ? AND series_id = ?"
        self.cursor.execute(query, (position, series_id))
        self.conn.commit()

    # Set the value of a position.
    def set_position(self, position, series_id, value):
        query = "UPDATE positions SET value = ? WHERE position = ? AND series_id = ?"
        self.cursor.execute(query, (value, position, series_id))
        self.conn.commit()

    # Reset all positions to 0 for a given series_id.
    def reset_positions(self, series_id):
        query = "UPDATE positions SET value = 0 WHERE series_id = ?"
        self.cursor.execute(query, (series_id,))
        self.conn.commit()



    # Manage coefficients:
    # Set the value of a coefficient.
    def set_coefficient(self, coefficient_id, series_id, value):
        query = "UPDATE coefficients SET value = ? WHERE coefficient_id = ? AND series_id = ?"
        self.cursor.execute(query, (value, coefficient_id, series_id))
        self.conn.commit()

 

    # Manage prices:
    # Update the price for a price in a given series_id.
    def set_price(self, price_id, series_id, price):
        query = "UPDATE prices SET price = ? WHERE price_id = ? AND series_id = ?"
        self.cursor.execute(query, (price, price_id, series_id))
        self.conn.commit()

    # Add a new price to the series in a given series_id.
    def add_price(self, series_id, description, price):
        query = "INSERT INTO prices (description, price, series_id) VALUES (?, ?, ?)"
        self.cursor.execute(query, (description, price, series_id))
        self.conn.commit()



    # Getters:
    # Get all workers for a given series index.
    def get_series_workers(self, series_id):
        self.cursor.execute("SELECT * FROM workers WHERE series_id = ?", (series_id,))
        return self.cursor.fetchall()

    # Get all prices for a given series index.
    def get_prices(self, series_id):
        self.cursor.execute("SELECT * FROM prices WHERE series_id = ?", (series_id,))
        return self.cursor.fetchall()

   # Get all coefficients for a given series_id.
    def get_coefficients(self, series_id):
        self.cursor.execute("SELECT coefficient_id, value FROM coefficients WHERE series_id = ?", (series_id,))
        return {row[0]: row[1] for row in self.cursor.fetchall()}

    # Get all positions for a given series_id.
    def get_positions(self, series_id):
        self.cursor.execute("SELECT position, value FROM positions WHERE series_id = ?", (series_id,))
        return {row[0]: row[1] for row in self.cursor.fetchall()}



    # Function which will create the first 18 already pre-defined prices.
    def add_predefined_prices(self):
        prices = [
            ("DR (sliekšņi)", 4.20),
            ("DR (sliekšņi + plēve)", 5.67),
            ("LR + DR (plastmasas stiprinājumi)", 1.68),
            ("LR (montāžas plēve)", 1.47),
            ("LR (plastmasas stiprinājumi/mont. plēve)", 2.94),
            ("LV alumīnijs", 2.37),
            ("LV koks", 1.05),
            ("DV alumīnijs", 6.30),
            ("DV koks", 2.63),
            ("DV bloka", 4.62),
            ("silikona logs 1-4", 1.84),
            ("logu montāža <3.5 m2", 5.88),
            ("logu montāža >3.5 m2 (lielie)", 18.90),
            ("speciālie + slīpie + eļļots", 25.00),
            ("balkona durvju montāža", 4.83),
            ("ārdurvju montāža", 9.03),
            ("ugunsdrošo durvju montāža", 15.00),
            ("durvju pildiņi, stiklošana", 0.53),
            ("durvju rāmju savienošana (pāris)", 5.25)
        ]

        series_id = self.get_last_series_id()

        for price in prices:
            self.cursor.execute('''
                INSERT INTO prices (description, price, series_id) VALUES (?, ?, ?)
            ''', (price[0], price[1], series_id))

        self.conn.commit()

# Makes a single and globally accessible database class instance.
database = DatabaseOperations()
database.create_series()
database.add_predefined_prices()