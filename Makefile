.PHONY: help init tests test cov docs doc

help:
	@cat make-help.md

init:
	pip install -r requirements.txt

tests: test
test:
	py.test --cov=senml --cov-report=html --cov-report=term --pylint senml tests

cov:
	py.test --cov=senml --cov-report=html --cov-report=term senml tests
	xdg-open coverage_report_html/index.html

docs: doc
doc:
	$(MAKE) -C docs html
