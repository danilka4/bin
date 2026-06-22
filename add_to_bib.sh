#!/bin/sh

tmp_path="/tmp/temp.bib"
bib_path="/home/lizzy/Documents/theory/sources.bib"
author_list=$(grep '^@' "$bib_path" | sed 's/@[a-zA-Z]*{\(.*\),/\1/')

final_entry="$@"
final_entry=$(echo "$final_entry

")
final_key="$(echo "$final_entry" | grep '^@.*' | sed 's/@[a-zA-Z]*{\(.*\),/\1/' )"

if grep -q "{$final_key," "$bib_path"; then
    echo "Duplicate entry $final_key, try again"
    sleep 1
    echo "$final_entry" | tha stdin "${2}"
    exit 1
fi


# Logic to see if at beginning or end before doing binary search
if [[ "$final_key" < $(echo "$author_list" | head -n 1) ]]; then
    echo "$final_entry" | cat - "$bib_path" > "$tmp_path"
    mv "$tmp_path" "$bib_path"
    echo "Placing at the beginning"
elif [[ "$final_key" > $(echo "$author_list" | tail -n 1) ]]; then
    echo "$final_entry" | cat "$bib_path" - > "$tmp_path"
    mv "$tmp_path" "$bib_path"
    echo "Placing at the end"
else
    # Can do binary search but screw that
    for next_key in $author_list; do
        if [[ "$final_key" < "$next_key" ]]; then
            next_line=$(grep "$next_key" $bib_path | head -n 1)
            next_line="${next_line:1}"
            break
        fi
    done
    # echo $next_line
    next_ln=$(grep -n "$next_line" "$bib_path" | head -n 1 | sed 's/\([0-9]*\):.*/\1/')
    head -n "$((next_ln - 1))" "$bib_path" > /tmp/head.bib
    tail -n +"$next_ln" "$bib_path" > /tmp/tail.bib
    echo "$final_entry
" | cat /tmp/head.bib - /tmp/tail.bib > "$bib_path"
    echo "Placing before $next_key"
fi

