TARGET=flaviofigueiredo_tp2

all:
	pdflatex $(TARGET).tex
	pdflatex $(TARGET).tex
	bibtex $(TARGET)
	pdflatex $(TARGET).tex
	pdflatex $(TARGET).tex

clean:
	rm $(TARGET).aux  $(TARGET).log  $(TARGET).pdf
