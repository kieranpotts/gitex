#
# Task runner for this project's development lifecycle. Each target wraps a
# same-named script in `run/`.
#

.PHONY: install check fix help

help:
	@echo "Available targets:"
	@echo "  install  - Install project dependencies"
	@echo "  check    - Run all static and runtime tests"
	@echo "  fix      - Run all automated fixes"
	@echo "  help     - Show this help message"

install:
	./run/install

check:
	./run/check

fix:
	./run/fix
