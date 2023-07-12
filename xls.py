from openpyxl import Workbook
from sheet_with_often_scores import soccer_first_half_often
import openpyxl

workbook = openpyxl.Workbook()
sheet = workbook.active

results = [
    (1.29, 10.0, 3, 0, 2, 0),
    (1.85, 3.8, 2, 1, 0, 0),
    (3.2, 2.15, 0, 0, 1, 0),
    (2.63, 2.5, 1, 1, 0, 0),
    (1.6, 5.75, 0, 1, 1, 0),
    (1.62, 5.25, 0, 0, 1, 0),
    (2.75, 2.38, 0, 1, 1, 3),
    (1.95, 3.4, 1, 0, 1, 1),
    (1.45, 6.0, 1, 1, 1, 0),
    (5.5, 1.5, 2, 2, 2, 2),
    (1.53, 5.75, 2, 0, 2, 1),
    (3.8, 1.85, 1, 1, 0, 0),
    (1.3, 9.0, 0, 0, 0, 0),
    (1.57, 5.75, 1, 0, 0, 0),
    (1.18, 13.0, 2, 0, 1, 1),
    (2.6, 2.63, 1, 1, 2, 0),
    (5.0, 1.62, 1, 0, 0, 0),
    (7.0, 1.4, 0, 1, 0, 0),
    (2.38, 3.2, 1, 1, 1, 1),
    (1.5, 6.0, 0, 1, 1, 0),
    (3.1, 2.25, 1, 0, 0, 1),
    (1.91, 3.75, 1, 0, 0, 3),
    (1.8, 4.0, 2, 0, 2, 1),
    (4.5, 1.7, 0, 2, 0, 1),
    (1.75, 4.0, 0, 0, 0, 3),
    (1.8, 4.5, 2, 0, 0, 0),
    (8.0, 1.33, 0, 2, 0, 1),
    (2.2, 3.0, 1, 0, 1, 1),
    (1.57, 5.25, 0, 1, 2, 1),
    (1.75, 4.5, 1, 0, 1, 0),
    (1.36, 7.0, 1, 0, 1, 0),
    (2.63, 2.55, 0, 0, 0, 2),
    (4.75, 1.6, 1, 1, 1, 1),
    (1.95, 3.8, 3, 1, 1, 2),
    (1.33, 8.0, 0, 3, 1, 2),
    (2.63, 2.7, 3, 0, 2, 3),
    (3.5, 2.05, 1, 0, 0, 0),
    (2.25, 2.9, 0, 1, 0, 1),
    (1.4, 6.5, 1, 0, 0, 0),
    (3.5, 2.05, 1, 1, 0, 2),
    (1.17, 15.0, 2, 0, 0, 1),
    (1.8, 4.5, 1, 0, 0, 0),
    (3.1, 2.3, 1, 0, 0, 0),
    (2.15, 3.1, 0, 0, 1, 0),
    (1.3, 9.0, 1, 0, 0, 0),
    (1.17, 13.0, 0, 0, 3, 0),
    (1.57, 5.5, 3, 0, 0, 1),
    (1.95, 3.9, 2, 1, 0, 1),
    (1.53, 5.5, 3, 1, 1, 2),
    (2.45, 2.9, 2, 1, 2, 0),
    (9.0, 1.29, 1, 2, 0, 0),
    (1.73, 4.33, 1, 0, 0, 0),
    (1.25, 11.0, 0, 1, 3, 0),
    (1.73, 5.0, 0, 1, 2, 0),
    (1.6, 5.5, 4, 0, 2, 0),
    (2.4, 2.9, 3, 2, 1, 1),
    (2.9, 2.25, 0, 2, 2, 0),
    (4.5, 1.8, 0, 1, 1, 3),
    (2.5, 2.8, 0, 0, 0, 1),
    (1.62, 5.25, 2, 0, 2, 1),
    (1.83, 4.33, 0, 1, 0, 1),
    (3.5, 2.0, 1, 1, 0, 1),
    (5.25, 1.57, 1, 1, 2, 0),
    (2.25, 3.0, 1, 0, 0, 1),
    (1.73, 4.75, 1, 0, 0, 0),
    (2.25, 3.6, 1, 0, 1, 0),
    (3.0, 2.45, 0, 3, 0, 1),
    (1.91, 4.0, 5, 0, 1, 1),
    (2.63, 2.75, 0, 0, 1, 1),
    (1.91, 4.33, 0, 0, 0, 0),
    (2.38, 3.0, 1, 1, 1, 0),
    (1.18, 15.0, 0, 0, 3, 2),
    (2.3, 3.0, 0, 0, 2, 1),
    (1.2, 12.0, 1, 2, 2, 1),
    (4.5, 1.67, 0, 2, 1, 4),
    (4.75, 1.7, 0, 1, 0, 1),
    (5.25, 1.62, 1, 2, 1, 0),
    (1.14, 15.0, 3, 0, 0, 1),
    (3.0, 2.38, 1, 1, 0, 1),
    (2.2, 3.3, 1, 1, 0, 2),
    (2.88, 2.7, 0, 0, 0, 2),
    (1.45, 6.5, 1, 1, 1, 2),
    (2.8, 2.63, 1, 0, 1, 0),
    (3.4, 2.15, 1, 0, 2, 0),
    (2.7, 2.5, 1, 2, 1, 0),
    (2.0, 3.6, 1, 1, 0, 4),
    (13.0, 1.22, 0, 1, 1, 3),
    (1.57, 5.5, 0, 0, 2, 0),
    (4.0, 1.91, 1, 0, 0, 2),
    (2.9, 2.5, 0, 1, 0, 0),
    (2.05, 3.75, 0, 1, 0, 0),
    (2.7, 2.5, 1, 1, 1, 0),
    (4.75, 1.75, 1, 0, 0, 0),
    (1.57, 6.0, 1, 0, 1, 0),
    (1.57, 5.25, 1, 0, 0, 0),
    (3.5, 2.25, 1, 2, 0, 3),
    (2.2, 3.3, 0, 0, 0, 0),
    (5.75, 1.53, 0, 1, 0, 1),
    (1.62, 5.5, 2, 1, 0, 0),
    (2.7, 2.63, 1, 1, 0, 1),
    (3.75, 2.05, 0, 0, 1, 1),
    (2.25, 3.1, 0, 0, 2, 0),
    (1.73, 5.0, 1, 0, 0, 0)
]


print('FOR HOME TEAM FAVORITE AND EQUAL POWER TEAM')
for score in soccer_first_half_often:
    ultra_cases = ultra_2h_0 = ultra_2h_1 = ultra_2h_2 = 0
    super_cases = super_2h_0 = super_2h_1 = super_2h_2 = 0
    huge_cases = huge_2h_0 = huge_2h_1 = huge_2h_2 = 0
    strong_cases = strong_2h_0 = strong_2h_1 = strong_2h_2 = 0
    lite_cases = lite_2h_0 = lite_2h_1 = lite_2h_2 = 0
    equal_cases = equal_2h_0 = equal_2h_1 = equal_2h_2 = 0
    for match in results:
        half1_res = (match[2], match[3])
        half2_res = sum([match[4], match[5]])
        k1 = match[0]
        k2 = match[1]
        if 1<k1<=1.1:
            if score == half1_res:
                ultra_cases += 1
                if half2_res == 0:
                    ultra_2h_0 += 1
                if half2_res == 1:
                    ultra_2h_1 += 1
                if half2_res > 1:
                    ultra_2h_2 += 1
        if 1.1<k1<=1.25:
            if score == half1_res:
                super_cases += 1
                if half2_res == 0:
                    super_2h_0 += 1
                if half2_res == 1:
                    super_2h_1 += 1
                if half2_res > 1:
                    super_2h_2 += 1
        if 1.25<k1<=1.5:
            if score == half1_res:
                huge_cases += 1
                if half2_res == 0:
                    huge_2h_0 += 1
                if half2_res == 1:
                    huge_2h_1 += 1
                if half2_res > 1:
                    huge_2h_2 += 1
        if 1.5<k1<=1.8:
            if score == half1_res:
                strong_cases += 1
                if half2_res == 0:
                    strong_2h_0 += 1
                if half2_res == 1:
                    strong_2h_1 += 1
                if half2_res > 1:
                    strong_2h_2 += 1
        if 1.8<k1<=2.2:
            if score == half1_res:
                lite_cases += 1
                if half2_res == 0:
                    lite_2h_0 += 1
                if half2_res == 1:
                    lite_2h_1 += 1
                if half2_res > 1:
                    lite_2h_2 += 1
        else:
            if score == half1_res:
                equal_cases += 1
                if half2_res == 0:
                    equal_2h_0 += 1
                if half2_res == 1:
                    equal_2h_1 += 1
                if half2_res > 1:
                    equal_2h_2 += 1

    if any([ultra_cases, super_cases, huge_cases, strong_cases, lite_cases, equal_cases]):
        print('SCORE:',score)
        print("ULTRA",ultra_cases, ultra_2h_0 , ultra_2h_1, ultra_2h_2)
        print('SUPER',super_cases, super_2h_0, super_2h_1, super_2h_2)
        print('HUGE',huge_cases, huge_2h_0, huge_2h_1, huge_2h_2)
        print('STRONG',strong_cases, strong_2h_0, strong_2h_1, strong_2h_2)
        print('LITE', lite_cases, lite_2h_0, lite_2h_1, lite_2h_2)
        print('EQUAL', equal_cases, equal_2h_0, equal_2h_1, equal_2h_2)
        print()
        row_data = [
            ('SCORE',str(score)),
            ("ULTRA",ultra_cases, ultra_2h_0 , ultra_2h_1, ultra_2h_2),
            ('SUPER', super_cases, super_2h_0, super_2h_1, super_2h_2),
            ('HUGE', huge_cases, huge_2h_0, huge_2h_1, huge_2h_2),
            ('STRONG', strong_cases, strong_2h_0, strong_2h_1, strong_2h_2),
            ('LITE', lite_cases, lite_2h_0, lite_2h_1, lite_2h_2),
            ('EQUAL', equal_cases, equal_2h_0, equal_2h_1, equal_2h_2),
            (' ', ' ')

        ]
        for row in row_data:
            sheet.append(row)



sheet.append(("AWAY","TEAM","IS","FAVORITE"))
print('FOR AWAY TEAM FAVORITE')
for score in soccer_first_half_often:
    ultra_cases = ultra_2h_0 = ultra_2h_1 = ultra_2h_2 = 0
    super_cases = super_2h_0 = super_2h_1 = super_2h_2 = 0
    huge_cases = huge_2h_0 = huge_2h_1 = huge_2h_2 = 0
    strong_cases = strong_2h_0 = strong_2h_1 = strong_2h_2 = 0
    lite_cases = lite_2h_0 = lite_2h_1 = lite_2h_2 = 0
    equal_cases = equal_2h_0 = equal_2h_1 = equal_2h_2 = 0
    for match in results:
        half1_res = (match[2], match[3])
        half2_res = sum([match[4], match[5]])
        k1 = match[0]
        k2 = match[1]
        if 1<k2<=1.1:
            if score == half1_res:
                ultra_cases += 1
                if half2_res == 0:
                    ultra_2h_0 += 1
                if half2_res == 1:
                    ultra_2h_1 += 1
                if half2_res > 1:
                    ultra_2h_2 += 1
        if 1.1<k2<=1.25:
            if score == half1_res:
                super_cases += 1
                if half2_res == 0:
                    super_2h_0 += 1
                if half2_res == 1:
                    super_2h_1 += 1
                if half2_res > 1:
                    super_2h_2 += 1
        if 1.25<k2<=1.5:
            if score == half1_res:
                huge_cases += 1
                if half2_res == 0:
                    huge_2h_0 += 1
                if half2_res == 1:
                    huge_2h_1 += 1
                if half2_res > 1:
                    huge_2h_2 += 1
        if 1.5<k2<=1.8:
            if score == half1_res:
                strong_cases += 1
                if half2_res == 0:
                    strong_2h_0 += 1
                if half2_res == 1:
                    strong_2h_1 += 1
                if half2_res > 1:
                    strong_2h_2 += 1
        if 1.8<k2<=2.2:
            if score == half1_res:
                lite_cases += 1
                if half2_res == 0:
                    lite_2h_0 += 1
                if half2_res == 1:
                    lite_2h_1 += 1
                if half2_res > 1:
                    lite_2h_2 += 1


    if any([ultra_cases, super_cases, huge_cases, strong_cases, lite_cases, equal_cases]):
        print('SCORE:',score)
        print("ULTRA",ultra_cases, ultra_2h_0 , ultra_2h_1, ultra_2h_2)
        print('SUPER',super_cases, super_2h_0, super_2h_1, super_2h_2)
        print('HUGE',huge_cases, huge_2h_0, huge_2h_1, huge_2h_2)
        print('STRONG',strong_cases, strong_2h_0, strong_2h_1, strong_2h_2)
        print('LITE', lite_cases, lite_2h_0, lite_2h_1, lite_2h_2)
        print('EQUAL', equal_cases, equal_2h_0, equal_2h_1, equal_2h_2)
        print()
        row_data = [
            ('SCORE',str(score)),
            ("ULTRA",ultra_cases, ultra_2h_0 , ultra_2h_1, ultra_2h_2),
            ('SUPER', super_cases, super_2h_0, super_2h_1, super_2h_2),
            ('HUGE', huge_cases, huge_2h_0, huge_2h_1, huge_2h_2),
            ('STRONG', strong_cases, strong_2h_0, strong_2h_1, strong_2h_2),
            ('LITE', lite_cases, lite_2h_0, lite_2h_1, lite_2h_2),
            ('EQUAL', equal_cases, equal_2h_0, equal_2h_1, equal_2h_2),
            (' ', ' ')

        ]
        for row in row_data:
            sheet.append(row)
workbook.save('table.xlsx')
