#############################################################################
# Copyright (C) %YEAR% %AUTHOR% <%EMAIL%>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
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
	
	
	
