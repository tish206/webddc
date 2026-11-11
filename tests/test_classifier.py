import unittest
from src.classifier import DDCCategorizer
from src.router import DDCRouter

class TestDDCCategorizer(unittest.TestCase):
    def setUp(self):
        self.categorizer = DDCCategorizer()
        self.router = DDCRouter(self.categorizer)

    def test_python_categorization(self):
        result = self.categorizer.categorize_text("Python programming algorithms")
        self.assertEqual(result["assigned_code"], "005")
        self.assertEqual(result["main_class"], "000")

    def test_science_categorization(self):
        result = self.categorizer.categorize_text("Quantum physics and chemistry")
        self.assertEqual(result["assigned_code"], "500")

    def test_router_lookup_valid(self):
        data, status = self.router.handle_lookup("005.1")
        self.assertEqual(status, 200)
        self.assertEqual(data["data"]["code"], "005.1")

    def test_router_categorize_empty(self):
        data, status = self.router.handle_categorization("   ")
        self.assertEqual(status, 400)
        self.assertIn("error", data)

if __name__ == "__main__":
    unittest.main()
