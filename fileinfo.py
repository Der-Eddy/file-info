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
        print(self.name)
        print(self.size)
        print(self.ATime)
        print(self.MTime)
        print(self.CTime)
        print(self.MD5)
        print(self.SHA1)
        print(self.SHA256)
        print(self.SHA512)
        info.holdPrompt()

    def initGUI(self):
        #Needed for filedialog.askopenfilename()
        self.app = Tk()

    def GUIOutput(self):
        self.makeReadable('GUI')
        self.app.geometry('700x200')
        self.app.wm_title(f'{self.name} - {self.SHA256}')

        labelNames = ['Name: ', 'Size: ', 'Last Access: ', 'Last Modified: ', \
                      'Created at: ', 'MD5: ', 'SHA1: ', 'SHA256: ', 'SHA512: ']
        for i, labelName in enumerate(labelNames, start=0):
            Label(self.app, text=labelName).grid(row=i, sticky='W')


        eName1 = Entry(self.app)
        eName1.insert(0, self.name)
        eName1.configure(state='readonly') #for some reason Tkinter doesn't allow to insert to a readonly Entry
        eSize2 = Entry(self.app)
        eSize2.insert(0, self.size)
        eSize2.configure(state='readonly')
        eATime3 = Entry(self.app)
        eATime3.insert(0, self.ATime)
        eATime3.configure(state='readonly')
        eMTime4 = Entry(self.app)
        eMTime4.insert(0, self.MTime)
        eMTime4.configure(state='readonly')
        eCTime5 = Entry(self.app)
        eCTime5.insert(0, self.CTime)
        eCTime5.configure(state='readonly')
        eMD5 = Entry(self.app)
        eMD5.insert(0, self.MD5)
        eMD5.configure(state='readonly')
        eSHA1 = Entry(self.app)
        eSHA1.insert(0, self.SHA1)
        eSHA1.configure(state='readonly')
        eSHA256 = Entry(self.app)
        eSHA256.insert(0, self.SHA256)
        eSHA256.configure(state='readonly')
        eSHA512 = Entry(self.app)
        eSHA512.insert(0, self.SHA512)
        eSHA512.configure(state='readonly')

        eName1.grid(row=0, column=1)
        eSize2.grid(row=1, column=1)
        eATime3.grid(row=2, column=1)
        eMTime4.grid(row=3, column=1)
        eCTime5.grid(row=4, column=1)
        eMD5.grid(row=5, column=1)
        eSHA1.grid(row=6, column=1)
        eSHA256.grid(row=7, column=1)
        eSHA512.grid(row=8, column=1)
        self.app.grid_columnconfigure(1, minsize=100)

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
        #file = filedialog.askopenfilename()
        file = 'C:\\Users\\Eduard\\Desktop\\GifCam.exe'

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
