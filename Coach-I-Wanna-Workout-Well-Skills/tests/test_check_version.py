import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import URLError


spec = importlib.util.spec_from_file_location("check_version", Path(__file__).resolve().parents[1] / "scripts" / "check_version.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class VersionCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "version.json").write_text('{"version":"1.0.0"}', encoding="utf-8")
        root_patch = patch.object(checker, "SKILL_ROOT", self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    def test_unknown_region_does_not_make_network_request(self):
        with patch.object(checker, "fetch_version") as fetch:
            result = checker.check(None)
        self.assertEqual(result["status"], "needs_region")
        self.assertEqual(result["current_version"], "1.0.0")
        fetch.assert_not_called()

    def test_each_region_uses_its_own_source(self):
        for region, domain in (("cn", "gitee.com"), ("global", "github.com")):
            with self.subTest(region=region), patch.object(checker, "fetch_version", return_value="1.0.1") as fetch:
                result = checker.check(region)
                self.assertEqual(result["status"], "update_available")
                self.assertIn(domain, result["repository_url"])
                fetch.assert_called_once_with(checker.SOURCES[region]["manifest"], 4)

    def test_numeric_comparison_and_no_downgrade(self):
        (self.root / "version.json").write_text('{"version":"1.9.0"}', encoding="utf-8")
        for latest, status in (("1.10.0", "update_available"), ("1.9.0", "up_to_date"), ("1.8.0", "local_ahead")):
            with self.subTest(latest=latest), patch.object(checker, "fetch_version", return_value=latest):
                self.assertEqual(checker.check("cn")["status"], status)

    def test_network_failure_preserves_local_version(self):
        with patch.object(checker, "fetch_version", side_effect=URLError("offline")) as fetch:
            result = checker.check("cn")
        self.assertEqual(result["status"], "unavailable")
        self.assertEqual(result["current_version"], "1.0.0")
        self.assertIsNone(result["latest_version"])
        fetch.assert_called_once()

    def test_missing_local_version_is_not_reported_as_current(self):
        (self.root / "version.json").unlink()
        with patch.object(checker, "fetch_version") as fetch:
            result = checker.check("cn")
        self.assertEqual(result["status"], "unavailable")
        fetch.assert_not_called()

    def test_fetch_rejects_html_and_invalid_versions(self):
        for payload in (b"<html>login</html>", b'{"version":"latest"}', b'{"version":12}', b'{"other":"1.0.1"}', b"x" * 65537):
            with self.subTest(payload=payload[:30]), patch.object(checker, "urlopen", return_value=io.BytesIO(payload)):
                with self.assertRaises((ValueError, KeyError)):
                    checker.fetch_version("https://example.com/version.json", 4)

    def test_fetch_parses_utf8_json(self):
        with patch.object(checker, "urlopen", return_value=io.BytesIO(b'{"version":"2.0.0"}')):
            self.assertEqual(checker.fetch_version("https://example.com/version.json", 4), "2.0.0")

    def run_cli(self, args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = checker.main(args)
        return code, json.loads(out.getvalue())

    def test_region_survives_across_invocations(self):
        config = self.root / "settings" / "update-settings.json"
        with patch.object(checker, "fetch_version", return_value="1.0.0"):
            code, first = self.run_cli(["--config", str(config), "--region", "cn", "--remember-region"])
            _, second = self.run_cli(["--config", str(config)])
            self.run_cli(["--config", str(config), "--region", "global", "--remember-region"])
            _, switched = self.run_cli(["--config", str(config)])
        self.assertEqual(code, 0)
        self.assertEqual(first["region"], second["region"])
        self.assertEqual(second["region"], "cn")
        self.assertEqual(switched["region"], "global")
        self.assertEqual(json.loads(config.read_text()), {"region": "global"})

    def test_corrupt_config_requests_region_without_network(self):
        config = self.root / "settings.json"
        config.write_text("invalid", encoding="utf-8")
        with patch.object(checker, "fetch_version") as fetch:
            code, result = self.run_cli(["--config", str(config)])
        self.assertEqual(code, 1)
        self.assertEqual(result["status"], "needs_region")
        self.assertIn("config_error", result)
        fetch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
