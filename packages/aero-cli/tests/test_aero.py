import unittest
from aero.doctor import run_doctor, get_cpu_info, get_memory_info, get_gpu_info
from aero.power import PROFILES, get_current_profile
from aero.memory import get_top_memory_processes
from aero.dev import ENVIRONMENTS
from aero.net import DNS_PROVIDERS
from aero.ai import get_ai_status


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


if __name__ == "__main__":
    unittest.main()
