from sheet_with_often_scores import soccer_first_half_often
import re

file_name = "leagues/Serie A.txt"

def check_scores_and_odds(file_name):

    with open(file_name, 'r') as file:
        data = file.read()
        matches = data.split('<$>')
        results_list = []
        for num,match in enumerate(matches):
            try:
                cleaned_str = re.sub(r"[\[\]',]", "", match)
                lst = cleaned_str.split()
                index_1st, index_2nd = lst.index('1ST'), lst.index('2ND')
                t1_h1,t1_h2,t2_h1,t2_h2 = int(lst[index_1st+2]), int(lst[index_2nd+2]),int(lst[index_1st+4]),int(lst[index_2nd+4])
                k1, draw, k2 = float(lst[3]), float(lst[5]), float(lst[7])
                results_list.append([t1_h1, t2_h1, t1_h2, t2_h2, k1, k2])
            except:
                continue

    return results_list


clear_results = check_scores_and_odds(file_name)

import openpyxl


workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.append(('HOME', 'TEAM', 'IS', 'FAVORITE', 'OR', 'EQUAL POWER'))


for score in soccer_first_half_often:
    ultra_cases = ultra_2h_0 = ultra_2h_1 = ultra_2h_2 = 0
    super_cases = super_2h_0 = super_2h_1 = super_2h_2 = 0
    huge_cases = huge_2h_0 = huge_2h_1 = huge_2h_2 = 0
    strong_cases = strong_2h_0 = strong_2h_1 = strong_2h_2 = 0
    lite_cases = lite_2h_0 = lite_2h_1 = lite_2h_2 = 0
    equal_cases = equal_2h_0 = equal_2h_1 = equal_2h_2 = 0
    for match in clear_results:
        half1_res = (match[0], match[1])
        half2_res = sum([match[2], match[3]])
        k1 = match[4]
        k2 = match[5]
        if 1 < k1 <= 1.1:
            if score == half1_res:
                ultra_cases += 1
                if half2_res == 0:
                    ultra_2h_0 += 1
                if half2_res == 1:
                    ultra_2h_1 += 1
                if half2_res > 1:
                    ultra_2h_2 += 1
        if 1.1 < k1 <= 1.25:
            if score == half1_res:
                super_cases += 1
                if half2_res == 0:
                    super_2h_0 += 1
                if half2_res == 1:
                    super_2h_1 += 1
                if half2_res > 1:
                    super_2h_2 += 1
        if 1.25 < k1 <= 1.5:
            if score == half1_res:
                huge_cases += 1
                if half2_res == 0:
                    huge_2h_0 += 1
                if half2_res == 1:
                    huge_2h_1 += 1
                if half2_res > 1:
                    huge_2h_2 += 1
        if 1.5 < k1 <= 1.8:
            if score == half1_res:
                strong_cases += 1
                if half2_res == 0:
                    strong_2h_0 += 1
                if half2_res == 1:
                    strong_2h_1 += 1
                if half2_res > 1:
                    strong_2h_2 += 1
        if 1.8 < k1 <= 2.2:
            if score == half1_res:
                lite_cases += 1
                if half2_res == 0:
                    lite_2h_0 += 1
                if half2_res == 1:
                    lite_2h_1 += 1
                if half2_res > 1:
                    lite_2h_2 += 1
        if k1 > 2.2 and k1 <= k2:
            if score == half1_res:
                equal_cases += 1
                if half2_res == 0:
                    equal_2h_0 += 1
                if half2_res == 1:
                    equal_2h_1 += 1
                if half2_res > 1:
                    equal_2h_2 += 1

    if any([ultra_cases, super_cases, huge_cases, strong_cases, lite_cases, equal_cases]):
        print('SCORE:', score)
        print("ULTRA", ultra_cases, ultra_2h_0, ultra_2h_1, ultra_2h_2)
        print('SUPER', super_cases, super_2h_0, super_2h_1, super_2h_2)
        print('HUGE', huge_cases, huge_2h_0, huge_2h_1, huge_2h_2)
        print('STRONG', strong_cases, strong_2h_0, strong_2h_1, strong_2h_2)
        print('LITE', lite_cases, lite_2h_0, lite_2h_1, lite_2h_2)
        print('EQUAL', equal_cases, equal_2h_0, equal_2h_1, equal_2h_2)
        print()
        row_data = [
            ('SCORE', str(score)),
            ("ULTRA", ultra_cases, ultra_2h_0, ultra_2h_1, ultra_2h_2),
            ('SUPER', super_cases, super_2h_0, super_2h_1, super_2h_2),
            ('HUGE', huge_cases, huge_2h_0, huge_2h_1, huge_2h_2),
            ('STRONG', strong_cases, strong_2h_0, strong_2h_1, strong_2h_2),
            ('LITE', lite_cases, lite_2h_0, lite_2h_1, lite_2h_2),
            ('EQUAL', equal_cases, equal_2h_0, equal_2h_1, equal_2h_2),
            (' ', ' ')

        ]
        for row in row_data:
            sheet.append(row)

sheet.append(("AWAY", "TEAM", "IS", "FAVORITE"))
print('FOR AWAY TEAM FAVORITE')
for score in soccer_first_half_often:
    ultra_cases = ultra_2h_0 = ultra_2h_1 = ultra_2h_2 = 0
    super_cases = super_2h_0 = super_2h_1 = super_2h_2 = 0
    huge_cases = huge_2h_0 = huge_2h_1 = huge_2h_2 = 0
    strong_cases = strong_2h_0 = strong_2h_1 = strong_2h_2 = 0
    lite_cases = lite_2h_0 = lite_2h_1 = lite_2h_2 = 0
    equal_cases = equal_2h_0 = equal_2h_1 = equal_2h_2 = 0
    for match in clear_results:
        half1_res = (match[0], match[1])
        half2_res = sum([match[2], match[3]])
        k1 = match[4]
        k2 = match[5]
        if 1 < k2 <= 1.1:
            if score == half1_res:
                ultra_cases += 1
                if half2_res == 0:
                    ultra_2h_0 += 1
                if half2_res == 1:
                    ultra_2h_1 += 1
                if half2_res > 1:
                    ultra_2h_2 += 1
        if 1.1 < k2 <= 1.25:
            if score == half1_res:
                super_cases += 1
                if half2_res == 0:
                    super_2h_0 += 1
                if half2_res == 1:
                    super_2h_1 += 1
                if half2_res > 1:
                    super_2h_2 += 1
        if 1.25 < k2 <= 1.5:
            if score == half1_res:
                huge_cases += 1
                if half2_res == 0:
                    huge_2h_0 += 1
                if half2_res == 1:
                    huge_2h_1 += 1
                if half2_res > 1:
                    huge_2h_2 += 1
        if 1.5 < k2 <= 1.8:
            if score == half1_res:
                strong_cases += 1
                if half2_res == 0:
                    strong_2h_0 += 1
                if half2_res == 1:
                    strong_2h_1 += 1
                if half2_res > 1:
                    strong_2h_2 += 1
        if 1.8 < k2 <= 2.2:
            if score == half1_res:
                lite_cases += 1
                if half2_res == 0:
                    lite_2h_0 += 1
                if half2_res == 1:
                    lite_2h_1 += 1
                if half2_res > 1:
                    lite_2h_2 += 1
        if k2 > 2.2 and k2 < k1:
            if score == half1_res:
                equal_cases += 1
                if half2_res == 0:
                    equal_2h_0 += 1
                if half2_res == 1:
                    equal_2h_1 += 1
                if half2_res > 1:
                    equal_2h_2 += 1

    if any([ultra_cases, super_cases, huge_cases, strong_cases, lite_cases, equal_cases]):
        print('SCORE:', score)
        print("ULTRA", ultra_cases, ultra_2h_0, ultra_2h_1, ultra_2h_2)
        print('SUPER', super_cases, super_2h_0, super_2h_1, super_2h_2)
        print('HUGE', huge_cases, huge_2h_0, huge_2h_1, huge_2h_2)
        print('STRONG', strong_cases, strong_2h_0, strong_2h_1, strong_2h_2)
        print('LITE', lite_cases, lite_2h_0, lite_2h_1, lite_2h_2)
        print('EQUAL', equal_cases, equal_2h_0, equal_2h_1, equal_2h_2)
        print()
        row_data = [
            ('SCORE', str(score)),
            ("ULTRA", ultra_cases, ultra_2h_0, ultra_2h_1, ultra_2h_2),
            ('SUPER', super_cases, super_2h_0, super_2h_1, super_2h_2),
            ('HUGE', huge_cases, huge_2h_0, huge_2h_1, huge_2h_2),
            ('STRONG', strong_cases, strong_2h_0, strong_2h_1, strong_2h_2),
            ('LITE', lite_cases, lite_2h_0, lite_2h_1, lite_2h_2),
            ('EQUAL', equal_cases, equal_2h_0, equal_2h_1, equal_2h_2),
            (' ', ' ')

        ]
        for row in row_data:
            sheet.append(row)
workbook.save('leagu.xlsx')





