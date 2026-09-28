.PHONY: test install clean lint doctor benchmark help

PYTHON := python3
CLI_DIR := packages/aero-cli
GUI_DIR := packages/aero-welcome

help:
	@echo "⚡ Aero Linux Developer Makefile"
	@echo "=========================================="
	@echo "  make test        - Run complete 56+ unit test suite"
	@echo "  make install     - Install Aero CLI & Control Center locally"
	@echo "  make doctor      - Run real-time hardware diagnostics"
	@echo "  make benchmark   - Run multi-core CPU & RAM benchmark"
	@echo "  make clean       - Remove cached bytecode and temp artifacts"
	@echo "=========================================="

test:
	@echo "Running Aero test suite..."
	@cd $(CLI_DIR) && PYTHONPATH=. $(PYTHON) -m unittest discover -s tests -v

install:
	@bash install.sh

doctor:
	@PYTHONPATH=$(CLI_DIR) $(PYTHON) $(CLI_DIR)/bin/aero doctor

benchmark:
	@PYTHONPATH=$(CLI_DIR) $(PYTHON) $(CLI_DIR)/bin/aero benchmark

lint:
	@$(PYTHON) -m py_compile $(CLI_DIR)/aero/*.py $(CLI_DIR)/bin/aero $(GUI_DIR)/bin/aero-welcome
	@echo "All modules compiled clean with zero syntax errors."

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleaned build artifacts."
