.phony: all build clean

all: build


build: clean
	@mkdir -p build && cd build && \
		cmake .. && \
		cmake --build . --config Release

clean:
	@rm -rf build
