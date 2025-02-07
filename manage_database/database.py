import sqlite3
import time

class DatabaseOperations:
    def __init__(self):
        self.conn = sqlite3.connect('manage_database/database.sqlite3')
        self.cursor = self.conn.cursor()
        self.conn.execute("PRAGMA foreign_keys = ON;")  # Ensure foreign keys are enforced.
        self.create_tables()
        self.initialize_first_run()

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
                description TEXT NOT NULL,
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



# ------ Manage series: ------
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

        # Copy coefficients from the previous series (if exists)
        previous_series_id = series_id - 1
        self.cursor.execute('''
            INSERT INTO coefficients (coefficient_id, description, value, series_id)
            SELECT coefficient_id, description, value, ? FROM coefficients WHERE series_id = ?
        ''', (series_id, previous_series_id))

        # Copy workers from the previous series
        previous_series_id = series_id - 1
        self.cursor.execute('''
            INSERT INTO workers (series_id, name, surname, efficiency, working)
            SELECT ?, name, surname, efficiency, working FROM workers WHERE series_id = ?
        ''', (series_id, previous_series_id))

        # Copy prices from the previous series, but use the default value for count
        previous_series_id = series_id - 1
        self.cursor.execute('''
            INSERT INTO prices (description, price, series_id)
            SELECT description, price, ? FROM prices WHERE series_id = ?
        ''', (series_id, previous_series_id))

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



# ------ Manage workers: ------
    # Add a worker to the worker table.
    def add_series_worker(self, series_id, name, surname, efficiency):
        query = "INSERT INTO workers (series_id, name, surname, efficiency) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (series_id, name, surname, efficiency))
        self.conn.commit()

    def delete_worker(self, worker_id):
        query = "DELETE FROM workers WHERE worker_id = ?"
        self.cursor.execute(query, (worker_id,))
        self.conn.commit()

    # Edit a worker's efficiency.
    def edit_worker(self, worker_id, efficiency):
        query = "UPDATE workers SET efficiency = ? WHERE worker_id = ?"
        self.cursor.execute(query, (efficiency, worker_id))
        self.conn.commit()

    # Reverse the working status of a worker.
    def toggle_working(self, worker_id):
        query = "UPDATE workers SET working = NOT working WHERE worker_id = ?"
        self.cursor.execute(query, (worker_id,))
        self.conn.commit()



# ------ Manage positions: ------
    # Add 1 to a position's value.
    def add_one(self, position, series_id):
        query = "UPDATE positions SET value = value + 1 WHERE position = ? AND series_id = ?"
        self.cursor.execute(query, (position, series_id))
        self.conn.commit()

    # Remove 1 from a position's value.
    def remove_one(self, position, series_id):
        # Check current value
        self.cursor.execute("SELECT value FROM positions WHERE position = ? AND series_id = ?", (position, series_id))
        current_value = self.cursor.fetchone()[0]
        if current_value > 0:
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



# ------ Manage coefficients: ------
    # Set the value of a coefficient.
    def set_coefficient(self, coefficient_id, series_id, value):
        query = "UPDATE coefficients SET value = ? WHERE coefficient_id = ? AND series_id = ?"
        self.cursor.execute(query, (value, coefficient_id, series_id))
        self.conn.commit()

 

# ------ Manage prices: ------
    # Add 1 to a price's count.
    def add_one_price(self, price_id):
        query = "UPDATE prices SET count = count + 1 WHERE price_id = ?"
        self.cursor.execute(query, (price_id,))
        self.conn.commit()

    # Remove 1 from a price's count.
    def remove_one_price(self, price_id):
        # Check current count
        self.cursor.execute("SELECT count FROM prices WHERE price_id = ?", (price_id,))
        current_count = self.cursor.fetchone()[0]
        if current_count > 0:
            query = "UPDATE prices SET count = count - 1 WHERE price_id = ?"
            self.cursor.execute(query, (price_id,))
            self.conn.commit()
        
    # Set the count of a price.
    def set_price_count(self, count, price_id):
        query = "UPDATE prices SET count = ? WHERE price_id = ?"
        self.cursor.execute(query, (count, price_id))
        self.conn.commit()

    # Update the price for a price in a given series_id.
    def set_price(self, price, price_id):
        query = "UPDATE prices SET price = ? WHERE price_id = ?"
        self.cursor.execute(query, (price, price_id))
        self.conn.commit()

    # Add a new price to the series in a given series_id.
    def add_price(self, series_id, description, price):
        query = "INSERT INTO prices (description, price, series_id) VALUES (?, ?, ?)"
        self.cursor.execute(query, (description, price, series_id))
        self.conn.commit()

    # Delete a price from the series in a given series_id.
    def delete_price(self, price_id):
        query = "DELETE FROM prices WHERE price_id = ?"
        self.cursor.execute(query, (price_id,))
        self.conn.commit()

    # Resets the count of all prices in a given series_id.
    def reset_prices(self, series_id):
        query = "UPDATE prices SET count = 0 WHERE series_id = ?"
        self.cursor.execute(query, (series_id,))
        self.conn.commit()


# ------ Getters: ------
    # Get all workers for a given series index.
    def get_series_workers(self, series_id):
        self.cursor.execute("SELECT worker_id, name, surname, efficiency, working FROM workers WHERE series_id = ?", (series_id,))
        return {row[0]: {"worker_id": row[0], "name": row[1], "surname": row[2], "efficiency": row[3], "working": row[4]} for row in self.cursor.fetchall()}

    # Get all prices for a given series index.
    def get_prices(self, series_id):
        self.cursor.execute("SELECT price_id, description, price, count FROM prices WHERE series_id = ?", (series_id,))
        return {row[0]: {"price_id": row[0], "description": row[1], "price": row[2], "count": row[3]} for row in self.cursor.fetchall()}

   # Get all coefficients for a given series_id.
    def get_coefficients(self, series_id):
        self.cursor.execute("SELECT coefficient_id, description, value FROM coefficients WHERE series_id = ?", (series_id,))
        return {row[0]: {"coefficient_id": row[0], "description": row[1], "value": row[2]} for row in self.cursor.fetchall()}

    # Get all positions for a given series_id.
    def get_positions(self, series_id):
        self.cursor.execute("SELECT position, value FROM positions WHERE series_id = ?", (series_id,))
        return {row[0]: row[1] for row in self.cursor.fetchall()}

    # Function, which will return the sum of all position values in the series.
    def get_sum_positions(self, series_id):
        self.cursor.execute("SELECT SUM(value) FROM positions WHERE series_id = ?", (series_id,))
        return self.cursor.fetchone()[0]
    
    # Function, which will return the sum of all prices in the series.
    def get_sum_prices(self, series_id):
        self.cursor.execute("SELECT SUM(price * count) FROM prices WHERE series_id = ?", (series_id,))
        return self.cursor.fetchone()[0]



# ------ Other functions: ------
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

    # Adds pre-defined coefficients.
    def add_predefined_coefficients(self):
        coefficients = [
            (1, "1. pozīcija", 0.66),
            (2, "2. pozīcija", 1.33),
            (3, "3. pozīcija", 0.5),
            (4, "4. pozīcija", 0.33),
            (5, "5. pozīcija", 1.33),
            (6, "6. pozīcija", 1.0),
            (7, "7. pozīcija", 0.8),
            (8, "8. pozīcija", 2.0),
            (9, "9. pozīcija", 0.66),
            (10, "Krāsotavas kļūda", 0.1),
            (11, "Kvalitātes pārbaude", 0.1)
        ]

        series_id = self.get_last_series_id()

        for coefficient in coefficients:
            self.cursor.execute('''
                INSERT INTO coefficients (coefficient_id, description, value, series_id) VALUES (?, ?, ?, ?)
            ''', (coefficient[0], coefficient[1], coefficient[2], series_id))

        self.conn.commit()

    # Function which will initialize the database with the first series and predefined prices.
    def initialize_first_run(self):
        # Check if the series table is empty
        self.cursor.execute('SELECT COUNT(*) FROM series')
        if self.cursor.fetchone()[0] == 0:
            # No series exist, so this is the first run
            self.create_series()
            self.add_predefined_prices()
            self.add_predefined_coefficients()

# Makes a single and globally accessible database class instance.
database = DatabaseOperations()