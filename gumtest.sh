#S=$(gum format < README.md)
#gum pager "$S"

S=$(gum input --placeholder "package name")
echo "installiing $S"