CXX = g++
CXXFLAGS = -std=c++17 -O3 -Wextra -g
TARGET = sorting
ALGDIR = algorithms

OBJECTS = sorting.o mergesort.o quicksort.o sort.o

INPUT_DIR = data/array_input
OUTPUT_DIR = data/array_output
MEASURE_DIR = data/measurements
ALGORITHMS = quicksort mergesort sort

# Regla principal
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)

# Compilación
sorting.o: sorting.cpp
	$(CXX) $(CXXFLAGS) -c sorting.cpp

mergesort.o: $(ALGDIR)/mergesort.cpp
	$(CXX) $(CXXFLAGS) -c $(ALGDIR)/mergesort.cpp

quicksort.o: $(ALGDIR)/quicksort.cpp
	$(CXX) $(CXXFLAGS) -c $(ALGDIR)/quicksort.cpp

sort.o: $(ALGDIR)/sort.cpp
	$(CXX) $(CXXFLAGS) -c $(ALGDIR)/sort.cpp

# Ejecutar todos los inputs con todos los algoritmos
run: $(TARGET)
	@mkdir -p $(MEASURE_DIR) $(OUTPUT_DIR)
	@for alg in $(ALGORITHMS); do \
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

# Limpiar ejecutable y objetos
clean:
	rm -f $(OBJECTS) $(TARGET)

reset-results:
	rm -f $(MEASURE_DIR)/*.csv
	rm -f $(OUTPUT_DIR)/*.txt

.PHONY: run clean reset-results