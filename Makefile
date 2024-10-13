# Makefile

# Variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
PACKAGE_DIR = package
ZIP_FILE = deployment-package.zip
REQUIREMENTS = requirements.txt

# Targets

.PHONY: all install zip clean

all: install zip

# Set up virtual environment and install dependencies
install:
	@echo "Setting up virtual environment..."
	@test -d $(VENV) || python3 -m venv $(VENV)
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS) -t $(PACKAGE_DIR)

# Package the code and dependencies into a ZIP file
zip: install
	@echo "Copying source files..."
	cp .env handler.py core.py $(PACKAGE_DIR)/
	@echo "Creating ZIP package..."
	cd $(PACKAGE_DIR) && zip -r ../$(ZIP_FILE) .
	@echo "Cleaning up..."
	rm -rf $(PACKAGE_DIR)
	@echo "Package created: $(ZIP_FILE)"

# Clean up virtual environment and ZIP file
clean:
	@echo "Removing virtual environment and ZIP package..."
	rm -rf $(VENV) $(ZIP_FILE)
	@echo "Clean complete."

