#!/bin/sh

option="${1}"
echo $option >&2
case ${option} in
    # *arxiv*) echo "Doing an arxiv"
    #     vibes="arxiv"
    #     echo "Eat shit, this isn't implemented yet"
    #     exit 1
    #     ;;
    *doi*) echo "doi url" >&2
        vibes="doi"
        url="${option}"
        number="$(echo "$url" | sed 's/.*\.org\/\(.*\)/\1/')"
        # echo $url
        # echo $number
        ;;
    10.*) echo "doi number" >&2
        vibes="doi"
        number="${option}"
        url="https://doi.org/$number"
        # echo $url
        # echo $number
        ;;
    [0-9][0-9][0-9]*) echo "isbn" >&2
        vibes="isbn"
        # isbn=0226511928
        isbn="${option}"
        url="http://openlibrary.org/search.json?q=${isbn}&fields=title,subtitle,author_name,publish_year,publisher,isbn,publish_place"
        ;;
    *openreview*) #echo "openreview"
        vibes="openreview"
        url="${option}"
        number="$(echo "$url" | grep -oP '(?<=id=)[a-zA-Z0-9_]+')"
        # echo $number
        ;;
    https://*) #echo "url generally"
        vibes="website"
        url="${option}"
        ;;
    *) echo "Crying, pissing, and shitting" >&2
        exit 1
esac


case ${vibes} in
    # "arxiv") echo "Doing an arxiv"
    #     echo "Eat shit, this isn't implemented yet"
    #     exit 1
    #     ;;
    "doi") echo "requesting ${url}" >&2
        art="$(curl -LH "Accept: application/x-bibtex" "${url}")"
        tabbed="$(echo $art | sed 's/@\([a-zA-Z]*\){\([a-zA-Z0-9_]*\), title/@\1{\2,\n    title/' | sed 's/month=\([a-zA-Z0-9]*\),/month={\1},/'| sed 's/DOI/doi/' | sed 's/ISSN/issn/' | sed 's/}, /},\n    /g' | sed 's/} }/},\n}/' | sed 's/=/ = /')"
        ;;
    "isbn") echo "isbn" >&2
        art="$(curl $url)"
        tabbed="$(echo "$art" | python3 -c "import sys, json; a = json.load(sys.stdin); relevant=a['docs'][0]; title=relevant['title']; subtitle = relevant['subtitle'] if 'subtitle' in relevant.keys() else ''; year=relevant['publish_year'][0]; authors=' and '.join([f'{name.split(' ')[1]}, {name.split(' ')[0]}' for name in relevant['author_name']]);publisher=','.join(relevant['publisher']);isbn='$isbn';publish_place=','.join(relevant['publish_place']) if 'publish_place' in relevant.keys() else '';print('@book{heheheha,\n    title = {'+title+'},\n    subtitle = {'+subtitle+'},\n    author = {'+authors+'},\n    year = {'+str(year)+'},\n    publisher = {'+publisher+'},\n    isbn = {'+str(isbn)+'},\n    location = {'+publish_place+'},\n}')")" # removed heheheha because author logic added after
        ;;
    "openreview") echo "openreview" >&2
        tabbed="$(yank_openreview.py $number)"
        ;;
    "website")
        tabbed="@online{,
    author = {},
    title = {},
    year = {},
    month = {},
    publisher = {},
    url = {$url},
    urldate = {$(date -I)},
}"
        ;;
    *) echo "How did you get here"
        exit 1
esac

echo "$tabbed"
