from Cut import BiMM
import question_analysis
import re
import os


class QuestionClassify:
    def __init__(self):
        BiMM.init()
        self.path = '/'.join(os.path.dirname(__file__).split('\\'))
        self.analysis = question_analysis.QuestionAnalysis()

    def classify(self, sentence):
        # 双向最大匹配
        words = BiMM.cut_words(sentence)
        kind = ""
        POS = []
        for word, flag in words:
            POS.append(flag)
        if "key_ts" in POS:
            kind = "key_ts"
        elif "key_tz" in POS:
            kind = "key_tz"
        elif "key_xz" in POS:
            kind = "key_xz"
        elif "key_zf" in POS:
            kind = "key_zf"
        elif "key_sf" in POS:
            kind = "key_sf"
        if kind == "key_ts":
            print(sentence, "特殊问句\n", words)
            # print(sentence)
            return self.analysis.question_ts(sentence, words)
        elif kind == "key_tz":
            print(sentence, "特指问句\n", words)
            # print(sentence)
            return self.analysis.question_tz(sentence, words)
        elif kind == "key_xz":
            print(sentence, "选择问句\n", words)
            # print(sentence)
            return self.analysis.question_xz(sentence, words)
        elif kind == "key_zf":
            print(sentence, "正反问句\n", words)
            # print(sentence)
            return self.analysis.question_zf(sentence, words)
        elif kind == "key_sf":
            print(sentence, "是非问句\n", words)
            # print(sentence)
            return self.analysis.question_sf(sentence, words)
        else:
            print('Sorry，请用问句的形式提问，或者反馈一下。')
            self.write_log(sentence)
            return
        # if "key_ts" in POS:
        #     kind = "特殊问句"
        #     print(sentence, kind)
        #     print(words)
        #     self.analysis.question_ts(sentence, words)
        # elif "key_tz" in POS:
        #     kind = "特指问句"
        #     print(sentence, kind)
        #     self.analysis.question_tz(sentence, words)
        # elif "key_xz" in POS:
        #     kind = "选择问句"
        #     print(sentence, kind)
        #     self.analysis.question_xz(sentence, words)
        # elif "key_zf" in POS:
        #     kind = "正反问句"
        #     print(sentence, kind)
        #     self.analysis.question_zf(sentence, words)
        # elif "key_sf" in POS:
        #     kind = "是非问句"
        #     print(sentence, kind)
        #     self.analysis.question_sf(sentence, words)

    def write_log(self, sentence):
        with open(f'{self.path}/log.txt', 'a+', encoding='utf-8') as f:
            f.write(sentence + '\n')

    def main(self):
        while True:
            print("请输入您要问的问题")
            sentence = input()
            if not sentence:
                break
            print(self.classify(sentence))

    def test(self):
        # 问句
        with open("query_bak.txt", "r", encoding='utf-8') as f:
            # print(f.readline())
            sentence = re.split('\n', f.read().rstrip('\n'))
        for sentence in sentence:
            print(self.classify(sentence))

    def debug(self):
        # 问句
        with open("log.txt", "r", encoding='utf-8') as f:
            # print(f.readline())
            sentence = re.split('\n', f.read().rstrip('\n'))
        for sentence in sentence:
            print(self.classify(sentence))


if __name__ == '__main__':
    handler = QuestionClassify()
    handler.main()
    # handler.test()
    # handler.debug()
