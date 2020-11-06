# marc_crawler 

*In honor of my crafty and stingy teacher, Marc. Pero es un buen hombre*.

Author: Tien

Last Update: 2020-10-20

### Introduction

This is a crawler task assigned by my Spanish teacher Marc, aiming to batch download the pages from the Diccionario de la Real Academia Española (DRAE, https://www.rae.es/) and parse it into a collection of definitions, according to the request of his superior. As his student, Tien is not paid anything for sure, therefore it is currently a non-profit, open-source project so far.

The input of this file is a list of vocabulary copied down from the textbook 《现代西班牙语学生用书》(Español Moderno - Libro del Alumno).

The output is ideally a PDF file with a certain template and all the DRAE definitions of the given vocabulary. However, it would be also acceptable if the result is in other formats (which can be converted to PDF easily).

The program is written in python 3.7, with the help of some common libraries including bs4, urllib, etc. To convert HTML into PDF, a software and python library 'wkhtmltopdf' (https://wkhtmltopdf.org/downloads.html) is also used in this program. 

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
- HTML output is finished. (2020-10-20)
- PDF output function is not good, because it's hard to find the HTML to PDF converting tool whose visualization is as good as browsers. As a result, this step has to be done manually.
  - Tried 'wkhtmltopdf', however many fonts were missing, and the word spacing is totally messed up.
  - Tried 'win32com.client' for '.doc' and '.pdf' conversion, while some fonts (titles) are still missing. This solution might be useful in some circumstances, thus it is kept in the main.py.
  - 'webbrowser' is used at the end of the script, opening the output html with default browser.
- A larger-scale test is to be carried out, to test the stability of the software.
- Estimated to finish on: 2020-10-25.

### Issues

- The verb conjugation tables take up a lot of space, while they didn't appear in the previous samples. Whether they should be kept in the HTML or omitted remains to be checked with Marc.
  - Answer: The verb conjugation table should be removed.
- Similarly, whether the etymology sections should be kept or omitted, remains a question.
  - Answer: Word etymology is an interesting part and can be helpful to students. Thus we can keep them.
- The CSS from DRAE contains some printer-friendly features, which provides different styles for browser and printer. However, it is expected to have the 'browser-style' in the 'printed PDF'. Therefore, some modifications in CSS should be done in the next step.
  - Result: Issue fixed in the 2020-10-20 update, by deleting a few lines of CSS code in template (html_top.html) with the beginning of "@media only print..."
- An additional request was mentioned by Marc, which is to keep only the top (3) definitions of a word. However Tien, the developer, suggested that it might cause some confusion, since the definitions are grouped by part of speech in DRAE result.
  - This request is put aside temporarily.
- Duplicate results appeared when inputting the transitive and pronominal forms of a verb, e. g. asombrar, asombrarse.
  - The problem is because both transitive and pronominal forms share a same page in DRAE. The URL "https://dle.rae.es/asombrarse" auto-redirects to "https://dle.rae.es/asombrar".
  - The temporary measure is to remove the pronominal verbs in the inputs (or replace them with the transitive form).
  - In the future, there should be a input checker. If pronominal, then omit '-se', and compare it with the processed ones; if not in history, then process.