.phony: all build clean demo test

all: build


build: clean
	@mkdir -p build && cd build && \
		cmake .. && \
		cmake --build . --config Release

clean:
	@rm -rf build src/pymui/pymui.*.so
	@find . -type d -name __pycache__ -exec rm -rf {} \; -prune
	@find . -type d -path ".*_cache"  -exec rm -rf {} \; -prune

demo:
	@uv run tests/pymui_sdl_demo.py


test:
	@uv run pytest
