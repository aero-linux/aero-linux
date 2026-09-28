import unittest
import os
import shutil
import subprocess
from aero.doctor import run_doctor, get_cpu_info, get_memory_info, get_gpu_info
from aero.power import PROFILES, get_current_profile
from aero.memory import get_top_memory_processes
from aero.dev import ENVIRONMENTS, NATIVE_STACKS
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
from aero.json_tools import format_json_str, minify_json_str, query_json_path
from aero.crypto_tools import generate_uuid, generate_token, compute_hash
from aero.jwt_tools import b64_encode_str, b64_decode_str, decode_jwt_token
from aero.net_diagnostics import dns_dig, ping_host
from aero.ai_tools import audit_ai_memory_footprint, PROMPT_TEMPLATES
from aero.hardware_tuning import get_hardware_fan_status, FAN_PROFILES
from aero.dev_utils import convert_color, time_execution
from aero.osd import handle_osd_action
from aero.trash import get_trash_items, empty_trash_bin
from aero.display import set_night_light
from aero.calc import calculate_expression
from aero.battery_daemon import check_battery_alerts
from aero.archive_tools import compress_archive, extract_archive
from aero.file_search import search_files_by_name, search_text_content
from aero.nvme_wear import get_ssd_wear_stats
from aero.autotile import is_autotile_running, stop_autotiling
from aero.wine_runner import run_windows_app
from aero.gpu_switcher import get_current_gpu_mode, GPU_MODES
from aero.phone_connect import show_phone_status, get_phone_devices
from aero.accent_manager import apply_accent_color, ACCENT_PRESETS
from aero.appimage_mgr import integrate_appimage, list_appimages, remove_appimage
from aero.store_engine import search_universal_store
from aero.zoom_mgr import zoom_in, zoom_out, zoom_reset, set_zoom, zoom_peek
from aero.power_daemon import get_ac_power_status, apply_power_state
from aero.repair import run_system_repair
from aero.git_tools import scan_local_git_workspaces, print_git_workspaces


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
        self.assertIn("java", ENVIRONMENTS)
        self.assertIn("ai", ENVIRONMENTS)
        self.assertIn("postgres", ENVIRONMENTS)
        self.assertIn("redis", ENVIRONMENTS)
        self.assertIn("node", NATIVE_STACKS)
        self.assertIn("rust", NATIVE_STACKS)
        self.assertIn("java", NATIVE_STACKS)

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

    def test_json_tools(self):
        raw = '{"name": "Aero", "version": 1.0, "tools": ["cli", "gui"]}'
        fmt = format_json_str(raw)
        self.assertIn("\n", fmt)
        mini = minify_json_str(raw)
        self.assertNotIn("\n", mini)
        val = query_json_path(raw, "tools.0")
        self.assertEqual(val, "cli")

    def test_crypto_tools(self):
        u = generate_uuid()
        self.assertEqual(len(u), 36)
        tok = generate_token(16, "hex")
        self.assertEqual(len(tok), 16)
        h = compute_hash("hello world", "sha256")
        self.assertEqual(len(h), 64)

    def test_jwt_base64_tools(self):
        b64 = b64_encode_str("test_payload")
        dec = b64_decode_str(b64)
        self.assertEqual(dec, "test_payload")
        
        # Test mock JWT
        mock_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlJvbml0IiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        res = decode_jwt_token(mock_jwt)
        self.assertEqual(res["payload"]["name"], "Ronit")

    def test_dns_dig(self):
        res = dns_dig("localhost")
        self.assertIn("A", res)

    def test_ping_host(self):
        res = ping_host("127.0.0.1", count=1)
        self.assertIn("latencies", res)

    def test_ai_tools_vram(self):
        self.assertIn("coding", PROMPT_TEMPLATES)
        self.assertIn("reasoning", PROMPT_TEMPLATES)

    def test_fan_hardware(self):
        self.assertIn("silent", FAN_PROFILES)
        self.assertIn("turbo", FAN_PROFILES)
        st = get_hardware_fan_status()
        self.assertIn("fan_mode", st)

    def test_color_converter(self):
        c = convert_color("#00f2fe")
        self.assertEqual(c["hex"], "#00F2FE")
        self.assertEqual(c["r"], 0)
        self.assertEqual(c["g"], 242)
        self.assertEqual(c["b"], 254)

    def test_time_execution(self):
        res = time_execution("echo test")
        self.assertEqual(res["exit_code"], 0)
        self.assertTrue(res["elapsed_sec"] >= 0)

    def test_osd_actions(self):
        r1 = handle_osd_action("volume-up")
        self.assertEqual(r1["action"], "volume-up")
        r2 = handle_osd_action("brightness-up")
        self.assertEqual(r2["action"], "brightness-up")
        r3 = handle_osd_action("mute")
        self.assertEqual(r3["action"], "mute")

    def test_trash_and_night_light(self):
        trash = get_trash_items()
        self.assertIsInstance(trash, list)
        self.assertTrue(empty_trash_bin())
        res_nl = set_night_light(False)
        self.assertFalse(res_nl)

    def test_calc_and_battery_daemon(self):
        c1 = calculate_expression("1024 * 16")
        self.assertEqual(c1["result"], 16384)
        c2 = calculate_expression("sqrt(256) + 4")
        self.assertEqual(c2["result"], 20.0)
        bat = check_battery_alerts()
        self.assertIn("capacity", bat)

    def test_archive_tools(self):
        test_dir = "/tmp/aero_test_archive_dir"
        os.makedirs(test_dir, exist_ok=True)
        with open(os.path.join(test_dir, "hello.txt"), "w") as f:
            f.write("Aero Archive Test")
        res_zip = compress_archive(test_dir, "/tmp/aero_test_bundle.zip")
        self.assertEqual(res_zip["status"], "created")
        res_unzip = extract_archive("/tmp/aero_test_bundle.zip", "/tmp/aero_test_unzip_dest")
        self.assertEqual(res_unzip["status"], "extracted")
        # Cleanup
        shutil.rmtree(test_dir, ignore_errors=True)
        shutil.rmtree("/tmp/aero_test_unzip_dest", ignore_errors=True)
        if os.path.exists("/tmp/aero_test_bundle.zip"):
            os.remove("/tmp/aero_test_bundle.zip")

    def test_file_and_content_search(self):
        files = search_files_by_name("*.py", root_dir="/home/ronit138/aero-linux/packages/aero-cli/aero")
        self.assertTrue(len(files) > 0)
        matches = search_text_content("class", root_dir="/home/ronit138/aero-linux/packages/aero-cli/tests")
        self.assertTrue(len(matches) > 0)

    def test_nvme_wear_stats(self):
        wear = get_ssd_wear_stats()
        self.assertIn("drives", wear)

    def test_autotiling_support(self):
        running = is_autotile_running()
        self.assertIsInstance(running, bool)
        stop_res = stop_autotiling()
        self.assertIn("status", stop_res)

    def test_wine_runner(self):
        res = run_windows_app("/tmp/non_existent_app.exe")
        self.assertEqual(res["status"], "error")

    def test_gpu_switcher(self):
        self.assertIn("hybrid", GPU_MODES)
        self.assertIn("integrated", GPU_MODES)
        gpu = get_current_gpu_mode()
        self.assertIn("mode", gpu)

    def test_phone_connect(self):
        devs = get_phone_devices()
        self.assertIsInstance(devs, list)

    def test_monitor_and_updater_gui_helpers(self):
        # Verify monitor and updater scripts exist and are executable
        mon_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-monitor"
        upd_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-updater"
        self.assertTrue(os.path.exists(mon_path))
        self.assertTrue(os.access(mon_path, os.X_OK))
        self.assertTrue(os.path.exists(upd_path))
        self.assertTrue(os.access(upd_path, os.X_OK))

    def test_accent_manager_studio(self):
        self.assertIn("cyan", ACCENT_PRESETS)
        self.assertIn("purple", ACCENT_PRESETS)
        res = apply_accent_color("cyan")
        self.assertEqual(res["status"], "applied")

    def test_appimage_manager(self):
        # Non-existent file test
        res = integrate_appimage("/tmp/non_existent_app.AppImage")
        self.assertEqual(res["status"], "error")
        apps = list_appimages()
        self.assertIsInstance(apps, list)
        rem = remove_appimage("non_existent_slug")
        self.assertEqual(rem["status"], "not_found")

    def test_store_search_engine(self):
        results = search_universal_store("code")
        self.assertIsInstance(results, list)
        self.assertTrue(any("VS Code" in r["name"] or "code" in r["id"].lower() for r in results))

    def test_zoom_manager(self):
        res = set_zoom(1.25)
        self.assertEqual(res["status"], "ok")
        self.assertEqual(res["percent"], 125)
        res_rst = zoom_reset()
        self.assertEqual(res_rst["percent"], 100)
        peek_res = zoom_peek(scale=1.30, duration=0.1)
        self.assertEqual(peek_res["status"], "peeking")

    def test_autonomous_power_daemon(self):
        ac_status = get_ac_power_status()
        self.assertIsInstance(ac_status, bool)
        res = apply_power_state(ac_status)
        self.assertEqual(res["status"], "applied")

    def test_wifi_and_snapshot_gui_scripts(self):
        wifi_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-wifi"
        snap_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-snapshot-gui"
        self.assertTrue(os.path.exists(wifi_path))
        self.assertTrue(os.access(wifi_path, os.X_OK))
        self.assertTrue(os.path.exists(snap_path))
        self.assertTrue(os.access(snap_path, os.X_OK))

    def test_hardware_gui_centers(self):
        bt_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-bluetooth"
        aud_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-audio"
        disp_path = "/home/ronit138/aero-linux/packages/aero-displays" if os.path.exists("/home/ronit138/aero-linux/packages/aero-displays") else "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-displays"
        self.assertTrue(os.path.exists(bt_path))
        self.assertTrue(os.access(bt_path, os.X_OK))
        self.assertTrue(os.path.exists(aud_path))
        self.assertTrue(os.access(aud_path, os.X_OK))
        self.assertTrue(os.path.exists(disp_path))
        self.assertTrue(os.access(disp_path, os.X_OK))

    def test_spotlight_gui_helper(self):
        spot_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-spotlight"
        self.assertTrue(os.path.exists(spot_path))
        self.assertTrue(os.access(spot_path, os.X_OK))

    def test_gamehub_and_connect_gui_scripts(self):
        gh_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-gamehub"
        cn_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-connect-gui"
        self.assertTrue(os.path.exists(gh_path))
        self.assertTrue(os.access(gh_path, os.X_OK))
        self.assertTrue(os.path.exists(cn_path))
        self.assertTrue(os.access(cn_path, os.X_OK))

    def test_power_and_nightlight_gui_scripts(self):
        pwr_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-power-gui"
        nl_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-nightlight-gui"
        self.assertTrue(os.path.exists(pwr_path))
        self.assertTrue(os.access(pwr_path, os.X_OK))
        self.assertTrue(os.path.exists(nl_path))
        self.assertTrue(os.access(nl_path, os.X_OK))

    def test_theme_and_cleaner_gui_scripts(self):
        th_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-theme-gui"
        cl_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-cleaner-gui"
        self.assertTrue(os.path.exists(th_path))
        self.assertTrue(os.access(th_path, os.X_OK))
        self.assertTrue(os.path.exists(cl_path))
        self.assertTrue(os.access(cl_path, os.X_OK))

    def test_vault_gui_script(self):
        vault_gui_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-vault-gui"
        self.assertTrue(os.path.exists(vault_gui_path))
        self.assertTrue(os.access(vault_gui_path, os.X_OK))

    def test_welcome_control_center_completeness(self):
        welcome_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-welcome"
        self.assertTrue(os.path.exists(welcome_path))
        self.assertTrue(os.access(welcome_path, os.X_OK))

    def test_about_and_screenshot_gui_scripts(self):
        abt_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-about-gui"
        scr_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-screenshot-gui"
        self.assertTrue(os.path.exists(abt_path))
        self.assertTrue(os.access(abt_path, os.X_OK))
        self.assertTrue(os.path.exists(scr_path))
        self.assertTrue(os.access(scr_path, os.X_OK))

    def test_iso_builder_script(self):
        bld_path = "/home/ronit138/aero-linux/build/build.sh"
        self.assertTrue(os.path.exists(bld_path))
        self.assertTrue(os.access(bld_path, os.X_OK))
        res = subprocess.run(["bash", "-n", bld_path], capture_output=True)
        self.assertEqual(res.returncode, 0)

    def test_repair_engine(self):
        results = run_system_repair()
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 4)
        for r in results:
            self.assertIn("component", r)
            self.assertIn("status", r)
            self.assertIn("message", r)

    def test_repair_gui_script(self):
        rep_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-repair-gui"
        self.assertTrue(os.path.exists(rep_path))
        self.assertTrue(os.access(rep_path, os.X_OK))

    def test_notes_gui_script(self):
        notes_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-notes-gui"
        self.assertTrue(os.path.exists(notes_path))
        self.assertTrue(os.access(notes_path, os.X_OK))

    def test_color_gui_script(self):
        col_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-color-gui"
        self.assertTrue(os.path.exists(col_path))
        self.assertTrue(os.access(col_path, os.X_OK))

    def test_font_gui_script(self):
        f_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-font-gui"
        self.assertTrue(os.path.exists(f_path))
        self.assertTrue(os.access(f_path, os.X_OK))

    def test_ports_gui_script(self):
        p_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-ports-gui"
        self.assertTrue(os.path.exists(p_path))
        self.assertTrue(os.access(p_path, os.X_OK))

    def test_shortcuts_gui_script(self):
        s_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-shortcuts-gui"
        self.assertTrue(os.path.exists(s_path))
        self.assertTrue(os.access(s_path, os.X_OK))

    def test_flasher_gui_script(self):
        flash_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-flasher-gui"
        self.assertTrue(os.path.exists(flash_path))
        self.assertTrue(os.access(flash_path, os.X_OK))

    def test_logs_gui_script(self):
        logs_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-logs-gui"
        self.assertTrue(os.path.exists(logs_path))
        self.assertTrue(os.access(logs_path, os.X_OK))

    def test_services_gui_script(self):
        srv_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-services-gui"
        self.assertTrue(os.path.exists(srv_path))
        self.assertTrue(os.access(srv_path, os.X_OK))

    def test_startup_gui_script(self):
        st_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-startup-gui"
        self.assertTrue(os.path.exists(st_path))
        self.assertTrue(os.access(st_path, os.X_OK))

    def test_sync_gui_script(self):
        sync_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-sync-gui"
        self.assertTrue(os.path.exists(sync_path))
        self.assertTrue(os.access(sync_path, os.X_OK))

    def test_disk_gui_script(self):
        disk_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-disk-gui"
        self.assertTrue(os.path.exists(disk_path))
        self.assertTrue(os.access(disk_path, os.X_OK))

    def test_speed_gui_script(self):
        speed_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-speed-gui"
        self.assertTrue(os.path.exists(speed_path))
        self.assertTrue(os.access(speed_path, os.X_OK))

    def test_git_gui_script(self):
        git_gui_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-git-gui"
        self.assertTrue(os.path.exists(git_gui_path))
        self.assertTrue(os.access(git_gui_path, os.X_OK))

    def test_git_workspace_scanner(self):
        repos = scan_local_git_workspaces(scan_roots=["/home/ronit138/aero-linux"])
        self.assertIsInstance(repos, list)
        self.assertGreaterEqual(len(repos), 1)
        aero_repo = next((r for r in repos if r["name"] == "aero-linux"), None)
        self.assertIsNotNone(aero_repo)
        if aero_repo is not None:
            self.assertEqual(aero_repo["branch"], "main")
        printed = print_git_workspaces(scan_roots=["/home/ronit138/aero-linux"])
        self.assertIsInstance(printed, list)

    def test_quick_settings_gui_script(self):
        qs_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-quick-settings"
        self.assertTrue(os.path.exists(qs_path))
        self.assertTrue(os.access(qs_path, os.X_OK))

    def test_audio_bt_wifi_displays_gui_scripts(self):
        for script in ["aero-audio", "aero-bluetooth", "aero-wifi", "aero-displays"]:
            path = f"/home/ronit138/aero-linux/packages/aero-welcome/bin/{script}"
            self.assertTrue(os.path.exists(path), f"Missing {script}")
            self.assertTrue(os.access(path, os.X_OK), f"Not executable: {script}")

    def test_gamehub_connect_monitor_updater_gui_scripts(self):
        for script in ["aero-gamehub", "aero-connect-gui", "aero-monitor", "aero-updater"]:
            path = f"/home/ronit138/aero-linux/packages/aero-welcome/bin/{script}"
            self.assertTrue(os.path.exists(path), f"Missing {script}")
            self.assertTrue(os.access(path, os.X_OK), f"Not executable: {script}")

    def test_firewall_gui_script(self):
        fw_path = "/home/ronit138/aero-linux/packages/aero-welcome/bin/aero-firewall-gui"
        self.assertTrue(os.path.exists(fw_path))
        self.assertTrue(os.access(fw_path, os.X_OK))


if __name__ == "__main__":
    unittest.main()
