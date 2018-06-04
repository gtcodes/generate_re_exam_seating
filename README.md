## Seating plan generator

# Description
This is a project to automatically generate seating plans for re-exams at gtg.

It works by taking a tab seperated file and extracting the students from it.
Then it will place all students in an appripiate class room sorted by name.

The python script will then create tex files that can be compiled to pdf.

The bash script will run the python script with the supplied file (-i flag) or download the file from gtg's prövningssite if -d <date> is supplied. It will then compile the latex files with pdflatex and, if -p is supplied, also print it to the standard printer.

The script assumes there is a directory called output in base git directory.

# Description of python program
The program first downloads the csv and extracts the relevant information. That is name, if they have computer or not and test length.

It sorts by name and if a student is registered for more than one test. It merges those.

The function that splits the students into different rooms is quite simple. First it will put all students that require a computer into T26. Then depending on how many students there are they are put into different class rooms. This can easily be added if some other configuration is prefered.

It generates the seating plan by merges some pre-existing latex header and then creating tikz nodes for each student. Look up the tikz package to get some information on how it works.

We chose to use different classes for each room as they behave somewhat differently. But rooms in the same category are very similar. This also means that if you wish to use T3/T4 for example. Just implement how they generally look and its fine.

The cols and rows in the rooms are the number of tables. Then it is assumed that all tables can seat two students if needed. All rooms so far implemented will try to add one person to each table before splitting.

When the seating plan is done it will be printed to a file in the output directory. The program will also print a row to the printInfo.txt file. This is done via the PrinterInfoWriter class. Please only use this to write to the printInfo file to avoid corruptions.

# Description of bash program
The bash program parses the input flags then creates the seating plan via the python script.

The bash script assumes that there is a printer called torg. Even if you wish to print it still asks you before printing. This is just because it is easy to scroll in the bash history and then accidentaly get lots of prints :/.
