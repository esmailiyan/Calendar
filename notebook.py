﻿from pages import *
import os


class Notebook():
    def __init__(self, **kwargs) -> None:
        # general
        self.name = kwargs.get('name', 'Untitle-Notebook')
        self.rtl = kwargs.get('rtl', True)
        self.width = kwargs.get('width', 148)
        self.height = kwargs.get('height', 210)
        self.scale = kwargs.get('scale', 2.83465)

        # Trim Mark
        self.trimMarkMargin = kwargs.get('trimMarkMargin', 3)
        self.trimMark = kwargs.get('trimMark', 0)

        # margin and padding
        self.margin = kwargs.get(
            'margin',
            {'top': 5, 'outside': 5, 'bottom': 5, 'inside': 0}
        )
        if isinstance(self.margin, list):
            lst = ['top', 'outside', 'bottom', 'inside']
            self.margin = dict(zip(lst, self.margin))

        self.padding = kwargs.get(
            'padding',
            {'top': 32, 'outside': 0, 'bottom': 10, 'inside': 0}
        )
        if isinstance(self.padding, list):
            lst = ['top', 'outside', 'bottom', 'inside']
            self.padding = dict(zip(lst, self.padding))

        # line and dot peroperty
        self.lineHeight = kwargs.get('lineHeight', 6)
        self.lineWidth = kwargs.get('lineWidth', 0.05)

        # colors
        self.bgColor = kwargs.get('bgColor', 'none')
        self.lineColor = kwargs.get('lineColor', '#999')

        # pages
        self.pages = kwargs.get('pages', [])

        # info on page
        self.guide = kwargs.get('guide', False)

    def addEmptyPage(self):
        page = Page(**self.__dict__)
        self.pages.append(page)

    def addLinePage(self):
        page = LinePage(**self.__dict__)
        self.pages.append(page)

    def addDotPage(self):
        page = DotPage(**self.__dict__)
        self.pages.append(page)

    def addChecklistPage(self, **kwargs):
        page = ChecklistPage(**self.__dict__, **kwargs)
        self.pages.append(page)

    def addOneYearPage(self, year, title='', **kwargs):
        page = OneYearPage(year, title, **self.__dict__, **kwargs)
        self.pages.append(page)

    def toHTML(self, Dir=''):
        if not os.path.exists(os.path.join(Dir, self.name)):
            os.mkdir(os.path.join(Dir, self.name))

        if not os.path.exists(os.path.join(Dir, self.name, 'pages')):
            os.mkdir(os.path.join(Dir, self.name, 'pages'))

        _direction = "rtl" if self.rtl else "ltr"
        htmlTxt = f'<html>\n<head>\n<style>\nhtml,body{{margin:0;padding:0;direction:{_direction};}}\n</style>\n</head>\n<body>\n'
        for i in range(len(self.pages)):
            if i % 2 == 0 ^ self.rtl:
                pageDir = 'right'
            else:
                pageDir = 'left'
            print(
                f'#{i+1:>3}: {str(self.pages[i].__class__)[8:-2].split(".")[-1]}({pageDir[:1]})')

            svg = self.pages[i].page[pageDir]
            svg.name = f'p{i:03}'
            svg.save(
                "/".join([Dir, self.name, 'pages']),
                width=f'{self.pages[i].svgWidth}mm',
                height=f'{self.pages[i].svgHeight}mm'
            )
            path = "/".join(['pages', f"{svg.name}.svg"])

            htmlTxt += f'<img src="{path}" >\n'

        htmlTxt += '</body>\n</html>'

        with open(os.path.join(Dir, self.name, 'index.html'), "w") as f:
            f.write(htmlTxt)

    def toPrintHTML(self, Dir='', loopPaper=5):
        if not os.path.exists(os.path.join(Dir, self.name)):
            os.mkdir(os.path.join(Dir, self.name))

        if not os.path.exists(os.path.join(Dir, self.name, 'pages')):
            os.mkdir(os.path.join(Dir, self.name, 'pages'))

        _direction = "rtl" if self.rtl else "ltr"
        htmlTxt = f'<html>\n<head>\n<style>\nhtml,body{{margin:0;padding:0;direction:{_direction};}}\n</style>\n</head>\n<body>\n'

        for i in range(len(self.pages)):
            if i % 2 == 0 ^ self.rtl:
                pageDir = 'right'
            else:
                pageDir = 'left'
            print(
                f'#{i+1:>3}: {str(self.pages[i].__class__)[8:-2].split(".")[-1]}({pageDir[:1]})')

            svg = self.pages[i].page[pageDir]
            svg.name = f'p{i:03}'
            svg.save(
                "/".join([Dir, self.name, 'pages']),
                width=f'{self.pages[i].svgWidth}mm',
                height=f'{self.pages[i].svgHeight}mm'
            )

        for d in range(0, len(self.pages)-1, loopPaper*4):
            for i in range(0, loopPaper*2, 2):
                for p in [d+loopPaper*4-i-1, d+i, d+i+1, d+loopPaper*4-i-2]:
                    name = f'p{p:03}'
                    path = "/".join(['pages', f"{name}.svg"])
                    htmlTxt += f'<img src="{path}" >\n'

        htmlTxt += '</body>\n</html>'

        with open(os.path.join(Dir, self.name, 'index.html'), "w") as f:
            f.write(htmlTxt)

    def toPDF(self, Dir='', removeSvgs=True, removePdfs=True):
        try:
            if not os.path.exists(os.path.join(Dir, self.name)):
                os.mkdir(os.path.join(Dir, self.name))

            if not os.path.exists(os.path.join(Dir, self.name, 'pages')):
                os.mkdir(os.path.join(Dir, self.name, 'pages'))

            for i in range(len(self.pages)):
                if i % 2 == 0 ^ self.rtl:
                    pageDir = 'right'
                else:
                    pageDir = 'left'
                print(
                    f'#{i+1:>3}: {str(self.pages[i].__class__)[8:-2].split(".")[-1]}({pageDir[:1]})')

                svg = self.pages[i].page[pageDir]
                svg.name = f'p{i:03}'
                path_ = os.path.join(Dir, self.name, 'pages')
                svg.save(
                    path_,
                    width=f'{self.pages[i].svgWidth}mm',
                    height=f'{self.pages[i].svgHeight}mm'
                )

                fpath = os.path.join(path_, svg.name)
                os.system(
                    f'inkscape "{fpath}.svg" --export-filename="{fpath}.pdf"')
                if removeSvgs:
                    os.system(f'rm "{fpath}.svg"')

            path = os.path.join(Dir, self.name, 'pages')
            path2 = os.path.join(Dir, self.name)
            os.chdir(f"{path}")

            os.system(f'pdfunite *.pdf ../cal.pdf')

            if removePdfs:
                os.chdir(f"{path2}")
                os.system(f'rm -r pages')

            os.chdir(os.path.dirname(os.path.realpath(__file__)))
        except:
            print('"inkscape" and "pdfunite" requirement for use toPDF function.')

    def toPrintPDF(self, Dir='', loopPaper=5, removeSvgs=True, removePdfs=True):
        self.toPDF(Dir, removeSvgs=removeSvgs, removePdfs=False)

        if loopPaper > 0:
            names = []
            for d in range(0, len(self.pages)-1, loopPaper*4):
                for i in range(0, loopPaper*2, 2):
                    for p in [d+loopPaper*4-i-1, d+i, d+i+1, d+loopPaper*4-i-2]:
                        names.append(f'p{p:03}.pdf')

            path = os.path.join(Dir, self.name, 'pages')
            os.chdir(f"{path}")
            name = " ".join(names)
            os.system(f'pdfunite {name} ../cal-print.pdf')
            os.chdir(os.path.dirname(os.path.realpath(__file__)))

        if removePdfs:
            path2 = os.path.join(Dir, self.name)
            os.chdir(f"{path2}")
            os.system(f'rm -r pages')
            os.chdir(os.path.dirname(os.path.realpath(__file__)))

            print('pdfs removed')
