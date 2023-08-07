from sheet_with_often_scores import soccer_first_half_often
import re
import openpyxl

file_name = "leaguesBB/WNBA.txt"

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

def count_roi(cases, plus, k = 1):
    roi = round((plus / cases)*100 * k - 100, 2) if cases!= 0 else 0
    return roi

def main_checks(data, team1_input = 1, team2_input= 1, desired = 1, k = 1) -> list[list, int, int]:

    positive= 0
    cases = 0
    print(len(data))
    totals_ultra_h = totals_super_h = totals_alt_h = 0
    totals_ultra_a = totals_super_a = totals_alt_a = 0
    totals_ultra_h_c = totals_super_h_c = totals_alt_h_c = 0 # (1 - 1.2, 1.21 - 1.4, 1.41 - 1.6, 1.6 - 1.8) home favor cases
    totals_ultra_a_c = totals_super_a_c = totals_alt_a_c = 0    # (1 - 1.2, 1.21 - 1.4, 1.41 - 1.6, 1.6 - 1.8) away favor cases

    cases_h = positive_a = positive_h = cases_a =0

    for game in data:


        try:
            scores = game[:-2]
            k1, k2 = game[-2], game[-1]

            t1q1, t1q2, t1q3, t1q4 = [int(i) for i in scores[1:5]]
            t2q1, t2q2, t2q3, t2q4 = [int(i) for i in scores[-4:]] if len(scores) == 10 else [int(i) for i in scores[-5:-1]]
            q1 = t1q1 + t2q1
            q2 = t1q2 + t2q2
            q3 = t1q3 + t2q3
            q4 = t1q4 + t2q4
            half1 = q1 + q2
            half2 = q3 + q4
        except:
            continue

        '''  check '''

        print('-----')
        print(k1, k2)
        if  1 < k1 <= 1.2:
            if True:
                totals_ultra_h_c += 1
                if t1q1 > team1_input :
                    print(game, '   <- YES HOME ULTRA LOST')
                    totals_ultra_h += 1
                else:
                    print(game, '   <- NO HOME ULTRA LOST')

        if  1.2 < k1 <= 1.4:
            if True:
                totals_super_h_c += 1
                if t1q1 > team1_input :
                    print(game, '   <- YES HOME SUPER LOST')
                    totals_super_h +=1
                else:
                    print(game, '   <- NO HOME SUPER LOST')

        if  1.22 < k1 <= 1.45:                      # !!!!!!!!!!!!!!!!!!!!
            if True:
                totals_alt_h_c += 1
                if t1q1 > team1_input :
                    print(game, '   <- YES HOME ALT LOST')
                    totals_alt_h +=1
                else:
                    print(game, '   <- NO HOME ALT LOST')



        if  1 < k2 <= 1.2:
            if True:
                totals_ultra_a_c += 1
                if t2q1 > team1_input :
                    print(game, '   <- YES AWAY ULTRA LOST')
                    totals_ultra_a += 1
                else:
                    print(game, '   <- NO AWAY ULTRA LOST')

        if  1.2 < k2 <= 1.4:
            if True:
                totals_super_a_c += 1
                if t2q1 > team1_input:
                    print(game, '   <- YES AWAY SUPER LOST')
                    totals_super_a +=1
                else:
                    print(game, '   <- NO AWAY SUPER LOST')

        if  1.6< k2 <= 1.8:
            if True:
                totals_alt_a_c += 1
                if t2q1 > team1_input:
                    print(game, '   <- YES AWAY ALT LOST')
                    totals_alt_a +=1
                else:
                    print(game, '   <- NO AWAY ALT LOST')



    roi_ultra_h  = count_roi(totals_ultra_h_c, totals_ultra_h, k = k)
    roi_super_h = count_roi(totals_super_h_c, totals_super_h, k= k)
    roi_alt_h = count_roi(totals_alt_h_c, totals_alt_h, k =k)

    roi_ultra_a  = count_roi(totals_ultra_a_c, totals_ultra_a, k = k)
    roi_super_a = count_roi(totals_super_a_c, totals_super_a, k= k)
    roi_alt_a = count_roi(totals_alt_a_c, totals_alt_a, k=k)

    print('HOME FOCUS')
    print('ULTRA: :', totals_ultra_h, totals_ultra_h_c, roi_ultra_h)
    print('SUPER  :', totals_super_h, totals_super_h_c, roi_super_h)
    print('ALT    :', totals_alt_h, totals_alt_h_c ,roi_alt_h)
    # print('HUGE   :', totals_huge_h, totals_huge_h_c, roi_huge)
    # print('LITE   :', totals_lite_h, totals_lite_h_c, roi_lite)
    # print('OTHER  :', totals_other_h, totals_other_h_c, roi_other)
    print()
    print('AWAY FOCUS')
    print('ULTRA: :', totals_ultra_a, totals_ultra_a_c, roi_ultra_a)
    print('SUPER  :', totals_super_a, totals_super_a_c, roi_super_a)
    print('ALT    :', totals_alt_a, totals_alt_a_c ,roi_alt_a)
    # print('COMMON :', positive, cases, count_roi(cases, positive, k = k))
    # print("CASES    :" ,cases)
    # print("POSITIVE :", positive)
    # print('ROI      :', count_roi(cases, positive, k = 1.7))
main_checks(clear_results, team1_input = 10 , team2_input = 15 ,desired= 42,k = 1.8) # k = 1.7



