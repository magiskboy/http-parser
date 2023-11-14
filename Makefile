CC := gcc

CFLAGS := -Wall

LDFLAGS := 

benc: benchmark.o pparser.o
	${CC} benchmark.o pparser.o -o benc
	./benc

main: main.o pparser.o
	${CC} main.o pparser.o -o main
	./main

pparser.o: pparser.c pparser.h
	${CC} ${CFLAGS} pparser.c pparser.h -c

benchmark.o: benchmark.c
	${CC} ${CFLAGS} benchmark.c -c

main.o: main.c
	${CC} ${CFLAGS} main.c -c

clean:
	rm -f *.o
	rm -f *.gch
	rm -f benc
