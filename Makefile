help:
	@echo "command: clean to clear all pycaches"

clean:
	find . -name \*.pyc -delete
	find . -type d -name "__pycache__" -delete