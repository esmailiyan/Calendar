﻿from pages import *
from notebook import Notebook
import json


class Calendar(Notebook):
    def __init__(self, dataJsonPath, **kwargs) -> None:
        super().__init__(**kwargs)
        # general
        self.name = kwargs.get('name', 'Untitle-Calendar')
        self.dataJsonPath = dataJsonPath
        self.readDataJson()

        # design
        self.layout = kwargs.get('layout', 'left')
        self.daysHeight = kwargs.get('daysHeight', 4)
        self.lineShiftDown = kwargs.get('lineShiftDown', 0)

        # Data show
        self.calendarOrder = kwargs.get('calendarOrder', ['sh', 'wc', 'ic'])
        self.showEvents = kwargs.get('showEvents', True)
        self.showWeekdays = kwargs.get('showWeekdays', False)
        self.showFullCalendar = kwargs.get('showFullCalendar', False)

        # font style
        self.fontHeightScl = kwargs.get('fontHeightScl', 0.67)
        self.fontFamily = kwargs.get('fontFamily', 'Anjoman')

        fontWeight = kwargs.get('fontWeight', {})
        defaultFontWeight = {
            'firstCal': 'Thin',
            'holiday': 'Thin',
            'firstCalWeekdays': 'ExtraLight',
            'firstCalWeekdaysHoliday': 'ExtraLight',
            'secondCal': 'Thin',
            'thirdCal': 'Thin',
            'monthAndWeek': 'Light',
            'Events': 'ExtraLight',
        }
        self.fontWeight = {}
        for k, v in defaultFontWeight.items():
            self.fontWeight[k] = fontWeight.get(k, v)

        fontSize = kwargs.get('fontSize', {})
        defaultFontSize = {
            'firstCal':  self.lineHeight * self.daysHeight * 2,
            'holiday':  self.lineHeight * self.daysHeight * 2,
            'firstCalWeekdays': 8,
            'firstCalWeekdaysHoliday': 8,
            'secondCal': 8,
            'thirdCal': 8,
            'monthAndWeek': 8,
            'Events': 5,
        }
        self.fontSize = {}
        for k, v in defaultFontSize.items():
            self.fontSize[k] = fontSize.get(k, v)

        # colors
        self.primaryColor = kwargs.get('primaryColor', '#000')
        self.secondColor = kwargs.get('secondColor', '#ddd')

    def readDataJson(self):
        try:
            with open(self.dataJsonPath) as f:
                self.dataJson = json.load(f)
        except:
            print('JSON file is not exist.')
            exit()

    def weekKeys(self, i):
        pass

    def addWeekPage(self, i):
        page = WeekPage(self.weekKeys(i), **self.__dict__)
        self.pages.append(page)
