from Cut import BiMM
import question_analysis
import re


class QuestionClassify:
    def __init__(self):
        BiMM.init()
        self.analysis = question_analysis.QuestionAnalysis()

    def classify(self, sentence):
        # 双向最大匹配
        words = BiMM.cut_words(sentence)
        print(words)
        kind = ""
        POS = []
        for word, flag in words:
            POS.append(flag)
        if "key_ts" in POS:
            self.analysis.question_ts(sentence, words)
            kind = "特殊问句"
        elif "key_tz" in POS:
            self.analysis.question_tz(sentence, words)
            kind = "特指问句"
        elif "key_xz" in POS:
            self.analysis.question_xz(sentence, words)
            kind = "选择问句"
        elif "key_zf" in POS:
            self.analysis.question_zf(sentence, words)
            kind = "正反问句"
        elif "key_sf" in POS:
            self.analysis.question_sf(sentence, words)
            kind = "是非问句"
        print(sentence, kind)

    def main(self):
        while True:
            print("请输入您要问的问题")
            sentence = input()
            if not sentence:
                break
            self.classify(sentence)

    def test(self):
        # 问句
        with open("query_bak.txt", "r", encoding='utf-8') as f:
            # print(f.readline())
            sentence = re.split('\n', f.read().rstrip('\n'))
        for sentence in sentence:
            self.classify(sentence)

    def debug(self):
        # 问句
        with open("log.txt", "r", encoding='utf-8') as f:
            # print(f.readline())
            sentence = re.split('\n', f.read().rstrip('\n'))
        for sentence in sentence:
            self.classify(sentence)


if __name__ == '__main__':
    handler = QuestionClassify()
    # handler.main()
    handler.test()
    # handler.debug()
