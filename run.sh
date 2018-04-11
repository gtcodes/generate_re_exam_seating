texDir="pdf"
separator='a\t'
noCsv=1
clearPdfDir=1
while getopts ":s:i:d:hkn" opt; do
  case $opt in
    s)
      separator=$OPTARG
      ;;
    h)
      printf "bash script for automatically creating seating plans for re-exams\n"
      printf "use the script by running \n\n ./run -i <path/to/csv>.\n\nThis will generate tex files and pdfs in the supplied directory. The standard directory is ./pdf.\n"
      printf "The script will remove all .log and .aux files in the supplied tex directory. They can be kept by adding the -k flag\n"
      printf "\nsupported flags are:"
      printf "\n-s <separator>. This will set the specified <seperator> as the csv separator. The standard separator is tab."
      printf "\n-i <path/to/csv> for specifying the input file"
      printf "\n-k flag for keeping all .log and .aux files from pdflatex."
      printf "\n-d <directory>. This changes the directory which the pdf and tex files are stored in. Note that this directory must exist and will not be created. The standard directory is ./pdf."
      printf "\n-h display this text."
      exit
      ;;
    i)
      csvFile=$OPTARG
      noCsv=0
      ;;
    k)
      clearPdfDir=0
      ;;
    d)
      texDir="$OPTARG"
      echo $texDir
      ;;
    ?)
      echo "Invalid parameter: -$OPTARG" >&2
      exit
      ;;
  esac
done

if [ $noCsv = 1 ]; then
  echo "no input file supplied. Please supply an input file using the -i flag" >&2
  exit
fi

python3 python/autoTable.py $csvFile $texDir $separator

for i in "$texDir/*"
do
  for file in $i
  do
    pdflatex -output-directory "$texDir" -no-file-line-error $file
  done
done

if [ $clearPdfDir = 1 ]; then
  for i in "$texDir/*.aux" "$texDir/*.log"
  do
    for file in $i
    do
      rm $file
    done
  done
fi
