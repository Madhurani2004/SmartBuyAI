import unittest
import sqlite3
import tempfile
import os


class TestPurchaseOrderDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".db"
        )
        self.temp_file.close()

        self.connection = sqlite3.connect(self.temp_file.name)

        self.connection.execute("""
            CREATE TABLE purchase_orders (
                order_id TEXT PRIMARY KEY,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                unit_price REAL NOT NULL CHECK(unit_price >= 0),
                total_cost REAL NOT NULL CHECK(total_cost >= 0),
                status TEXT NOT NULL
            )
        """)

        self.connection.commit()

    def tearDown(self):
        self.connection.close()
        os.remove(self.temp_file.name)

    def test_save_and_retrieve_purchase_order(self):
        self.connection.execute(
            """
            INSERT INTO purchase_orders
            (order_id, quantity, unit_price, total_cost, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("PO-TEST-001", 100, 40, 4000, "Created")
        )

        self.connection.commit()

        result = self.connection.execute(
            "SELECT * FROM purchase_orders WHERE order_id = ?",
            ("PO-TEST-001",)
        ).fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "PO-TEST-001")
        self.assertEqual(result[1], 100)
        self.assertEqual(result[2], 40)
        self.assertEqual(result[3], 4000)
        self.assertEqual(result[4], "Created")

    def test_duplicate_order_id_is_rejected(self):
        order = (
            "PO-TEST-002",
            100,
            40,
            4000,
            "Created"
        )

        self.connection.execute(
            """
            INSERT INTO purchase_orders
            (order_id, quantity, unit_price, total_cost, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            order
        )

        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                """
                INSERT INTO purchase_orders
                (order_id, quantity, unit_price, total_cost, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                order
            )

    def test_zero_quantity_is_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                """
                INSERT INTO purchase_orders
                (order_id, quantity, unit_price, total_cost, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                ("PO-TEST-003", 0, 40, 0, "Created")
            )

    def test_negative_unit_price_is_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                """
                INSERT INTO purchase_orders
                (order_id, quantity, unit_price, total_cost, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                ("PO-TEST-004", 100, -40, -4000, "Created")
            )


if __name__ == "__main__":
    unittest.main()
