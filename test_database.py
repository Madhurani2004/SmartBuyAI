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
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_cost REAL NOT NULL,
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


if __name__ == "__main__":
    unittest.main()