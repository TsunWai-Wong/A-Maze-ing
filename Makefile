# === VARIABLES ===
PY = python3
MAIN = a_maze_ing.py

# === INSTALL STUFF ===
install:
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install flake8 mypy
	pip install mlx-2.2-py3-none-any.whl

# === RUN PROJECT, RUN ===
run:
	$(PY) $(MAIN) config.txt

# === DEBUG MODE ===
debug:
	$(PY) -m pdb $(MAIN) config.txt

# === CLEAN TEMP FILES ===
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.pyc" -delete

# === LINT (MANDATORY) ===
lint:
	flake8 .
	mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

# === STRICT LINT ===
lint-strict:
	flake8 .
	mypy . --strict