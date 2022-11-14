help:
	@echo "\nAvailable commnads:"
	@echo ">> clean : removes all pycaches" | sed 's/^/   /'
	@echo ">> commit : commits all changes to git" | sed 's/^/   /'

clean:
	find . -name \*.pyc -delete
	find . -type d -name "__pycache__" -delete

commit:
	@git add -A
	@DESCRIPTION=$$(gum write --width 60 --height 6 --base.margin "1 1" --cursor.foreground 31 --placeholder "Details of this change (CTRL+D to finish)");\
	gum confirm --selected.background 31 "Commit changes?" && git commit -m "$$DESCRIPTION"
	git push origin master