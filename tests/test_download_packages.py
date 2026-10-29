"""Verify standalone ZIP downloads match the GitHub repository sources.

This protects users from accidentally downloading a launcher without its script
or receiving an out-of-date snapshot after changes to the original script.
"""
from pathlib import Path
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = {
    "Windows-HealthCheck.zip": {
        "Lancer-Windows-HealthCheck.cmd": "PowerShell/Lancer-Windows-HealthCheck.cmd",
        "Windows-HealthCheck.ps1": "PowerShell/Windows-HealthCheck.ps1",
    },
    "Security-BaselineChecker.zip": {
        "Lancer-Security-BaselineChecker.cmd": "PowerShell/Lancer-Security-BaselineChecker.cmd",
        "Security-BaselineChecker.ps1": "PowerShell/Security-BaselineChecker.ps1",
    },
    "AD-BulkUserCreation.zip": {
        "Lancer-AD-BulkUserCreation.cmd": "PowerShell/Lancer-AD-BulkUserCreation.cmd",
        "AD-BulkUserCreation.ps1": "PowerShell/AD-BulkUserCreation.ps1",
        "ad-users.example.csv": "examples/ad-users.example.csv",
    },
    "Network-Doctor.zip": {
        "Lancer-Network-Doctor.cmd": "Python/Lancer-Network-Doctor.cmd",
        "network_doctor.py": "Python/network_doctor.py",
    },
    "Linux-HealthCheck.zip": {
        "Lancer-Linux-HealthCheck.cmd": "Bash/Lancer-Linux-HealthCheck.cmd",
        "linux-healthcheck.sh": "Bash/linux-healthcheck.sh",
    },
}


class DownloadPackageTests(unittest.TestCase):
    def test_all_download_archives(self):
        for archive_name, files in PACKAGES.items():
            with self.subTest(archive=archive_name):
                with zipfile.ZipFile(ROOT / "downloads" / archive_name) as archive:
                    self.assertIsNone(archive.testzip(), "Archive contains a corrupted entry")
                    self.assertEqual(set(archive.namelist()), set(files) | {"README-FR-EN.txt"})
                    for name, source in files.items():
                        with self.subTest(file=name):
                            expected = (ROOT / source).read_bytes()
                            self.assertEqual(archive.read(name), expected)


if __name__ == "__main__":
    unittest.main()
