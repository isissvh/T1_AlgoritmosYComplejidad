CXX = g++
CXXFLAGS = -std=c++17 -O3 -Wextra -g
TARGET = matrix_multiplication
ALGDIR = algorithms

OBJECTS = matrix_multiplication.o naive.o strassen.o

INPUT_DIR = data/matrix_input
OUTPUT_DIR = data/matrix_output
MEASURE_DIR = data/measurements/multiplication
ALGORITHMS = naive strassen

# Regla principal
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)

# Compilación
matrix_multiplication.o: matrix_multiplication.cpp
	$(CXX) $(CXXFLAGS) -c matrix_multiplication.cpp

naive.o: $(ALGDIR)/naive.cpp
	$(CXX) $(CXXFLAGS) -c $(ALGDIR)/naive.cpp

strassen.o: $(ALGDIR)/strassen.cpp
	$(CXX) $(CXXFLAGS) -c $(ALGDIR)/strassen.cpp

# Ejecutar todos los inputs con todos los algoritmos
# Se recorren solo los archivos *_1.txt para no repetir pares
run: $(TARGET)
	@mkdir -p $(MEASURE_DIR) $(OUTPUT_DIR)
	@for alg in $(ALGORITHMS); do \
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

# Limpiar ejecutable y objetos
clean:
	rm -f $(OBJECTS) $(TARGET)

reset-results:
	rm -f $(MEASURE_DIR)/*.csv
	rm -f $(OUTPUT_DIR)/*.txt

.PHONY: run clean reset-results