CXX = g++
CXXFLAGS = -std=c++17 -O3 -Wextra -g
TARGET = sorting
ALGDIR = algorithms

OBJECTS = sorting.o mergesort.o quicksort.o sort.o

INPUT_DIR = data/array_input
OUTPUT_DIR = data/array_output
MEASURE_DIR = data/measurements
ALGORITHMS = quicksort mergesort sort

PYTHON = python3
PLOT_SCRIPT = scripts/plot_generator.py
ARRAY_SCRIPT = scripts/array_generator.py

$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)

sorting.o: sorting.cpp
	$(CXX) $(CXXFLAGS) -c sorting.cpp

mergesort.o: $(ALGDIR)/mergesort.cpp
	$(CXX) $(CXXFLAGS) -c $(ALGDIR)/mergesort.cpp

quicksort.o: $(ALGDIR)/quicksort.cpp
	$(CXX) $(CXXFLAGS) -c $(ALGDIR)/quicksort.cpp

sort.o: $(ALGDIR)/sort.cpp
	$(CXX) $(CXXFLAGS) -c $(ALGDIR)/sort.cpp	

array:
	$(PYTHON) $(ARRAY_SCRIPT)

run: array $(TARGET)
	@mkdir -p $(MEASURE_DIR) $(OUTPUT_DIR)
	@set -- $(INPUT_DIR)/*.txt; \
	if [ "$$1" = "$(INPUT_DIR)/*.txt" ]; then \
		echo "No se encontraron archivos de entrada en $(INPUT_DIR)"; \
		exit 1; \
	fi; \
	for alg in $(ALGORITHMS); do \
		for file in $(INPUT_DIR)/*.txt; do \
			base=$$(basename "$$file" .txt); \
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

all: array run plots

clean:
	rm -f $(OBJECTS) $(TARGET)

reset-results:
	rm -f $(MEASURE_DIR)/*.csv
	rm -f $(OUTPUT_DIR)/*.txt

reset-plots:
	rm -f data/plots/*.png

.PHONY: array run plots all clean reset-results reset-plots
