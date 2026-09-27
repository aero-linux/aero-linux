import unittest
from aero.doctor import run_doctor, get_cpu_info, get_memory_info, get_gpu_info
from aero.power import PROFILES, get_current_profile
from aero.memory import get_top_memory_processes
from aero.dev import ENVIRONMENTS
from aero.net import DNS_PROVIDERS
from aero.ai import get_ai_status
from aero.monitor import render_bar
from aero.security import audit_security
from aero.benchmark import cpu_worker
from aero.docker_tools import check_docker
from aero.thermals import get_temperatures
from aero.clipboard import check_clipboard
from aero.themes import THEMES
from aero.share import get_local_ip
from aero.battery import get_battery_health
from aero.audio import LATENCY_PRESETS
from aero.fonts import NERD_FONTS
from aero.db_tools import DATABASES
from aero.vm import check_kvm


class TestAeroCLI(unittest.TestCase):
    def test_cpu_info(self):
        cpu = get_cpu_info()
        self.assertIn("cores", cpu)
        self.assertGreater(cpu["cores"], 0)

    def test_memory_info(self):
        mem = get_memory_info()
        self.assertIn("total_mb", mem)
        self.assertGreater(mem["total_mb"], 0)

    def test_power_profiles_definition(self):
        self.assertIn("battery", PROFILES)
        self.assertIn("balanced", PROFILES)
        self.assertIn("boost", PROFILES)
        self.assertIn("gaming", PROFILES)

    def test_get_current_profile(self):
        prof = get_current_profile()
        self.assertIn(prof, PROFILES)

    def test_top_memory_processes(self):
        procs = get_top_memory_processes(5)
        self.assertIsInstance(procs, list)
        if procs:
            self.assertIn("pid", procs[0])
            self.assertIn("rss_mb", procs[0])

    def test_doctor_full_report(self):
        report = run_doctor()
        self.assertIn("os", report)
        self.assertIn("kernel", report)
        self.assertIn("cpu", report)
        self.assertIn("memory", report)
        self.assertIn("ai_stack", report)

    def test_dev_environments(self):
        self.assertIn("node", ENVIRONMENTS)
        self.assertIn("python", ENVIRONMENTS)
        self.assertIn("rust", ENVIRONMENTS)
        self.assertIn("go", ENVIRONMENTS)
        self.assertIn("c", ENVIRONMENTS)
        self.assertIn("postgres", ENVIRONMENTS)
        self.assertIn("redis", ENVIRONMENTS)

    def test_dns_providers(self):
        self.assertIn("cloudflare", DNS_PROVIDERS)
        self.assertIn("quad9", DNS_PROVIDERS)
        self.assertIn("google", DNS_PROVIDERS)

    def test_ai_status(self):
        status = get_ai_status()
        self.assertIn("ollama_installed", status)
        self.assertIn("ollama_running", status)

    def test_render_bar(self):
        bar = render_bar(50.0, width=10)
        self.assertEqual(len(bar), 10)
        self.assertTrue(bar.startswith("█████"))

    def test_audit_security(self):
        sec = audit_security()
        self.assertIn("firewall_active", sec)
        self.assertIn("aslr_enabled", sec)

    def test_cpu_worker(self):
        res = cpu_worker(10)
        self.assertEqual(res, sum(i * i for i in range(1, 10)))

    def test_check_docker(self):
        # Function returns a boolean based on environment
        res = check_docker()
        self.assertIsInstance(res, bool)

    def test_thermals(self):
        res = get_temperatures()
        self.assertIsInstance(res, list)

    def test_clipboard(self):
        res = check_clipboard()
        self.assertIsInstance(res, bool)

    def test_themes(self):
        self.assertIn("cyber-cyan", THEMES)
        self.assertIn("tokyo-night", THEMES)
        self.assertIn("nord", THEMES)
        self.assertIn("gruvbox", THEMES)

    def test_share_ip(self):
        ip = get_local_ip()
        self.assertIsInstance(ip, str)
        self.assertTrue(len(ip) >= 7)

    def test_battery_health(self):
        health = get_battery_health()
        self.assertIn("present", health)

    def test_audio_presets(self):
        self.assertIn("low", LATENCY_PRESETS)
        self.assertIn("medium", LATENCY_PRESETS)
        self.assertIn("high", LATENCY_PRESETS)

    def test_fonts(self):
        self.assertIn("jetbrains-mono", NERD_FONTS)
        self.assertIn("fira-code", NERD_FONTS)

    def test_databases(self):
        self.assertIn("postgres", DATABASES)
        self.assertIn("redis", DATABASES)
        self.assertIn("mysql", DATABASES)
        self.assertIn("mongo", DATABASES)

    def test_kvm(self):
        res = check_kvm()
        self.assertIsInstance(res, bool)


if __name__ == "__main__":
    unittest.main()
