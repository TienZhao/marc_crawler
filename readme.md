# marc_crawler 

*In honor of my crafty and stingy teacher, Marc. Pero es un buen hombre*.

Author: Tien

Last Update: 2020-10-20

### Introduction

This is a crawler task assigned by my Spanish teacher Marc, aiming to batch download the pages from the Diccionario de la Real Academia Española (DRAE) and parse it into a collection of definitions, according to the request of his superior. As his student, Tien is not paid anything for sure, therefore it is currently a non-profit, open-source project so far.

The input of this file is a list of vocabulary copied down from the textbook 《现代西班牙语学生用书》(Español Moderno - Libro del Alumno).

The output is ideally a PDF file with a certain template and all the DRAE definitions of the given vocabulary. However, it would be also acceptable if the result is in other formats (which can be converted to PDF easily).

The program is written in python 3.7, with the help of some common libraries including bs4, urllib, etc.

### Roadmap

- Read the input TXT into an array of words.
- Make an empty HTML file with the CSS of DRAE.
- Download the DRAE result pages according to the vocabulary array. (Or open from the local history.)
- Parse the definition elements (\<article\>) and copy them to the output HTML.
- Save the output HTML file.
- Save the PDF file accordingly.

### Update

- The project started and the requirements are defined. (2020-10-13)
- The roadmap is drafted. (2020-10-18)
- Crawler function is finished. (2020-10-19)
- HTML output is generally good, but with some minor issues. (2020-10-20)
- Estimated to finish on: 2020-10-25.

### Issues

- The verb conjugation tables take up a lot of space, while they didn't appear in the previous samples. Whether they should be kept remain to be checked with Marc.
- The CSS from DRAE contains some printer-friendly features, which provides different styles for browser and printer. However, it is expected to have the 'browser-style' in the 'printed PDF'. Therefore, some modifications in CSS should be done in the next step.