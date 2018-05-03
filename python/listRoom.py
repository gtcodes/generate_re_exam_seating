from room import Room

class ListRoom(Room):

    def __init__(self, name, col, row):
        super().__init__(name, col, row)

    def createSeating(self, students):
        seating = ''
        for s in students:
            seating += "\\item " + s.name + '\n'
        return(seating)
    
    def latexHeader(self):
        return ('\\documentclass{article}\n'
                '\\usepackage[utf8]{inputenc}\n'
                '\n'
                '\\begin{document}\n'
                '\\begin{center}\n'
                '\\huge T26\n'
                '\\end{center}\n'
                '\\vspace{7mm}\n'
                '\\begin{itemize}\n'
                '\\large\n'
                )


    def latexFooter(self):
        return ('\\end{itemize}\n'
                '\\end{document}\n'
                )
