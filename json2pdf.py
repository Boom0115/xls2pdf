# require reportlab from https://bitbucket.org/rptlab/reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A3, A4, B5, landscape, portrait
from reportlab.lib.colors import pink, black, red, blue, green
import json

class Json2pdf():
    # カードサイズ定義
    size_of_tcg = {
        'standard': {'w': 6.3, 'h': 8.8},
           'small': {'w': 5.9, 'h': 8.6},
          'arcade': {'w': 5.8, 'h': 8.1},
    }
    # フォント設定
    font_name = 'HeiseiKakuGo-W5'
    font_size = 12
    pdfmetrics.registerFont(UnicodeCIDFont(font_name))

    padd_h = 0.0
    f_offset = 0.2
    b_offset = 2.1 - f_offset

    padd_l = 1.0
    line_width = 0.5

    card_w = size_of_tcg['standard']['w']
    card_h = size_of_tcg['standard']['h']

    def __init__(self, in_file, out_file):
        self.in_file = in_file
        self.out_file = out_file
        pass

    def init_page(self, max_title=9):
        self.canvas.setFont(self.font_name, self.font_size)
        self.canvas.setDash(1, 2)
        # 裏面を印刷する

        # 横罫線
        for y in range(0, 4):
            y_pos = self.padd_h + (y * self.card_h)
            self.canvas.line(self.b_offset * cm, y_pos * cm,
                        (3 * self.card_w + self.b_offset) * cm, y_pos * cm)

        # 縦罫線
        for x in range(0, 4):
            x_pos = x * self.card_w
            self.canvas.line((x_pos + self.b_offset) * cm, self.padd_h * cm,
                        (x_pos + self.b_offset) * cm, (self.padd_h + 3 * self.card_h) * cm)
        # 裏表紙
        for i in range(0, max_title):
            offset_x = 2 - (i % 3)
            offset_y = 3 - (i // 3 % 3)
            x1 = offset_x * self.card_w + (self.card_w / 2.0) + self.b_offset
            y1 = offset_y * self.card_h - 3.0
            self.canvas.drawCentredString(x1 * cm, y1 * cm, self.title_info['title'])
            self.canvas.drawCentredString(x1 * cm, (y1 + 1.0) * cm, self.title_info['version'])

        self.canvas.showPage()
        self.canvas.setFont(self.font_name, self.font_size)
        self.canvas.setDash(1, 2)

        # 表面の罫線を印刷する
        for y in range(0, 4):
            y_pos = self.padd_h + (y * self.card_h)
            self.canvas.line(self.f_offset * cm, y_pos * cm,
                        (3 * self.card_w + self.f_offset) * cm, y_pos * cm)

        for x in range(0, 4):
            x_pos = x * self.card_w
            self.canvas.line((self.f_offset + x_pos) * cm, self.padd_h * cm,
                        (self.f_offset + x_pos) * cm, (self.padd_h + 3 * self.card_h) * cm)

    def drawCardInfo(self):
        '''カード情報を印刷する'''
        for i, card in enumerate(self.card_info):
            if i % 9 == 0:
                if i > 0:
                    self.canvas.showPage()

                max_title = len(self.card_info) - i
                if max_title > 9:
                    max_title = 9
                self.init_page(max_title)
            offset_x = i % 3
            offset_y = 3 - (i // 3 % 3)
            x1 = offset_x * self.card_w + 2.0
            y1 = offset_y * self.card_h - 1.0
            for col, params in enumerate(card):
                label = str(params[0])
                value = str(params[1])
                if label == 'text':
                    #cur_y = y1 - self.card_h
                    cur_y = y1 - (0.5 * col)
                    #textObj = self.canvas.beginText()
                    #textObj.setTextOrigin(x1*cm, cur_y*cm)
                    #textObj.setFont(self.font_name, 8)
                    #textObj.textLine(value)
                    #self.canvas.drawString(x1 * cm, cur_y * cm, value)
                    self.canvas.setFont(self.font_name, 5)
                    text_x = x1 - 1.5
                    for idx, line in enumerate(value.split('\n')):
                        cur_y = y1 - (0.5 * col + 0.3 * idx)
                        self.canvas.drawString(text_x * cm, cur_y * cm, line)
                    self.canvas.setFont(self.font_name, self.font_size)

                else:
                    cur_y = y1 - (0.5 * col)
                    self.canvas.drawRightString(x1 * cm, cur_y * cm, label + ': ')
                    self.canvas.drawString(x1 * cm, cur_y * cm, value)


    def export(self):

        # .json ファイルからカード情報を取得
        with open(self.in_file, mode='r', encoding='utf-8') as f:
            j_info = json.load(f)

        self.card_info = j_info['card_info']
        self.title_info = j_info['title_info']

        # .pdf 生成開始
        self.canvas = canvas.Canvas(self.out_file)

        # PDF文書設定
        self.canvas.setAuthor(self.title_info['author'])
        self.canvas.setTitle(self.title_info['title'])
        self.canvas.setSubject(self.title_info['version'])

        # A4
        self.canvas.setPageSize(portrait(A4))  # A4縦
        # self.canvas.setPageSize(landscape(A4)) # A4横

        # カラー設定
        #self.canvas.setFillColorRGB(100, 0, 0, 0.5)
        self.canvas.setFillColor(black)
        self.canvas.setStrokeColor(black)
        self.canvas.setLineWidth(self.line_width)

        # カードページ生成
        self.drawCardInfo()

        # 最終出力
        # self.canvas.restoreState()
        self.canvas.showPage()
        self.canvas.save()

if __name__ == '__main__':
    i_file = './tmp/tmp_card_info.json'
    o_file = './out/card.pdf'
    json_to_pdf = Json2pdf(i_file, o_file)
    json_to_pdf.export()
