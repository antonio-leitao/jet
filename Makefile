
help:
	@echo "\nAvailable commnads:"
	@echo ">> clean : removes all pycaches" | sed 's/^/   /'
	@echo ">> commit : commits all changes to git" | sed 's/^/   /'
	@echo ">> release : builds and releases package to Pypy" | sed 's/^/   /'
	@echo ">> add : adds dependency to project with pip" | sed 's/^/   /'

init: 
	@pip install pip-chill 
clean:
	@find . -name \*.pyc -delete
	@find . -type d -name "__pycache__" -delete

commit:
	@git add -A
	@DESCRIPTION=$$(gum write --width 60 --height 6 --base.margin "1 1" --cursor.foreground 31 --placeholder "Details of this change (CTRL+D to finish)");\
	gum confirm --selected.background 31 "Commit changes?" && git commit -m "$$DESCRIPTION"
	@git push origin master

release:
	@python -m build

add:
	@PACKAGE=$$(gum input --placeholder "Type package name");\
	echo "installing $$PACKAGE"

update:
	@UPDATE=$$(gum choose "Major" "Minor" "Patch" --limit "1" --cursor.margin "0 1" --cursor.foreground "");\
	VERSION=$(shell grep -m 1 version pyproject.toml | tr -s ' ' | tr -d '"' | tr -d "'" | cut -d' ' -f3);\
	IFS=. read major minor patch <<<"$$VERSION";\
	if [ "$$UPDATE" = "Major" ]; then\
        major=$$(( $$major + 1 ));\
    fi;\
	if [ "$$UPDATE" = "Minor" ]; then\
        minor=$$(( $$minor + 1 ));\
    fi;\
	if [ "$$UPDATE" = "Patch" ]; then\
        patch=$$(($$patch + 1));\
    fi;\
	NEW="$$major.$$minor.$$patch";\
	sed -i "" "s/^version = ".*"/version = \"$$NEW\"/" pyproject.toml
	
changelog:
	@msg=$$(gum write --width 60 --height 6 --base.margin "1 1" --cursor.foreground 31 --placeholder "Details of this change (CTRL+D to finish)");\
	commit=$$(git log --oneline -1);\
	sha=$$(echo "$$commit" | awk '{print $$1}');\
	echo "- $$sha: $${msg%$$'\n'*}" >> CHANGELOG.md;\
	echo "$$msg" >> CHANGELOG.md
