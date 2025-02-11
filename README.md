# kytarycz-akordy-generator
Very simple Python project to generate PDF files from online chordbook akordy.kytary.cz.

# What it does?
This generator parses https://akordy.kytary.cz website and finds all available songs. Then it downloads each individual song HTML and prints it into PDF with all the original formatting.

Python 3 is required for this to work.

# How to use?
1. Download file `kytarycz-generator.py` and install all its Python dependencies.
2. Open command line and navigate to arbitrary folder where you want to store your PDF files.
3. Run `python "<path-to-kytarycz-generator.py>"`
4. Wait.

Run `python "<path-to-kytarycz-generator.py>" --help` to see all available switches and options.