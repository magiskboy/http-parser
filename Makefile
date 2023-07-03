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
	${CC} ${CFLAGS} pparser.c pparser.h -c pparser.o

benchmark.o: benchmark.c
	${CC} ${CFLAGS} benchmark.c -c benchmark.o

main.o: main.c
	${CC} ${CFLAGS} main.c -c main.o

clean:
	rm *.o
	rm *.gch
