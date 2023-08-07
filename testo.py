import re
import os
from soccer_nice import nice_dict
from sheet_with_often_scores import soccer_first_half_often

file_name = "leagues/Slovenia 2. SNL.txt"

def check_scores_and_odds(file_name):
    base_name = os.path.basename(file_name)
    name_without_extension = os.path.splitext(base_name)[0]
    return name_without_extension

league = check_scores_and_odds(file_name)

if league not in nice_dict:
    nice_dict[league] = {
        'home': {
            'ultra': [],
            'super': [],
            'huge': [],
            'strong': [],
            'lite': [],
            'equal': []
        },
        'away': {
            'ultra': [],
            'super': [],
            'huge': [],
            'strong': [],
            'lite': [],
            'equal': []
        }
    }

clear_results = check_scores_and_odds(file_name)

league = check_scores_and_odds(file_name)


nice_dict = {}

def check_scores_and_odds(file_name):

    with open(file_name, 'r') as file:
        data = file.read()
        matches = data.split('\n')
        results_list = []
        lst_list = []

        for num,match in enumerate(matches):
            try:
                if num > 40000:
                    break


                cleaned_str = re.sub(r"[\[\]',]", "", match)
                lst = cleaned_str.split()
                # print(lst)
                lst_list.append(lst)
                index_1st, index_2nd = lst.index('1ST'), lst.index('2ND')
                t1_h1,t1_h2,t2_h1,t2_h2 = int(lst[index_1st+2]), int(lst[index_2nd+2]),int(lst[index_1st+4]),int(lst[index_2nd+4])
                index_odds = lst.index('ODDS')
                # print(lst)
                coef_list = lst[index_odds:]
                k1, k2 = float(coef_list[2]) if coef_list[2] != '-' else float(coef_list[8]), float(coef_list[6]) if \
                coef_list[6] != '-' else float(coef_list[12])
                results_list.append([t1_h1, t2_h1, t1_h2, t2_h2, k1, k2])
                # print(k1, k2)

            except:
                continue

    return results_list

clear_results = check_scores_and_odds(file_name)

home_ultra_score = []
home_super_score = []
home_huge_score = []
home_strong_score = []
home_lite_score = []
home_equal_score = []

for score in soccer_first_half_often:
    ultra_cases = ultra_2h_0 = ultra_2h_1 = ultra_2h_2 = 0
    super_cases = super_2h_0 = super_2h_1 = super_2h_2 = 0
    huge_cases = huge_2h_0 = huge_2h_1 = huge_2h_2 = 0
    strong_cases = strong_2h_0 = strong_2h_1 = strong_2h_2 = 0
    lite_cases = lite_2h_0 = lite_2h_1 = lite_2h_2 = 0
    equal_cases = equal_2h_0 = equal_2h_1 = equal_2h_2 = 0
    for num,match in enumerate(clear_results):

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
    loc = 'home'
    str_score = f'{score[0]}{score[1]}'
    if ultra_cases >= 1 and ultra_2h_0 == 0 or\
            ultra_cases >= 8 and ultra_2h_0 <= 1 or \
            ultra_cases >= 14 and ultra_2h_0 <= 2 or \
            ultra_cases >= 20 and ultra_2h_0 <= 3 or \
            ultra_cases >= 27 and ultra_2h_0 <= 4 or \
            ultra_cases >= 33 and ultra_2h_0 <= 5 or \
            ultra_cases >= 40 and ultra_2h_0 <= 6 or \
            40<ultra_cases<=80 and ultra_2h_0 / ultra_cases < 0.163 or \
            80<ultra_cases<=120 and ultra_2h_0 / ultra_cases < 0.168  or \
            ultra_cases > 120 and ultra_2h_0 / ultra_cases < 0.169 :
                home_ultra_score.append(str_score)


    if super_cases >= 1 and super_2h_0 == 0 or\
            super_cases >= 8 and super_2h_0 <= 1 or \
            super_cases >= 14 and super_2h_0 <= 2 or \
            super_cases >= 20 and super_2h_0 <= 3 or \
            super_cases >= 27 and super_2h_0 <= 4 or \
            super_cases >= 33 and super_2h_0 <= 5 or \
            super_cases >= 40 and super_2h_0 <= 6 or \
            40<super_cases<=80 and super_2h_0 / super_cases < 0.163 or \
            80<super_cases<=120 and super_2h_0 / super_cases < 0.168  or \
            super_cases > 120 and super_2h_0 / super_cases < 0.169 :
                home_super_score.append(str_score)

    if huge_cases >= 2 and huge_2h_0 == 0 or\
            huge_cases >= 8 and huge_2h_0 <= 1 or \
            huge_cases >= 14 and huge_2h_0 <= 2 or \
            huge_cases >= 20 and huge_2h_0 <= 3 or \
            huge_cases >= 27 and huge_2h_0 <= 4 or \
            huge_cases >= 33 and huge_2h_0 <= 5 or \
            huge_cases >= 40 and huge_2h_0 <= 6 or \
            40<huge_cases<=80 and huge_2h_0 / huge_cases < 0.163 or \
            80<huge_cases<=120 and huge_2h_0 / huge_cases < 0.168  or \
            huge_cases > 120 and huge_2h_0 / huge_cases < 0.169 :
                home_huge_score.append(str_score)

    if strong_cases >= 2 and strong_2h_0 == 0 or\
            strong_cases >= 8 and strong_2h_0 <= 1 or \
            strong_cases >= 13 and strong_2h_0 <= 2 or \
            strong_cases >= 19 and strong_2h_0 <= 3 or \
            strong_cases >= 27 and strong_2h_0 <= 4 or \
            strong_cases >= 33 and strong_2h_0 <= 5 or \
            strong_cases >= 40 and strong_2h_0 <= 6 or \
            40<strong_cases<=80 and strong_2h_0/ strong_cases < 0.163 or \
            80<strong_cases<=120 and strong_2h_0 / strong_cases < 0.168  or \
            strong_cases > 120 and strong_2h_0 / strong_cases < 0.169 :
                home_strong_score.append(str_score)

    if lite_cases >= 2 and lite_2h_0 == 0 or\
            lite_cases >= 8 and lite_2h_0<= 1 or \
            lite_cases >= 13 and lite_2h_0 <= 2 or \
            lite_cases >= 19 and lite_2h_0<= 3 or \
            lite_cases >= 27 and lite_2h_0 <= 4 or \
            lite_cases >= 33 and lite_2h_0 <= 5 or \
            lite_cases>= 40 and lite_2h_0 <= 6 or \
            40<lite_cases<=80 and lite_2h_0 / lite_cases < 0.163 or \
            80<lite_cases<=120 and lite_2h_0 / lite_cases< 0.168  or \
            lite_cases > 120 and lite_2h_0 / lite_cases < 0.169 :
                home_lite_score.append(str_score)

    if equal_cases >= 2 and equal_2h_0 == 0 or\
            equal_cases >= 8 and equal_2h_0<= 1 or \
            equal_cases>= 13 and equal_2h_0 <= 2 or \
            equal_cases >= 19 and equal_2h_0 <= 3 or \
            equal_cases >= 27 and equal_2h_0 <= 4 or \
            equal_cases >= 33 and equal_2h_0 <= 5 or \
            equal_cases >= 40 and equal_2h_0 <= 6 or \
            40<equal_cases<=80 and equal_2h_0 / equal_cases < 0.163 or \
            80<equal_cases<=120 and equal_2h_0/ equal_cases < 0.168  or \
            equal_cases > 120 and equal_2h_0 / equal_cases < 0.169 :
                home_equal_score.append(str_score)

away_ultra_score = []
away_super_score = []
away_huge_score = []
away_strong_score = []
away_lite_score = []
away_equal_score = []

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

    loc = 'away'
    str_score = f'{score[0]}{score[1]}'
    if ultra_cases >= 1 and ultra_2h_0 == 0 or\
            ultra_cases >= 8 and ultra_2h_0 <= 1 or \
            ultra_cases >= 14 and ultra_2h_0 <= 2 or \
            ultra_cases >= 20 and ultra_2h_0 <= 3 or \
            ultra_cases >= 27 and ultra_2h_0 <= 4 or \
            ultra_cases >= 33 and ultra_2h_0 <= 5 or \
            ultra_cases >= 40 and ultra_2h_0 <= 6 or \
            40<ultra_cases<=80 and ultra_2h_0 / ultra_cases < 0.163 or \
            80<ultra_cases<=120 and ultra_2h_0 / ultra_cases < 0.168  or \
            ultra_cases > 120 and ultra_2h_0 / ultra_cases < 0.169 :
                away_ultra_score.append(str_score)


    if super_cases >= 1 and super_2h_0 == 0 or\
            super_cases >= 8 and super_2h_0 <= 1 or \
            super_cases >= 14 and super_2h_0 <= 2 or \
            super_cases >= 20 and super_2h_0 <= 3 or \
            super_cases >= 27 and super_2h_0 <= 4 or \
            super_cases >= 33 and super_2h_0 <= 5 or \
            super_cases >= 40 and super_2h_0 <= 6 or \
            40<super_cases<=80 and super_2h_0 / super_cases < 0.163 or \
            80<super_cases<=120 and super_2h_0 / super_cases < 0.168  or \
            super_cases > 120 and super_2h_0 / super_cases < 0.169 :
                away_super_score.append(str_score)

    if huge_cases >= 2 and huge_2h_0 == 0 or\
            huge_cases >= 8 and huge_2h_0 <= 1 or \
            huge_cases >= 14 and huge_2h_0 <= 2 or \
            huge_cases >= 20 and huge_2h_0 <= 3 or \
            huge_cases >= 27 and huge_2h_0 <= 4 or \
            huge_cases >= 33 and huge_2h_0 <= 5 or \
            huge_cases >= 40 and huge_2h_0 <= 6 or \
            40<huge_cases<=80 and huge_2h_0 / huge_cases < 0.163 or \
            80<huge_cases<=120 and huge_2h_0 / huge_cases < 0.168  or \
            huge_cases > 120 and huge_2h_0 / huge_cases < 0.169 :
                away_huge_score.append(str_score)

    if strong_cases >= 2 and strong_2h_0 == 0 or\
            strong_cases >= 8 and strong_2h_0 <= 1 or \
            strong_cases >= 13 and strong_2h_0 <= 2 or \
            strong_cases >= 19 and strong_2h_0 <= 3 or \
            strong_cases >= 27 and strong_2h_0 <= 4 or \
            strong_cases >= 33 and strong_2h_0 <= 5 or \
            strong_cases >= 40 and strong_2h_0 <= 6 or \
            40<strong_cases<=80 and strong_2h_0/ strong_cases < 0.163 or \
            80<strong_cases<=120 and strong_2h_0 / strong_cases < 0.168  or \
            strong_cases > 120 and strong_2h_0 / strong_cases < 0.169 :
                away_strong_score.append(str_score)

    if lite_cases >= 2 and lite_2h_0 == 0 or\
            lite_cases >= 8 and lite_2h_0<= 1 or \
            lite_cases >= 13 and lite_2h_0 <= 2 or \
            lite_cases >= 19 and lite_2h_0<= 3 or \
            lite_cases >= 27 and lite_2h_0 <= 4 or \
            lite_cases >= 33 and lite_2h_0 <= 5 or \
            lite_cases>= 40 and lite_2h_0 <= 6 or \
            40<lite_cases<=80 and lite_2h_0 / lite_cases < 0.163 or \
            80<lite_cases<=120 and lite_2h_0 / lite_cases< 0.168  or \
            lite_cases > 120 and lite_2h_0 / lite_cases < 0.169 :
                away_lite_score.append(str_score)

    if equal_cases >= 2 and equal_2h_0 == 0 or\
            equal_cases >= 8 and equal_2h_0<= 1 or \
            equal_cases>= 13 and equal_2h_0 <= 2 or \
            equal_cases >= 19 and equal_2h_0 <= 3 or \
            equal_cases >= 27 and equal_2h_0 <= 4 or \
            equal_cases >= 33 and equal_2h_0 <= 5 or \
            equal_cases >= 40 and equal_2h_0 <= 6 or \
            40<equal_cases<=80 and equal_2h_0 / equal_cases < 0.163 or \
            80<equal_cases<=120 and equal_2h_0/ equal_cases < 0.169  or \
            equal_cases > 120 and equal_2h_0 / equal_cases < 0.169 :
                away_equal_score.append(str_score)


nice_dict[league] = {
    'home': {
        'ultra': home_ultra_score,
        'super': home_super_score,
        'huge': home_huge_score,
        'strong': home_strong_score,
        'lite': home_lite_score,
        'equal': home_equal_score
        },
    'away': {
        'ultra': away_ultra_score,
        'super': away_super_score,
        'huge': away_huge_score,
        'strong': away_strong_score,
        'lite': away_lite_score,
        'equal': away_equal_score
    }
}

with open('soccer_nice.py', 'a') as f:
    f.write("\nnice_dict[{}] = {}".format(repr(league), repr(nice_dict[league])))