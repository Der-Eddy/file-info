#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import hashlib
import datetime
import platform
from tkinter import Tk, Label, Entry, StringVar, filedialog

class Fileinfo:
    def __init__(self, filePath):
        self.file = filePath
        self.getStats()

    def getStats(self):
        self.name = os.path.basename(self.file)
        self.stats = os.stat(self.file)
        self.size = self.stats.st_size
        self.KBSize = round(self.size / 1024, 3)
        self.MBSize = round(self.size / 1024 / 1024, 3)
        self.ATime = datetime.datetime.fromtimestamp(self.stats.st_atime)
        self.MTime = datetime.datetime.fromtimestamp(self.stats.st_mtime)
        self.CTime = datetime.datetime.fromtimestamp(self.stats.st_ctime)
        self.getHashes()
        self.initGUI()

    def getHashes(self):
        self.MD5 = self.getHash(hashlib.md5())
        self.SHA1 = self.getHash(hashlib.sha1())
        self.SHA256 = self.getHash(hashlib.sha256())
        self.SHA512 = self.getHash(hashlib.sha512())

    def getHash(self, hashAlgorithm=hashlib.sha256()):
        blocksize = 65536
        algo = hashAlgorithm
        with open(self.file, 'rb') as file:
            buffer = file.read(blocksize)
            while len(buffer) > 0:
                algo.update(buffer)
                buffer = file.read(blocksize)
        return algo.hexdigest()

    def makeReadable(self, format='GUI'):
        formatDate = '%d.%m.%y %H:%M:%S'
        if format == 'Console':
            self.name = f'Name: {self.name}'
            self.size = f'Size: {self.MBSize} MB ({self.size} Bytes)'
            self.ATime = f'Last Access: {self.ATime:{formatDate}}'
            self.MTime = f'Last Modified: {self.MTime:{formatDate}}'
            self.CTime = f'Created at: {self.CTime:{formatDate}}'
            self.MD5 = f'MD5: {self.MD5}'
            self.SHA1 = f'SHA1: {self.SHA1}'
            self.SHA256 = f'SHA256: {self.SHA256}'
            self.SHA512 = f'SHA512: {self.SHA512}'
        elif format == 'GUI':
            self.size = f'{self.MBSize} MB ({self.size} Bytes)'
            self.ATime = f'{self.ATime:{formatDate}}'
            self.MTime = f'{self.MTime:{formatDate}}'
            self.CTime = f'{self.CTime:{formatDate}}'

    def consoleOutput(self):
        self.makeReadable('Console')
        entryList = [self.name, self.size, self.ATime, self.MTime, self.CTime, \
                     self.MD5, self.SHA1, self.SHA256, self.SHA512]
        for entry in entryList:
            print(entry)
        info.holdPrompt()

    def initGUI(self):
        #Needed for filedialog.askopenfilename()
        self.app = Tk()

    def GUIOutput(self):
        self.makeReadable('GUI')
        self.app.geometry('900x200')
        self.app.wm_title(f'{self.name} - {self.SHA256}')

        labelList = ['Name: ', 'Size: ', 'Last Access: ', 'Last Modified: ', \
                      'Created at: ', 'MD5: ', 'SHA1: ', 'SHA256: ', 'SHA512: ']
        for i, labelName in enumerate(labelList, start=0):
            Label(self.app, text=labelName).grid(row=i, sticky='W')

        entryList = [self.name, self.size, self.ATime, self.MTime, self.CTime, \
                     self.MD5, self.SHA1, self.SHA256, self.SHA512]

        for i, entry in enumerate(entryList, start=0):
            tmpEntry = Entry(self.app, width=130)
            tmpEntry.insert(0, entry)
            tmpEntry.configure(state='readonly') #for some reason Tkinter doesn't allow to insert to a readonly Entry
            tmpEntry.grid(row=i, column=1)

        self.app.mainloop()

    @staticmethod
    def holdPrompt():
        #A windows thing
        if platform.system() == 'Windows':
            input("Press enter to close the program")

if __name__ == '__main__':
    try:
        file = sys.argv[1]
    except IndexError:
        #root.withdraw()
        file = filedialog.askopenfilename()
        #file = 'C:\\Users\\Eduard\\Desktop\\GifCam.exe'

    info = Fileinfo(file)

    info.GUIOutput()
    '''
    try:
        if sys.argv[2].lower == 'nogui' or sys.argv[2].lower == '--nogui':
            info.consoleOutput()
        else:
            info.GUIOutput()
    except IndexError:
        info.GUIOutput()
    '''
