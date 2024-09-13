# A simple Makefile to build the VDI sample code
#

EXECUTABLE=vdipipesample
LD_FLAGS=-luuid -lrt -lpthread -lsqlvdi
LD_LIBRARY_PATH=/opt/mssql/lib

$(EXECUTABLE): vdipipesample.cpp vdi.h vdierror.h
	clang++ -o $(EXECUTABLE) -g -std=c++11 vdipipesample.cpp $(LD_FLAGS) -L $(LD_LIBRARY_PATH)

clean:
	rm $(EXECUTABLE)


