from spider import xywy_analyze_info_2,xywy_write_info
import os


if __name__ == '__main__':
    for i in range(1000):
        print(i)
        for j in range(3):
            try:
                if j == 0:
                    info = xywy_analyze_info_2.analyze_disease_info(i)
                    xywy_write_info.write_disease_info(info)
                # elif j == 1:
                #     info = xywy_analyze_info_2.analyze_drug_info(i)
                #     xywy_write_info.write_drug_info(info)
                # else:
                #     info = xywy_analyze_info_2.analyze_symptom_info(i)
                #     xywy_write_info.write_symptom_info(info)

            except Exception as e:
                with open('error.txt', 'a') as f:
                    f.write(f'xywy_analyze_info_2:{j} id={i}\n')
