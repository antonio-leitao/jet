help:
	@echo "command: clean to clear all pycaches"

clean:
	find . -name \*.pyc -delete
	find . -type d -name "__pycache__" -delete
	
commit:
	@git add -A
	@DESCRIPTION=$$(gum write --placeholder "Details of this change (CTRL+D to finish)");\
	gum confirm "Commit changes?" && git commit -m "$$DESCRIPTION"