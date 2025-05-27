# Find the bibkey of a title in a bibliography

title="$1"
bib_path=~/Documents/theory/sources.bib
line_number="$(grep -n "{$title}" $bib_path | cut -f1 -d:)"
line_number=$(( $line_number-1 ))
line="$(sed "$line_number""q;d" $bib_path)"
found_bib_key=false


while ! $found_bib_key
do
    case $line in
        @*)
            found_bib_key=true
            ;;
        *)
            line_number=$(( $line_number-1 ))
            line="$(sed "$line_number""q;d" $bib_path)"
            ;;
    esac
done

bib_key=$(echo "$line" | sed 's/@.*{\(.*\),/\1/')
echo "~/Documents/theory/notes/$bib_key.md"
