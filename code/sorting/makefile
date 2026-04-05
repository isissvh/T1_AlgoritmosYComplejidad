CXX = g++
CXXFLAGS = -std=c++17 -O3 -Wextra -g
TARGET = sorting
ALGDIR = algorithms

OBJECTS = sorting.o mergesort.o quicksort.o sort.o

INPUT_DIR = data/array_input
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
	@mkdir -p $(MEASURE_DIR)
	@for alg in $(ALGORITHMS); do \
		for file in $(INPUT_DIR)/*.txt; do \
			base=$$(basename $$file .txt); \
			IFS="_"; set -- $$base; \
			if [ $$# -ne 4 ]; then \
				echo "Saltando archivo con formato inválido: $$base"; \
				continue; \
			fi; \
			n=$$1; t=$$2; d=$$3; m=$$4; \
			echo "Ejecutando $$alg con $$base"; \
			./$(TARGET) $$alg $$n $$t $$d $$m; \
		done; \
	done

# Limpiar ejecutable y objetos
clean:
	rm -f $(OBJECTS) $(TARGET)

.PHONY: run clean