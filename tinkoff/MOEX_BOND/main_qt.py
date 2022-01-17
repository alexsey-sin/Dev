#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QHeaderView, QFileDialog
import json

# from bond import Bond
from threadLoadMOEX import ThreadLoadMOEX


# https://habr.com/ru/company/skillfactory/blog/576912/
# https://dearpygui.readthedocs.io/en/latest/tutorials/first-steps.html

class Win(QtWidgets.QMainWindow):
    cycle = 0
    allTypesBOND = True
    lastItemTypeBond = -1
    progress = 0
    listAllBonds = {}
    bndTableModel = QtGui.QStandardItemModel()

    def __init__(self):
        super(Win, self).__init__()
        self.ui = uic.loadUi('main_form.ui')
        self.ui.show()

        self.ui.progressBar.hide()
        comboTypeBond = self.ui.comboBoxTypeBONDS
        for i in range(6):
            # if i == 0:
            #     comboTypeBond.addItem("Все")
            # else:
            comboTypeBond.addItem(f"Combobox Item {i}")

            item = comboTypeBond.model().item(comboTypeBond.count() - 1, 0)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable
                          | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Checked)  # Unchecked/Checked
            # item.model().itemChanged.connect(self.OnComboItemChanged)

        # comboTypeBond.activated.connect(self.OnAllSelectTypeBONDS)
        self.ui.menuLoadFile.triggered.connect(self.OnMenuLoadFile)
        self.ui.menuSaveFile.triggered.connect(self.OnMenuSaveFile)
        self.ui.menuLoadOfMOEX.triggered.connect(self.OnMenuLoadOfMOEX)
        self.ui.buttonUpdate.pressed.connect(self.OnButtonUpdate)
        self.ui.pushButton.pressed.connect(self.OnPushButton)
        self.ui.checkNominalStart.stateChanged.connect(
            lambda: self.ui.editNominalStart.setEnabled(
                self.ui.checkNominalStart.isChecked()))
        self.ui.checkNominalStop.stateChanged.connect(
            lambda: self.ui.editNominalStop.setEnabled(
                self.ui.checkNominalStop.isChecked()))
        self.ui.checkDateStart.stateChanged.connect(
            lambda: self.ui.dateStart.setEnabled(
                self.ui.checkDateStart.isChecked()))
        self.ui.checkDateStop.stateChanged.connect(
            lambda: self.ui.dateStop.setEnabled(
                self.ui.checkDateStop.isChecked()))
        self.ui.checkBoxTypeBONDS.stateChanged.connect(
            lambda: self.ui.comboBoxTypeBONDS.setEnabled(
                self.ui.checkBoxTypeBONDS.isChecked()))

        col_name = ['Тикер', 'Название', 'Погашение', 'Номинал', 'куп/год',
                    'Купон', 'Тип', 'Дох.%']
        self.bndTableModel = QtGui.QStandardItemModel(parent=app)
        self.bndTableModel.setColumnCount(len(col_name))
        self.bndTableModel.setHorizontalHeaderLabels(col_name)
        
        tbl = self.ui.tableView
        tbl.setModel(self.bndTableModel)
        tbl.setColumnWidth(0, 100)
        tbl.setColumnWidth(1, 200)
        tbl.setColumnWidth(2, 80)
        tbl.setColumnWidth(3, 60)
        tbl.setColumnWidth(4, 60)
        tbl.setColumnWidth(5, 60)
        tbl.setColumnWidth(6, 60)
        tbl.setColumnWidth(7, 60)
        tbl.verticalHeader().setVisible(False)
        tbl.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        tbl.verticalHeader().setDefaultSectionSize(16)

        # tbl.setStyleSheet(
            # 'QTableWidget::item {selection-background-color: darkgray;'
            # 'text-align: center; padding-left: 10px;}')
        # tbl.setStyleSheet('QTableWidget::item {padding-left: 10px}')
        tbl.setStyleSheet('QTableView::item {padding: 10dpx}')
        # QTableView.item padding: 10dpx
        # delegate = AlignDelegate(self.ui.tableView)background-color: yellow; padding-left: 20px; 
        # self.ui.tableView.setItemDelegateForColumn(2, AlignDelegate(self.ui.tableView))
        # self.ui.tableView.setRowHeight(0, 20)
        # self.ui.tableView.horizontalHeader().resizeSection(0, 160)
        # self.ui.statusbar.setStyleSheet('QStatusBar {background: red; border: 1px solid red; border-radius: 3px;}')

    def OnMenuLoadFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Открыть файл', './archive.json')[0]
        try:
            # Bond.LoadFile(fname)
            f = open(fname, 'r', encoding='utf-8')  # "archive.json"
            self.listAllBonds = json.load(f)
            self.statusBar().showMessage(f'Загружено из файла: {len(self.listAllBonds)} бумаг.')
        except Exception as exc:
            self.statusBar().showMessage(f'Ошибка чтения из файла: {exc}')

        if len(self.listAllBonds) > 0:
            self.OutTableView()

    def OnMenuSaveFile(self):
        fname = QFileDialog.getSaveFileName(self, 'Сохранить в файл', './archive.json')[0]
        cnt = len(self.listAllBonds)
        output = json.dumps(self.listAllBonds)
        try:
            # Bond.SaveFile(fname)
            f = open(fname, 'w', encoding='utf-8')
            f.write(output)
            self.statusBar().showMessage(f'Записано в файл: {cnt} бумаг.')
        except Exception as exc:
            self.statusBar().showMessage(f'Ошибка записи в файл: {exc}')

    def OnMenuLoadOfMOEX(self):
        self.thread = QThread()
        self.threadLoadMOEX = ThreadLoadMOEX()
        self.threadLoadMOEX.moveToThread(self.thread)

        self.threadLoadMOEX.int_value.connect(self.OnSignalThreadMOEXInt)
        self.threadLoadMOEX.message_value.connect(self.OnSignalThreadMOEXMessage)
        self.threadLoadMOEX.text_value.connect(self.OnSignalThreadMOEXText)
        self.threadLoadMOEX.dict_value.connect(self.OnSignalThreadMOEXDict)

        self.thread.started.connect(self.threadLoadMOEX.run)
        self.thread.start()

    def OnSignalThreadMOEXInt(self, value):
        if value <= 100:
            self.ui.progressBar.show()
            self.ui.progressBar.setValue(value)

    def OnSignalThreadMOEXMessage(self, text):
        self.statusBar().showMessage(text, 3000)

    def OnSignalThreadMOEXText(self, text):
        self.ui.textEdit.append(text)

    def OnSignalThreadMOEXDict(self, dct):
        self.listAllBonds = dct
        self.OutTableView()
        # for kkk, vvv in dct.items():
        #     self.ui.textEdit.append(f"{kkk}: {vvv['NAME']}; {vvv['MATDATE']}; {vvv['FACEVALUE']}p.; \
        #     {vvv['COUPONFREQUENCY']}; {vvv['COUPONVALUE']}p.; {vvv['TYPE']};")
        # self.ui.textEdit.append(text)

    def OutTableView(self):
        self.bndTableModel.removeRows(0, self.bndTableModel.rowCount())
        # self.listAllBonds
        for sec_id, body in self.listAllBonds.items():
            it_ticker = QtGui.QStandardItem(sec_id)
            it_name = QtGui.QStandardItem(body['NAME'])
            it_matdate = QtGui.QStandardItem(body['MATDATE'])
            it_facevalue = QtGui.QStandardItem(body['FACEVALUE'])
            it_couponfrequency = QtGui.QStandardItem(body['COUPONFREQUENCY'])
            it_couponvalue = QtGui.QStandardItem(body['COUPONVALUE'])
            it_type = QtGui.QStandardItem(body['TYPE'])

            self.bndTableModel.appendRow([it_ticker, it_name, it_matdate, it_facevalue,
                it_couponfrequency, it_couponvalue, it_type])

        # col_name = ['Код', 'Название', 'Погашение', 'Номинал', 'купонов в год', 'Купон', 'Тип облигации', 'Доходность,%']
        # bndTableModel = QtGui.QStandardItemModel(parent=app)
        # bndTableModel.setColumnCount(len(col_name))
        # bndTableModel.setHorizontalHeaderLabels(col_name)
        # item1 = QtGui.QStandardItem('row')
        # item2 = QtGui.QStandardItem('col')
        # item3 = QtGui.QStandardItem('ddd')
        # item4 = QtGui.QStandardItem('sss')
        # item5 = QtGui.QStandardItem('aaa')
        # self.bndTableModel.appendRow([item1, item2, item3, item4, item5])
        
        # bndTableModel.columnWidth(0, 160)
        # bndTableModel.setColumnWidth(5, 20)
        # self.ui.tableView.setModel(bndTableModel)
        # self.ui.tableView.
        # self.ui.tableView.se
        # self.ui.tableView.setModel(bndTableModel)
        # self.ui.tableView.setColumnWidth(0, 160)
        # self.ui.tableView.setColumnCount(3)
        # self.ui.tableView.setHorizontalHeaderLabels(["Header 1", "Header 2", "Header 3"])
        # self.ui.tableView.setRowCount(1)        # и одну строку в таблице

        all_cnt = len(self.listAllBonds)
        view_cnt = all_cnt
        self.statusBar().showMessage(f'Всего: {view_cnt} из {all_cnt}.', 0)

    def OnButtonUpdate(self):
        cnt = 0

        for i in range(self.ui.comboBoxTypeBONDS.count()):
            # item = self.ui.comboBoxTypeBONDS.model().item(0,0)
            if self.ui.comboBoxTypeBONDS.model().item(i, 0).checkState() == QtCore.Qt.Checked:
                cnt += 1

        self.statusBar().showMessage('Выбрано: ' + str(cnt))
        self.OutTableView()

    # Словарь с облигациями будет иметь такую структуру:
    # d_dict = {
    #     'FRU000A101PV5': {
    #         'NAME': "Т5555чи БО-01"
    #         'MATDATE': "jjjj05-23",
    #         'FACEVALUE': "10y0",
    #         'COUPONFREQUENCY': "4",
    #         'COUPONVALUE': "34.9",
    #         'TYPE': "exchvffdds_bond"
    #     }
    #     'RU000A101PV6': {
    #         'NAME': "ТД РКС-Сочи БО-01"
    #         'MATDATE': "2023-05-23",
    #         'FACEVALUE': "1000",
    #         'COUPONFREQUENCY': "4",
    #         'COUPONVALUE': "34.9",
    #         'TYPE': "exchange_bond"
    #     }
    #     ...
    # }

    # def OnCheckNominalStart(self):
    #     # isCheck = self.ui.checkNominalStart.isChecked()
    #     self.ui.editNominalStart.setEnabled(self.ui.checkNominalStart.isChecked())
    #     # if self.ui.checkNominalStart.isChecked() == True:
    #     #     self.ui.editNominalStart.setEnabled(True)
    #     # else:
    #     #     self.ui.editNominalStart.setDisabled(True)
    #     # s = self.ui.comboBoxTypeBONDS.model().item(1,0)
    #     self.statusBar().showMessage(f'{self.ui.checkNominalStart.isChecked()}')

    # def OnComboItemChanged(self, item):
    #     lst = item.text().split()
    #     i = lst[-1]
    #     if self.lastItemTypeBond != i:
    #         print(f'{i}')
    #         self.lastItemTypeBond = i

    def OnPushButton(self):
        # self.ui.tableView.setRowHeight(0, 20)
        
        
        sk = self.ui.comboBoxTypeBONDS.itemText(2)
        self.statusBar().showMessage(sk)
        self.progress += 5
        if self.progress <= 100:
            self.ui.progressBar.show()
            self.ui.progressBar.setValue(self.progress)

    # def OnAllSelectTypeBONDS(self):
    #     self.cycle += 1
    #     self.allTypesBOND = not self.allTypesBOND

    #     c = self.ui.comboBoxTypeBONDS.count()
    #     for i in range(1, self.ui.comboBoxTypeBONDS.count()):
    #         if self.allTypesBOND == True:
    #             self.ui.comboBoxTypeBONDS.model().item(i,0).setCheckState(QtCore.Qt.Checked) #Unchecked/Checked
    #         else:
    #             self.ui.comboBoxTypeBONDS.model().item(i,0).setCheckState(QtCore.Qt.Unchecked) #Unchecked/Checked
    #     self.statusBar().showMessage(f'Изменений: {self.cycle} {c}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Win()
    sys.exit(app.exec_())

# https://overcoder.net/q/1992576/%D1%84%D0%BB%D0%B0%D0%B6%D0%BA%D0%B8-%D0%B2-combobox-%D1%81-%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%D0%BC-pyqt
# https://doc.qt.io/qt-5/qmenu.html


# class CheckableComboBoxItem(QtWidgets.QComboBox.QStandartItem):
# def

# пример:
# from PyQt5 import QtGui, QtCore, QtWidgets
# import sys, os

# # subclass
# class CheckableComboBox(QtWidgets.QComboBox):
# # once there is a checkState set, it is rendered
# # here we assume default Unchecked
# def addItem(self, item):
# super(CheckableComboBox, self).addItem(item)
# item = self.model().item(self.count()-1,0)
# item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
# item.setCheckState(QtCore.Qt.Unchecked)

# def itemChecked(self, index):
# item = self.model().item(i,0)
# return item.checkState() == QtCore.Qt.Checked

# # the basic main()
# app = QtWidgets.QApplication(sys.argv)
# dialog = QtWidgets.QMainWindow()
# mainWidget = QtWidgets.QWidget()
# dialog.setCentralWidget(mainWidget)
# ComboBox = CheckableComboBox(mainWidget)
# for i in range(6):
# ComboBox.addItem("Combobox Item " + str(i))

# dialog.show()
# sys.exit(app.exec_())
