from cal import Calendar
import os

rootPath = os.getcwd()

printProperty = {
    'margin': [19, 14, 19, 14],
    'trimMark': 5,
    'trimMarkMargin': 7,
}
previewProperty = {
    'margin': [0, 0, 0, 0],
    'trimMark': 5,
    'trimMarkMargin': 7,
}

example = {
    'width': 160,
    'name': 'سالنامه ۱۴۰۴',
    'padding': [25, 0, 9, 0],
    'lineHeight': 5,
    'daysHeight': 5,
    'showWeekdays': False,
    'weekend': [6],
    'secondColor': '#f00',
}

newBook = Calendar('data.json',
                   startDate='1404-1-1',
                   **previewProperty,
                   **example
                   )

newBook.addFirstPage(years=['1404', '2025 - 2026', '1447 - 1448'],
                     turnOfYear=['پنجشنبه ۳۰ اسفند ۱۴۰۳', 'ساعت ۱۲:۳۱:۳۰'])

newBook.addLinePage()
newBook.addChecklistPage(title='اهداف سال ۱۴۰۴',
                         pattern='01', checkboxscale=0.7)

newBook.addOneYearPage(year=1404, title='سال ۱۴۰۴')
newBook.addHolidaysPage(year=1404, title='تعطیلات رسمی ۱۴۰۴')

for i in range(53):
    newBook.addLinePage()
    newBook.addWeekPage(i+1)

newBook.addLinePage()
newBook.toHTML(rootPath)