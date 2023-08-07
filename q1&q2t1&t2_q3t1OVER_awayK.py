from sheet_with_often_scores import soccer_first_half_often
import re
import openpyxl

file_name = "leaguesBB/BBL.txt"


def check_scores_and_odds(file_name):

    with open(file_name, 'r') as file:
        data = file.read()
        matches = data.split('\n')

        results_list = []
        lst_list = []
        for num,match in enumerate(matches):
            try:

                if num > 3000:
                    break
                cleaned_str = re.sub(r"[\[\]',]", "", match)
                lst = cleaned_str.split()
                scores = []
                print(lst)
                for i in lst:
                    if i.isdigit():
                        scores.append(int(i))
                    if '<$>' in i:
                        score_4q = i.split('<$>')
                        scores.append(int(score_4q[0]))
                        break
                coefs = []
                index_odds = lst.index('ODDS')

                coef_list = lst[index_odds:]
                k1, k2 = float(coef_list[2]) if coef_list[2] != '-' else float(coef_list[6]), float(coef_list[4]) if coef_list[4] != '-' else float(coef_list[8])
                results_list.append(scores + [k1] + [k2])
            except:
                continue
    return results_list

clear_results = check_scores_and_odds(file_name)

def count_roi(cases, plus, k=1):
    roi = round((plus / cases) * 100 * k - 100, 2) if cases != 0 else 0
    return roi


def main_checks(data, q1_in=1, q2_in=1, desired=1, k=1) -> list[list, int, int]:
    positive = 0
    cases = 0
    print(len(data))
    totals_ultra_h = totals_super_h = totals_huge_h = totals_lite_h = totals_other_h = 0
    totals_ultra_h_c = totals_super_h_c = totals_huge_h_c = totals_lite_h_c = totals_other_h_c = 0  # (1 - 1.2, 1.21 - 1.4, 1.41 - 1.6, 1.6 - 1.8) home favor cases
    totals_ultra_a_c = totals_super_a_c = totals_huge_a_c = totals_lite_a_c = 0  # (1 - 1.2, 1.21 - 1.4, 1.41 - 1.6, 1.6 - 1.8) away favor cases
    totals_ultra_a = totals_super_a = totals_huge_a = totals_lite_a = 0
    cases = positive = 0

    for game in data:
        try:
            scores = game[:-2]
            k1, k2 = game[-2], game[-1]

            t1q1, t1q2, t1q3, t1q4 = [int(i) for i in scores[1:5]]
            t2q1, t2q2, t2q3, t2q4 = [int(i) for i in scores[-4:]] if len(scores) == 10 else [int(i) for i in
                                                                                              scores[-5:-1]]
            q1 = t1q1 + t2q1
            q2 = t1q2 + t2q2
            q3 = t1q3 + t2q3
            q4 = t1q4 + t2q4
            half1 = q1 + q2
            half2 = q3 + q4
        except:
            continue

        '''  check '''
        if k2:

            if t1q1 > q1_in and t2q1 > q2_in and t1q2 > q1_in and t2q2 > q2_in:
                cases += 1
                print(t1q1 + t2q1, t1q2 + t2q2, q1_in, q2_in)
                print('YES')
                if t1q3 > desired:
                    print(game, '   <- YES /// COMMON')

                    positive += 1
                else:
                    print(game, '   <- NO /// COMMON')
            else:
                print(t1q1 + t2q1, t1q2 + t2q2, q1, q2)
                print('NO')

        if 1 < k2 <= 1.2:
            if t1q1 > q1_in and t2q1 > q2_in and t1q2 > q1_in and t2q2 > q2_in:
                totals_ultra_h_c += 1
                if t1q3 > desired:
                    print(game, '   <- YES')
                    totals_ultra_h += 1
                else:
                    print(game, '   <- NO')

        if 1.2 < k2 <= 1.4:
            if t2q1 > q1_in and t2q1 > q2_in and t1q2 > q1_in and t2q2 > q2_in:
                totals_super_h_c += 1
                if t1q3 > desired:
                    print(game, '   <- YES')
                    totals_super_h += 1
                else:
                    print(game, '   <- NO')

        if 1.4 < k2 <= 1.6:
            if t1q1 > q1_in and t2q1 > q2_in and t1q2 > q1_in and t2q2 > q2_in:
                totals_huge_h_c += 1
                if t1q3 > desired:
                    print(game, '   <- YES /// HUGE')
                    totals_huge_h += 1
                else:
                    print(game, '   <- NO /// HUGE')

        if 1.6 < k2 <= 1.8:
            if t1q1 > q1_in and t2q1 > q2_in and t1q2 > q1_in and t2q2 > q2_in:
                totals_lite_h_c += 1
                if t1q3 > desired:
                    print(game, '   <- YES /// LITE')
                    totals_lite_h += 1
                else:
                    print(game, '   <- NO /// LITE')

        if k2 > 1.8:
            if t1q1 > q1_in and t2q1 > q2_in and t1q2 > q1_in and t2q2 > q2_in:
                totals_other_h_c += 1
                if t1q3 > desired:
                    print(game, '   <- YES /// OTHER')
                    totals_other_h += 1
                else:
                    print(game, '   <- NO ///  OTHER')

    roi_ultra = count_roi(totals_ultra_h_c, totals_ultra_h, k=k)
    roi_super = count_roi(totals_super_h_c, totals_super_h, k=k)
    roi_huge = count_roi(totals_huge_h_c, totals_huge_h, k=k)
    roi_lite = count_roi(totals_lite_h_c, totals_lite_h, k=k)
    roi_other = count_roi(totals_other_h_c, totals_other_h, k=k)

    print('ULTRA: :', totals_ultra_h, totals_ultra_h_c, roi_ultra)
    print('SUPER  :', totals_super_h, totals_super_h_c, roi_super)
    print('HUGE   :', totals_huge_h, totals_huge_h_c, roi_huge)
    print('LITE   :', totals_lite_h, totals_lite_h_c, roi_lite)
    print('OTHER  :', totals_other_h, totals_other_h_c, roi_other)
    print()
    print('COMMON :', positive, cases, count_roi(cases, positive, k=k))
    # print("CASES    :" ,cases)
    # print("POSITIVE :", positive)
    # print('ROI      :', count_roi(cases, positive, k = 1.7))


main_checks(clear_results, q1_in=20 ,  q2_in= 15, desired=19 , k=1.7)  # k = 1.7



