import time, string, socket, random, os, pdfkit, webbrowser
import urllib.request
import http.cookiejar
from bs4 import BeautifulSoup


def make_output_path(_suffix):
    # Make file name out of current time and the given suffix, e.g. '2020-10-19-15-14.html'
    if _suffix[0:1] != '.':
        _suffix = '.' + _suffix
    _file_name = time.strftime("%Y-%m-%d-%H-%M", time.localtime()) + _suffix
    path = os.path.join(working_dir, _file_name)
    return path


def write_html_template(_template_path, _output_html_path):
    # Dump the HTML template to the output file
    fr = open(_template_path, 'r', encoding='UTF-8')
    template = fr.read()
    fr.close()

    fw = open(_output_html_path, 'a', encoding='UTF-8')
    fw.write(template)
    fw.close()
    return True


def read_local_html(_word, _html_folder_path):
    _file_path = _html_folder_path + _word + '.html'
    _fr = open(_file_path, 'r', encoding='UTF-8')
    _data = _fr.read()
    print("The local page of [" + _word + "] is opened successfully!")
    return _data


def data_downloader(_word, _html_folder_path):
    # Download DRAE result page of the given keyword to a local folder
    socket.setdefaulttimeout(20)
    # Set HTTP connection headers
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gb2313,utf-8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
        "Connection": "keep-alive",
        "referer": "google.com"
    }
    # Set cookie
    cjar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
    headall = []
    # Assemble the headers
    for key, value in headers.items():
        item = (key, value)
        headall.append(item)
    opener.addheaders = headall
    # Install the customized opener to global environment
    urllib.request.install_opener(opener)

    # Make DRAE result url from the keyword
    _url = 'https://dle.rae.es/' + _word
    _http_url = urllib.parse.quote(_url, safe=string.printable)

    # Open result page
    response = urllib.request.urlopen(_http_url, timeout=10)
    _data = response.read()

    # Download the HTML and save it to a local folder
    _html_path = _html_folder_path + _word + ".html"
    _f = open(_html_path, "wb")
    _f.write(_data)
    _f.close()

    print("The page of [" + _word + "] is downloaded successfully!")
    return _data


def read_input_txt(_path):
    # Read input TXT file
    crawl_work_arr = []
    fr = open(_path, 'r', encoding='UTF-8')
    for line in fr:
        # Lower-case all letters and omit the blanks
        crawl_work_arr.append(line[:-1].lower().strip())
    return crawl_work_arr


def crawler(_input_arr, _log_file_path, _output_html_path):
    # CRAWLER
    _progress = 0
    _workload = len(_input_arr)
    _html_folder_path = os.path.join(working_dir, 'html/')
    _file_name_arr = get_html_name_in_dir(_html_folder_path)
    while _progress < _workload:
        _word = _input_arr[_progress]
        _progress += 1
        try:
            if has_word_result(_word, _file_name_arr):
                _page_data = read_local_html(_word, _html_folder_path)
                write_log('local', _progress, _word, _log_file_path)
                time.sleep(random.random() * 2)
            else:
                _page_data = data_downloader(_word, _html_folder_path)
                write_log('downloaded', _progress, _word, _log_file_path)
            _article_arr = parse_article(_page_data)
            write_articles(_article_arr, _output_html_path)
        except:
            print('Error occurred in downloading ' + _word + '!')
            write_log('error', _progress, _word, _log_file_path)


def write_log(_status, _progress, _word, _log_file_path):
    # Write the progress into a TXT log file
    ff = open(_log_file_path, 'a', encoding='UTF-8')
    if _status == 'downloaded':
        ff.write(str(_progress) + '. Managed to download the page of ' + _word + '\n')
    elif _status == 'local':
        ff.write(str(_progress) + '. Managed to open the local page file of ' + _word + '\n')
    elif _status == 'error':
        ff.write(str(_progress) + '. Failed to download the page of ' + _word + '\n')
    else:
        ff.write(str(_progress) + '. Unknown error occurred when processing ' + _word + '\n')
    ff.close()


def count_articles(result):
    # Count the <article> tags in the HTML file, return the quantity
    articles = result.find_all('article')
    return len(articles)


def count_resultados(soup):
    # Count the <div> tags with id = 'resultados' in the HTML file, return the quantity
    tables = soup.find_all('div', id='resultados')
    return len(tables)


def parse_article(page_data):
    # Parse the <article> tags in the HTML file
    soup = BeautifulSoup(page_data, "html.parser")
    if count_resultados(soup) > 0:
        result = soup.find_all('div', id='resultados')[0]
        if count_articles(result) > 0:
            _article_arr = []
            for article in result.find_all('article'):
                _article_arr.append(article)
    return _article_arr


def write_articles(_article_arr, _output_path):
    # Dump the array of <article> tags into the output HTML file
    fw = open(_output_path, 'a', encoding='UTF-8')
    for _article in _article_arr:
        if _article.find('table', class_='cnj'):
            # Skip the <article> of verb conjugations
            continue
        else:
            fw.write(str(_article))
    fw.close()
    return True


def get_html_name_in_dir(_dir_path):
    # Get all the HTML file names in the given directory, return a file name array
    _file_name_arr = []
    _file_list = os.listdir(_dir_path)
    for _file_name in _file_list:
        if _file_name[-5:] == '.html':
            if _file_name not in _file_name_arr:
                _file_name_arr.append(_file_name)
    return _file_name_arr


def has_word_result(_word, _file_name_arr):
    _file_name = _word + '.html'
    if _file_name in _file_name_arr:
        return True
    else:
        return False


def print_pdf(path_wkhtmltopdf, output_html_path, output_pdf_path):
    config = pdfkit.configuration(wkhtmltopdf = path_wkhtmltopdf)
    pdfkit.from_file(output_html_path, output_pdf_path, configuration=config)


def print_word(output_html_path, output_word_path, output_pdf_path):
    import win32com.client
    word = win32com.client.Dispatch('Word.Application')
    doc = word.Documents.Add(output_html_path)
    doc.SaveAs(output_word_path, FileFormat=0)
    doc.SaveAs(output_pdf_path, FileFormat=17)
    doc.Close()
    word.Quit()


def main():
    # Create output file name in the format of '2020-10-19-15-14.html'
    output_html_path = make_output_path('.html')
    output_word_path = make_output_path('.doc')
    output_pdf_path = make_output_path('.pdf')
    # Write the top part of HTML (copied from a DRAE result page) into the output HTML file.
    write_html_template(top_template_path, output_html_path)

    # Read input words from a txt file, where each word takes a line.
    # All letters are lower-cased in this step.
    words_to_crawl_arr = read_input_txt(input_txt_path)
    # Download all the pages of the input words
    crawler(words_to_crawl_arr, log_file_path, output_html_path)

    # Write the bottom part of HTML (copied from a DRAE result page) into the output HTML file.
    write_html_template(bottom_template_path, output_html_path)
    time.sleep(random.random() * 1)

    # Convert the HTML to PDF
    # [IMPORTANT] Both functions can give the pdf output, but neither render the fonts perfectly.as the browsers do.
    # print_pdf(path_wkhtmltopdf, output_html_path, output_pdf_path)
    print_word(output_html_path, output_word_path, output_pdf_path)
    webbrowser.open(output_html_path)


if __name__ == '__main__':
    # Path of HTML templates
    working_dir = os.path.dirname(__file__)
    input_txt_path = os.path.join(working_dir, 'input.txt')
    top_template_path = os.path.join(working_dir, 'html_top.html')
    bottom_template_path = os.path.join(working_dir, 'html_bottom.html')
    log_file_path = os.path.join(working_dir, 'log.txt')

    # [IMPORTANT] Wkhtmltopdf can't render the fonts perfectly.
    # Path of locally installed wkhtmltopdf
    # Downloaded here: https://wkhtmltopdf.org/downloads.html
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

    # Execute the main function
    main()
