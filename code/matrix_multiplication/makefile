CXX = g++
CXXFLAGS = -std=c++17 -O3 -Wextra -g
TARGET = matrix_multiplication
ALGDIR = algorithms

OBJECTS = matrix_multiplication.o naive.o strassen.o

INPUT_DIR = data/matrix_input
OUTPUT_DIR = data/matrix_output
MEASURE_DIR = data/measurements/multiplication
ALGORITHMS = naive strassen

PYTHON = python3
PLOT_SCRIPT = scripts/plot_generator.py
MATRIX_SCRIPT = scripts/matrix_generator.py

$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)

matrix_multiplication.o: matrix_multiplication.cpp
	$(CXX) $(CXXFLAGS) -c matrix_multiplication.cpp

naive.o: $(ALGDIR)/naive.cpp
	$(CXX) $(CXXFLAGS) -c $(ALGDIR)/naive.cpp

strassen.o: $(ALGDIR)/strassen.cpp
	$(CXX) $(CXXFLAGS) -c $(ALGDIR)/strassen.cpp

matrix:
	$(PYTHON) $(MATRIX_SCRIPT)

run: matrix $(TARGET)
	@mkdir -p $(MEASURE_DIR) $(OUTPUT_DIR)
	@set -- $(INPUT_DIR)/*.txt; \
	if [ "$$1" = "$(INPUT_DIR)/*.txt" ]; then \
		echo "No se encontraron archivos de entrada en $(INPUT_DIR)"; \
		exit 1; \
	fi; \
	for alg in $(ALGORITHMS); do \
		for file in $(INPUT_DIR)/*_1.txt; do \
			base=$$(basename "$$file" _1.txt); \
			n=$${base%%_*}; \
			rest=$${base#*_}; \
			t=$${rest%%_*}; \
			rest=$${rest#*_}; \
			d=$${rest%%_*}; \
			m=$${rest#*_}; \
			echo "Ejecutando $$alg con $$base"; \
			./$(TARGET) $$alg $$n $$t $$d $$m; \
		done; \
	done

plots:
	$(PYTHON) $(PLOT_SCRIPT)

all: matrix plots

clean:
	rm -f $(OBJECTS) $(TARGET)

reset-results:
	rm -f $(MEASURE_DIR)/*.csv
	rm -f $(OUTPUT_DIR)/*.txt

.PHONY: matrix run plots all clean reset-results
