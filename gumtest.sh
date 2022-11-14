#!/bin/bash

#printf $(gum style --background 31 "Choose some modules") #38! #74

#DESC=$(echo -e $(gum style --faint "\nSome huge description whicch should totally be truncated"))

#echo -e $(gum choose --no-limit --selected.foreground "38" --cursor.foreground "38" "Module Ops \n $(gum style --faint "Some huge description whicch should totally be truncated")" "Module Ops \n$(gum style --faint "Some thuge description whicch should totally be truncated")")

#echo -e $(gum choose --no-limit --selected.foreground "" --cursor.foreground "" "Module Ops $DESC" "Module Ops \n$(gum style --faint "Some thuge description whicch should totally be truncated")")


gum choose --no-limit --selected.foreground "38" --cursor.foreground "38" "Module \n ops $(gum style --faint "Descritionero lero")" "Array ops $(gum style --faint "Some description")" "Unit tests $(gum style --faint "Last description")"