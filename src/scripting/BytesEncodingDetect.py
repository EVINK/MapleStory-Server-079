"""
BytesEncodingDetect - Converted from Java source
Original: scripting/BytesEncodingDetect.java
Package: scripting
"""

from io import IOBase
from pathlib import Path
from socket import socket
from typing import Optional, Any
import os


class BytesEncodingDetect(Encoding):
    """
    Class BytesEncodingDetect
    Extends: Encoding
    """

    def __init__(self):
        self.debug = False
        self.debug = False
        self.GBFreq = new int[94][94]
        self.GBKFreq = new int[126][191]
        self.Big5Freq = new int[94][158]
        self.Big5PFreq = new int[126][191]
        self.EUC_TWFreq = new int[94][94]
        self.KRFreq = new int[94][94]
        self.JPFreq = new int[94][94]
        self.initialize_frequencies()


    def main(self, argc: list) -> None:
        result = BytesEncodingDetect.OTHER
        sinodetector = BytesEncodingDetect()
        for i in range(len(argc)):
            if (argc[i].startswith("http:  # ")) {
                try:
                    result = sinodetector.detectEncoding(URL(argc[i]))
                except MalformedURLException as e:
                    print("Bad URL " + e)
            else:
                if argc[i] == ("-d"):
                    sinodetector.debug = True
                    continue
                result = sinodetector.detectEncoding(File(argc[i]))
            print(BytesEncodingDetect.nicename[result])

    def detectEncoding(self, testurl: Any) -> int:
        rawtext = new byte[10000]
        bytesread = 0
        byteoffset = 0
        guess = BytesEncodingDetect.OTHER
        try:
            chinesestream = None
            for (chinesestream = testurl.openStream(); (bytesread = chinesestream.read(rawtext, byteoffset, len(rawtext) - byteoffset)) > 0; byteoffset += bytesread) {}
            chinesestream.close()
            guess = self.detectEncoding(rawtext)
        except IOError as e:
            print("Error loading or using URL " + e)
            guess = -1
        return guess

    def detectEncoding_testfile(self, testfile: Any) -> int:
        rawtext = new byte[testfile]
        try:
            chinesefile = FileInputStream(testfile)
            chinesefile.read(rawtext)
            chinesefile.close()
        except IOError as e:
            print("Error: " + e)
        return self.detectEncoding(rawtext)

    def detectEncoding_rawtext(self, rawtext: bytes) -> int:
        maxscore = 0
        encoding_guess = BytesEncodingDetect.OTHER
        scores = new int[BytesEncodingDetect.TOTALTYPES]
        scores[BytesEncodingDetect.GB2312] = self.gb2312_probability(rawtext)
        scores[BytesEncodingDetect.GBK] = self.gbk_probability(rawtext)
        scores[BytesEncodingDetect.GB18030] = self.gb18030_probability(rawtext)
        scores[BytesEncodingDetect.HZ] = self.hz_probability(rawtext)
        scores[BytesEncodingDetect.BIG5] = self.big5_probability(rawtext)
        scores[BytesEncodingDetect.CNS11643] = self.euc_tw_probability(rawtext)
        scores[BytesEncodingDetect.ISO2022CN] = self.iso_2022_cn_probability(rawtext)
        scores[BytesEncodingDetect.UTF8] = self.utf8_probability(rawtext)
        scores[BytesEncodingDetect.UNICODE] = self.utf16_probability(rawtext)
        scores[BytesEncodingDetect.EUC_KR] = self.euc_kr_probability(rawtext)
        scores[BytesEncodingDetect.CP949] = self.cp949_probability(rawtext)
        scores[BytesEncodingDetect.JOHAB] = 0
        scores[BytesEncodingDetect.ISO2022KR] = self.iso_2022_kr_probability(rawtext)
        scores[BytesEncodingDetect.ASCII] = self.ascii_probability(rawtext)
        scores[BytesEncodingDetect.SJIS] = self.sjis_probability(rawtext)
        scores[BytesEncodingDetect.EUC_JP] = self.euc_jp_probability(rawtext)
        scores[BytesEncodingDetect.ISO2022JP] = self.iso_2022_jp_probability(rawtext)
        scores[BytesEncodingDetect.UNICODET] = 0
        scores[BytesEncodingDetect.UNICODES] = 0
        scores[BytesEncodingDetect.ISO2022CN_GB] = 0
        scores[BytesEncodingDetect.ISO2022CN_CNS] = 0
        scores[BytesEncodingDetect.OTHER] = 0
        for index in range(BytesEncodingDetect.TOTALTYPES):
            if self.debug:
                print("Encoding " + BytesEncodingDetect.nicename[index] + " score " + scores[index])
            if scores[index] > maxscore:
                encoding_guess = index
                maxscore = scores[index]
        if maxscore <= 50:
            encoding_guess = BytesEncodingDetect.OTHER
        return encoding_guess

