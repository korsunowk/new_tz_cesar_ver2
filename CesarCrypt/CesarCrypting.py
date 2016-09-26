# -*- coding: utf-8 -*-


class CesarCrypting:
    def __init__(self):
        self.alphabet = str()
        self.eng_vocabulary = set()

        self.fill_alphabet()
        self.fill_vocabulary()

    def fill_alphabet(self):
        for i in range(97, 123):  # 97-123 - англ алфавит
            self.alphabet += (chr(i))  # создание списка алфавита

    def fill_vocabulary(self):
        tmp = open("static/eng_slovar.txt", "r")  # cоздание множества словаря слов
        for line in tmp:
            for word in line.split(' '):
                self.eng_vocabulary.add(word)

    def encrypting(self, text, key):
        cesar_text = ''
        it = 0
        for i in text.lower():
            try:
                int(i)  # проверка символа на int
                cesar_text += i
            except ValueError:
                if i == ' ':  # проверка на пробел в тексте
                    cesar_text += ' '
                else:
                    if self.alphabet.find(i) >= 0:  # проверка на входимость в алфавит
                        letter = self.alphabet.find(i) + key
                        if letter > 25:
                            letter -= 26
                        if text[it].isupper():
                            cesar_text += chr(letter + 97).upper()
                        else:
                            cesar_text += chr(letter + 97)
                    else:                       # если нет в алфавите, то символ не изменяется
                        cesar_text += i
                it += 1
        return cesar_text

    def decrypting(self, cesar_text, key):
        normal_text = ''
        it = 0
        for i in cesar_text.lower():
            try:
                int(i)  # проверка символа на число
                normal_text += i
            except ValueError:
                if i == ' ':  # проверка на пробел в тексте
                    normal_text += ' '
                else:
                    if self.alphabet.find(i) >= 0:  # проверка на входимость в алфавит
                        letter = self.alphabet.find(i) - key
                        if letter < 0:
                            letter += 26
                        if cesar_text[it].isupper():
                            normal_text += chr(letter + 97).upper()
                        else:
                            normal_text += chr(letter + 97)
                    else:  # если нет в алфавите, то символ не изменяется
                        normal_text += i
                it += 1
        return normal_text

    def find_text(self, text):
        for word in text.split(' '):
            if word in self.eng_vocabulary:         # поиск слова из введенного текста в словаре
                return True
        return False
