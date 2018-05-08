#!/bin/bash

texDir="pdf"
separator="\t"
noCsv=1
clearPdfDir=1
print=0
download=0
while getopts ":s:i:d:t:hpkn" opt; do
  case $opt in
    s)
      separator=$OPTARG
      ;;
    h)
      printf "bash script for automatically creating seating plans for re-exams\n"
      printf "use the script by running \n\n ./run -i <path/to/csv>. or ./run -i <date> to download the csv from the provning site."
      printf "\n\nThis will generate tex files and pdfs in the supplied directory. The standard directory is ./pdf.\n"
      printf "The script will remove all .log and .aux files in the supplied tex directory. They can be kept by adding the -k flag\n"
      printf "\nsupported flags are:"
      printf "\n-s <separator>. This will set the specified <seperator> as the csv separator. The standard separator is tab."
      printf "\n-i <path/to/csv> for specifying the inre-exam"
      printf "\n-k flag for keeping all .log and .aux files from pdflatex."
      printf "\n-d <date> for specifying a date which the re-exam occures. Format is yyyy-mm-dd"
      printf "\n-t <Tex directory>. This changes the directory which the pdf and tex files are stored in."
      printf "\n    Note that this directory must exist and will not be created. The standard directory is ./pdf."
      printf "\n-p flag will print the results to the standard printer"
      printf "\n-h display this text."
      exit
      ;;
    i)
      fileName=$OPTARG
      noCsv=0
      ;;
    k)
      clearPdfDir=0
      ;;
    d)
      date="$OPTARG"
      noCsv=0
      download=1
      ;;
    t)
      texDir="$OPTARG"
      echo $texDir
      ;;
    p)
      print=1
      ;;
    ?)
      echo "Invalid parameter: -$OPTARG" >&2
      exit
      ;;
  esac
done

if [ $noCsv = 1 ]; then
  echo "no input file supplied. Please supply an input file using the -i flag or a date with the -d flag" >&2
  exit
fi

if [ $download = 1 ]; then
  fileName="$date.xls"
  wget -O $fileName "82.193.176.94/provning/db/$date.xls"
fi

python3 python/autoTable.py $fileName $texDir $separator

for file in $texDir/*.tex
do
    pdflatex -output-directory $texDir -no-file-line-error $file > "$texDir/pdflog.txt"
done

if [ $print = 1 ]; then
  for file in $texDir/*.pdf
  do
    while read p
    do
      echo $p
      IFS=' '
      read -ra Field <<< "$p"
      echo "$texDir/${Field[0]}" "$file" 
      if [ $texDir/${Field[0]} = "$file" ]; then
        echo lp -d torg $file -o media="${Field[1]}"
      fi
    done <"$texDir/printInfo.txt"
  done
fi

if [ $clearPdfDir = 1 ]; then
  for i in $texDir/*.aux $texDir/*.log
    do
      rm $i
    done
fi
