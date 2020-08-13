import bizbuysell as bbsapp
import cross_site
import math
import mergertech as mtapp
import os
import sqlite3
import sunbelt as sbapp
import time
import tworld as twapp
try:
    import bs4 as bs
    import openpyxl
    import pandas as pd
    from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
    import requests
except ImportError:
    import install_requirements
    import bs4 as bs
    import openpyxl
    import pandas as pd
    from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
    from pandastable import Table
    import requests

states_list = ("Alabama", "Alaska", "Arizona", "Arkansas", "California", \
    "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", \
    "Idaho","Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", \
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", \
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", \
    "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", \
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", \
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", \
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", \
    "West Virginia", "Wisconsin", "Wyoming")

version_info = "Version 1.0.6 \nUpdated 8/12/20"

from sys import platform
def platform_format(font, mac_size, bold, weight):
    if sys.platform == "darwin":
        font.setPointSize(mac_size)
        font.setBold(bold)
        font.setWeight(weight)
    else:
        font.setPointSize(math.floor(mac_size * 0.7))
        font.setBold(bold)
        font.setWeight(math.floor(weight * 0.7))

class Ui_BrokeredDealEvaluator(object):
    def setupUi(self, BrokeredDealEvaluator):
        BrokeredDealEvaluator.setObjectName("BrokeredDealEvaluator")
        BrokeredDealEvaluator.resize(810, 610)
        BrokeredDealEvaluator.setAutoFillBackground(True)
        horizontal = QtWidgets.QSizePolicy.Expanding
        vertical = QtWidgets.QSizePolicy.Expanding
        sizePolicy = QtWidgets.QSizePolicy(horizontal, vertical)
        self.centralwidget = QtWidgets.QWidget(BrokeredDealEvaluator)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setSizePolicy(sizePolicy)

        # Page Layout
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(20, 10, 761, 511))
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setSizePolicy(sizePolicy)

        # Exit Button
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(340, 540, 121, 32))
        self.exitButton.setObjectName("exitButton")
        self.exitButton.setSizePolicy(sizePolicy)
        self.exitButton.clicked.connect(QtWidgets.QApplication.instance().quit)
        

        # Home Page
        self.home = QtWidgets.QWidget()
        self.home.setObjectName("home")
        self.backgroundImage = QtWidgets.QLabel(self.home)
        self.backgroundImage.setGeometry(QtCore.QRect(20, 10, 771, 511))
        self.backgroundImage.setScaledContents(True)
        self.backgroundImage.setObjectName("backgroundImage")
        self.line = QtWidgets.QFrame(self.home)
        self.line.setGeometry(QtCore.QRect(260, 225, 261, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.label_7 = QtWidgets.QLabel(self.home)
        self.label_7.setGeometry(QtCore.QRect(260, 30, 251, 20))
        font = QtGui.QFont()
        platform_format(font, 14, True, 75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        self.daysSinceLastSearch = QtWidgets.QLCDNumber(self.home)
        self.daysSinceLastSearch.setGeometry(QtCore.QRect(430, 60, 51, 41))
        self.daysSinceLastSearch.setFont(font)
        self.daysSinceLastSearch.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.daysSinceLastSearch.setObjectName("daysSinceLastSearch")
        self.daysSinceLastSearch.setStyleSheet("""QLCDNumber {
            background-color: #B6A19E;
            color: #E6E6FA;
        }""")
        
        path = os.path.dirname(sys.modules[__name__].__file__)
        connection = sqlite3.connect("appbin/past_scrapes.db")
        c = connection.cursor()
        cols = ("Listing Title", "Tagline", "Cash Flow", "Description", \
            "Score", "URL", "Source")
        c.execute("""CREATE TABLE IF NOT EXISTS
            scrape_history(
            listing_title text,
            tagline text,
            cash_flow text,
            description text,
            score integer,
            url text,
            source text,
            scrape_date date)""")
        c.execute("""SELECT CAST(
            JULIANDAY('now') - JULIANDAY(MAX(scrape_date))
            AS INTEGER) FROM scrape_history""")
        exists = c.fetchone()
        if exists[0]:
            self.daysSinceLastSearch.display(int(exists[0]))
        connection.commit()
        connection.close()

        self.label_8 = QtWidgets.QLabel(self.home)
        self.label_8.setGeometry(QtCore.QRect(280, 60, 91, 21))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.home)
        self.label_9.setGeometry(QtCore.QRect(280, 80, 111, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.home)
        self.label_10.setGeometry(QtCore.QRect(290, 260, 201, 20))
        
        font = QtGui.QFont()
        platform_format(font, 14, True, 75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.minScoreSpinBox = QtWidgets.QSpinBox(self.home)
        self.minScoreSpinBox.setGeometry(QtCore.QRect(350, 150, 65, 24))
        self.minScoreSpinBox.setMinimum(-10)
        self.minScoreSpinBox.setProperty("value", 2)
        self.minScoreSpinBox.setObjectName("minScoreSpinBox")
        self.label_11 = QtWidgets.QLabel(self.home)
        self.label_11.setGeometry(QtCore.QRect(250, 120, 281, 16))
        self.label_11.setObjectName("label_11")
        
        self.scrapeAllSubmit = QtWidgets.QPushButton(self.home)
        self.scrapeAllSubmit.setGeometry(QtCore.QRect(330, 180, 101, 32))
        self.scrapeAllSubmit.setObjectName("scrapeAllSubmit")
        self.scrapeAllSubmit.clicked.connect(lambda: self.scour_all())
        
        self.newOrAll = QtWidgets.QComboBox(self.home)
        self.newOrAll.setGeometry(QtCore.QRect(295, 120, 65, 20))
        self.newOrAll.setObjectName("newOrAll")
        self.newOrAll.addItem("")
        self.newOrAll.addItem("")

        self.whichsite = QtWidgets.QLabel(self.home)
        self.whichsite.setGeometry(QtCore.QRect(270, 290, 241, 21))
        self.whichsite.setObjectName("whichsite")
        self.bbsOption_2 = QtWidgets.QRadioButton(self.home)
        self.bbsOption_2.setGeometry(QtCore.QRect(300, 320, 191, 20))
        self.bbsOption_2.setObjectName("bbsOption_2")
        self.mtOption_2 = QtWidgets.QRadioButton(self.home)
        self.mtOption_2.setGeometry(QtCore.QRect(300, 340, 221, 20))
        self.mtOption_2.setObjectName("mtOption_2")
        self.sbOption_2 = QtWidgets.QRadioButton(self.home)
        self.sbOption_2.setGeometry(QtCore.QRect(300, 360, 191, 20))
        self.sbOption_2.setObjectName("sbOption_2")
        self.twOption_2 = QtWidgets.QRadioButton(self.home)
        self.twOption_2.setGeometry(QtCore.QRect(300, 380, 191, 20))
        self.twOption_2.setObjectName("twOption_2")
                
        self.bySiteSubmit = QtWidgets.QPushButton(self.home)
        self.bySiteSubmit.setGeometry(QtCore.QRect(330, 410, 101, 32))
        self.bySiteSubmit.setObjectName("bySiteSubmit")
        self.bySiteSubmit.clicked.connect(lambda: self.scour_by_site())
        self.stackedWidget.addWidget(self.home)


        # Page 1: How it Works
        self.howItWorks = QtWidgets.QWidget()
        self.howItWorks.setObjectName("howItWorks")
        self.howDoesItWork = QtWidgets.QTextBrowser(self.howItWorks)
        self.howDoesItWork.setGeometry(QtCore.QRect(90, 20, 601, 441))
        self.howDoesItWork.setObjectName("howDoesItWork")
        self.returnToStart_1 = QtWidgets.QPushButton(self.howItWorks)
        self.returnToStart_1.setGeometry(QtCore.QRect(320, 471, 121, 32))
        self.returnToStart_1.setObjectName("returnToStart_1")
        self.returnToStart_1.clicked.connect(lambda: self.return_to_start())
        self.returnToStart_1.raise_()
        self.howDoesItWork.raise_()
        self.stackedWidget.addWidget(self.howItWorks)


        # Page 2: Licenses
        self.licenses = QtWidgets.QWidget()
        self.licenses.setObjectName("licenses")
        self.banner = QtWidgets.QLabel(self.licenses)
        self.banner.setGeometry(QtCore.QRect(10, 20, 311, 431))
        self.banner.setStyleSheet("background-image: url(:/appResources/sidebar.png)")
        self.banner.setText("")
        self.banner.setPixmap(QtGui.QPixmap(":/appResources/sidebar.png"))
        self.banner.setScaledContents(True)
        self.banner.setObjectName("banner")
        self.licenseScript = QtWidgets.QTextBrowser(self.licenses)
        self.licenseScript.setGeometry(QtCore.QRect(340, 20, 401, 431))
        self.licenseScript.setObjectName("licenseScript")
        self.returnToStart_2 = QtWidgets.QPushButton(self.licenses)
        self.returnToStart_2.setGeometry(QtCore.QRect(320, 470, 121, 32))
        self.returnToStart_2.setObjectName("returnToStart_2")
        self.returnToStart_2.clicked.connect(lambda: self.return_to_start())
        self.stackedWidget.addWidget(self.licenses)


        # Page 3: Previous Scrapes
        self.prevScrapes = QtWidgets.QWidget()
        self.prevScrapes.setObjectName("prevScrapes")
        self.prevScrapesHeader = QtWidgets.QLabel(self.prevScrapes)
        self.prevScrapesHeader.setGeometry(QtCore.QRect(310, 20, 151, 20))
        
        font = QtGui.QFont()
        platform_format(font, 18, True, 75)
        self.prevScrapesHeader.setFont(font)
        self.prevScrapesHeader.setObjectName("prevScrapesHeader")
        self.prevScrapesTable = QtWidgets.QTableWidget(self.prevScrapes)
        self.prevScrapesTable.setGeometry(QtCore.QRect(30, 70, 721, 231))
        self.prevScrapesTable.setObjectName("prevScrapesTable")
        self.prevScrapesTable.setColumnCount(8)
        self.prevScrapesTable.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.prevScrapesTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.prevScrapesTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.prevScrapesTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.prevScrapesTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.prevScrapesTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.prevScrapesTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.prevScrapesTable.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.prevScrapesTable.setHorizontalHeaderItem(7, item)

        path = os.path.dirname(sys.modules[__name__].__file__)
        conn = sqlite3.connect("appbin/past_scrapes.db")
        past_df = pd.read_sql_query("SELECT * FROM scrape_history", conn)
        past_df = past_df.sort_values(by=["score"], ascending=False)
        conn.commit()
        conn.close()
        
        for i in range(past_df.shape[0]):
            rowPosition = self.prevScrapesTable.rowCount()
            self.prevScrapesTable.insertRow(rowPosition)
            for j in range(past_df.shape[1]):
                self.prevScrapesTable.setItem(rowPosition, j, \
                QtWidgets.QTableWidgetItem(str(past_df.iloc[i, j])))

        self.mostRecentLabel = QtWidgets.QLabel(self.prevScrapes)
        self.mostRecentLabel.setGeometry(QtCore.QRect(240, 50, 191, 16))
        self.mostRecentLabel.setObjectName("mostRecentLabel")
        self.lastScrapeDate = QtWidgets.QLabel(self.prevScrapes)
        self.lastScrapeDate.setGeometry(QtCore.QRect(440, 50, 90, 16))
        
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lastScrapeDate.setFont(font)
        self.lastScrapeDate.setObjectName("lastScrapeDate")
        self.line_2 = QtWidgets.QFrame(self.prevScrapes)
        self.line_2.setGeometry(QtCore.QRect(230, 310, 295, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        
        self.totalResults = QtWidgets.QLabel(self.prevScrapes)
        self.totalResults.setGeometry(QtCore.QRect(580, 300, 81, 20))
        self.totalResults.setObjectName("totalResults")
        self.totalResultsPS = QtWidgets.QLabel(self.prevScrapes)
        self.totalResultsPS.setGeometry(QtCore.QRect(670, 300, 60, 20))
        self.totalResultsPS.setObjectName("totalResultsPS")
        self.totalResultsPS.setText(str(len(past_df)))

        self.viewBySite = QtWidgets.QLabel(self.prevScrapes)
        self.viewBySite.setGeometry(QtCore.QRect(240, 321, 281, 20))
        font = QtGui.QFont()
        platform_format(font, 14, True, 75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.viewBySite.setFont(font)
        self.viewBySite.setObjectName("viewBySite")
        
        self.allOption = QtWidgets.QRadioButton(self.prevScrapes)
        self.allOption.setGeometry(QtCore.QRect(300, 346, 191, 20))
        self.allOption.setObjectName("allOption")
        self.bbsOption = QtWidgets.QRadioButton(self.prevScrapes)
        self.bbsOption.setGeometry(QtCore.QRect(300, 363, 191, 20))
        self.bbsOption.setObjectName("bbsOption")
        self.mtOption = QtWidgets.QRadioButton(self.prevScrapes)
        self.mtOption.setGeometry(QtCore.QRect(300, 380, 221, 20))
        self.mtOption.setObjectName("mtOption")
        self.sbOption = QtWidgets.QRadioButton(self.prevScrapes)
        self.sbOption.setGeometry(QtCore.QRect(300, 397, 191, 20))
        self.sbOption.setObjectName("sbOption")
        self.twOption = QtWidgets.QRadioButton(self.prevScrapes)
        self.twOption.setGeometry(QtCore.QRect(300, 414, 191, 20))
        self.twOption.setObjectName("twOption")
        self.viewBySiteButton = QtWidgets.QPushButton(self.prevScrapes)
        self.viewBySiteButton.setGeometry(QtCore.QRect(350, 430, 61, 32))
        self.viewBySiteButton.setObjectName("viewBySiteButton")
        self.viewBySiteButton.clicked.connect(lambda: \
            self.filter_prev_scrapes())

        self.line_3 = QtWidgets.QFrame(self.prevScrapes)
        self.line_3.setGeometry(QtCore.QRect(250, 455, 261, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")

        self.returnToStart_3 = QtWidgets.QPushButton(self.prevScrapes)
        self.returnToStart_3.setGeometry(QtCore.QRect(320, 470, 121, 32))
        self.returnToStart_3.setObjectName("returnToStart_3")
        self.returnToStart_3.clicked.connect(lambda: self.return_to_start())
        self.stackedWidget.addWidget(self.prevScrapes)


        # Page 4: Starred Results
        self.starredResults = QtWidgets.QWidget()
        self.starredResults.setObjectName("starredResults")
        self.starredResultsHeader = QtWidgets.QLabel(self.starredResults)
        self.starredResultsHeader.setGeometry(QtCore.QRect(310, 20, 141, 20))

        font = QtGui.QFont()
        platform_format(font, 18, True, 75)
        self.starredResultsHeader.setFont(font)
        self.starredResultsHeader.setObjectName("starredResultsHeader")
        self.totalResults_2 = QtWidgets.QLabel(self.starredResults)
        self.totalResults_2.setGeometry(QtCore.QRect(560, 450, 81, 20))
        self.totalResults_2.setObjectName("totalResults_2")
        self.totalResultsSR = QtWidgets.QLabel(self.starredResults)
        self.totalResultsSR.setGeometry(QtCore.QRect(660, 450, 60, 20))
        self.totalResultsSR.setObjectName("totalResultsSR")

        self.starredResultsTable = QtWidgets.QTableWidget(self.starredResults)
        self.starredResultsTable.setGeometry(QtCore.QRect(20, 80, 721, 371))
        self.starredResultsTable.setObjectName("starredResultsTable")
        self.starredResultsTable.setColumnCount(8)
        self.starredResultsTable.setRowCount(0)
        
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.starredResultsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.starredResultsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.starredResultsTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.starredResultsTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.starredResultsTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.starredResultsTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.starredResultsTable.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.starredResultsTable.setHorizontalHeaderItem(7, item)
        
        path = os.path.dirname(sys.modules[__name__].__file__)
        conn = sqlite3.connect("appbin/past_scrapes.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS
            scrape_history(
            listing_title text,
            tagline text,
            cash_flow text,
            description text,
            score integer,
            url text,
            source text,
            scrape_date date)""")
        conn.commit()
        conn.close()
        
        self.withSelectedResults = QtWidgets.QLabel(self.starredResults)
        self.withSelectedResults.setGeometry(QtCore.QRect(100, 60, 141, 16))
        self.withSelectedResults.setObjectName("withSelectedResults")
        self.exportToXL = QtWidgets.QCommandLinkButton(self.starredResults)
        self.exportToXL.setGeometry(QtCore.QRect(250, 50, 141, 31))
        self.exportToXL.setObjectName("exportToXL")
        self.exportToXL.clicked.connect(lambda: \
            self.excelify_listings(self.starredResultsTable))
        self.removeFromSR = QtWidgets.QCommandLinkButton(self.starredResults)
        self.removeFromSR.setGeometry(QtCore.QRect(500, 50, 181, 31))
        self.removeFromSR.setObjectName("removeFromSR")
        self.removeFromSR.clicked.connect(lambda: self.remove_from_sr())
        self.followURL = QtWidgets.QCommandLinkButton(self.starredResults)
        self.followURL.setGeometry(QtCore.QRect(400, 50, 91, 31))
        self.followURL.setObjectName("followURL")
        self.followURL.clicked.connect(lambda: \
            self.browse_web(self.starredResultsTable))
        
        font = QtGui.QFont()
        platform_format(font, 9, False, 65)
        font.setItalic(True)
        self.selectInstructions_6 = QtWidgets.QLabel(self.starredResults)
        self.selectInstructions_6.setGeometry(QtCore.QRect(30, 452, 260, 16))
        self.selectInstructions_6.setObjectName("selectInstructions_6")
        self.selectInstructions_6.setFont(font)

        self.returnToStart_4 = QtWidgets.QPushButton(self.starredResults)
        self.returnToStart_4.setGeometry(QtCore.QRect(320, 470, 121, 32))
        self.returnToStart_4.setObjectName("returnToStart_4")
        self.returnToStart_4.clicked.connect(lambda: self.return_to_start())
        self.stackedWidget.addWidget(self.starredResults)


        # Page 5: Keywords
        self.keywordsPage = QtWidgets.QWidget()
        self.keywordsPage.setObjectName("keywordsPage")
        self.keywordsHeader = QtWidgets.QLabel(self.keywordsPage)
        self.keywordsHeader.setGeometry(QtCore.QRect(230, 20, 301, 20))
        
        font = QtGui.QFont()
        platform_format(font, 17, True, 75)
        self.keywordsHeader.setFont(font)
        self.keywordsHeader.setObjectName("keywordsHeader")

        self.label_41 = QtWidgets.QLabel(self.keywordsPage)
        self.label_41.setGeometry(QtCore.QRect(130, 50, 541, 20))
        self.label_41.setObjectName("label_41")
        self.label_42 = QtWidgets.QLabel(self.keywordsPage)
        self.label_42.setGeometry(QtCore.QRect(129, 70, 561, 20))
        self.label_42.setObjectName("label_42")
        self.label_43 = QtWidgets.QLabel(self.keywordsPage)
        self.label_43.setGeometry(QtCore.QRect(130, 90, 541, 20))
        self.label_43.setObjectName("label_43")
        self.label_44 = QtWidgets.QLabel(self.keywordsPage)
        self.label_44.setGeometry(QtCore.QRect(130, 110, 521, 20))
        self.label_44.setObjectName("label_44")
        self.label_45 = QtWidgets.QLabel(self.keywordsPage)
        self.label_45.setGeometry(QtCore.QRect(130, 130, 511, 20))
        self.label_45.setObjectName("label_45")
        self.label_46 = QtWidgets.QLabel(self.keywordsPage)
        self.label_46.setGeometry(QtCore.QRect(130, 150, 531, 20))
        self.label_46.setObjectName("label_46")
        self.label_47 = QtWidgets.QLabel(self.keywordsPage)
        self.label_47.setGeometry(QtCore.QRect(130, 170, 521, 20))
        self.label_47.setObjectName("label_47")
        self.label_49 = QtWidgets.QLabel(self.keywordsPage)
        self.label_49.setGeometry(QtCore.QRect(200, 200, 381, 16))
        self.label_49.setObjectName("label_49")
        
        self.positiveHeader = QtWidgets.QLabel(self.keywordsPage)
        self.positiveHeader.setGeometry(QtCore.QRect(210, 240, 60, 21))
        font = QtGui.QFont()
        platform_format(font, 15, True, 75)
        self.positiveHeader.setFont(font)
        self.positiveHeader.setObjectName("positiveHeader")
        self.negativeHeader = QtWidgets.QLabel(self.keywordsPage)
        self.negativeHeader.setGeometry(QtCore.QRect(480, 240, 71, 21))
        font = QtGui.QFont()
        platform_format(font, 15, True, 75)
        self.negativeHeader.setFont(font)
        self.negativeHeader.setObjectName("negativeHeader")
        self.positiveWords = QtWidgets.QTextBrowser(self.keywordsPage)
        self.positiveWords.setGeometry(QtCore.QRect(130, 270, 220, 191))
        self.positiveWords.setObjectName("positiveWords")
        self.negativeWords = QtWidgets.QTextBrowser(self.keywordsPage)
        self.negativeWords.setGeometry(QtCore.QRect(410, 270, 220, 191))
        self.negativeWords.setObjectName("negativeWords")

        self.label_84 = QtWidgets.QLabel(self.keywordsPage)
        self.label_84.setGeometry(QtCore.QRect(408, 200, 171, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_84.setFont(font)
        self.label_84.setObjectName("label_84")

        self.returnToStart_5 = QtWidgets.QPushButton(self.keywordsPage)
        self.returnToStart_5.setGeometry(QtCore.QRect(320, 470, 121, 32))
        self.returnToStart_5.setObjectName("returnToStart_5")
        self.returnToStart_5.clicked.connect(lambda: self.return_to_start())
        self.stackedWidget.addWidget(self.keywordsPage)


        # Page 6: Edit Keywords
        self.edited_pos_keywords = None
        self.edited_neg_keywords = None
        self.editKeywords = QtWidgets.QWidget()
        self.editKeywords.setObjectName("editKeywords")
        self.editKeywordsHeader = QtWidgets.QLabel(self.editKeywords)
        self.editKeywordsHeader.setGeometry(QtCore.QRect(220, 20, 341, 20))
        
        font = QtGui.QFont()
        platform_format(font, 17, True, 75)
        self.editKeywordsHeader.setFont(font)
        self.editKeywordsHeader.setObjectName("editKeywordsHeader")
        
        self.label_52 = QtWidgets.QLabel(self.editKeywords)
        self.label_52.setGeometry(QtCore.QRect(160, 50, 461, 20))
        self.label_52.setObjectName("label_52")
        self.label_53 = QtWidgets.QLabel(self.editKeywords)
        self.label_53.setGeometry(QtCore.QRect(160, 70, 421, 20))
        self.label_53.setObjectName("label_53")
        self.label_54 = QtWidgets.QLabel(self.editKeywords)
        self.label_54.setGeometry(QtCore.QRect(159, 90, 471, 20))
        self.label_54.setObjectName("label_54")
        self.label_55 = QtWidgets.QLabel(self.editKeywords)
        self.label_55.setGeometry(QtCore.QRect(159, 110, 461, 20))
        self.label_55.setObjectName("label_55")
        self.label_56 = QtWidgets.QLabel(self.editKeywords)
        self.label_56.setGeometry(QtCore.QRect(569, 59, 21, 41))
        
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_56.setFont(font)
        self.label_56.setObjectName("label_56")
        self.label_57 = QtWidgets.QLabel(self.editKeywords)
        self.label_57.setGeometry(QtCore.QRect(160, 130, 471, 20))
        self.label_57.setObjectName("label_57")
        self.label_58 = QtWidgets.QLabel(self.editKeywords)
        self.label_58.setGeometry(QtCore.QRect(180, 150, 401, 20))
        self.label_58.setText("")
        self.label_58.setObjectName("label_58")
        
        
        font = QtGui.QFont()
        platform_format(font, 13, True, 75)
        self.label_61 = QtWidgets.QLabel(self.editKeywords)
        self.label_61.setGeometry(QtCore.QRect(160, 160, 171, 20))
        self.label_61.setFont(font)
        self.label_61.setObjectName("label_61")
        self.negativeHeader_2 = QtWidgets.QLabel(self.editKeywords)
        self.negativeHeader_2.setGeometry(QtCore.QRect(480, 210, 71, 21))
        font = QtGui.QFont()
        platform_format(font, 15, True, 75)
        self.negativeHeader_2.setFont(font)
        self.negativeHeader_2.setObjectName("negativeHeader_2")
        self.positiveHeader_2 = QtWidgets.QLabel(self.editKeywords)
        self.positiveHeader_2.setGeometry(QtCore.QRect(230, 210, 60, 21))
        font = QtGui.QFont()
        platform_format(font, 15, True, 75)
        self.positiveHeader_2.setFont(font)
        self.positiveHeader_2.setObjectName("positiveHeader_2")
        self.label_62 = QtWidgets.QLabel(self.editKeywords)
        self.label_62.setGeometry(QtCore.QRect(160, 180, 211, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_62.setFont(font)
        self.label_62.setObjectName("label_62")
        self.label_63 = QtWidgets.QLabel(self.editKeywords)
        self.label_63.setGeometry(QtCore.QRect(410, 160, 221, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_63.setFont(font)
        self.label_63.setObjectName("label_63")
        self.label_64 = QtWidgets.QLabel(self.editKeywords)
        self.label_64.setGeometry(QtCore.QRect(410, 180, 221, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_64.setFont(font)
        self.label_64.setObjectName("label_64")

        self.editPosWords = QtWidgets.QPlainTextEdit(self.editKeywords)
        self.editPosWords.setGeometry(QtCore.QRect(160, 240, 200, 150))
        self.editPosWords.setObjectName("editPosWords")
        self.editNegWords = QtWidgets.QPlainTextEdit(self.editKeywords)
        self.editNegWords.setGeometry(QtCore.QRect(410, 240, 200, 150))
        self.editNegWords.setObjectName("editNegWords")
        self.editKeywordsSubmit = QtWidgets.QPushButton(self.editKeywords)
        self.editKeywordsSubmit.setGeometry(QtCore.QRect(320, 400, 121, 32))
        self.editKeywordsSubmit.setObjectName("editKeywordsSubmit")
        self.editKeywordsSubmit.clicked.connect(lambda: self.update_keywords())
        self.line_4 = QtWidgets.QFrame(self.editKeywords)
        self.line_4.setGeometry(QtCore.QRect(257, 440, 251, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")

        self.returnToStart_6 = QtWidgets.QPushButton(self.editKeywords)
        self.returnToStart_6.setGeometry(QtCore.QRect(320, 470, 121, 32))
        self.returnToStart_6.setObjectName("returnToStart_6")
        self.returnToStart_6.clicked.connect(lambda: self.return_to_start())
        self.stackedWidget.addWidget(self.editKeywords)


        # Page 7: Cross-site Scrape Parameters
        self.cross_site_settings = ["bbs", "mt", "sb", "tw"]
        self.crossSiteScrapeParams = QtWidgets.QWidget()
        self.crossSiteScrapeParams.setObjectName("crossSiteScrapeParams")
        self.crossSiteSubheading = QtWidgets.QLabel(self.crossSiteScrapeParams)
        self.crossSiteSubheading.setGeometry(QtCore.QRect(298, 50, 171, 16))
        
        font = QtGui.QFont()
        platform_format(font, 15, True, 75)
        self.crossSiteSubheading.setFont(font)
        self.crossSiteSubheading.setObjectName("crossSiteSubheading")
        self.line_7 = QtWidgets.QFrame(self.crossSiteScrapeParams)
        self.line_7.setGeometry(QtCore.QRect(290, 440, 181, 20))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")

        self.parameter_header_3 = QtWidgets.QLabel(self.crossSiteScrapeParams)
        self.parameter_header_3.setGeometry(QtCore.QRect(270, 20, 221, 21))
        font = QtGui.QFont()
        platform_format(font, 16, True, 75)
        self.parameter_header_3.setFont(font)
        self.parameter_header_3.setObjectName("parameter_header_3")
        
        self.updateSettings = QtWidgets.QPushButton(self.crossSiteScrapeParams)
        self.updateSettings.setGeometry(QtCore.QRect(310, 360, 141, 32))
        self.updateSettings.setObjectName("updateSettings")
        self.updateSettings.clicked.connect(lambda: self.update_crosssite())
        
        self.label_78 = QtWidgets.QLabel(self.crossSiteScrapeParams)
        self.label_78.setGeometry(QtCore.QRect(330, 100, 101, 16))
        self.label_78.setObjectName("label_78")

        self.bbsCheckBox = QtWidgets.QCheckBox(self.crossSiteScrapeParams)
        self.bbsCheckBox.setGeometry(QtCore.QRect(300, 130, 151, 20))
        self.bbsCheckBox.setChecked(True)
        self.bbsCheckBox.setTristate(False)
        self.bbsCheckBox.setObjectName("bbsCheckBox")
        
        self.mtCheckBox = QtWidgets.QCheckBox(self.crossSiteScrapeParams)
        self.mtCheckBox.setGeometry(QtCore.QRect(300, 150, 171, 20))
        self.mtCheckBox.setChecked(True)
        self.mtCheckBox.setObjectName("mtCheckBox")

        self.sbCheckBox = QtWidgets.QCheckBox(self.crossSiteScrapeParams)
        self.sbCheckBox.setGeometry(QtCore.QRect(300, 170, 171, 20))
        self.sbCheckBox.setChecked(True)
        self.sbCheckBox.setObjectName("sbCheckBox")

        self.twCheckBox = QtWidgets.QCheckBox(self.crossSiteScrapeParams)
        self.twCheckBox.setGeometry(QtCore.QRect(300, 190, 171, 20))
        self.twCheckBox.setChecked(True)
        self.twCheckBox.setObjectName("twCheckBox")
        
        self.label_80 = QtWidgets.QLabel(self.crossSiteScrapeParams)
        self.label_80.setGeometry(QtCore.QRect(200, 400, 381, 20))
        self.label_80.setObjectName("label_80")
        self.label_81 = QtWidgets.QLabel(self.crossSiteScrapeParams)
        self.label_81.setGeometry(QtCore.QRect(200, 420, 381, 16))
        self.label_81.setObjectName("label_81")

        self.returnToStart_9 = QtWidgets.QPushButton(self.crossSiteScrapeParams)
        self.returnToStart_9.setGeometry(QtCore.QRect(320, 470, 121, 32))
        self.returnToStart_9.setObjectName("returnToStart_9")
        self.returnToStart_9.clicked.connect(lambda: self.return_to_start())
        self.stackedWidget.addWidget(self.crossSiteScrapeParams)
        

        # Page 8: Website Information
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.tabWidget = QtWidgets.QTabWidget(self.page)
        self.tabWidget.setGeometry(QtCore.QRect(20, 50, 751, 391))
        self.tabWidget.setObjectName("tabWidget")

        # Tab 1: BizBuySell
        self.BizBuySell = QtWidgets.QWidget()
        self.BizBuySell.setObjectName("BizBuySell")
        self.bbsVisitWebsite = QtWidgets.QCommandLinkButton(self.BizBuySell)
        self.bbsVisitWebsite.setGeometry(QtCore.QRect(60, 160, 131, 31))
        self.bbsVisitWebsite.setObjectName("bbsVisitWebsite")
        self.bbsVisitWebsite.clicked.connect(lambda: \
            self.visit_website("http://www.bizbuysell.com"))
        self.bbsLogo = QtWidgets.QLabel(self.BizBuySell)
        self.bbsLogo.setGeometry(QtCore.QRect(30, 40, 201, 61))
        self.bbsLogo.setStyleSheet("background-image: url(:/appResources/bbslogo.png)")
        self.bbsLogo.setText("")
        self.bbsLogo.setPixmap(QtGui.QPixmap(":/appResources/bbslogo.png"))
        self.bbsLogo.setScaledContents(True)
        self.bbsLogo.setObjectName("bbsLogo")
        self.bbsDesc = QtWidgets.QTextBrowser(self.BizBuySell)
        self.bbsDesc.setGeometry(QtCore.QRect(250, 40, 481, 301))
        self.bbsDesc.setObjectName("bbsDesc")
        self.tabWidget.addTab(self.BizBuySell, "")

        # Tab 2: MergerTech
        self.MergerTech = QtWidgets.QWidget()
        self.MergerTech.setObjectName("MergerTech")
        self.mtVisitWebsite = QtWidgets.QCommandLinkButton(self.MergerTech)
        self.mtVisitWebsite.setGeometry(QtCore.QRect(60, 160, 131, 31))
        self.mtVisitWebsite.setObjectName("mtVisitWebsite")
        self.mtVisitWebsite.clicked.connect(lambda: \
            self.visit_website("http://www.mergertech.com"))
        self.mtLogo = QtWidgets.QLabel(self.MergerTech)
        self.mtLogo.setGeometry(QtCore.QRect(30, 40, 201, 61))
        self.mtLogo.setStyleSheet("background-image: url(:/appResources/mtlogo.png)")
        self.mtLogo.setText("")
        self.mtLogo.setPixmap(QtGui.QPixmap(":/appResources/mtlogo.png"))
        self.mtLogo.setScaledContents(True)
        self.mtLogo.setObjectName("mtLogo")
        self.mtDesc = QtWidgets.QTextBrowser(self.MergerTech)
        self.mtDesc.setGeometry(QtCore.QRect(280, 40, 450, 260))
        self.mtDesc.setObjectName("mtDesc")
        self.tabWidget.addTab(self.MergerTech, "")

        # Tab 3: SunbeltNetwork
        self.Sunbelt = QtWidgets.QWidget()
        self.Sunbelt.setObjectName("Sunbelt")
        self.sblogo2 = QtWidgets.QLabel(self.Sunbelt)
        self.sblogo2.setGeometry(QtCore.QRect(30, 40, 201, 61))
        self.sblogo2.setStyleSheet("background-image: url(:/appResources/sunbeltlogo.png)")
        self.sblogo2.setText("")
        self.sblogo2.setPixmap(QtGui.QPixmap(":/appResources/sunbeltlogo.png"))
        self.sblogo2.setScaledContents(True)
        self.sblogo2.setObjectName("sblogo2")
        self.sbVisitWebsite = QtWidgets.QCommandLinkButton(self.Sunbelt)
        self.sbVisitWebsite.setGeometry(QtCore.QRect(60, 160, 131, 31))
        self.sbVisitWebsite.setObjectName("sbVisitWebsite")
        self.sbVisitWebsite.clicked.connect(lambda: \
            self.visit_website("http://www.sunbeltnetwork.com"))
        self.sbDesc = QtWidgets.QTextBrowser(self.Sunbelt)
        self.sbDesc.setGeometry(QtCore.QRect(280, 40, 450, 260))
        self.sbDesc.setObjectName("sbDesc")
        self.tabWidget.addTab(self.Sunbelt, "")

        # Tab 4: TWorld
        self.TWorld = QtWidgets.QWidget()
        self.TWorld.setObjectName("TWorld")
        self.twlogo2 = QtWidgets.QLabel(self.TWorld)
        self.twlogo2.setGeometry(QtCore.QRect(30, 40, 201, 61))
        self.twlogo2.setStyleSheet("background-image: url(:/appResources/twlogo.png)")
        self.twlogo2.setText("")
        self.twlogo2.setPixmap(QtGui.QPixmap(":/appResources/twlogo.png"))
        self.twlogo2.setScaledContents(True)
        self.twlogo2.setObjectName("twlogo2")
        self.twVisitWebsite = QtWidgets.QCommandLinkButton(self.TWorld)
        self.twVisitWebsite.setGeometry(QtCore.QRect(60, 160, 131, 31))
        self.twVisitWebsite.setObjectName("twVisitWebsite")
        self.twVisitWebsite.clicked.connect(lambda: \
            self.visit_website("http://www.tworld.com"))
        self.twDesc = QtWidgets.QTextBrowser(self.TWorld)
        self.twDesc.setGeometry(QtCore.QRect(280, 40, 450, 260))
        self.twDesc.setObjectName("sbDesc")
        self.tabWidget.addTab(self.TWorld, "")

        font = QtGui.QFont()
        platform_format(font, 16, True, 75)
        self.label_82 = QtWidgets.QLabel(self.page)
        self.label_82.setGeometry(QtCore.QRect(250, 0, 311, 20))
        self.label_82.setFont(font)
        self.label_82.setObjectName("label_82")

        self.returnToStart_10 = QtWidgets.QPushButton(self.page)
        self.returnToStart_10.setGeometry(QtCore.QRect(320, 470, 121, 32))
        self.returnToStart_10.setObjectName("returnToStart_10")
        self.returnToStart_10.clicked.connect(lambda: self.return_to_start())
        self.stackedWidget.addWidget(self.page)


        # Page 9: How to Use
        self.howToUse = QtWidgets.QWidget()
        self.howToUse.setObjectName("howToUse")
        self.howToUseHeader = QtWidgets.QLabel(self.howToUse)
        self.howToUseHeader.setGeometry(QtCore.QRect(280, 10, 201, 16))

        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.howToUseHeader.setFont(font)
        self.howToUseHeader.setObjectName("howToUseHeader")
        self.instructionsText = QtWidgets.QTextBrowser(self.howToUse)
        self.instructionsText.setGeometry(QtCore.QRect(80, 40, 611, 411))
        self.instructionsText.setObjectName("instructionsText")

        self.returnToStart_11 = QtWidgets.QPushButton(self.howToUse)
        self.returnToStart_11.setGeometry(QtCore.QRect(320, 470, 121, 32))
        self.returnToStart_11.setObjectName("returnToStart_11")
        self.returnToStart_11.clicked.connect(lambda: self.return_to_start())
        self.stackedWidget.addWidget(self.howToUse)


        # Page 10: Send Feedback
        self.sendFeedbackPage = QtWidgets.QWidget()
        self.sendFeedbackPage.setObjectName("sendFeedbackPage")
        self.sendFeedbackHeader = QtWidgets.QLabel(self.sendFeedbackPage)
        self.sendFeedbackHeader.setGeometry(QtCore.QRect(260, 20, 251, 20))
        
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.sendFeedbackHeader.setFont(font)
        self.sendFeedbackHeader.setObjectName("sendFeedbackHeader")

        self.label_86 = QtWidgets.QLabel(self.sendFeedbackPage)
        self.label_86.setGeometry(QtCore.QRect(220, 60, 341, 20))
        self.label_86.setObjectName("label_86")
        self.label_87 = QtWidgets.QLabel(self.sendFeedbackPage)
        self.label_87.setGeometry(QtCore.QRect(230, 80, 341, 20))
        self.label_87.setObjectName("label_87")
        self.label_88 = QtWidgets.QLabel(self.sendFeedbackPage)
        self.label_88.setGeometry(QtCore.QRect(230, 100, 341, 20))
        self.label_88.setObjectName("label_88")
        self.label_89 = QtWidgets.QLabel(self.sendFeedbackPage)
        self.label_89.setGeometry(QtCore.QRect(230, 120, 311, 20))
        self.label_89.setObjectName("label_89")

        self.yourEmail = QtWidgets.QLabel(self.sendFeedbackPage)
        self.yourEmail.setGeometry(QtCore.QRect(210, 170, 131, 16))
        self.yourEmail.setObjectName("yourEmail")
        self.inputEmail = QtWidgets.QLineEdit(self.sendFeedbackPage)
        self.inputEmail.setGeometry(QtCore.QRect(360, 170, 221, 21))
        self.inputEmail.setObjectName("inputEmail")
        self.yourTopic = QtWidgets.QLabel(self.sendFeedbackPage)
        self.yourTopic.setGeometry(QtCore.QRect(210, 200, 131, 16))
        self.yourTopic.setObjectName("yourTopic")
        self.inputTopic = QtWidgets.QLineEdit(self.sendFeedbackPage)
        self.inputTopic.setGeometry(QtCore.QRect(360, 200, 221, 21))
        self.inputTopic.setObjectName("inputTopic")
        self.yourMessage = QtWidgets.QLabel(self.sendFeedbackPage)
        self.yourMessage.setGeometry(QtCore.QRect(210, 230, 131, 16))
        self.yourMessage.setObjectName("yourMessage")
        self.inputMessage = QtWidgets.QPlainTextEdit(self.sendFeedbackPage)
        self.inputMessage.setGeometry(QtCore.QRect(360, 230, 221, 111))
        self.inputMessage.setObjectName("inputMessage")
        self.sendFeedback = QtWidgets.QPushButton(self.sendFeedbackPage)
        self.sendFeedback.setGeometry(QtCore.QRect(320, 360, 121, 32))
        self.sendFeedback.setObjectName("sendFeedback")
        self.sendFeedback.clicked.connect(lambda: self.send_feedback())

        self.line_8 = QtWidgets.QFrame(self.sendFeedbackPage)
        self.line_8.setGeometry(QtCore.QRect(320, 450, 118, 3))
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")

        self.returnToStart_12 = QtWidgets.QPushButton(self.sendFeedbackPage)
        self.returnToStart_12.setGeometry(QtCore.QRect(320, 470, 121, 32))
        self.returnToStart_12.setObjectName("returnToStart_12")
        self.returnToStart_12.clicked.connect(lambda: self.return_to_start())
        self.stackedWidget.addWidget(self.sendFeedbackPage)


        ###################### RESULTS PAGES ######################

        # Page 11: BBS Listings
        self.bbsListing = QtWidgets.QWidget()
        self.bbsListing.setObjectName("bbsListing")
        self.bbsListingsHeader = QtWidgets.QLabel(self.bbsListing)
        self.bbsListingsHeader.setGeometry(QtCore.QRect(290, 20, 181, 16))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        
        self.bbsListingsHeader.setFont(font)
        self.bbsListingsHeader.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.bbsListing)
        self.label_2.setGeometry(QtCore.QRect(275, 40, 211, 20))
        self.label_2.setObjectName("label_2")

        self.statesBox = QtWidgets.QComboBox(self.bbsListing)
        self.statesBox.setGeometry(QtCore.QRect(290, 60, 181, 21))
        self.statesBox.setEditable(True)
        setting = QtWidgets.QComboBox.AdjustToMinimumContentsLength
        self.statesBox.setSizeAdjustPolicy(setting)
        self.statesBox.setObjectName("statesBox")
        self.statesBox.addItem("")
        self.statesBox.setItemText(1, "")
        self.statesBox.setItemText(2, "")
        self.bbs_settings = None
        self.bbsSubmit = QtWidgets.QPushButton(self.bbsListing)
        self.bbsSubmit.setGeometry(QtCore.QRect(320, 90, 121, 32))
        self.bbsSubmit.setObjectName("bbsSubmit")
        self.bbsSubmit.clicked.connect(lambda: self.scour_bbs())

        self.bbsResultsTable = QtWidgets.QTableWidget(self.bbsListing)
        self.bbsResultsTable.setGeometry(QtCore.QRect(0, 150, 771, 321))
        self.bbsResultsTable.setColumnCount(6)
        self.bbsResultsTable.setObjectName("bbsResultsTable")
        self.bbsResultsTable.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.bbsResultsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.bbsResultsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.bbsResultsTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.bbsResultsTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.bbsResultsTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.bbsResultsTable.setHorizontalHeaderItem(5, item)

        bbsheader = self.bbsResultsTable.horizontalHeader()
        bbsheader.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(65)
        self.selectInstructions = QtWidgets.QLabel(self.bbsListing)
        self.selectInstructions.setGeometry(QtCore.QRect(25, 472, 270, 16))
        self.selectInstructions.setObjectName("selectInstructions")
        self.selectInstructions.setFont(font)

        self.numberOfResults = QtWidgets.QLabel(self.bbsListing)
        self.numberOfResults.setGeometry(QtCore.QRect(580, 470, 121, 16))
        self.numberOfResults.setObjectName("numberOfResults")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.bbsResultsCount = QtWidgets.QLabel(self.bbsListing)
        self.bbsResultsCount.setGeometry(QtCore.QRect(720, 470, 41, 16))
        self.bbsResultsCount.setObjectName("bbsResultsCount")
        self.bbsResultsCount.setFont(font)
        self.exportToXL_2 = QtWidgets.QCommandLinkButton(self.bbsListing)
        self.exportToXL_2.setGeometry(QtCore.QRect(240, 120, 141, 31))
        self.exportToXL_2.setWhatsThis("")
        self.exportToXL_2.setObjectName("exportToXL_2")
        self.exportToXL_2.clicked.connect(lambda: \
            self.excelify_listings(self.bbsResultsTable))
        self.label_35 = QtWidgets.QLabel(self.bbsListing)
        self.label_35.setGeometry(QtCore.QRect(90, 130, 141, 16))
        self.label_35.setObjectName("label_35")
        self.addToSR_2 = QtWidgets.QCommandLinkButton(self.bbsListing)
        self.addToSR_2.setGeometry(QtCore.QRect(490, 120, 181, 31))
        self.addToSR_2.setWhatsThis("")
        self.addToSR_2.setObjectName("addToSR_2")
        self.addToSR_2.clicked.connect(lambda: self.starify_bbs())
        self.followURL_2 = QtWidgets.QCommandLinkButton(self.bbsListing)
        self.followURL_2.setGeometry(QtCore.QRect(390, 120, 91, 31))
        self.followURL_2.setWhatsThis("")
        self.followURL_2.setObjectName("followURL_2")
        self.followURL_2.clicked.connect(lambda: \
            self.browse_web(self.bbsResultsTable))
        
        self.bbslogo_label = QtWidgets.QLabel(self.bbsListing)
        self.bbslogo_label.setGeometry(QtCore.QRect(30, 30, 171, 51))
        self.bbslogo_label.setStyleSheet("""\
            background-image: url(:/appResources/bbslogo.png)""")
        self.bbslogo_label.setText("")
        self.bbslogo_label.setPixmap(QtGui.QPixmap(":/appResources/bbslogo.png"))
        self.bbslogo_label.setScaledContents(True)
        self.bbslogo_label.setObjectName("bbslogo_label")

        self.returnToStart_13 = QtWidgets.QPushButton(self.bbsListing)
        self.returnToStart_13.setGeometry(QtCore.QRect(320, 470, 121, 32))
        self.returnToStart_13.setObjectName("returnToStart_13")
        self.returnToStart_13.clicked.connect(lambda: self.return_to_start())
        self.stackedWidget.addWidget(self.bbsListing)


        # Page 12: MT Listings
        self.mtListing = QtWidgets.QWidget()
        self.mtListing.setObjectName("mtListing")
        self.mergerTechHeader = QtWidgets.QLabel(self.mtListing)
        self.mergerTechHeader.setGeometry(QtCore.QRect(290, 20, 191, 16))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.mergerTechHeader.setFont(font)
        self.mergerTechHeader.setObjectName("mergerTechHeader")

        self.mtResultsTable = QtWidgets.QTableWidget(self.mtListing)
        self.mtResultsTable.setGeometry(QtCore.QRect(0, 130, 771, 341))
        self.mtResultsTable.setColumnCount(5)
        self.mtResultsTable.setObjectName("mtResultsTable")
        self.mtResultsTable.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.mtResultsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.mtResultsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.mtResultsTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.mtResultsTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.mtResultsTable.setHorizontalHeaderItem(4, item)

        mtheader = self.mtResultsTable.horizontalHeader()
        mtheader.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.label_6 = QtWidgets.QLabel(self.mtListing)
        self.label_6.setGeometry(QtCore.QRect(240, 50, 291, 20))
        self.label_6.setObjectName("label_6")

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(65)
        self.selectInstructions_2 = QtWidgets.QLabel(self.mtListing)
        self.selectInstructions_2.setGeometry(QtCore.QRect(25, 472, 270, 16))
        self.selectInstructions_2.setObjectName("selectInstructions_2")
        self.selectInstructions_2.setFont(font)

        self.numberOfResults_2 = QtWidgets.QLabel(self.mtListing)
        self.numberOfResults_2.setGeometry(QtCore.QRect(580, 470, 121, 16))
        self.numberOfResults_2.setObjectName("numberOfResults_2")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.mtResultsCount = QtWidgets.QLabel(self.mtListing)
        self.mtResultsCount.setGeometry(QtCore.QRect(720, 470, 41, 16))
        self.mtResultsCount.setObjectName("mtResultsCount")
        self.mtResultsCount.setFont(font)
        self.exportToXL_3 = QtWidgets.QCommandLinkButton(self.mtListing)
        self.exportToXL_3.setGeometry(QtCore.QRect(260, 100, 141, 31))
        self.exportToXL_3.setObjectName("exportToXL_3")
        self.exportToXL_3.clicked.connect(lambda: \
            self.excelify_listings(self.mtResultsTable))
        self.label_36 = QtWidgets.QLabel(self.mtListing)
        self.label_36.setGeometry(QtCore.QRect(110, 110, 141, 16))
        self.label_36.setObjectName("label_36")
        self.addToSR_3 = QtWidgets.QCommandLinkButton(self.mtListing)
        self.addToSR_3.setGeometry(QtCore.QRect(410, 100, 181, 31))
        self.addToSR_3.setWhatsThis("")
        self.addToSR_3.setObjectName("addToSR_3")
        self.addToSR_3.clicked.connect(lambda: self.starify_mt())

        self.label_37 = QtWidgets.QLabel(self.mtListing)
        self.label_37.setGeometry(QtCore.QRect(270, 70, 231, 16))
        self.label_37.setObjectName("label_37")

        self.mtlogo_label = QtWidgets.QLabel(self.mtListing)
        self.mtlogo_label.setGeometry(QtCore.QRect(30, 30, 171, 51))
        self.mtlogo_label.setStyleSheet("""\
            background-image: url(:/appResources/mtlogo.png)""")
        self.mtlogo_label.setText("")
        self.mtlogo_label.setPixmap(QtGui.QPixmap(":/appResources/mtlogo.png"))
        self.mtlogo_label.setScaledContents(True)
        self.mtlogo_label.setObjectName("mtlogo_label")

        self.returnToStart_14 = QtWidgets.QPushButton(self.mtListing)
        self.returnToStart_14.setGeometry(QtCore.QRect(320, 470, 121, 32))
        self.returnToStart_14.setObjectName("returnToStart_14")
        self.returnToStart_14.clicked.connect(lambda: self.return_to_start())
        self.stackedWidget.addWidget(self.mtListing)


        # Page 13: SBN Listings
        self.sunbeltListing = QtWidgets.QWidget()
        self.sunbeltListing.setObjectName("sunbeltListing")
        self.sunbeltHeader = QtWidgets.QLabel(self.sunbeltListing)
        self.sunbeltHeader.setGeometry(QtCore.QRect(270, 20, 221, 20))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        
        self.sunbeltHeader.setFont(font)
        self.sunbeltHeader.setTextFormat(QtCore.Qt.PlainText)
        self.sunbeltHeader.setObjectName("sunbeltHeader")
        self.label_4 = QtWidgets.QLabel(self.sunbeltListing)
        self.label_4.setGeometry(QtCore.QRect(280, 40, 211, 20))
        self.label_4.setObjectName("label_4")
        self.sbSubmit = QtWidgets.QPushButton(self.sunbeltListing)
        self.sbSubmit.setGeometry(QtCore.QRect(320, 90, 121, 32))
        self.sbSubmit.setObjectName("sbSubmit")
        self.sbSubmit.clicked.connect(lambda: self.scour_sb())

        self.statesBox_2 = QtWidgets.QComboBox(self.sunbeltListing)
        self.statesBox_2.setGeometry(QtCore.QRect(290, 60, 181, 21))
        self.statesBox_2.setEditable(True)
        policy = QtWidgets.QComboBox.AdjustToMinimumContentsLength
        self.statesBox_2.setSizeAdjustPolicy(policy)
        self.statesBox_2.setObjectName("statesBox_2")
        self.statesBox_2.addItem("")
        self.statesBox_2.setItemText(1, "")
        self.statesBox_2.setItemText(2, "")
        for state in states_list:
            self.statesBox.addItem(state)
            self.statesBox_2.addItem(state)
        self.sbn_settings = None

        self.sbResultsTable = QtWidgets.QTableWidget(self.sunbeltListing)
        self.sbResultsTable.setGeometry(QtCore.QRect(0, 150, 771, 321))
        policy = QtCore.Qt.ScrollBarAlwaysOn
        self.sbResultsTable.setVerticalScrollBarPolicy(policy)
        self.sbResultsTable.setHorizontalScrollBarPolicy(policy)
        self.sbResultsTable.setColumnCount(8)
        self.sbResultsTable.setObjectName("sbResultsTable")
        self.sbResultsTable.setRowCount(0)
        
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.sbResultsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.sbResultsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.sbResultsTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.sbResultsTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.sbResultsTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.sbResultsTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.sbResultsTable.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.sbResultsTable.setHorizontalHeaderItem(7, item)

        font = QtGui.QFont()
        platform_format(font, 9, True, 65)
        font.setItalic(True)
        self.selectInstructions_3 = QtWidgets.QLabel(self.sunbeltListing)
        self.selectInstructions_3.setGeometry(QtCore.QRect(30, 472, 270, 16))
        self.selectInstructions_3.setObjectName("selectInstructions_3")
        self.selectInstructions_3.setFont(font)

        self.numberOfResults_3 = QtWidgets.QLabel(self.sunbeltListing)
        self.numberOfResults_3.setGeometry(QtCore.QRect(580, 470, 121, 16))
        self.numberOfResults_3.setObjectName("numberOfResults_3")
        font = QtGui.QFont()
        platform_format(font, 14, True, 75)
        self.sbResultsCount = QtWidgets.QLabel(self.sunbeltListing)
        self.sbResultsCount.setGeometry(QtCore.QRect(720, 470, 41, 16))
        self.sbResultsCount.setObjectName("sbResultsCount")
        self.sbResultsCount.setFont(font)
        self.addToSR_4 = QtWidgets.QCommandLinkButton(self.sunbeltListing)
        self.addToSR_4.setGeometry(QtCore.QRect(500, 120, 181, 31))
        self.addToSR_4.setObjectName("addToSR_4")
        self.addToSR_4.clicked.connect(lambda: self.starify_sb())
        self.followURL_4 = QtWidgets.QCommandLinkButton(self.sunbeltListing)
        self.followURL_4.setGeometry(QtCore.QRect(400, 120, 91, 31))
        self.followURL_4.setObjectName("followURL_4")
        self.followURL_4.clicked.connect(lambda: \
            self.browse_web(self.sbResultsTable))
        self.label_38 = QtWidgets.QLabel(self.sunbeltListing)
        self.label_38.setGeometry(QtCore.QRect(100, 130, 141, 16))
        self.label_38.setObjectName("label_38")
        self.exportToXL_4 = QtWidgets.QCommandLinkButton(self.sunbeltListing)
        self.exportToXL_4.setGeometry(QtCore.QRect(250, 120, 141, 31))
        self.exportToXL_4.setObjectName("exportToXL_4")
        self.exportToXL_4.clicked.connect(lambda: \
            self.excelify_listings(self.sbResultsTable))
        self.sblogo = QtWidgets.QLabel(self.sunbeltListing)
        self.sblogo.setGeometry(QtCore.QRect(30, 30, 171, 51))
        self.sblogo.setStyleSheet("""\
            background-image: url(:/appResources/sunbeltlogo.png)""")
        self.sblogo.setText("")
        self.sblogo.setPixmap(QtGui.QPixmap(":/appResources/sunbeltlogo.png"))
        self.sblogo.setScaledContents(True)
        self.sblogo.setObjectName("sblogo")

        self.returnToStart_15 = QtWidgets.QPushButton(self.sunbeltListing)
        self.returnToStart_15.setGeometry(QtCore.QRect(320, 470, 121, 32))
        self.returnToStart_15.setObjectName("returnToStart_15")
        self.returnToStart_15.clicked.connect(lambda: self.return_to_start())
        self.stackedWidget.addWidget(self.sunbeltListing)


        # Page 14: TW Listings
        self.tworldListing = QtWidgets.QWidget()
        self.tworldListing.setObjectName("tworldListing")
        self.tworldHeader = QtWidgets.QLabel(self.tworldListing)
        self.tworldHeader.setGeometry(QtCore.QRect(305, 20, 221, 20))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        
        self.tworldHeader.setFont(font)
        self.tworldHeader.setTextFormat(QtCore.Qt.PlainText)
        self.tworldHeader.setObjectName("tworldHeader")
        self.label_5 = QtWidgets.QLabel(self.tworldListing)
        self.label_5.setGeometry(QtCore.QRect(280, 40, 211, 20))
        self.label_5.setObjectName("label_5")
        self.twSubmit = QtWidgets.QPushButton(self.tworldListing)
        self.twSubmit.setGeometry(QtCore.QRect(320, 90, 121, 32))
        self.twSubmit.setObjectName("twSubmit")
        self.twSubmit.clicked.connect(lambda: self.scour_tw())

        self.twResultsTable = QtWidgets.QTableWidget(self.tworldListing)
        self.twResultsTable.setGeometry(QtCore.QRect(0, 150, 771, 321))
        policy = QtCore.Qt.ScrollBarAlwaysOn
        self.twResultsTable.setVerticalScrollBarPolicy(policy)
        self.twResultsTable.setHorizontalScrollBarPolicy(policy)
        self.twResultsTable.setColumnCount(9)
        self.twResultsTable.setObjectName("twResultsTable")
        self.twResultsTable.setRowCount(0)
        
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.twResultsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.twResultsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.twResultsTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.twResultsTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.twResultsTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.twResultsTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.twResultsTable.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.twResultsTable.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.twResultsTable.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.twResultsTable.setHorizontalHeaderItem(9, item)

        twheader = self.twResultsTable.horizontalHeader()
        twheader.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        
        self.statesBox_3 = QtWidgets.QComboBox(self.tworldListing)
        self.statesBox_3.setGeometry(QtCore.QRect(290, 60, 181, 21))
        self.statesBox_3.setEditable(True)
        policy = QtWidgets.QComboBox.AdjustToMinimumContentsLength
        self.statesBox_3.setSizeAdjustPolicy(policy)
        self.statesBox_3.setObjectName("statesBox_3")
        self.statesBox_3.addItem("")
        self.statesBox_3.setItemText(1, "")
        self.statesBox_3.setItemText(2, "")
        for state in states_list:
            self.statesBox.addItem(state)
            self.statesBox_3.addItem(state)

        font = QtGui.QFont()
        platform_format(font, 9, True, 65)
        font.setItalic(True)
        self.selectInstructions_4 = QtWidgets.QLabel(self.tworldListing)
        self.selectInstructions_4.setGeometry(QtCore.QRect(30, 472, 270, 16))
        self.selectInstructions_4.setObjectName("selectInstructions_4")
        self.selectInstructions_4.setFont(font)

        self.numberOfResults_4 = QtWidgets.QLabel(self.tworldListing)
        self.numberOfResults_4.setGeometry(QtCore.QRect(580, 470, 121, 16))
        self.numberOfResults_4.setObjectName("numberOfResults_4")
        font = QtGui.QFont()
        platform_format(font, 14, True, 75)
        self.twResultsCount = QtWidgets.QLabel(self.tworldListing)
        self.twResultsCount.setGeometry(QtCore.QRect(720, 470, 41, 16))
        self.twResultsCount.setObjectName("sbResultsCount")
        self.twResultsCount.setFont(font)
        self.addToSR_5 = QtWidgets.QCommandLinkButton(self.tworldListing)
        self.addToSR_5.setGeometry(QtCore.QRect(500, 120, 181, 31))
        self.addToSR_5.setObjectName("addToSR_5")
        self.addToSR_5.clicked.connect(lambda: self.starify_tw())
        self.followURL_5 = QtWidgets.QCommandLinkButton(self.tworldListing)
        self.followURL_5.setGeometry(QtCore.QRect(400, 120, 91, 31))
        self.followURL_5.setObjectName("followURL_5")
        self.followURL_5.clicked.connect(lambda: \
            self.browse_web(self.twResultsTable))
        self.label_39 = QtWidgets.QLabel(self.tworldListing)
        self.label_39.setGeometry(QtCore.QRect(100, 130, 141, 16))
        self.label_39.setObjectName("label_39")
        self.exportToXL_5 = QtWidgets.QCommandLinkButton(self.tworldListing)
        self.exportToXL_5.setGeometry(QtCore.QRect(250, 120, 141, 31))
        self.exportToXL_5.setObjectName("exportToXL_5")
        self.exportToXL_5.clicked.connect(lambda: \
            self.excelify_listings(self.twResultsTable))
        self.twlogo = QtWidgets.QLabel(self.tworldListing)
        self.twlogo.setGeometry(QtCore.QRect(30, 30, 171, 51))
        self.twlogo.setStyleSheet("""\
            background-image: url(:/appResources/twlogo.png)""")
        self.twlogo.setText("")
        self.twlogo.setPixmap(QtGui.QPixmap(":/appResources/twlogo.png"))
        self.twlogo.setScaledContents(True)
        self.twlogo.setObjectName("twlogo")

        self.returnToStart_16 = QtWidgets.QPushButton(self.tworldListing)
        self.returnToStart_16.setGeometry(QtCore.QRect(320, 470, 121, 32))
        self.returnToStart_16.setObjectName("returnToStart_16")
        self.returnToStart_16.clicked.connect(lambda: self.return_to_start())
        self.stackedWidget.addWidget(self.tworldListing)


        # Page 15: Cross-site Listings
        self.crossSiteScrape = QtWidgets.QWidget()
        self.crossSiteScrape.setObjectName("crossSiteScrape")
        self.crossSiteDataHeader = QtWidgets.QLabel(self.crossSiteScrape)
        self.crossSiteDataHeader.setGeometry(QtCore.QRect(300, 10, 171, 20))
        
        font = QtGui.QFont()
        platform_format(font, 15, True, 75)
        self.crossSiteDataHeader.setFont(font)
        self.crossSiteDataHeader.setObjectName("crossSiteDataHeader")
        self.label_13 = QtWidgets.QLabel(self.crossSiteScrape)
        self.label_13.setGeometry(QtCore.QRect(240, 40, 281, 20))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.crossSiteScrape)
        self.label_14.setGeometry(QtCore.QRect(270, 60, 231, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.crossSiteScrape)
        self.label_15.setGeometry(QtCore.QRect(338, 60, 31, 16))

        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.totalNewListings = QtWidgets.QLCDNumber(self.crossSiteScrape)
        self.totalNewListings.setGeometry(QtCore.QRect(340, 80, 81, 31))
        self.totalNewListings.setObjectName("totalNewListings")
        self.totalScoringHigher = QtWidgets.QLCDNumber(self.crossSiteScrape)
        self.totalScoringHigher.setGeometry(QtCore.QRect(340, 150, 81, 31))
        self.totalScoringHigher.setObjectName("totalScoringHigher")
        self.label_16 = QtWidgets.QLabel(self.crossSiteScrape)
        self.label_16.setGeometry(QtCore.QRect(250, 130, 231, 16))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.crossSiteScrape)
        self.label_17.setGeometry(QtCore.QRect(322, 130, 31, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.minScoreLabel = QtWidgets.QLabel(self.crossSiteScrape)
        self.minScoreLabel.setGeometry(QtCore.QRect(494, 130, 31, 16))

        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.minScoreLabel.setFont(font)
        self.minScoreLabel.setObjectName("minScoreLabel")
        self.csResultsTable = QtWidgets.QTableWidget(self.crossSiteScrape)
        self.csResultsTable.setGeometry(QtCore.QRect(5, 221, 761, 241))
        self.csResultsTable.setObjectName("csResultsTable")
        self.csResultsTable.setColumnCount(7)
        self.csResultsTable.setRowCount(0)
        
        self.csResultsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.csResultsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.csResultsTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.csResultsTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.csResultsTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.csResultsTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.csResultsTable.setHorizontalHeaderItem(6, item)

        self.addToSR_6 = QtWidgets.QCommandLinkButton(self.crossSiteScrape)
        self.addToSR_6.setGeometry(QtCore.QRect(500, 190, 181, 31))
        self.addToSR_6.setObjectName("addToSR_6")
        self.addToSR_6.clicked.connect(lambda: self.starify_crosssite())
        self.followURL_6 = QtWidgets.QCommandLinkButton(self.crossSiteScrape)
        self.followURL_6.setGeometry(QtCore.QRect(400, 190, 91, 31))
        self.followURL_6.setObjectName("followURL_6")
        self.followURL_6.clicked.connect(lambda: \
            self.browse_web(self.csResultsTable))
        self.label_40 = QtWidgets.QLabel(self.crossSiteScrape)
        self.label_40.setGeometry(QtCore.QRect(100, 200, 141, 16))
        self.label_40.setObjectName("label_40")
        self.exportToXL_6 = QtWidgets.QCommandLinkButton(self.crossSiteScrape)
        self.exportToXL_6.setGeometry(QtCore.QRect(250, 190, 141, 31))
        self.exportToXL_6.setObjectName("exportToXL_6")
        self.exportToXL_6.clicked.connect(lambda: \
            self.excelify_listings(self.csResultsTable))

        font = QtGui.QFont()
        platform_format(font, 9, False, 65)
        font.setItalic(True)
        self.selectInstructions_5 = QtWidgets.QLabel(self.crossSiteScrape)
        self.selectInstructions_5.setGeometry(QtCore.QRect(30, 472, 270, 16))
        self.selectInstructions_5.setObjectName("selectInstructions_5")
        self.selectInstructions_5.setFont(font)

        self.returnToStart_17 = QtWidgets.QPushButton(self.crossSiteScrape)
        self.returnToStart_17.setGeometry(QtCore.QRect(320, 470, 121, 32))
        self.returnToStart_17.setObjectName("returnToStart_17")
        self.returnToStart_17.clicked.connect(lambda: self.return_to_start())
        self.stackedWidget.addWidget(self.crossSiteScrape)


        # Page 16: Web Browsers
        self.fakeChrome = QtWidgets.QWidget()
        self.fakeChrome.setObjectName("fakeChrome")

        self.urlBar = QtWidgets.QLineEdit(self.fakeChrome)
        self.urlBar.setGeometry(QtCore.QRect(124, 6, 585, 31))
        self.urlBar.setClearButtonEnabled(True)
        self.urlBar.setObjectName("urlBar")
        self.backButton = QtWidgets.QPushButton(self.fakeChrome)
        self.backButton.setEnabled(False)
        self.backButton.setGeometry(QtCore.QRect(16, 6, 49, 40))
        self.backButton.setObjectName("backButton")
        self.backButton.clicked.connect(lambda: \
            self.webbrowser_button("back"))
        self.forwardButton = QtWidgets.QPushButton(self.fakeChrome)
        self.forwardButton.setEnabled(False)
        self.forwardButton.setGeometry(QtCore.QRect(66, 6, 49, 40))
        self.forwardButton.setObjectName("forwardButton")
        self.forwardButton.clicked.connect(lambda: \
            self.webbrowser_button("forward"))
        self.enterButton = QtWidgets.QPushButton(self.fakeChrome)
        self.enterButton.setGeometry(QtCore.QRect(712, 6, 55, 40))
        self.enterButton.setObjectName("enterButton")
        self.enterButton.clicked.connect(lambda: self.hit_enter())

        self.browserTabs = QtWidgets.QTabWidget(self.fakeChrome)
        self.browserTabs.setGeometry(QtCore.QRect(0, 50, 761, 401))
        self.browserTabs.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.browserTabs.setUsesScrollButtons(True)
        self.browserTabs.setTabsClosable(True)
        self.browserTabs.setMovable(True)
        self.browserTabs.setObjectName("browserTabs")
        self.browserTabs.tabBarClicked.connect(self.change_tabs)
        self.browserTabs.tabCloseRequested.connect(self.close_tabs)

        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.webEngineView_1 = QtWebEngineWidgets.QWebEngineView(self.tab1)
        self.webEngineView_1.setGeometry(QtCore.QRect(0, 0, 761, 371))
        self.page_view = WebEnginePage(self.webEngineView_1)
        self.webEngineView_1.setPage(self.page_view)
        self.webEngineView_1.setMouseTracking(True)
        self.webEngineView_1.setUrl(QtCore.QUrl("https://www.bizbuysell.com/"))
        self.webEngineView_1.setZoomFactor(0.8)
        self.webEngineView_1.setObjectName("webEngineView_1")
        self.browserTabs.addTab(self.tab1, "")

        self.returnToStart_18 = QtWidgets.QPushButton(self.fakeChrome)
        self.returnToStart_18.setGeometry(QtCore.QRect(320, 470, 121, 32))
        self.returnToStart_18.setObjectName("returnToStart_18")
        self.returnToStart_18.clicked.connect(lambda: self.return_to_start())
        
        self.stackedWidget.addWidget(self.fakeChrome)
        BrokeredDealEvaluator.setCentralWidget(self.centralwidget)
        

        ###################### MENU & STATUS BAR ######################

        
        self.statusbar = QtWidgets.QStatusBar(BrokeredDealEvaluator)
        self.statusbar.setObjectName("statusbar")
        BrokeredDealEvaluator.setStatusBar(self.statusbar)

        self.menuBar = QtWidgets.QMenuBar(BrokeredDealEvaluator)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 810, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuScoring_Algorithm = QtWidgets.QMenu(self.menuBar)
        self.menuScoring_Algorithm.setObjectName("menuScoring_Algorithm")
        self.menuResults = QtWidgets.QMenu(self.menuBar)
        self.menuResults.setObjectName("menuResults")
        self.menuWebsites = QtWidgets.QMenu(self.menuBar)
        self.menuWebsites.setObjectName("menuWebsites")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuEvaluator = QtWidgets.QMenu(self.menuBar)
        self.menuEvaluator.setObjectName("menuEvaluator")

        BrokeredDealEvaluator.setMenuBar(self.menuBar)
        self.actionAppInfo = QtWidgets.QAction(BrokeredDealEvaluator)
        self.actionAppInfo.setObjectName("actionAppInfo")
        self.actionAppInfo.triggered.connect(lambda: \
            self.stackedWidget.setCurrentIndex(1))
        self.actionVersion = QtWidgets.QAction(BrokeredDealEvaluator)
        self.actionVersion.setObjectName("actionVersion")
        self.actionVersion.triggered.connect(lambda: \
            self.show_popup("Brokered Deal Evaluator Version", \
            QtWidgets.QMessageBox.Information, version_info))

        self.actionLicenses = QtWidgets.QAction(BrokeredDealEvaluator)
        self.actionLicenses.setObjectName("actionLicenses")
        self.actionLicenses.triggered.connect(lambda: \
            self.stackedWidget.setCurrentIndex(2))
        self.actionHome_Page = QtWidgets.QAction(BrokeredDealEvaluator)
        self.actionHome_Page.setObjectName("actionHome_Page")
        self.actionHome_Page.triggered.connect(lambda: self.return_to_start())
        self.actionView_Past_Entries = QtWidgets.QAction(BrokeredDealEvaluator)
        self.actionView_Past_Entries.setObjectName("actionView_Past_Entries")
        self.actionView_Past_Entries.triggered.connect(lambda: \
            self.stackedWidget.setCurrentIndex(3))
        self.actionStarred_Results = QtWidgets.QAction(BrokeredDealEvaluator)
        self.actionStarred_Results.setObjectName("actionStarred_Results")
        self.actionStarred_Results.triggered.connect(lambda: \
            self.view_starred_results())
        self.actionClear_Records = QtWidgets.QAction(BrokeredDealEvaluator)
        self.actionClear_Records.setObjectName("actionClear_Records")
        self.actionClear_Records.triggered.connect(lambda: \
            self.clear_records())
        self.actionExport = QtWidgets.QAction(BrokeredDealEvaluator)
        self.actionExport.setObjectName("actionExport")
        self.actionExport.triggered.connect(lambda: self.export_shortcut())
        self.actionExport.setDisabled(True)
        self.actionView_Keywords = QtWidgets.QAction(BrokeredDealEvaluator)
        self.actionView_Keywords.setObjectName("actionView_Keywords")
        self.actionView_Keywords.triggered.connect(lambda: \
            self.stackedWidget.setCurrentIndex(5))
        self.actionHow_to_Use = QtWidgets.QAction(BrokeredDealEvaluator)
        self.actionHow_to_Use.setObjectName("actionHow_to_Use")
        self.actionHow_to_Use.triggered.connect(lambda: \
            self.stackedWidget.setCurrentIndex(9))
        self.actionSend_Feedback = QtWidgets.QAction(BrokeredDealEvaluator)
        self.actionSend_Feedback.setObjectName("actionSend_Feedback")
        self.actionSend_Feedback.triggered.connect(lambda: \
            self.stackedWidget.setCurrentIndex(10))
        self.actionFull_Scrape = QtWidgets.QAction(BrokeredDealEvaluator)
        self.actionFull_Scrape.setObjectName("actionFull_Scrape")
        self.actionFull_Scrape.triggered.connect(lambda: \
            self.stackedWidget.setCurrentIndex(7))
        self.actionEditKeywords = QtWidgets.QAction(BrokeredDealEvaluator)
        self.actionEditKeywords.setObjectName("actionEditKeywords")
        self.actionEditKeywords.triggered.connect(lambda: \
            self.stackedWidget.setCurrentIndex(6))
        self.actionEnter = QtWidgets.QAction(BrokeredDealEvaluator)
        self.actionEnter.setObjectName("actionEnter")
        self.actionEnter.triggered.connect(lambda: self.hit_enter())
        self.actionInformation = QtWidgets.QAction(BrokeredDealEvaluator)
        self.actionInformation.setObjectName("actionInformation")
        self.actionInformation.triggered.connect(lambda: \
            self.stackedWidget.setCurrentIndex(8))

        self.menuScoring_Algorithm.addAction(self.actionView_Keywords)
        self.menuScoring_Algorithm.addAction(self.actionEditKeywords)
        self.menuResults.addAction(self.actionView_Past_Entries)
        self.menuResults.addAction(self.actionStarred_Results)
        self.menuResults.addSeparator()
        self.menuResults.addAction(self.actionExport)
        self.menuResults.addSeparator()
        self.menuResults.addAction(self.actionClear_Records)
        self.menuHelp.addAction(self.actionHow_to_Use)
        self.menuHelp.addAction(self.actionSend_Feedback)
        self.menuWebsites.addAction(self.actionFull_Scrape)
        self.menuWebsites.addAction(self.actionInformation)
        self.menuEvaluator.addAction(self.actionAppInfo)
        self.menuEvaluator.addAction(self.actionVersion)
        self.menuEvaluator.addAction(self.actionLicenses)
        self.menuEvaluator.addSeparator()
        self.menuEvaluator.addAction(self.actionHome_Page)
        self.menuBar.addAction(self.menuEvaluator.menuAction())
        self.menuBar.addAction(self.menuResults.menuAction())
        self.menuBar.addAction(self.menuScoring_Algorithm.menuAction())
        self.menuBar.addAction(self.menuWebsites.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(BrokeredDealEvaluator)
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(BrokeredDealEvaluator)


    def add_to_sr(self, df):
        """Adds a dataframe to the Starred Results database.
        Incoming dataframe must already be in the correct
        format of columns, as described below.
        """

        path = os.path.dirname(sys.modules[__name__].__file__)
        connection = sqlite3.connect("appbin/past_scrapes.db")
        c = connection.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS
            starred_results(
            listing_title text,
            tagline text,
            cash_flow text,
            description text,
            score integer,
            url text,
            source text,
            added_date date)""")

        command = """REPLACE INTO 
            starred_results(listing_title, tagline, cash_flow,
            description, score, url, source, added_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, date('now'))"""
        for index, row in df.iterrows():
            package = (row["Listing Title"], row["Tagline"], \
            row["Cash Flow"], row["Description"], row["Score"], \
            row["URL"], row["Source"])
            c.execute(command, package)

        connection.commit()
        connection.close()
        QtGui.QGuiApplication.processEvents()


    def browse_web(self, table):
        """Opens selected results from table of your choice
        in a web browser window.
        """
        
        selected_rows = []
        row_items = []
        n_cols = table.columnCount()
        for i in range(table.rowCount()):
            for j in range(n_cols):
                item = table.item(i, j)
                if item.isSelected() and i not in selected_rows:
                    selected_rows.append(i)
                    items = [table.item(i, k).text() for k in range(n_cols)]
                    row_items.append(items)

        if not row_items:
            self.show_popup("Please try again", QtWidgets.QMessageBox.Warning,\
                "No URLS selected.", "Select listings by clicking.")

        tbls = (self.bbsResultsTable, self.sbResultsTable, self.twResultsTable)
        if table in tbls:
            urls = [item[-1] for item in row_items]
        elif table == self.csResultsTable:
            urls = [item[-2] for item in row_items]
        elif table == self.starredResultsTable:
            urls = [items[-3] for item in row_items]
        urls = list(filter(lambda url: url[:7] != "mailto:", urls))
        self.webEngineView_1.setUrl(QtCore.QUrl(urls[0]))
        self.webEngineView_1.urlChanged.connect(self.update_urlbar)
        self.urlBar.setText(urls[0])

        for i, url in enumerate(urls[1:]):
            idx = str(i + 2)
            setattr(self, "tab" + idx, QtWidgets.QWidget())
            getattr(self, "tab" + idx).setObjectName("tab" + idx)
            setattr(self, "webEngineView_" + idx, \
                QtWebEngineWidgets.QWebEngineView(getattr(self, "tab" + idx)))

            setattr(self, "page_view" + idx, \
                WebEnginePage(getattr(self, "webEngineView_" + idx)))
            getattr(self, "webEngineView_" + idx).setPage(getattr(self, \
                "page_view" + idx))
            dimensions = QtCore.QRect(0, 0, 761, 371)
            getattr(self, "webEngineView_" + idx).setGeometry(dimensions)
            getattr(self, "webEngineView_" + idx).setMouseTracking(True)
            getattr(self, "webEngineView_" + idx).setUrl(QtCore.QUrl(url))
            getattr(self, "webEngineView_" + idx).setZoomFactor(0.8)
            getattr(self, "webEngineView_" + idx).urlChanged.connect(\
                self.update_urlbar)
            getattr(self, "webEngineView_" + idx).setObjectName(\
                "webEngineView" + idx)
            self.browserTabs.addTab(getattr(self, "tab" + idx), \
                "Listing " + idx)
        
        self.newTab = QtWidgets.QWidget()
        self.newTab.setObjectName("newTab")
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.newTab)
        self.webEngineView.setGeometry(QtCore.QRect(0, 0, 761, 371))
        self.page_view = WebEnginePage(self.webEngineView)
        self.webEngineView.setPage(self.page_view)
        self.webEngineView.setMouseTracking(True)
        self.webEngineView.setUrl(QtCore.QUrl("https://www.google.com/"))
        self.webEngineView.setZoomFactor(0.8)
        self.webEngineView.setObjectName("webEngineView")
        self.browserTabs.addTab(self.newTab, "New Tab")
        self.browserTabs.setTabText(self.browserTabs.indexOf(self.newTab), \
            QtCore.QCoreApplication.translate("BrokeredDealEvaluator", "New Tab"))

        self.actionExport.setDisabled(True)
        self.stackedWidget.setCurrentIndex(16)


    def change_tabs(self, idx):
        """Idx is the new tab of the Fake Chrome browser chosen.
        This method sets the URL Bar text accordingly.
        """
        idx += 1
        if idx != self.browserTabs.count():
            url_now = getattr(self, "webEngineView_" + str(idx)).url()
        else:
            url_now = self.webEngineView.url()
        self.urlBar.setText(url_now.toString())


    def clear_records(self):
        """Deletes records for both Starred Results and Past Scrapes."""
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Clear Records")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("Are you sure?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Cancel|\
            QtWidgets.QMessageBox.Yes)
        msg.setInformativeText("All records from Starred Results and " \
            + "Previous Scrapes will be wiped.")
        clicked = msg.exec_()
        if clicked == QtWidgets.QMessageBox.Yes:
            path = os.path.dirname(sys.modules[__name__].__file__)
            connection = sqlite3.connect("appbin/past_scrapes.db")
            c = connection.cursor()
            c.execute("DROP TABLE IF EXISTS starred_results")
            c.execute("DROP TABLE IF EXISTS scrape_history")
            connection.commit()
            connection.close()

        self.populate_starred_results()


    def close_tabs(self, idx):
        """Closes tabs in the tab browser widget (for Fake Chrome).
        This also goes through and renames the subsequent Web
        Engine Views, so that you can still update the URLs
        correctly even though the ordering is off.
        """

        if self.browserTabs.count() == 1:
            self.return_to_start()
            
        else:
            def rename_attribute(obj, old_name, new_name):
                obj.__dict__[new_name] = obj.__dict__.pop(old_name)

            if idx + 1 != self.browserTabs.count():
                rename_attribute(self, "webEngineView_" + str(idx + 1), \
                    "NullWebEngineView")
                for i in range(idx + 1, self.browserTabs.count()):
                    rename_attribute(self, "webEngineView_" + str(i + 1), \
                        "webEngineView_" + str(i))
            
            self.browserTabs.removeTab(idx)


    def excelify_listings(self, table):
        """Turns selected results from table of your choice
        into an Excel Spreadsheet, and prompts for a save name
        and location.
        """

        selected_rows = []
        row_items = []
        n_cols = table.columnCount()
        for i in range(table.rowCount()):
            for j in range(n_cols):
                item = table.item(i, j)
                if item.isSelected() and i not in selected_rows:
                    selected_rows.append(i)
                    items = [table.item(i, k).text() for k in range(n_cols)]
                    row_items.append(items)

        cols = [table.horizontalHeaderItem(n).text() for n in range(n_cols)]
        df = pd.DataFrame(row_items, columns=cols)
        self.export_dialog(df, table)


    def export_dialog(self, df, table):
        from pathlib import Path
        from datetime import date
        today = date.today().strftime("%d%b%y")
        if table == self.bbsResultsTable:
            site = "BBS"
        elif table == self.mtResultsTable:
            site = "MT"
        elif table == self.sbResultsTable:
            site = "SBN"
        elif table == self.twResultsTable:
            site = "TW"
        elif table == self.csResultsTable:
            site = "Cross-Site"
        elif table == self.starredResultsTable:
            site = "Starred"
        else:
            site = "Brokered"

        default = f"/{site} Deal Evaluator Results - {today}"
        home_dir = str(Path.home()) + default
        dialog = BrokeredDealEvaluator
        name, filter_type = QtWidgets.QFileDialog.getSaveFileName(dialog, \
            "Export as Spreadsheet", home_dir, "Excel files (*.xlsx);; \
                CSV files (*.csv)")
        if (filter_type == "Excel files (*.xlsx)"):
            df.to_excel(name, index=False)
        elif (filter_type == "CSV files (*.csv)"):
            df.to_csv(name, index=False)


    def export_shortcut(self):
        if self.stackedWidget.currentIndex() == 4:
            self.excelify_listings(self.starredResultsTable)
        elif self.stackedWidget.currentIndex() == 11:
            self.excelify_listings(self.bbsResultsTable)
        elif self.stackedWidget.currentIndex() == 12:
            self.excelify_listings(self.mtResultsTable)
        elif self.stackedWidget.currentIndex() == 13:
            self.excelify_listings(self.sbResultsTable)
        elif self.stackedWidget.currentIndex() == 14:
            self.excelify_listings(self.twResultsTable)
        elif self.stackedWidget.currentIndex() == 15:
            self.excelify_listings(self.csResultsTable)


    def filter_prev_scrapes(self):
        self.prevScrapesTable.setRowCount(0)
        path = os.path.dirname(sys.modules[__name__].__file__)
        conn = sqlite3.connect("appbin/past_scrapes.db")
        if self.allOption.isChecked():
            past_df = pd.read_sql_query("SELECT * FROM scrape_history", conn)
        elif self.bbsOption.isChecked():
            past_df = pd.read_sql_query("""SELECT * FROM scrape_history
                WHERE source LIKE 'BizBuySell.com'""", conn)
        elif self.mtOption.isChecked():
            past_df = pd.read_sql_query("""SELECT * FROM scrape_history
                WHERE source LIKE 'MergerTech.com'""", conn)
        elif self.sbOption.isChecked():
            past_df = pd.read_sql_query("""SELECT * FROM scrape_history
                WHERE source LIKE 'SunbeltNetwork.com'""", conn)
        elif self.twOption.isChecked():
            past_df = pd.read_sql_query("""SELECT * FROM scrape_history
                WHERE source LIKE 'TWorld.com'""", conn)
            
        past_df = past_df.sort_values(by=["score"], ascending=False)
        c = conn.cursor()
        c.execute("SELECT MAX(scrape_date) FROM scrape_history")
        exists = c.fetchone()
        conn.commit()
        conn.close()
        
        for i in range(past_df.shape[0]):
            rowPosition = self.prevScrapesTable.rowCount()
            self.prevScrapesTable.insertRow(rowPosition)
            for j in range(past_df.shape[1]):
                self.prevScrapesTable.setItem(rowPosition, j, \
                QtWidgets.QTableWidgetItem(str(past_df.iloc[i, j])))

        self.totalResultsPS.setText(str(len(past_df)))
        if exists:
            self.lastScrapeDate.setText(exists[0])
        else:
            self.lastScrapeDate.setText("None")
        
        QtGui.QGuiApplication.processEvents()
        self.prevScrapesTable.update()
        self.totalResultsPS.update()
        self.lastScrapeDate.update()


    def hit_enter(self):
        """What happens when you hit Return/Enter?"""
        if self.stackedWidget.currentIndex() == 16:
            idx = self.browserTabs.currentIndex() + 1
            if idx != self.browserTabs.count():
                url_now = getattr(self, "webEngineView_" + str(idx)).url()
            else:
                url_now = self.webEngineView.url()

            input_url = QtCore.QUrl(self.urlBar.text())
            if (input_url != url_now) and (idx != self.browserTabs.count()):
                getattr(self, "webEngineView_" + str(idx)).setUrl(input_url)
            elif (input_url != url_now) and (idx == self.browserTabs.count()):
                self.webEngineView.setUrl(input_url)


    def open_sf_dialog(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FileDialog()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()


    def populate_starred_results(self):
        path = os.path.dirname(sys.modules[__name__].__file__)
        conn = sqlite3.connect("appbin/past_scrapes.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS
            starred_results(
            listing_title text,
            tagline text,
            cash_flow text,
            description text,
            score integer,
            url text,
            source text,
            added_date date)""")

        star_df = pd.read_sql_query("SELECT * FROM starred_results", conn)
        conn.commit()
        conn.close()

        self.starredResultsTable.setRowCount(0)
        starredHeader = self.starredResultsTable.horizontalHeader()
        if len(star_df) > 0:
            for i in range(star_df.shape[0]):
                rowPosition = self.starredResultsTable.rowCount()
                self.starredResultsTable.insertRow(rowPosition)
                for j in range(star_df.shape[1]):
                    self.starredResultsTable.setItem(rowPosition, j, \
                    QtWidgets.QTableWidgetItem(str(star_df.iloc[i, j])))
            for n in (0, 2, 6):
                starredHeader.setSectionResizeMode(n, \
                QtWidgets.QHeaderView.ResizeToContents)
        else:
            for n in range(7):
                starredHeader.setSectionResizeMode(n, \
                    QtWidgets.QHeaderView.Stretch)

        self.totalResultsSR.setText(str(self.starredResultsTable.rowCount()))
        QtGui.QGuiApplication.processEvents()
        self.totalResultsSR.update()


    def remove_from_sr(self):
        """Removes rows from the Starred Results table."""

        selected_rows = []
        items = []
        # Find rows in the table with selected elements
        for i in range(self.starredResultsTable.rowCount()):
            for j in range(self.starredResultsTable.columnCount()):
                item = self.starredResultsTable.item(i, j)
                if item.isSelected() and i not in selected_rows:
                    selected_rows.append(i)
                    items.append([self.starredResultsTable.item(i, 0).text(), \
                        self.starredResultsTable.item(i, 5).text()])

        path = os.path.dirname(sys.modules[__name__].__file__)
        connection = sqlite3.connect("appbin/past_scrapes.db")
        c = connection.cursor()
        command = """DELETE FROM starred_results
            WHERE listing_title=? AND url=?"""
        for item in items:
            c.execute(command, item)
        connection.commit()
        connection.close()

        self.populate_starred_results()
        self.starredResultsTable.update()
        self.totalResultsSR.setText(str(self.starredResultsTable.rowCount()))
        if self.starredResultsTable.rowCount() == 0:
            starredHeader = self.starredResultsTable.horizontalHeader()
            starredHeader.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        QtGui.QGuiApplication.processEvents()
        self.totalResultsSR.update()


    def return_to_start(self):
        self.actionExport.setDisabled(True)
        self.stackedWidget.setCurrentIndex(0)


    def scour_by_site(self):
        if self.bbsOption_2.isChecked():
            self.stackedWidget.setCurrentIndex(11)
        elif self.mtOption_2.isChecked():
            self.scour_mt()
            self.stackedWidget.setCurrentIndex(12)
        elif self.sbOption_2.isChecked():
            self.stackedWidget.setCurrentIndex(13)
        elif self.twOption_2.isChecked():
            self.stackedWidget.setCurrentIndex(14)
        self.actionExport.setDisabled(False)


    def scour_bbs(self):
        state_choice = str(self.statesBox.currentText())
        self.bbsResultsTable.setRowCount(0)
        bbsheader = self.bbsResultsTable.horizontalHeader()
        bbsheader.setSectionResizeMode(0, \
            QtWidgets.QHeaderView.ResizeToContents)
        
        if self.edited_pos_keywords is None and self.edited_neg_keywords is None:
            case = bbsapp.BizBuySell([state_choice], settings=self.bbs_settings)
        else:
            case = bbsapp.BizBuySell([state_choice], settings=self.bbs_settings, \
                positive_inputs=self.edited_pos_keywords, \
                negative_inputs=self.edited_neg_keywords)
        df = case.make_dataframe()
        for i in range(df.shape[0]):
            rowPosition = self.bbsResultsTable.rowCount()
            self.bbsResultsTable.insertRow(rowPosition)
            for j in range(df.shape[1]):
                self.bbsResultsTable.setItem(rowPosition, j, \
                QtWidgets.QTableWidgetItem(str(df.iloc[i, j])))
        self.bbsResultsCount.setText(str(self.bbsResultsTable.rowCount()))
        
        QtGui.QGuiApplication.processEvents()
        self.bbsResultsCount.update()
        

    def scour_mt(self):
        self.mtResultsTable.setRowCount(0)
        mtheader = self.mtResultsTable.horizontalHeader()
        mtheader.setSectionResizeMode(0, \
            QtWidgets.QHeaderView.ResizeToContents)
        mtheader.setSectionResizeMode(1, \
            QtWidgets.QHeaderView.Stretch)
        mtheader.setSectionResizeMode(2, \
            QtWidgets.QHeaderView.Stretch)
        mtheader.setSectionResizeMode(3, \
            QtWidgets.QHeaderView.ResizeToContents)
        
        if self.edited_pos_keywords is None and self.edited_neg_keywords is None:
            case = mtapp.MergerTech()
        else:
            case = mtapp.MergerTech(positive_inputs=self.edited_pos_keywords, \
                negative_inputs=self.edited_neg_keywords)
        df = case.make_dataframe()
        for i in range(df.shape[0]):
            rowPosition = self.mtResultsTable.rowCount()
            self.mtResultsTable.insertRow(rowPosition)
            for j in range(df.shape[1]):
                self.mtResultsTable.setItem(rowPosition, j, \
                QtWidgets.QTableWidgetItem(str(df.iloc[i, j])))
        self.mtResultsCount.setText(str(self.mtResultsTable.rowCount()))


    def scour_sb(self):
        state_choice = str(self.statesBox_2.currentText())
        self.sbResultsTable.setRowCount(0)
        sbheader = self.sbResultsTable.horizontalHeader()
        sbheader.setSectionResizeMode(0, \
            QtWidgets.QHeaderView.ResizeToContents)
        
        if self.edited_pos_keywords is None and self.edited_neg_keywords is None:
            case = sbapp.Sunbelt([state_choice], settings=self.sbn_settings)
        else:
            case = sbapp.Sunbelt([state_choice], settings=self.sbn_settings, \
                positive_inputs=self.edited_pos_keywords, \
                negative_inputs=self.edited_neg_keywords)
        df = case.make_dataframe()
        for i in range(df.shape[0]):
            rowPosition = self.sbResultsTable.rowCount()
            self.sbResultsTable.insertRow(rowPosition)
            for j in range(df.shape[1]):
                self.sbResultsTable.setItem(rowPosition, j, \
                QtWidgets.QTableWidgetItem(str(df.iloc[i, j])))
        self.sbResultsCount.setText(str(self.sbResultsTable.rowCount()))
        
        QtGui.QGuiApplication.processEvents()
        self.sbResultsCount.update()


    def scour_tw(self):
        state_choice = str(self.statesBox_3.currentText())
        self.twResultsTable.setRowCount(0)
        twheader = self.twResultsTable.horizontalHeader()
        twheader.setSectionResizeMode(0, \
            QtWidgets.QHeaderView.ResizeToContents)
        twheader.setSectionResizeMode(4, \
            QtWidgets.QHeaderView.ResizeToContents)
        
        if self.edited_pos_keywords is None and self.edited_neg_keywords is None:
            case = twapp.TWorld([state_choice])
        else:
            case = twapp.TWorld([state_choice], \
                positive_inputs=self.edited_pos_keywords, \
                negative_inputs=self.edited_neg_keywords)
        df = case.make_dataframe()
        for i in range(df.shape[0]):
            rowPosition = self.twResultsTable.rowCount()
            self.twResultsTable.insertRow(rowPosition)
            for j in range(df.shape[1]):
                self.twResultsTable.setItem(rowPosition, j, \
                QtWidgets.QTableWidgetItem(str(df.iloc[i, j])))
        self.twResultsCount.setText(str(self.twResultsTable.rowCount()))
        
        QtGui.QGuiApplication.processEvents()
        self.sbResultsCount.update()


    def scour_all(self):
        min_score = self.minScoreSpinBox.value()
        self.minScoreLabel.setText(f"{min_score}: ")
        
        if self.edited_pos_keywords is None and self.edited_neg_keywords is None:
            case = cross_site.FullScrape(include=self.cross_site_settings)
        else:
            case = cross_site.FullScrape(include=self.cross_site_settings, \
                positive_inputs=self.edited_pos_keywords, \
                negative_inputs=self.edited_neg_keywords)

        setting = self.newOrAll.currentText()
        if setting == "all":
            self.label_17.setText("total")
            self.label_16.setText(\
                "Number of          results scoring at least")
            df, size = case.check_above_score(min_score, "all")
        elif setting == "new":
            self.label_17.setText("new")
            self.label_16.setText(\
                "Number of         results scoring at least")
            df, size = case.check_above_score(min_score, "new")

        self.csResultsTable.clearContents()
        csheader = self.csResultsTable.horizontalHeader()
        csheader.setSectionResizeMode(0, \
            QtWidgets.QHeaderView.ResizeToContents)
        csheader.setSectionResizeMode(6, \
            QtWidgets.QHeaderView.ResizeToContents)
        
        for i in range(df.shape[0]):
            rowPosition = self.csResultsTable.rowCount()
            self.csResultsTable.insertRow(rowPosition)
            for j in range(df.shape[1]):
                self.csResultsTable.setItem(rowPosition, j, \
                QtWidgets.QTableWidgetItem(str(df.iloc[i, j])))

        row_count = self.csResultsTable.rowCount()
        self.totalNewListings.display(size)
        self.totalScoringHigher.display(row_count)

        QtGui.QGuiApplication.processEvents()
        self.stackedWidget.setCurrentIndex(15)
        self.actionExport.setDisabled(False)


    def send_feedback(self):
        import smtplib
        import ssl
        from email.mime.text import MIMEText
        author = self.inputEmail.text()
        recipient = ["shaun.radgowski@yale.edu"]
        sender = "brokereddealevaluator@gmail.com"
        password = "x62x72x6fx6bx65x72x65x64*"
        topic = self.inputTopic.text()
        note = self.inputMessage.toPlainText()

        if not author:
            self.show_popup("Add Email", QtWidgets.QMessageBox.Critical, \
                "Cannot send email. Please input your email!")
            return 0

        elif not note:
            self.show_popup("Add Message", QtWidgets.QMessageBox.Critical, \
                "Cannot send email. Please input your feedback!")
            return 0

        subject = "Brokered Deal Evaluator Feedback"
        body = f"""FEEDBACK from the Brokered Deal Evaluator Application:
        \n\nSENDER: {author}
        \n\nTOPIC: {topic}
        \n\nMESSAGE: {note}"""
        msg = MIMEText(body)
        msg["Subject"] = "Brokered Deal Evaluator Feedback"
        msg["From"] = sender
        msg["To"] = "shaun.radgowski@yale.edu"

        context = ssl.create_default_context()
        server = "smtp.gmail.com"
        try:
            with smtplib.SMTP_SSL(server, 465, context=context) as mail:
                mail.login(sender, password)
                mail.sendmail(sender, recipient, msg.as_string())
        except Exception as e:
            self.show_popup("Email Error", QtWidgets.QMessageBox.Critical, \
                "Cannot send email. Error occured:", info=e)
        else:
            self.show_popup("Email Sent", QtWidgets.QMessageBox.Information,\
                "Success!", "Feedback email has been sent to the developer.")


    def show_popup(self, title, icon, text, info=None):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setIcon(icon)
        msg.setText(text)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        if info:
            msg.setInformativeText(info)
        msg.exec_()


    def starify_bbs(self):
        """Adds selected listings from BBS results page
        to the 'Starred Results' listing page.
        """

        selected_rows = []
        row_items = []
        for i in range(self.bbsResultsTable.rowCount()):
            for j in range(self.bbsResultsTable.columnCount()):
                item = self.bbsResultsTable.item(i, j)
                if item.isSelected() and i not in selected_rows:
                    selected_rows.append(i)
                    items = []
                    for k in range(self.bbsResultsTable.columnCount()):
                        items.append(self.bbsResultsTable.item(i, k).text())
                    items.append("BizBuySell.com")
                    row_items.append(items)

        cols = ("Listing Title", "Tagline", "Cash Flow", "Description", \
            "Score", "URL", "Source")
        df = pd.DataFrame(row_items, columns=cols)
        self.add_to_sr(df)


    def starify_crosssite(self):
        """Adds selected listings from Cross-Site results page
        to the 'Starred Results' listing page.
        """

        selected_rows = []
        row_items = []
        for i in range(self.csResultsTable.rowCount()):
            for j in range(self.csResultsTable.columnCount()):
                item = self.csResultsTable.item(i, j)
                if item.isSelected() and i not in selected_rows:
                    selected_rows.append(i)
                    items = [self.csResultsTable.item(i, k).text() for \
                        k in range(self.csResultsTable.columnCount())]
                    row_items.append(items)

        cols = ("Listing Title", "Tagline", "Cash Flow", "Description", \
            "Score", "URL", "Source")
        df = pd.DataFrame(row_items, columns=cols)
        self.add_to_sr(df)


    def starify_mt(self):
        """Adds selected listings from MT results page
        to the 'Starred Results' listing page.
        """

        selected_rows = []
        row_items = []
        for i in range(self.mtResultsTable.rowCount()):
            for j in range(self.mtResultsTable.columnCount()):
                item = self.mtResultsTable.item(i, j)
                if item.isSelected() and i not in selected_rows:
                    selected_rows.append(i)
                    items = []
                    for k in range(2):
                        items.append(self.mtResultsTable.item(i, k).text())
                    items.append("(No Cash Flow)")
                    for k in range(2, 5):
                        items.append(self.mtResultsTable.item(i, k).text())
                    items.append("MergerTech.com")
                    row_items.append(items)

        cols = ("Listing Title", "Tagline", "Cash Flow", "Description", \
            "Score", "URL", "Source")
        df = pd.DataFrame(row_items, columns=cols)
        self.add_to_sr(df)


    def starify_prev_searches(self):
        """Adds selected listings from previous searches page
        to the 'Starred Results' listing page.
        """
        
        row_count = self.starredResultsTable.rowCount()
        column_count = self.starredResultsTable.columnCount()
        selected_rows = []
        for i in range(row_count):
            for j in range(column_count):
                item = self.starredResultsTable.item(i, j)
                if item.isSelected() and i not in selected_rows:
                    selected_rows.append(i)


    def starify_sb(self):
        """Adds selected listings from SB results page
        to the 'Starred Results' listing page.
        """

        selected_rows = []
        row_items = []
        for i in range(self.sbResultsTable.rowCount()):
            for j in range(self.sbResultsTable.columnCount()):
                item = self.sbResultsTable.item(i, j)
                if item.isSelected() and i not in selected_rows:
                    selected_rows.append(i)
                    items = []
                    items.append(self.sbResultsTable.item(i, 0).text())
                    items.append("(No Tagline)")
                    for k in (3, 5, 6, 7):
                        items.append(self.sbResultsTable.item(i, k).text())
                    items.append("SunbeltNetwork.com")
                    row_items.append(items)

        cols = ("Listing Title", "Tagline", "Cash Flow", "Description", \
            "Score", "URL", "Source")
        df = pd.DataFrame(row_items, columns=cols)
        self.add_to_sr(df)


    def starify_tw(self):
        """Adds selected listings from TW results page
        to the 'Starred Results' listing page.
        """

        selected_rows = []
        row_items = []
        for i in range(self.twResultsTable.rowCount()):
            for j in range(self.twResultsTable.columnCount()):
                item = self.twResultsTable.item(i, j)
                if item.isSelected() and i not in selected_rows:
                    selected_rows.append(i)
                    items = []
                    for k in (0, 1, 3, 5, 7, 8):
                        items.append(self.twResultsTable.item(i, k).text())
                    items.append("TWorld.com")
                    row_items.append(items)

        cols = ("Listing Title", "Tagline", "Cash Flow", "Description", \
            "Score", "URL", "Source")
        df = pd.DataFrame(row_items, columns=cols)
        self.add_to_sr(df)


    def update_crosssite(self):
        self.cross_site_settings = []
        if self.bbsCheckBox.isChecked():
            self.cross_site_settings.append("bbs")
        if self.mtCheckBox.isChecked():
            self.cross_site_settings.append("mt")
        if self.sbCheckBox.isChecked():
            self.cross_site_settings.append("sb")
        if self.twCheckBox.isChecked():
            self.cross_site_settings.append("tw")


    def update_urlbar(self, q):
        self.urlBar.setText(q.toString())
        self.urlBar.setCursorPosition(0)
        self.backButton.setEnabled(True)


    def update_keywords(self):
        pos_words = self.editPosWords.toPlainText()
        neg_words = self.editNegWords.toPlainText()
        self.edited_pos_keywords = pos_words.split(", ")
        self.edited_neg_keywords = neg_words.split(", ")


    def view_starred_results(self):
        self.populate_starred_results()
        self.totalResultsSR.setText(str(self.starredResultsTable.rowCount()))
        self.stackedWidget.setCurrentIndex(4)
        self.actionExport.setDisabled(False)


    def visit_website(self, url):
        count = self.browserTabs.count()
        if "bizbuysell" in url:
            title = "BizBuySell.com"
        elif "mergertech" in url:
            title = "MergerTech.com"
        elif "sunbeltnetwork" in url:
            title = "SunbeltNetwork.com"
        elif "tworld" in url:
            title = "TWorld.com"

        if count == 1:
            self.webEngineView_1.setUrl(QtCore.QUrl(url))
            self.newTab = QtWidgets.QWidget()
            self.newTab.setObjectName("newTab")
            self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.newTab)
            self.webEngineView.setGeometry(QtCore.QRect(0, 0, 761, 371))
            self.page_view = WebEnginePage(self.webEngineView)
            self.webEngineView.setPage(self.page_view)
            self.webEngineView.setMouseTracking(True)
            self.webEngineView.setUrl(QtCore.QUrl("https://www.google.com/"))
            self.webEngineView.setZoomFactor(0.8)
            self.webEngineView.setObjectName("webEngineView")
            self.browserTabs.addTab(self.newTab, "New Tab")
            appname = "BrokeredDealEvaluator"
            self.browserTabs.setTabText(self.browserTabs.indexOf(self.newTab),\
                QtCore.QCoreApplication.translate(appname, "New Tab"))

            self.browserTabs.setCurrentIndex(0)
            
        else:
            if hasattr(self, "newTab"):
                name = "tab" + str(count)
                web_name = "webEngineView_" + str(count)
                setattr(self, name, QtWidgets.QWidget())
                getattr(self, name).setObjectName(name)
                setattr(self, web_name, \
                    QtWebEngineWidgets.QWebEngineView(getattr(self, name)))

                setattr(self, "page_view" + str(count), \
                    WebEnginePage(getattr(self, web_name)))
                getattr(self, web_name).setPage(getattr(self, \
                    "page_view" + str(count)))
                dimensions = QtCore.QRect(0, 0, 761, 371)
                getattr(self, web_name).setGeometry(dimensions)
                getattr(self, web_name).setMouseTracking(True)
                getattr(self, web_name).setUrl(QtCore.QUrl(url))
                getattr(self, web_name).setZoomFactor(0.8)
                getattr(self, web_name).setObjectName(\
                    "webEngineView" + str(count))
                self.browserTabs.addTab(getattr(self, name), title)
                self.browserTabs.setCurrentIndex(count)

        self.actionExport.setDisabled(True)
        self.urlBar.setText(url)
        self.stackedWidget.setCurrentIndex(16)


    def webbrowser_button(self, button):
        """Idx is the new tab of the Fake Chrome browser chosen.
        This method sets the URL Bar text accordingly.
        """
        idx = self.browserTabs.currentIndex() + 1
        if idx != self.browserTabs.count():
            engine = getattr(self, "webEngineView_" + str(idx))
        else:
            engine = self.webEngineView.url()

        if button == "back":
            engine.back()
            self.forwardButton.setEnabled(True)
        elif button == "forward":
            engine.forward()


    def retranslateUi(self, BrokeredDealEvaluator):
        """Sets translatable text; Adds text to labels;
        Sets Status Tip for each item.
        """
        _translate = QtCore.QCoreApplication.translate
        appname = "BrokeredDealEvaluator"
        returntext = "Return to Start"
        BrokeredDealEvaluator.setWindowTitle(_translate(appname, \
            "Brokered Deal Evaluator"))
        BrokeredDealEvaluator.setWhatsThis(_translate(appname, \
            "Web-scraping tool for combing through Private Equity " + \
            "listings and scoring them based on a keyword algorithm."))
        

        # Home Page
        self.exitButton.setStatusTip(_translate(appname, \
            "Close the application."))
        self.exitButton.setText(_translate(appname, "Exit Program"))
        self.whichsite.setText(_translate(appname, \
            "Which site should we search through?"))
        self.bbsOption_2.setText(_translate(appname, \
            "           BizBuySell"))
        self.mtOption_2.setText(_translate(appname, \
            "         MergerTech"))
        self.sbOption_2.setText(_translate(appname, \
            "      SunbeltNetwork"))
        self.twOption_2.setText(_translate(appname, \
            "          Transworld"))
        self.bySiteSubmit.setStatusTip(_translate(appname, \
            "Search through selected sites."))
        self.bySiteSubmit.setText(_translate(appname, "Go"))
        self.label_7.setText(_translate(appname, \
            "Check for new deals across all sites:"))
        self.label_8.setText(_translate(appname, "Days since last"))
        self.label_9.setText(_translate(appname, "cross-site search:"))
        self.label_10.setText(_translate(appname, \
            "Check for new deals by site:"))
        self.label_11.setText(_translate(appname, \
            "Display                  listings with a score above:"))
        self.scrapeAllSubmit.setStatusTip(_translate(appname, \
            "Search through all sites."))
        self.scrapeAllSubmit.setText(_translate(appname, "Go"))
        self.newOrAll.setItemText(0, _translate(appname, "new"))
        self.newOrAll.setItemText(1, _translate(appname, "all"))
        
        # How Does It Work Page
        with open("appbin/hdiw.html", "r") as f:
            hdiw_string = f.read()
        self.howDoesItWork.setHtml(_translate(appname, hdiw_string))
        self.returnToStart_1.setText(_translate(appname, returntext))
        
        # Licenses Page
        with open("appbin/license.html", "r") as f:
            license_string = f.read()
        self.licenseScript.setHtml(_translate(appname, license_string))
        self.returnToStart_2.setText(_translate(appname, returntext))
        
        # Previous Scrapes Table
        prevScrapesHeader = self.prevScrapesTable.horizontalHeader()
        prevScrapesHeader.setSectionResizeMode(6, \
            QtWidgets.QHeaderView.Stretch)
        for n in (0, 2, 6, 7):
            prevScrapesHeader.setSectionResizeMode(n, \
                QtWidgets.QHeaderView.ResizeToContents)

        self.prevScrapesHeader.setText(_translate(appname, "Previous Scrapes"))
        cols = ("Listing Title", "Tagline", "Cash Flow", "Description", \
            "Score", "URL", "Source", "Scrape Date")
        for i, col in enumerate(cols):
            item = self.prevScrapesTable.horizontalHeaderItem(i)
            item.setText(_translate(appname, col))

        self.mostRecentLabel.setText(_translate(appname, \
            "Most recent cross-site scrape:"))
        path = os.path.dirname(sys.modules[__name__].__file__)
        conn = sqlite3.connect("appbin/past_scrapes.db")
        c = conn.cursor()
        c.execute("SELECT MAX(scrape_date) FROM scrape_history")
        exists = c.fetchone()
        conn.commit()
        conn.close()
        if exists:
            self.lastScrapeDate.setText(_translate(appname, exists[0]))
        else:
            self.lastScrapeDate.setText(_translate(appname, "None"))

        self.returnToStart_3.setText(_translate(appname, returntext))
        self.totalResults.setText(_translate(appname, "Total results:"))
        self.viewBySite.setText(_translate(appname, \
            "View previous scrapes by individual site:"))
        self.allOption.setText(_translate(appname, \
            "                All Sites"))
        self.bbsOption.setText(_translate(appname, \
            "          BizBuySell.com"))
        self.mtOption.setText(_translate(appname, \
            "        MergerTech.com"))
        self.sbOption.setText(_translate(appname, \
            "     SunbeltNetwork.com"))
        self.twOption.setText(_translate(appname, \
            "        Transworld.com"))
        self.viewBySiteButton.setText(_translate(appname, "Go"))
        
        # Starred Results Table
        self.starredResultsHeader.setText(_translate(appname, \
            "Starred Results"))
        self.totalResults_2.setText(_translate(appname, "Total results:"))
        self.totalResultsSR.setText(_translate(appname, "0"))
        
        cols = ("Listing Title", "Tagline", "Cash Flow", "Description", \
            "Score", "URL", "Source", "Date Added")
        for i, col in enumerate(cols):
            item = self.starredResultsTable.horizontalHeaderItem(i)
            item.setText(_translate(appname, col))

        self.returnToStart_4.setText(_translate(appname, returntext))
        self.withSelectedResults.setText(_translate(appname, \
            "With selected results:"))
        self.exportToXL.setText(_translate(appname, \
            "Export to Spreadsheet"))
        self.removeFromSR.setText(_translate(appname, \
            "Remove from Starred Results"))
        self.followURL.setText(_translate(appname, "Follow URL"))
        
        # Keywords Page
        self.keywordsHeader.setText(_translate(appname, \
            "Keywords used in Scoring Algorithm"))
        self.label_41.setText(_translate(appname, \
            "These are the keywords being used to evaluate listings," + \
            " based on what type of equity"))
        self.label_42.setText(_translate(appname, \
            "the company is looking for, and/or which types of " + \
            "businesses are likely to sell to us. If"))
        self.label_43.setText(_translate(appname, \
            "these keywords are found anywhere in the listing's title," + \
            " tagline, or description, positive"))
        self.label_44.setText(_translate(appname, \
            "or negative points will be awarded accordingly. Common " + \
            "misspellings and misused"))
        self.label_45.setText(_translate(appname, \
            "words are also included because they still appear in " + \
            "listings. Even if the inclusion of"))
        self.label_46.setText(_translate(appname, \
            "these mistakes in a listing is (in and of itself) a faux" + \
            " pas, such errors are not met with"))
        self.label_47.setText(_translate(appname, \
            "further penalty. No points are given if a keyword is " + \
            "found inside of another word."))
        self.label_49.setText(_translate(appname, \
            "To add or remove keywords, visit"))
        self.label_84.setText(_translate(appname, \
            "Scoring Algorithm → Edit."))
        self.positiveHeader.setText(_translate(appname, "Positive"))
        self.negativeHeader.setText(_translate(appname, "Negative"))
        with open("appbin/pos_words.html", "r") as f:
            pos_words_string = f.read()
        self.positiveWords.setHtml(_translate(appname, pos_words_string))
        with open("appbin/neg_words.html", "r") as f:
            neg_words_string = f.read()
        self.negativeWords.setHtml(_translate(appname, neg_words_string))
        self.returnToStart_5.setText(_translate(appname, returntext))
        
        # Edit Keywords Page
        self.editKeywordsHeader.setText(_translate(appname, \
            "Edit Keywords used in Scoring Algorithm"))
        self.returnToStart_6.setText(_translate(appname, returntext))
        self.label_52.setText(_translate(appname, \
            "To temporarily edit the keyword list used in the scoring" + \
            " algorithm, simply"))
        self.label_53.setText(_translate(appname, \
            "make any changes to the two lists below, and click " + \
            "submit. This will"))
        self.label_54.setText(_translate(appname, \
            "change the original code, nor will it update the lists " + \
            "on the Scoring Algorithm"))
        self.label_55.setText(_translate(appname, \
            "→ Keywords page. Instead, it creates a temporary new " + \
            "scoring function that"))
        self.label_56.setText(_translate(appname, "not"))
        self.label_57.setText(_translate(appname, \
            "can be used until you exit this program. Rules for a " + \
            "successful keyword list:"))
        self.label_61.setText(_translate(appname, \
            "1. Write in all lowercase."))
        self.negativeHeader_2.setText(_translate(appname, "Negative"))
        self.positiveHeader_2.setText(_translate(appname, "Positive"))
        self.label_62.setText(_translate(appname, \
            "2. Include common misspellings."))
        self.label_63.setText(_translate(appname, \
            "3. Repeat words for more points."))
        self.label_64.setText(_translate(appname, \
            "4. Separate entries with \", \""))
        self.editPosWords.setPlainText(_translate(appname, \
            "recurring revenue, repeat revenue, b2b, b2b service, " + \
            "business-to-business, service, customer retention, " + \
            "retire, retiring, stepping down, retirement"))
        self.editNegWords.setPlainText(_translate(appname, \
            "restaurant, gas station, minority-owned, minority owned," + \
            " minority owner, woman-owned, women-owned, woman owned, " + \
            "women owned, woman owner, women owner, veteran-owned, " + \
            "veteran owned, veteran owner, convenience store, cafe, " + \
            "eatery, dining establishment, bistro, diner, bar, grill," + \
            " pub, service-disabled, francise, franchisor, franciser," + \
            " franchised, francize, franchizor, franchizer, franchized," + \
            " oil field, oilfield, swimming pool"))
        self.editKeywordsSubmit.setText(_translate(appname, "Submit"))
        
        # Cross-site Settings Page
        self.crossSiteSubheading.setText(_translate(appname, \
            "Full Cross-Site Scrape"))
        self.parameter_header_3.setText(_translate(appname, \
            "Search Parameter Settings:"))
        self.updateSettings.setText(_translate(appname, \
            "Update Settings"))
        self.bbsCheckBox.setText(_translate(appname, \
            "         BizBuySell.com"))
        self.label_78.setText(_translate(appname, \
            "Sites to include:"))
        self.mtCheckBox.setText(_translate(appname, \
            "       MergerTech.com"))
        self.sbCheckBox.setText(_translate(appname, \
            "    SunbeltNetwork.com"))
        self.twCheckBox.setText(_translate(appname, \
            "       Transworld.com"))
        self.label_80.setText(_translate(appname, "Updating the " + \
            "settings here will only change them temporarily;"))
        self.label_81.setText(_translate(appname, \
            "they will be reverted back when you close this application."))
        self.returnToStart_9.setText(_translate(appname, returntext))
        
        # Website Information Page
        self.tabWidget.setStatusTip(_translate(appname, \
            "Open BizBuySell.com in browser window."))
        self.bbsVisitWebsite.setText(_translate(appname, \
            "   Visit Website"))
        with open("appbin/bbs_desc.html", "r") as f:
            bbs_desc_string = f.read()
        self.bbsDesc.setHtml(_translate(appname, bbs_desc_string))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.BizBuySell),\
            _translate(appname, "BizBuySell"))

        self.mtVisitWebsite.setStatusTip(_translate(appname, \
            "Open MergerTech.com in browser window."))
        self.mtVisitWebsite.setText(_translate(appname, \
            "   Visit Website"))
        with open("appbin/mt_desc.html", "r") as f:
            mt_desc_string = f.read()
        self.mtDesc.setHtml(_translate(appname, mt_desc_string))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MergerTech),\
            _translate(appname, "MergerTech"))

        self.sbVisitWebsite.setStatusTip(_translate(appname, \
            "Open SunbeltNetwork.com in browser window."))
        self.sbVisitWebsite.setText(_translate(appname, \
            "   Visit Website"))
        with open("appbin/sb_desc.html", "r") as f:
            sb_desc_string = f.read()
        self.sbDesc.setHtml(_translate(appname, sb_desc_string))     
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Sunbelt),\
            _translate(appname, "Sunbelt"))

        self.twVisitWebsite.setStatusTip(_translate(appname, \
            "Open TWorld.com in browser window."))
        self.twVisitWebsite.setText(_translate(appname, \
            "   Visit Website"))
        with open("appbin/tw_desc.html", "r") as f:
            tw_desc_string = f.read()
        self.twDesc.setHtml(_translate(appname, tw_desc_string))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TWorld),\
            _translate(appname, "Transworld"))

        self.label_82.setText(_translate(appname, \
            "Information on Connected Search Sites"))
        self.returnToStart_10.setText(_translate(appname, returntext))

        # How to Use Page
        self.howToUseHeader.setText(_translate(appname, \
            "How to Use this Application"))
        with open("appbin/instructions.html", "r") as f:
            instructions_string = f.read()
        self.instructionsText.setHtml(_translate(appname, instructions_string))
        self.returnToStart_11.setText(_translate(appname, returntext))
        
        # Send Feedback Page
        self.sendFeedbackHeader.setText(_translate(appname, \
            "Send Feedback to Developer"))
        self.label_86.setText(_translate(appname, \
            "To send feedback over email to the software developer,"))
        self.label_87.setText(_translate(appname, \
            " please include your personal email address here."))
        self.label_88.setText(_translate(appname, \
            "Don't worry, this information is stored only in your"))
        self.label_89.setText(_translate(appname, \
            "message to the developer. It vanishes after you exit."))
        self.yourEmail.setText(_translate(appname, "Your email address:"))
        self.yourTopic.setText(_translate(appname, "Feedback topic:"))
        self.yourMessage.setText(_translate(appname, "Your message:"))
        self.sendFeedback.setText(_translate(appname, "Send Feedback"))
        self.returnToStart_12.setText(_translate(appname, returntext))
        
        ###################### RESULTS PAGES ######################

        # BBS Results Page
        self.bbsListingsHeader.setText(_translate(appname, \
            "BizBuySell.com Listings"))
        self.label_2.setText(_translate(appname, \
            "Choose state(s) to search through:"))
        self.statesBox.setItemText(0, _translate(appname, "All"))
        self.bbsSubmit.setText(_translate(appname, "Submit"))
        self.returnToStart_13.setText(_translate(appname, returntext))
        
        cols = ("Listing Title", "Tagline", "Cash Flow", "Description", \
            "Score", "URL")
        for i, col in enumerate(cols):
            item = self.bbsResultsTable.horizontalHeaderItem(i)
            item.setText(_translate(appname, col))

        from sys import platform
        if platform == "darwin":
            self.selectInstructions.setText(_translate(appname, \
                "To select multiple results: ⌘ + Click"))
        else:
            self.selectInstructions.setText(_translate(appname, \
                "To select multiple results: Shift + Click"))
        self.numberOfResults.setText(_translate(appname, \
            "Number of Results:"))
        self.bbsResultsCount.setText(_translate(appname, "0"))
        self.exportToXL_2.setStatusTip(_translate(appname, \
            "Export results to Excel Spreadsheet."))
        self.exportToXL_2.setText(_translate(appname, \
            "Export to Spreadsheet"))
        self.label_35.setText(_translate(appname, \
            "With selected results:"))
        self.addToSR_2.setStatusTip(_translate(appname, \
            "Add selected listing(s) to your starred results."))
        self.addToSR_2.setText(_translate(appname, \
            "Add to Starred Results"))
        self.followURL_2.setStatusTip(_translate(appname, \
            "Open listing URL in web browser."))
        self.followURL_2.setText(_translate(appname, "Follow URL"))
        
        # MT Results Page
        self.mergerTechHeader.setText(_translate(appname, \
            "MergerTech.com Listings"))
        self.returnToStart_14.setText(_translate(appname, returntext))
        
        cols = ("Listing Title", "Tagline", "Description", "Score", \
            "Contact Email")
        for i, col in enumerate(cols):
            item = self.mtResultsTable.horizontalHeaderItem(i)
            item.setText(_translate(appname, col))

        self.label_6.setText(_translate(appname, \
            "Note: MergerTech.com only offers a few listings"))
        self.label_37.setText(_translate(appname, \
            "at a time, you cannot search by state."))
        from sys import platform
        if platform == "darwin":
            self.selectInstructions_2.setText(_translate(appname, \
                "To select multiple results: ⌘ + Click"))
        else:
            self.selectInstructions_2.setText(_translate(appname, \
                "To select multiple results: Shift + Click"))
        self.numberOfResults_2.setText(_translate(appname, \
            "Number of Results:"))
        self.mtResultsCount.setText(_translate(appname, "0"))
        self.exportToXL_3.setWhatsThis(_translate(appname, \
            "Export results to Excel Spreadsheet."))
        self.exportToXL_3.setText(_translate(appname, \
            "Export to Spreadsheet"))
        self.label_36.setText(_translate(appname, \
            "With selected results:"))
        self.addToSR_3.setStatusTip(_translate(appname, \
            "Add selected listing(s) to your starred results."))
        self.addToSR_3.setText(_translate(appname, \
            "Add to Starred Results"))


        # SB Results Page
        self.sunbeltHeader.setText(_translate(appname, \
            "SunbeltNetwork.com Listings"))
        self.label_4.setText(_translate(appname, \
            "Choose state(s) to search through:"))
        self.returnToStart_15.setText(_translate(appname, returntext))
        self.sbSubmit.setText(_translate(appname, "Submit"))
        
        cols = ("Listing Title", "Price", "Revenue", "Cash Flow", \
            "Location", "Description", "Score", "URL")
        for i, col in enumerate(cols):
            item = self.sbResultsTable.horizontalHeaderItem(i)
            item.setText(_translate(appname, col))
        
        self.statesBox_2.setItemText(0, _translate(appname, "All"))
        from sys import platform
        if platform == "darwin":
            self.selectInstructions_3.setText(_translate(appname, \
                "To select multiple results: ⌘ + Click"))
        else:
            self.selectInstructions_3.setText(_translate(appname, \
                "To select multiple results: Shift + Click"))

        self.numberOfResults_3.setText(_translate(appname, \
            "Number of Results:"))
        row_count = str(self.sbResultsTable.rowCount())
        self.sbResultsCount.setText(_translate(appname, row_count))
        self.addToSR_4.setStatusTip(_translate(appname, \
            "Add selected listing(s) to your starred results."))
        self.addToSR_4.setText(_translate(appname, \
            "Add to Starred Results"))
        self.followURL_4.setStatusTip(_translate(appname, \
            "Follow listing's URL in a browser."))
        self.followURL_4.setText(_translate(appname, "Follow URL"))
        self.label_38.setText(_translate(appname, \
            "With selected results:"))
        self.exportToXL_4.setStatusTip(_translate(appname, \
            "Export results to an Excel Spreadsheet."))
        self.exportToXL_4.setText(_translate(appname, \
            "Export to Spreadsheet"))


        # TW Results Page
        self.tworldHeader.setText(_translate(appname, \
            "TWorld.com Listings"))
        self.label_5.setText(_translate(appname, \
            "Choose state(s) to search through:"))
        self.returnToStart_16.setText(_translate(appname, returntext))
        self.twSubmit.setText(_translate(appname, "Submit"))
        
        cols = ("Listing Title", "Tagline", "Price", \
            "Disc. Earnings", "Location", "Description", \
            "Contact Email", "Score", "URL")
        for i, col in enumerate(cols):
            item = self.twResultsTable.horizontalHeaderItem(i)
            item.setText(_translate(appname, col))
        
        self.statesBox_3.setItemText(0, _translate(appname, "All"))
        from sys import platform
        if platform == "darwin":
            self.selectInstructions_4.setText(_translate(appname, \
                "To select multiple results: ⌘ + Click"))
        else:
            self.selectInstructions_4.setText(_translate(appname, \
                "To select multiple results: Shift + Click"))

        self.numberOfResults_4.setText(_translate(appname, \
            "Number of Results:"))
        row_count = str(self.twResultsTable.rowCount())
        self.twResultsCount.setText(_translate(appname, row_count))
        self.addToSR_5.setStatusTip(_translate(appname, \
            "Add selected listing(s) to your starred results."))
        self.addToSR_5.setText(_translate(appname, \
            "Add to Starred Results"))
        self.followURL_5.setStatusTip(_translate(appname, \
            "Follow listing's URL in a browser."))
        self.followURL_5.setText(_translate(appname, "Follow URL"))
        self.label_39.setText(_translate(appname, \
            "With selected results:"))
        self.exportToXL_5.setStatusTip(_translate(appname, \
            "Export results to an Excel Spreadsheet."))
        self.exportToXL_5.setText(_translate(appname, \
            "Export to Spreadsheet"))


        # Cross-Site Results Page
        self.crossSiteDataHeader.setText(_translate(appname, \
            "Cross-Site Data Scrape"))
        self.label_13.setText(_translate(appname, \
            "Searching for new results across three sites..."))
        self.label_14.setText(_translate(appname, \
            "Number of          new search listings:"))
        self.label_15.setText(_translate(appname, "total"))
        self.label_16.setText(_translate(appname, \
            "Number of         results scoring above"))
        self.label_17.setText(_translate(appname, "new"))
        from sys import platform
        if platform == "darwin":
            self.selectInstructions_5.setText(_translate(appname, \
                "To select multiple results: ⌘ + Click"))
        else:
            self.selectInstructions_5.setText(_translate(appname, \
                "To select multiple results: Shift + Click"))
        self.minScoreLabel.setText(_translate(appname, "2:"))

        cols = ("Listing Title", "Tagline", "Cash Flow", \
            "Description", "Score", "URL", "Source")
        for i, col in enumerate(cols):
            item = self.csResultsTable.horizontalHeaderItem(i)
            item.setText(_translate(appname, col))
        
        self.addToSR_6.setStatusTip(_translate(appname, \
            "Add selected listing(s) to your starred results."))
        self.addToSR_6.setText(_translate(appname, \
            "Add to Starred Results"))
        self.followURL_6.setStatusTip(_translate(appname, \
            "Follow listing's URL in a browser."))
        self.followURL_6.setText(_translate(appname, "Follow URL"))
        self.label_40.setText(_translate(appname, "With selected results:"))
        self.exportToXL_6.setStatusTip(_translate(appname, \
            "Export results to an Excel Spreadsheet."))
        self.exportToXL_6.setText(_translate(appname, \
            "Export to Spreadsheet"))
        from sys import platform
        if platform == "darwin":
            self.selectInstructions_6.setText(_translate(appname, \
                "To select multiple results: ⌘ + Click"))
        else:
            self.selectInstructions.setText(_translate(appname, \
                "To select multiple results: Shift + Click"))
        self.returnToStart_17.setText(_translate(appname, returntext))

        # Web Browser
        self.browserTabs.setTabText(self.browserTabs.indexOf(self.tab1), \
            _translate(appname, "Listing 1"))
        self.returnToStart_18.setText(_translate(appname, "Return to Start"))
        self.urlBar.setPlaceholderText(_translate(appname, "Type URL Here"))
        self.backButton.setStatusTip(_translate(appname, "Go back one page"))
        self.backButton.setText(_translate(appname, "←"))
        self.forwardButton.setStatusTip(_translate(appname, \
            "Return to Last Webpage"))
        self.forwardButton.setText(_translate(appname, "→"))
        self.enterButton.setText(_translate(appname, "Go"))
        self.enterButton.setStatusTip(_translate(appname, "Visit URL"))
        
        # Menu Bar
        self.menuScoring_Algorithm.setTitle(_translate(appname, \
            "Scoring Algorithm"))
        self.menuResults.setTitle(_translate(appname, "Results"))
        self.menuHelp.setTitle(_translate(appname, "Help"))
        self.menuWebsites.setTitle(_translate(appname, "Websites"))
        self.menuEvaluator.setTitle(_translate(appname, "Evaluator"))
        self.actionAppInfo.setText(_translate(appname, "Application Info"))
        self.actionAppInfo.setStatusTip(_translate(appname, \
            "View how the application works."))
        self.actionVersion.setText(_translate(appname, "Version"))
        self.actionVersion.setStatusTip(_translate(appname, \
            "View which version of this application you have."))
        self.actionLicenses.setText(_translate(appname, "Licenses"))
        self.actionLicenses.setStatusTip(_translate(appname, \
            "View license information for the application."))
        self.actionView_Past_Entries.setText(_translate(appname, \
            "Previous Scrapes"))
        self.actionView_Past_Entries.setStatusTip(_translate(appname, \
            "View results from previous scrapes."))
        self.actionStarred_Results.setText(_translate(appname, \
            "Starred Results"))
        self.actionStarred_Results.setStatusTip(_translate(appname, \
            "View your starred results."))
        self.actionExport.setText(_translate(appname, "Export"))
        self.actionExport.setStatusTip(_translate(appname, \
            "Export selected results."))
        self.actionExport.setShortcut(_translate(appname, "Meta+E"))
        self.actionClear_Records.setText(_translate(appname, "Clear Records"))
        self.actionClear_Records.setStatusTip(_translate(appname, \
            "Delete all starred results and previous scrapes."))
        self.actionView_Keywords.setText(_translate(appname, "Keywords"))
        self.actionView_Keywords.setStatusTip(_translate(appname, \
            "View keywords used in scoring algorithm."))
        self.actionHow_to_Use.setText(_translate(appname, "How to Use"))
        self.actionHow_to_Use.setStatusTip(_translate(appname, \
            "View instructions for how to use this application."))
        self.actionSend_Feedback.setText(_translate(appname, \
            "Send Feedback"))
        self.actionSend_Feedback.setStatusTip(_translate(appname, \
            "Send feedback to application developer."))
        self.actionSend_Feedback.setShortcut(_translate(appname, "Meta+F"))

        self.actionFull_Scrape.setText(_translate(appname, "Full Scrape"))
        self.actionFull_Scrape.setStatusTip(_translate(appname, \
            "View settings for cross-site scrape."))
        self.actionEditKeywords.setText(_translate(appname, "Edit"))
        self.actionEditKeywords.setStatusTip(_translate(appname, \
            "Edit keywords used in scoring algorithm."))
        self.actionEnter.setShortcut(_translate(appname, "Enter"))
    
        self.actionHome_Page.setText(_translate(appname, "Home Page"))
        self.actionHome_Page.setShortcut(_translate(appname, "Meta+H"))
        self.actionInformation.setText(_translate(appname, "Information"))
        self.actionInformation.setStatusTip(_translate(appname, \
            "View information on each search site."))

class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        pass

from PyQt5 import QtWebEngineWidgets
from appbin import images_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    path = os.path.dirname(sys.modules[__name__].__file__)
    app.setWindowIcon(QtGui.QIcon(os.path.join(path, "wheel.png")))
    BrokeredDealEvaluator = QtWidgets.QMainWindow()

    ui = Ui_BrokeredDealEvaluator()
    ui.setupUi(BrokeredDealEvaluator)
    BrokeredDealEvaluator.show()
    sys.exit(app.exec_())
