tput sc # save cursor
gum style --foreground 240 "Press ctrl+d to submit" && gum choose "A" "B" "C" "D" "E" && tput rc && tput el
