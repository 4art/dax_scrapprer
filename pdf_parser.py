import re
import io

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
        # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text


class LC:
    def _init__(self, first_name="", last_name="", birth_date="", lc=""):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.lc = lc


def convert_tuple_to_lc_dict(t, company):
    lastname = t[0].replace(",", "").split(" ")[0]
    firstname = t[0].replace(",", "").split(" ")[1]
    birthdate = t[2].split(".")[2] + t[2].split(".")[1] + t[2].split(".")[0]
    return {"lastname": lastname,
            "firstname": firstname, "birthdate": birthdate, "lc": get_lc(lastname, firstname, birthdate),
            "company": company}


def convert_tuple_to_list(t, company):
    return convert_tuple_to_lc_dict(t, company)["c"]


def get_lc(firsname: str, lastname: str, birthdate: str) -> str:
    lastname_lc = convert_name_to_lc(firsname)
    firsname_lc = convert_name_to_lc(lastname)
    return f"{birthdate}{firsname_lc}{lastname_lc}"


def replace_non_engl(s: str) -> str:
    return s.upper().replace("ü", "UE").replace("Ö", "OE").replace("Ä", "AE").replace("ß", "SS").replace("É", "E")


def convert_name_to_lc(name: str) -> str:
    n = replace_non_engl(name)[0:5]
    while len(n) < 5:
        n = n + "#"
    return n


def parse_pdf(pdf_file="deutscheboerse.pdf", path="/tmp/reports/"):
    global text, company, l1
    text = extract_text_from_pdf('%s%s' % (path, pdf_file))
    company = text.split("a) Firma:")[1].split("b) Sitz, Niederlassung")[0] if len(text.split("a) Firma:")) == 2 else \
        text.split("a) Firma")[1].split("b) Sitz, Niederlassung")[0]
    l = re.findall(r"([A-ZÄÖÉ][a-zäöüé]*\,\s[A-ZÄÖßÉ][a-zäöüé]*\,)([^*]+\*)(\d{2}\.\d{2}\.\d{4})",
                   text_splitter(text))
    return list(map(lambda x: convert_tuple_to_lc_dict(x, company), l))


def text_splitter(text):
    if len(text.split("Vorstand:", 1)) == 2:
        return text.split("Vorstand:", 1)[1]
    else:
        if len(text.split("Geschäftsführer:", 1)) == 2:
            return text.split("Geschäftsführer:", 1)[1]
        else:
            if len(text.split("Mitglied des Vorstandes:", 1)) == 2:
                return text.split("Mitglied des Vorstandes:", 1)[1]

    return text


def get_files_in_dir_list(path):
    import os
    directory = os.fsencode(path)
    return list(map(lambda x: x.decode("utf-8"), os.listdir(directory)))


if __name__ == '__main__':
    path = "/tmp/reports/"
    l = []
    for file_name in get_files_in_dir_list(path):
        print(file_name)
        l.extend(parse_pdf(file_name, path))
    s = set(l)
    print(set(l))
