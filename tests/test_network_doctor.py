"""Unit tests: diagnostic classification, no network requests."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "Python"))
from network_doctor import classify

class ClassificationTests(unittest.TestCase):
    def test_dns_only_failure(self):
        self.assertIn("DNS KO", classify("192.168.1.20", "192.168.1.1", True, True, False, False))
    def test_external_tcp_failure(self):
        self.assertIn("Échec du test TCP", classify("192.168.1.20", "192.168.1.1", True, False, True, False))
    def test_gateway_ping_can_be_filtered(self):
        self.assertIn("ICMP probablement filtré", classify("192.168.1.20", "192.168.1.1", False, True, True, True))
    def test_target_failure(self):
        self.assertIn("service cible", classify("192.168.1.20", "192.168.1.1", True, True, True, False))
    def test_success(self):
        self.assertIn("Tests réussis", classify("192.168.1.20", "192.168.1.1", True, True, True, True))
    def test_missing_local_ip(self):
        self.assertIn("Aucune adresse IPv4", classify(None, None, None, False, False, False))

if __name__ == "__main__":
    unittest.main()
