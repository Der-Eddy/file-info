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
            self.CTime = f'Created: {self.CTime:{formatDate}}'
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
        #self.app.geometry('800x300')
        self.app.wm_title(f'{self.name} - {self.SHA256}')

        labelName=StringVar()
        labelName.set('Name:')
        labelFirst=Label(self.app, textvariable=labelName, height=4)
        labelFirst.pack(side='left')
        inputName=StringVar(None)
        inputName.set(self.name)
        inputFirst=Entry(self.app,textvariable=inputName,width=50)
        inputFirst.pack(side='left')

        labelSize=StringVar()
        labelSize.set('Size:')
        labelSecond=Label(self.app, textvariable=labelSize, height=4)
        labelSecond.pack(side='left')
        inputSize=StringVar(None)
        inputSize.set(self.size)
        inputSecond=Entry(self.app,textvariable=inputSize,width=50)
        inputSecond.pack(side='left')

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

    info.consoleOutput()
    '''
    try:
        if sys.argv[2].lower == 'nogui' or sys.argv[2].lower == '--nogui':
            info.consoleOutput()
        else:
            info.GUIOutput()
    except IndexError:
        info.GUIOutput()
    '''
