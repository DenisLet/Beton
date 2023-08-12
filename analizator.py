from sheet_with_often_scores import soccer_first_half_often
import re
import os
file_name = "leagues_soccer_made/Bundesliga.txt"

def check_scores_and_odds(file_name):

    with open(file_name, 'r') as file:
        data = file.read()
        matches = data.split('\n')
        results_list = []
        lst_list = []


        positive_cases = nigative_cases = all_cases = 0

        for num,match in enumerate(matches):
            try:
                if num > 11:
                    break


                cleaned_str = re.sub(r"[\[\]',]", "", match)
                lst = cleaned_str.split()
                # print(lst)
                lst_list.append(lst)
                index_1st, index_2nd = lst.index('1ST'), lst.index('2ND')
                t1_h1,t1_h2,t2_h1,t2_h2 = int(lst[index_1st+2]), int(lst[index_2nd+2]),int(lst[index_1st+4]),int(lst[index_2nd+4])
                str_1half = f'{t1_h1}{t2_h1}'
                index_odds = lst.index('ODDS')
                coef_list = lst[index_odds:]
                k1, k2 = float(coef_list[2]) if coef_list[2] != '-' else float(coef_list[8]), float(coef_list[6]) if \
                coef_list[6] != '-' else float(coef_list[12])
                results_list.append([t1_h1, t2_h1, t1_h2, t2_h2, k1, k2])
                match = lst[5:]
                goal_times= []
                for i, el in enumerate(match):
                    try:


                        score_change = match[i] + match[i + 2]

                        goal_minute = match[i - 1].replace('"', '')
                        if el.isdigit() and match[i + 1] == '-' and match[i + 2].isdigit() and goal_minute != 'HALF':
                            if '+' in goal_minute:
                                if goal_minute[0] == '4':
                                    goal_minute = 45
                                else:
                                    goal_minute = 90
                            goal_times.append((score_change, int(goal_minute)))
                    except:
                        break
                print(goal_times)
                half1 = [i for i in goal_times if i[1] < 46]
                half2 = [i for i in goal_times if i[1] > 45]
                goals_before75 = [i for i in goal_times if 45<i[1]<75]
                goals_before45_60 = [i for i in goal_times if 45<i[1]<61]
                goals_before60_75 = [i for i in goal_times if 60<i[1]<75]
                goals_after75 = [i for i in goal_times if  i[1] > 74]
                try:
                    t1_half1 = half1[-1][0][0] if len(half1)>0 else 0
                    t2_half1 = half1[-1][0][1] if len(half2)>0 else 0
                except:
                    t1_half1 = 0
                    t2_half1 = 0
                # print(half2)
                # print(half1)
                print()
                # print(half2)
                # print()

                # and half1[-1][0][0] == half1[-1][0][1] and len(goals_before45_60) == 1 and len(goals_before60_75) == 0
                if k1:
                    if len(half1)==0:
                        all_cases+=1
                    else:
                        nigative_cases+=1








                # if len(goal_times) >= 3 and goal_times[0][1] < 46 and goal_times[1][1] < 46  and goal_times[2][1] < 46:
                #     if len(goal_times) >=4 and goal_times[4][1] < 72:
                #         all_cases += 1
                #         if len(goal_times)>=5 and goal_times[-1][1]> 72:
                #             positive_cases += 1
                #             print(goal_times)
                #             print('PLUS')
                #         else:
                #             print(goal_times)
                #             print('MINUS')





            except Exception as s:
                print(s)
                continue
        print(all_cases, positive_cases)

    return results_list, lst_list


clear_results = check_scores_and_odds(file_name)
print(len(clear_results[0]))

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
    for num,match in enumerate(clear_results[0]):

        # print(match)
        half1_res = (match[0], match[1])
        half2_res = sum([match[2], match[3]])
        k1 = match[4]
        k2 = match[5]
        if 1 < k1 <= 1.1:

            if score == half1_res and score == (2,0):
                # print('ULTRA  -> ', 'HALF 1:', half1_res, 'HALF 2:', half2_res)
                # print(k1, k2)
                # print(match)
                # print(match)
                ultra_cases += 1
                if half2_res == 0:
                    ultra_2h_0 += 1
                if half2_res == 1:
                    ultra_2h_1 += 1
                if half2_res > 1:
                    ultra_2h_2 += 1
        if 1.1 < k1 <= 1.25:

            if score == half1_res:
                # print('SUPER  -> ', 'HALF 1:', half1_res, 'HALF 2:', half2_res)
                # print(k1, k2)
                # print(match)
                # print()
                super_cases += 1
                if half2_res == 0:
                    super_2h_0 += 1
                if half2_res == 1:
                    super_2h_1 += 1
                if half2_res > 1:
                    super_2h_2 += 1
        if 1.25 < k1 <= 1.5:

            if score == half1_res:
                # print('HUGE  -> ', 'HALF 1:', half1_res, 'HALF 2:', half2_res)
                # print(k1, k2)
                # print(match)
                # print()
                huge_cases += 1
                if half2_res == 0:
                    huge_2h_0 += 1
                if half2_res == 1:
                    huge_2h_1 += 1
                if half2_res > 1:
                    huge_2h_2 += 1
        if 1.5 < k1 <= 1.8:

            if score == half1_res:
                # print('STRONG  -> ', 'HALF 1:', half1_res, 'HALF 2:', half2_res)
                # print(k1, k2)
                # print(match)
                # print()
                strong_cases += 1
                if half2_res == 0:
                    strong_2h_0 += 1
                if half2_res == 1:
                    strong_2h_1 += 1
                if half2_res > 1:
                    strong_2h_2 += 1
        if 1.8 < k1 <= 2.2:

            if score == half1_res:
                # print('LITE  -> ', 'HALF 1:', half1_res, 'HALF 2:', half2_res)
                # print(k1, k2)
                # print(match)
                # print()
                lite_cases += 1
                if half2_res == 0:
                    lite_2h_0 += 1
                if half2_res == 1:
                    lite_2h_1 += 1
                if half2_res > 1:
                    lite_2h_2 += 1
        if k1 > 2.2 and k1 <= k2:

            if score == half1_res:
                # print('EQUAL  -> ', 'HALF 1:', half1_res, 'HALF 2:', half2_res)
                # print(k1, k2)
                # print(match)
                # print()
                equal_cases += 1
                if half2_res == 0:
                    equal_2h_0 += 1
                if half2_res == 1:
                    equal_2h_1 += 1
                if half2_res > 1:
                    equal_2h_2 += 1

    if any([ultra_cases, super_cases, huge_cases, strong_cases, lite_cases, equal_cases]):
        # print('SCORE:', score)
        # print("ULTRA", ultra_cases, ultra_2h_0, ultra_2h_1, ultra_2h_2)
        # print('SUPER', super_cases, super_2h_0, super_2h_1, super_2h_2)
        # print('HUGE', huge_cases, huge_2h_0, huge_2h_1, huge_2h_2)
        # print('STRONG', strong_cases, strong_2h_0, strong_2h_1, strong_2h_2)
        # print('LITE', lite_cases, lite_2h_0, lite_2h_1, lite_2h_2)
        # print('EQUAL', equal_cases, equal_2h_0, equal_2h_1, equal_2h_2)
        # print()
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
    for match in clear_results[0]:
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
        # print('SCORE:', score)
        # print("ULTRA", ultra_cases, ultra_2h_0, ultra_2h_1, ultra_2h_2)
        # print('SUPER', super_cases, super_2h_0, super_2h_1, super_2h_2)
        # print('HUGE', huge_cases, huge_2h_0, huge_2h_1, huge_2h_2)
        # print('STRONG', strong_cases, strong_2h_0, strong_2h_1, strong_2h_2)
        # print('LITE', lite_cases, lite_2h_0, lite_2h_1, lite_2h_2)
        # print('EQUAL', equal_cases, equal_2h_0, equal_2h_1, equal_2h_2)
        # print()
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

print(len(clear_results))


