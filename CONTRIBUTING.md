# 🛠️ Contributing to Aero Linux

Thank you for your interest in contributing to Aero Linux! We welcome pull requests for bug fixes, performance optimizations, desktop themes, and new CLI modules.

---

## 🏗️ Development Setup

1. **Fork & Clone:**
   ```bash
   git clone https://github.com/ronitgupta138/aero-linux.git
   cd aero-linux
   ```

2. **Run the Test Suite:**
   ```bash
   cd packages/aero-cli
   PYTHONPATH=. python3 -m unittest discover -s tests -v
   ```

3. **Verify Bytecode Compilation:**
   ```bash
   python3 -m py_compile aero/*.py bin/aero
   ```

---

## 🌿 Branching & Git Conventions

* Create a descriptive feature branch:
  * `feat/new-database-preset`
  * `fix/sway-waybar-translucency`
  * `docs/update-dual-boot-guide`
* Write clear, imperative commit messages:
  * `feat(cli): add aero gpu vram telemetry monitor`
  * `fix(power): correct p-state governor parsing for intel cpufreq`

---

## 🧪 PR Checklist

Before submitting your pull request:
- [ ] Added unit tests under `packages/aero-cli/tests/test_aero.py` for new commands.
- [ ] All 23+ unit tests pass cleanly (`python3 -m unittest discover`).
- [ ] Maintained zero third-party pip dependencies (standard library only).
- [ ] Updated command documentation in `docs/COMMANDS.md` and `README.md`.
