MODULE = _matrix
SOFILE = $(MODULE)$(shell python3-config --extension-suffix)
SRC = matrix.cpp matrix.h

.PHONY: all test clean
all: $(SOFILE)

$(SOFILE): $(SRC)
	g++ -O3 -Wall -shared -std=c++17 -fPIC -Wl,-undefined,dynamic_lookup `python3 -m pybind11 --includes` $< -o $@

test: $(SOFILE)
	@pytest

clean:
	@rm -rf $(MODULE)`python3-config --extension-suffix` __pycache__ .pytest_cache _matrix*