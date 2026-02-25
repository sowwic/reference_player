SHELL := /bin/bash

APP_NAME = reference-player
DIST_DIR = dist
BUILD_DIR = build
MKDOCS_SITE_DIR = site
TEST_OUTPUT_DIR = .test_output

APP_PATH = $(DIST_DIR)/$(APP_NAME).app
MAC_APPLICATIONS_DIR = /Applications


# Colors
BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
MAGENTA := \033[35m
CYAN := \033[36m
RESET := \033[0m

# Banner helper
define banner
	@printf "$(CYAN)==>$(RESET) $(1)\n"
endef

.PHONY: help 
help: ## Show this help message
	@echo "Available make targets:"
	@echo ""
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS=":.*?##"}; {printf "  %-15s %s\n", $$1, $$2}'
	@echo ""

.PHONY: clean
clean: ## Remove build artifacts, cache, and temporary files
	$(call banner, Cleaning project...)
	@rm -rf .pytest_cache
	@rm -rf .ruff_cache
	@rm -rf __pycache__
	@rm -rf .coverage
	@rm -rf src/**/__pycache__
	@rm -rf tests/**/__pycache__
	@rm -rf $(BUILD_DIR)
	@rm -rf $(DIST_DIR)
	@rm -rf $(TEST_OUTPUT_DIR)
	@rm -rf $(MKDOCS_SITE_DIR)
	@printf "$(GREEN)Clean up complete.$(RESET)\n"

.PHONY: lint
lint: ## Run the Ruff linter on source and test files
	$(call banner, Running Ruff linter...)
	@uv run ruff check src tests || true

.PHONY: lint-fix
lint-fix: ## Runs the Ruff linter on source and test files and applies fixes
	$(call banner, Running Ruff linter...)
	@uv run ruff check --fix src tests || true

.PHONY: format
format: ## Run the Ruff formatter on source and test files
	$(call banner, Running Ruff formatter...)
	@uv run ruff format src tests

.PHONY: pytest
pytest: ## Run pytest on tests directory
	$(call banner, Running pytest...)
	
	@uv run pytest tests
	
	
.PHONY: pytest-pdb
pytest-pdb: ## Run pytest with pdb on failure
	$(call banner, Cleaning pytest output dir...)
	@rm -rf $(TEST_OUTPUT_DIR)
	$(call banner, Running pytest with pdb...)
	
	@uv run pytest -vvv --pdb --log-cli-level=DEBUG tests
	
	
.PHONY: mkdocs
mkdocs:  ## Run MkDocs development server
	$(call banner, Building MkDocs documentation...)
	@uv run mkdocs serve
.PHONY: check
check: lint pytest. ## Run all checks (linting and testing)

build: qrc ## Build the application and QRCusing uv
	$(call banner, Building $(APP_NAME)...)
	@uv build



.PHONY: qrc
qrc:  ## Generate Python resources from Qt .qrc files
	$(call banner, Generating QRC resources...)
	@pyside6-rcc src/reference_player/resources/resources.qrc -o src/reference_player/resources/resources_rc.py
	@printf "$(GREEN)QRC generation complete.$(RESET)\n"

.PHONY: qml-object-dump
qmltypes:  ## Generate QML types json
	$(call banner, Generating QML types json...)
	pyside6-metaobjectdump src/**/*.py --out-file .qmltypes
	@printf "$(GREEN)QML types json generation complete.$(RESET)\n"

	
.PHONY: iconset
iconset:  ## Generate .icns icon from source PNG using sips and iconutil
	$(call banner, Generating iconset...)
	@mkdir -p resources/icons/reference-player.iconset
	@sips -z 16 16     src/reference_player/resources/icons/reference_player.png --out src/reference_player/resources/icons/reference-player.iconset/icon_16x16.png
	@sips -z 32 32     src/reference_player/resources/icons/reference_player.png --out src/reference_player/resources/icons/reference-player.iconset/icon_16x16@2x.png
	@sips -z 32 32     src/reference_player/resources/icons/reference_player.png --out src/reference_player/resources/icons/reference-player.iconset/icon_32x32.png
	@sips -z 64 64     src/reference_player/resources/icons/reference_player.png --out src/reference_player/resources/icons/reference-player.iconset/icon_32x32@2x.png
	@sips -z 128 128   src/reference_player/resources/icons/reference_player.png --out src/reference_player/resources/icons/reference-player.iconset/icon_128x128.png
	@sips -z 256 256   src/reference_player/resources/icons/reference_player.png --out src/reference_player/resources/icons/reference-player.iconset/icon_128x128@2x.png
	@sips -z 256 256   src/reference_player/resources/icons/reference_player.png --out src/reference_player/resources/icons/reference-player.iconset/icon_256x256.png
	@sips -z 512 512   src/reference_player/resources/icons/reference_player.png --out src/reference_player/resources/icons/reference-player.iconset/icon_256x256@2x.png
	@sips -z 512 512   src/reference_player/resources/icons/reference_player.png --out src/reference_player/resources/icons/reference-player.iconset/icon_512x512.png
	@sips -z 1024 1024 src/reference_player/resources/icons/reference_player.png --out src/reference_player/resources/icons/reference-player.iconset/icon_512x512@2x.png
	@iconutil -c icns src/reference_player/resources/icons/reference-player.iconset -o src/reference_player/resources/icons/reference-player.icns
	@printf "$(YELLOW)Removing temp iconset files...$(RESET)\n"
	@rm -rf src/reference_player/resources/icons/reference-player.iconset
	@printf "$(GREEN)Iconset generation complete.$(RESET)\n"

.PHONY: update-version
update-version: ## Update the version in pyproject.toml to match the VERSION file
	$(call banner, Updating version in pyproject.toml...)
	@VERSION=$$(cat VERSION); \
	printf "$(CYAN)==>$(RESET) Updating pyproject.toml version to %s\n" "$$VERSION"; \
	uv version $$VERSION
	
.PHONY: install
install:  ## Install the application using PyInstaller
	$(call banner, Installing $(APP_NAME) using PyInstaller...)
	@VERSION=$$(cat VERSION); \
	printf "$(CYAN)==>$(RESET) Installing $(APP_NAME) v%s into $(MAC_APPLICATIONS_DIR)...\n" "$$VERSION"; \
	cp -R "$(APP_PATH)" "$(MAC_APPLICATIONS_DIR)/"; \
	printf "$(GREEN)Installation complete.$(RESET)\n"
	
