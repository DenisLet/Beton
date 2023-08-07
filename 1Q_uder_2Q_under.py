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

                if num > 4000:
                    break
                cleaned_str = re.sub(r"[\[\]',]", "", match)
                lst = cleaned_str.split()
                scores = []
                # print(lst)
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


    print(len(data))
    totals_ultra_h = totals_super_h = totals_huge_h = totals_lite_h = totals_other_h = 0
    totals_ultra_h_c = totals_super_h_c = totals_huge_h_c = totals_lite_h_c = totals_other_h_c = 0 # (1 - 1.2, 1.21 - 1.4, 1.41 - 1.6, 1.6 - 1.8) home favor cases
    totals_ultra_a_c = totals_super_a_c = totals_huge_a_c = totals_lite_a_c = totals_other_a_c =0    # (1 - 1.2, 1.21 - 1.4, 1.41 - 1.6, 1.6 - 1.8) away favor cases
    totals_ultra_a = totals_super_a = totals_huge_a = totals_lite_a =totals_other_a = 0
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
        if  k1:

            if team1_input<=q1 <= team2_input :
                cases_h += 1
                if q2 <  desired :
                    positive_h += 1
                else:
                    True
            else:
                True

        if  1 < k1 <= 1.2:
            if team1_input<=q1 <= team2_input :
                totals_ultra_h_c += 1
                if q2 < desired:
                    print(game, '   <- YES')
                    totals_ultra_h += 1
                else:
                    print(game, '   <- NO')

        if  1.2 < k1 <= 1.4:
            if team1_input<=q1 <= team2_input :
                totals_super_h_c += 1
                if q2 < desired :
                    print(game, '   <- YES')
                    totals_super_h +=1
                else:
                    print(game, '   <- NO')


        if  1.4 < k1 <= 1.6:
            if team1_input<=q1 <= team2_input :
                totals_huge_h_c += 1
                if q2 < desired :
                    print(game, '   <- YES /// HUGE')
                    totals_huge_h +=1
                else:
                    print(game, '   <- NO /// HUGE')


        if  1.6< k1 <= 1.8:
            if team1_input<=q1 <= team2_input :
                totals_lite_h_c += 1
                if q2 < desired :
                    print(game, '   <- YES /// LITE')
                    totals_lite_h +=1
                else:
                    print(game, '   <- NO /// LITE')

        if  k1 > 1.8:
            if team1_input<=q1 <= team2_input :
                totals_other_h_c += 1
                if q2 < desired :
                    print(game, '   <- YES /// OTHER')
                    totals_other_h +=1
                else:
                    print(game, '   <- NO ///  OTHER')

        if  k2:

            if team1_input<=q1 <= team2_input :
                cases_a += 1
                if q2 <  desired :
                    positive_a += 1
                else:
                    True
            else:
                True

        if  1 < k2 <= 1.2:
            if team1_input<=q1 <= team2_input :
                totals_ultra_a_c += 1
                if q2 < desired:
                    print(game, '   <- YES')
                    totals_ultra_a += 1
                else:
                    print(game, '   <- NO')

        if  1.2 < k2 <= 1.4:
            if team1_input<=q1 <= team2_input :
                totals_super_a_c += 1
                if q2 < desired :
                    print(game, '   <- YES')
                    totals_super_a +=1
                else:
                    print(game, '   <- NO')


        if  1.4 < k2 <= 1.6:
            if team1_input<=q1 <= team2_input :
                totals_huge_a_c += 1
                if q2 < desired :
                    print(game, '   <- YES /// HUGE')
                    totals_huge_a +=1
                else:
                    print(game, '   <- NO /// HUGE')


        if  1.6< k2 <= 1.8:
            if team1_input<=q1 <= team2_input :
                totals_lite_a_c += 1
                if q2 < desired :
                    print(game, '   <- YES /// LITE')
                    totals_lite_a +=1
                else:
                    print(game, '   <- NO /// LITE')

        if  k2 > 1.8:
            if team1_input<=q1 <= team2_input :
                totals_other_a_c += 1
                if q2 < desired :
                    print(game, '   <- YES /// OTHER')
                    totals_other_a +=1
                else:
                    print(game, '   <- NO ///  OTHER')


    roi_ultra_h  = count_roi(totals_ultra_h_c, totals_ultra_h, k = k)
    roi_super_h = count_roi(totals_super_h_c, totals_super_h, k= k)
    roi_huge_h = count_roi(totals_huge_h_c, totals_huge_h, k=k)
    roi_lite_h = count_roi(totals_lite_h_c, totals_lite_h, k=k)
    roi_other_h = count_roi(totals_other_h_c, totals_other_h, k=k)

    roi_ultra_a  = count_roi(totals_ultra_a_c, totals_ultra_a, k = k)
    roi_super_a = count_roi(totals_super_a_c, totals_super_a, k= k)
    roi_huge_a = count_roi(totals_huge_a_c, totals_huge_a, k=k)
    roi_lite_a = count_roi(totals_lite_a_c, totals_lite_a, k=k)
    roi_other_a = count_roi(totals_other_a_c, totals_other_a, k=k)
    print()
    print('HOME FOCUS', 'CONFIG:',f'K:{k}, 1Q(UNDER inc.):{team1_input} - {team2_input}, BET 2Q UNDER:{desired}')
    print('ULTRA: :', totals_ultra_h, totals_ultra_h_c, roi_ultra_h)
    print('SUPER  :', totals_super_h, totals_super_h_c, roi_super_h)
    print('HUGE   :', totals_huge_h, totals_huge_h_c, roi_huge_h)
    print('LITE   :', totals_lite_h, totals_lite_h_c, roi_lite_h)
    print('OTHER  :', totals_other_h, totals_other_h_c, roi_other_h)
    print('COMMON :', positive_h, cases_h, count_roi(cases_h, positive_h, k = k))
    print('AWAY FOCUS')
    print('ULTRA: :', totals_ultra_a, totals_ultra_a_c, roi_ultra_a)
    print('SUPER  :', totals_super_a, totals_super_a_c, roi_super_a)
    print('HUGE   :', totals_huge_a, totals_huge_a_c, roi_huge_a)
    print('LITE   :', totals_lite_a, totals_lite_a_c, roi_lite_a)
    print('OTHER  :', totals_other_a, totals_other_a_c, roi_other_a)
    print('COMMON :', positive_a, cases_a, count_roi(cases_a, positive_a, k = k))

    # print("CASES    :" ,cases)
    # print("POSITIVE :", positive)
    # print('ROI      :', count_roi(cases, positive, k = 1.7))
main_checks(clear_results, team1_input =0 , team2_input = 30 ,desired= 40,k = 1.7) # k = 1.7



