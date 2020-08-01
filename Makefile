style_args = -v --max-line-length=100

.PHONY: stylecheck
stylecheck:
	pycodestyle $(style_args) .

.PHONY: test
test:
	python -m unittest