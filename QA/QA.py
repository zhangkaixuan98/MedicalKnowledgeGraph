import question_classify as question
import re


class ChatRobot:
    def __init__(self):
        self.classifier = question.QuestionClassify()


def main():
    """
    用户交互接口
    :return:
    """
    question.init()
    while True:
        print("请输入您要问的问题")
        sentence = input()
        if not sentence:
            break
        result = question.classify(sentence)
        print(f"{result}")


def test():
    question.init()
    # 问句
    with open("query_bak.txt", "r", encoding='utf-8') as f:
        # print(f.readline())
        query = re.split('\n', f.read().rstrip('\n'))
    for query in query:
        words = cut_words(query)
        print(words)

if __name__ == "__main__":
    # main()
    test()

















