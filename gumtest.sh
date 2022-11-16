S=$(gum format < README.md)
gum pager --margin="0 10" --border-foreground="131" --help.margin="0 10" "$S"
