# echo $1
temp_file=temp.md
x=$(printf '%q' "$1")
replacementDate="$(git log --follow --format=%ad --date=short "$1" | tail -1)"
# echo $replacementDate
sed -e "s/^date_created: [0-9\-]*$/date_created: $replacementDate/" "$1" > temp.md
cat temp.md > "$1"
