from Univutil.UnivWrapper import UnivUtilFunction

class InhaUniv(UnivUtilFunction):

    def deserializesource(self, data):
        #data is bitmasked integer ex) 0b00000000000111
        #sourceDeserializer is a list of strings
        #return the string that corresponds to the bitmasked integer

        sourceDeserializer = ['전체공지', '정석학술정보관', '프런티어 학부대학', '공과대학', '자연과학대학', '경영대학', '사범대학', '사회과학대학', '문과대학', '의과대학', '미래융합대학', '국제학부', '소프트웨어융합대학', '바이오시스템융합학부']
        ret = []
        for idx, source in enumerate(sourceDeserializer):
            if data & 1 << idx:
                ret.append(source)
        return ret