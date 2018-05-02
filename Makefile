#############################################################################
# Copyright (C) 2018  Rafal Kobel <rafalkobel@rafyco.pl>
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
# Author: Rafal Kobel <rafalkobel@rafyco.pl>
# Project: protemp
# Description: protemp - Project template 
#############################################################################


PYTHON=python3
SETUP=$(PYTHON) setup.py
RM=rm -rf
COPY=cp
DOC=epydoc
PYLINT=pylint
PYLINT_FLAGS=-f parseable -d I0011,R0801,R0902,R0903,R0921

DOC_FILE=templateme_docs
DOC_PDF=dist
PLINT_OUT=pylint.out


#############################################################################

all: test documentation build clean

ifeq ($(OS),Windows_NT)

build: build-example build-tgz build-wnd build-dumb
	@echo "Zbudowano elementy"
build-wnd:
	@$(SETUP) bdist_wininst
	@echo "Zbudowano instalator dla platformy Windows"

else

build: build-example build-tgz build-dumb
	@echo "Zbudowano elementy"

endif

build-tgz:
	@$(SETUP) bdist
	@echo "Zbudowano pakiet tgz"


build-dumb:
	@$(SETUP) bdist_dumb

documentation: doc-pdf doc-html

doc-pdf:
	@$(DOC) -v -o $(DOC_PDF) --pdf --name "protemp Documentation" protemp

doc-html:
	@$(DOC) -v protemp --html -o $(DOC_FILE)

pylint:
	@$(PYLINT) $(PYLINT_FLAGS) protemp

clean:
	@$(RM) $(DOC_PDF)/*.tex
	@$(RM) *.aux *.idx *.log *.out *.toc *.dvi
	@$(RM) $(DOC_PDF)/*.aux $(DOC_PDF)/*.idx $(DOC_PDF)/*.log $(DOC_PDF)/*.out build $(DOC_PDF)/*.toc $(DOC_PDF)/*.dvi
	@$(RM) */__pycache__

test:
	@$(PYTHON) -m protemp.tests

remove: clean
	@echo Usuwanie wygenerowanych plikow
	@$(RM) $(DOC_PDF) $(DOC_FILE)
	@$(RM) protemp.egg-info
	@$(RM) dist

install: remove
	@$(SETUP) install

jenkins-test: remove documentation test build clean
	@echo "Project jenkins"

help:
	@echo "Lista dostepnych polecen."
	@echo " "
	@echo "install       - Instalacja pakietu protemp"
	@echo "build         - Tworzenie plikow budowania"
	@echo "test          - Wykonanie testow"
	@echo "documentation - Budowanie dokumentacji."
	@echo "doc-pdf       - Budowanie dokumentacji pdf"
	@echo "doc-html      - Budowanie dokumentacji html"
	@echo "clean         - Usuniecie plikow budowania"
	@echo "remove        - Wyczyszczenie repozytorium ze zbednych plikow"
	@echo "jenkins-test  - Zadania dla mechanizmow Jenkinsa"
