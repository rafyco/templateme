#############################################################################
# Author: %AUTHOR% <%EMAIL%>
# Project: %NAME%
# Description:
#############################################################################


CC              = gcc
CXX             = g++
#INCPATH         = -I../mingw491_32/mkspecs/win32-g++'
LINKER          = 
LFLAGS          = -Wl,-subsystem,console -mthreads
ED              = sed
DEL_FILE        = rm -f
DEL_DIR         = rm -rf
MOVE            = mv -f
CHK_DIR_EXISTS  = test -d
MKDIR           = mkdir -p

OBJECTS_DIR     = bin/
TARGET         = $(OBJECTS_DIR)/%NAME%.exe


.SUFFIXES: .cpp .cc .cxx .c

.cpp.o:
	$(CXX) -c $(CXXFLAGS) $(INCPATH) -o $@ $<

.cc.o:
	$(CXX) -c $(CXXFLAGS) $(INCPATH) -o $@ $<

.cxx.o:
	$(CXX) -c $(CXXFLAGS) $(INCPATH) -o $@ $<

.c.o:
	$(CC) -c $(CFLAGS) $(INCPATH) -o $@ $<

####### Build rules

all: $(TARGET) build

clean:
	$(DEL_FILE) *.o $(OBJECTS_DIR)/*.o
	
# Please write regule for exe file compile	
$(TARGET): 
	
	
	
