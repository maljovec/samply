INCLUDEPATH=.
LIBS = -lann 

GCC = g++ -O4 

createCVT:  createCVT.o runUtils.o 
	$(GCC) -o createCVT createCVT.o runUtils.o $(LIBS)

createCVT.o:       createCVT.cpp runUtils.h
	$(GCC) -o createCVT.o -c createCVT.cpp -I$(INCLUDEPATH) 

runUtils.o:       runUtils.cpp
	$(GCC) -o runUtils.o -c runUtils.cpp 

clean:
	rm createCVT.o runUtils.o

