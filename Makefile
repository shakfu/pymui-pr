.phony: all build clean test

all: build


build: clean
	@mkdir -p build && cd build && \
		cmake .. && \
		cmake --build . --config Release

clean:
	@rm -rf build

test:
	@uv run pytest
