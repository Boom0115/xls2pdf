import xls2json
import json2pdf

def xls2pdf(path_xls):
    import os
    filename = os.path.splitext(os.path.basename(path_xls))[0]

    xls_file = path_xls

    json_file = './tmp/' + filename + '.json'
    pdf_file = './out/' + filename + '.pdf'

    excel_to_json = xls2json.Xls2json(xls_file, json_file)
    excel_to_json.export()

    json_to_pdf = json2pdf.Json2pdf(json_file, pdf_file)
    json_to_pdf.export()

def main():
    import glob
    import sys
    print(sys.argv)

    xls_files = glob.glob('./in/*.xlsx')
    for path_xls in xls_files:
        xls2pdf(path_xls)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--i', help='path for input excel files')
    parser.add_argument('--o', help='path for output pdf files')
    main()
    print('done')
