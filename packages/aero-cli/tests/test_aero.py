import unittest
import os
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
from aero.layout import set_desktop_layout
from aero.ai import calc_model_memory
from aero.kernel_mgr import PROFILES as KERNEL_PROFILES, audit_kernel_scheduler
from aero.vault import vault_set, vault_get, vault_delete, _load_vault
from aero.wallpaper import generate_wallpaper_svg, PALETTES
from aero.memory import get_memory_stats
from aero.perf_tools import get_cpu_stat_snapshot
from aero.sandbox import check_namespace_support
from aero.tracer import DNS_SERVERS
from aero.cleaner import get_disk_free_mb
from aero.cert_mgr import generate_dev_certificate
from aero.notifier import send_notification
from aero.health_checker import get_nvme_health, get_cpu_thermal_throttle_health
from aero.mock_server import MOCK_SCHEMAS
from aero.firewall import get_firewall_status
from aero.prompt_gen import render_prompt, get_git_branch_fast
from aero.app_store import APP_CATALOG
from aero.theme_scheduler import auto_apply_dynamic_theme
from aero.flasher import list_usb_drives
from aero.dotfiles_mgr import export_dotfiles, import_dotfiles
from aero.turbo_build import get_active_turbo_mounts
from aero.snippets import DEFAULT_SNIPPETS
from aero.log_streamer import get_oom_events
from aero.regex_tool import test_regex
from aero.diff_tool import show_file_diff


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

    def test_desktop_layout(self):
        res = set_desktop_layout("windows")
        self.assertTrue(res)

    def test_ai_calc_model_memory(self):
        res = calc_model_memory(8.0, "q4_k_m", 4096)
        self.assertEqual(res["params_b"], 8.0)
        self.assertTrue(res["weights_gb"] > 3.0)
        self.assertIsInstance(res["fits_with_aero_zram"], bool)

    def test_kernel_profiles(self):
        self.assertIn("lowlatency", KERNEL_PROFILES)
        self.assertIn("throughput", KERNEL_PROFILES)
        self.assertIn("powersave", KERNEL_PROFILES)

    def test_vault_crud(self):
        vault_set("TEST_SECRET_KEY", "ultra_secret_123")
        val = vault_get("TEST_SECRET_KEY")
        self.assertEqual(val, "ultra_secret_123")
        vault_delete("TEST_SECRET_KEY")
        self.assertNotIn("TEST_SECRET_KEY", _load_vault())

    def test_wallpaper_generation(self):
        out = generate_wallpaper_svg("cyber-cyan", "/tmp/test_aero_wall.svg")
        self.assertTrue(os.path.exists(out))
        with open(out) as f:
            content = f.read()
            self.assertIn("<svg", content)
            self.assertIn("AERO LINUX", content)
        if os.path.exists(out):
            os.remove(out)

    def test_memory_stats(self):
        stats = get_memory_stats()
        self.assertIn("total_mb", stats)
        self.assertIn("percent_used", stats)

    def test_perf_cpu_stat(self):
        snap = get_cpu_stat_snapshot()
        self.assertIn("cpu", snap)

    def test_sandbox_support(self):
        res = check_namespace_support()
        self.assertIsInstance(res, bool)

    def test_trace_dns_servers(self):
        self.assertIn("Cloudflare (1.1.1.1)", DNS_SERVERS)
        self.assertIn("Google (8.8.8.8)", DNS_SERVERS)

    def test_cleaner_disk_stats(self):
        free_mb = get_disk_free_mb()
        self.assertTrue(free_mb > 0)

    def test_cert_generator(self):
        res = generate_dev_certificate("test_domain", "/tmp/test_aero_cert")
        self.assertTrue(res)
        self.assertTrue(os.path.exists("/tmp/test_aero_cert/test_domain.crt"))
        self.assertTrue(os.path.exists("/tmp/test_aero_cert/test_domain.key"))
        # Cleanup
        if os.path.exists("/tmp/test_aero_cert"):
            for f in os.listdir("/tmp/test_aero_cert"):
                os.remove(os.path.join("/tmp/test_aero_cert", f))
            os.rmdir("/tmp/test_aero_cert")

    def test_notifier(self):
        res = send_notification("Test Title", "Test Message", "low", False)
        self.assertTrue(res)

    def test_health_checker(self):
        nvme = get_nvme_health()
        self.assertIn("nvme_devices", nvme)
        cpu = get_cpu_thermal_throttle_health()
        self.assertIn("throttle_events", cpu)

    def test_mock_schemas(self):
        self.assertIn("users", MOCK_SCHEMAS)
        self.assertIn("products", MOCK_SCHEMAS)
        self.assertIn("metrics", MOCK_SCHEMAS)

    def test_firewall_status(self):
        fw = get_firewall_status()
        self.assertIn("active", fw)
        self.assertIn("rules", fw)

    def test_prompt_renderer(self):
        p_bash = render_prompt("bash")
        self.assertIn("aero", p_bash)
        p_fish = render_prompt("fish")
        self.assertIn("aero", p_fish)

    def test_app_catalog(self):
        self.assertIn("vscode", APP_CATALOG)
        self.assertIn("docker", APP_CATALOG)
        self.assertIn("brave", APP_CATALOG)

    def test_theme_scheduler(self):
        theme = auto_apply_dynamic_theme()
        self.assertIn(theme, ["nord", "cyber-cyan", "gruvbox", "tokyo-night"])

    def test_usb_drives_listing(self):
        drives = list_usb_drives()
        self.assertIsInstance(drives, list)

    def test_dotfiles_export_import(self):
        tar = export_dotfiles("/tmp/aero_test_dotfiles")
        self.assertTrue(os.path.exists(tar))
        res = import_dotfiles(tar)
        self.assertTrue(res)
        if os.path.exists(tar):
            os.remove(tar)
        if os.path.exists("/tmp/aero_test_dotfiles"):
            os.rmdir("/tmp/aero_test_dotfiles")

    def test_turbo_mounts(self):
        mounts = get_active_turbo_mounts()
        self.assertIsInstance(mounts, list)

    def test_snippet_vault(self):
        self.assertIn("docker-prune", DEFAULT_SNIPPETS)
        self.assertIn("git-undo-commit", DEFAULT_SNIPPETS)
        self.assertIn("port-find", DEFAULT_SNIPPETS)

    def test_oom_events_check(self):
        ooms = get_oom_events()
        self.assertIsInstance(ooms, list)

    def test_regex_tool(self):
        res = test_regex(r"(?P<word>\w+)", "hello world")
        self.assertTrue(res["valid"])
        self.assertEqual(len(res["matches"]), 2)

    def test_diff_tool(self):
        # Create 2 temp files
        with open("/tmp/aero_diff_a.txt", "w") as f:
            f.write("Line 1\nLine 2\n")
        with open("/tmp/aero_diff_b.txt", "w") as f:
            f.write("Line 1\nLine 2 modified\nLine 3\n")
        
        diff = show_file_diff("/tmp/aero_diff_a.txt", "/tmp/aero_diff_b.txt")
        self.assertFalse(diff["identical"])
        self.assertTrue(diff["additions"] > 0)

        # Cleanup
        os.remove("/tmp/aero_diff_a.txt")
        os.remove("/tmp/aero_diff_b.txt")


if __name__ == "__main__":
    unittest.main()
