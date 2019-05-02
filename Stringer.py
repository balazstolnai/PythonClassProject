# -*- coding: utf-8 -*-


class Stringer:
    finalText = ""

    def maketext(self, text):
        self.finalText = ""
        for k in text:
            b = 0
            text_ = k.replace(u'\xa0', u' ')
            for a in text_:
                if a != "<" and b == 0:
                    self.finalText += a
                elif a == "<":
                    b = 1
                elif a == ">":
                    b = 0
        return self.finalText
