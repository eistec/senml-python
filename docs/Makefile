# Makefile for documentation

DOXYGEN ?= doxygen
BUILDDIR ?= $(CURDIR)

.PHONY: clean
clean:
	rm -rf html

.PHONY: html
html:
	$(DOXYGEN)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

.PHONY: view
view: html
	xdg-open $(BUILDDIR)/html/index.html
