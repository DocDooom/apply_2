# Makefile
PYTEST= pytest

TEST_DIR = tests

test:
	@echo "Running tests..."
	$(PYTEST) $(TEST_DIR)