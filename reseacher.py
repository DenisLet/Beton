from sheet_with_often_scores import soccer_first_half_often
import re
import openpyxl

workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.append(('HOME', 'TEAM', 'IS', 'FAVORITE', 'OR', 'EQUAL POWER'))

file_name = "leagues/Eredivisie.txt"

fouls = ('(Foul)', '(Roughing)', '(Holding)', "(Unsportsmanlike', 'conduct)", '(Tripping)', '(Elbowing)',
         "(Delay', 'of', 'game)", '(Impeding)', '(Handling)', '(Diving)')
penalty = '(Penalty)'
penalty_missed = "(Penalty', 'missed)"
goal_dis = 'Disallowed'
own_goal = "(Own', 'goal)"





def check_scores_and_odds(file_name):

    with open(file_name, 'r') as file:
        data = file.read()
        matches = data.split('<$>')
        results_list = []
        card_list = []
        for score in soccer_first_half_often:
            for num,match in enumerate(matches):
                if num >1100:
                    break
                try:
                    cleaned_str = re.sub(r"[\[\]',]", "", match)
                    lst = cleaned_str.split()
                    index_1st, index_2nd = lst.index('1ST'), lst.index('2ND')
                    t1_h1,t1_h2,t2_h1,t2_h2 = int(lst[index_1st+2]), int(lst[index_2nd+2]),int(lst[index_1st+4]),int(lst[index_2nd+4])
                    k1, draw, k2 = float(lst[3]), float(lst[5]), float(lst[7])
                    results_list.append([t1_h1, t2_h1, t1_h2, t2_h2, k1, k2])
                except:
                    continue

                yellow_cards_h2 = 0
                if 5<k1<10\
                        and score == (t1_h1,t2_h1):

                    for el in lst[index_2nd:]:
                        if el in fouls:
                            yellow_cards_h2+=1
                    card_list.append(yellow_cards_h2)
                    # print(yellow_cards_h2)

            print(card_list)
            count_greater_than_one = sum(1 for num in card_list if num > 2)
            all_cases = len(card_list) if len(card_list)!= 0 else 1; zero_cases = card_list.count(0); one_cases = card_list.count(1)
            two_cases = card_list.count(2); greather_cases = count_greater_than_one
            if all_cases> 3:

                print(score)
                print('CASES :', all_cases)
                print('ZEROS :', zero_cases, f'     {round(zero_cases/all_cases,3)*100}%')
                print('ONE   :', one_cases, f'    {round(one_cases/all_cases,3)*100}%' )
                print('TWO+  :', two_cases + greather_cases, f'    {round((two_cases + greather_cases) / all_cases, 2) * 100}%')
                print('TWO   :', two_cases, f'    {round(two_cases/all_cases,3)*100}%')
                print('THREE+:', count_greater_than_one, f'    {round(greather_cases/all_cases,3)*100}%')

            card_list = []






    return results_list

clear_results = check_scores_and_odds(file_name)

def coef_checker(clear_results):
    ultra_home = ultra_away = super_home = super_away = huge_home = huge_away = strong_home = strong_away = lite_home = lite_away = equal_home = equal_away = 0
    for match in clear_results:
        half1_res = (match[0], match[1])
        half2_res = sum([match[2], match[3]])
        k1 = match[4]
        k2 = match[5]
        if 1 < k1 <= 1.1:
            ultra_home += 1
        if 1.1 < k1 <= 1.25:
            super_home += 1
        if 1.25 < k1 <= 1.5:
            huge_home += 1
        if 1.5 < k1 <= 1.8:
            strong_home += 1
        if 1.8 < k1 <= 2.2:
            lite_home += 1
        if k1 > 2.2 and k1 <= k2:
            equal_home += 1

    for match in clear_results:
        half1_res = (match[0], match[1])
        half2_res = sum([match[2], match[3]])
        k1 = match[4]
        k2 = match[5]
        if 1 < k2 <= 1.1:
            ultra_away += 1
        if 1.1 < k2 <= 1.25:
            super_away += 1
        if 1.25 < k2 <= 1.5:
            huge_away += 1
        if 1.5 < k2 <= 1.8:
            strong_away += 1
        if 1.8 < k2 <= 2.2:
            lite_away += 1
        if k2 > 2.2 and k2 <= k1:
            equal_away += 1

    print('ULTRA HOME:', ultra_home)
    print('SUPER HOME:', super_home)
    print('HUGE HOME:', huge_home)
    print('STRONG HOME:', strong_home)
    print('LITE HOME:', lite_home)
    print('EQUAL HOME:', equal_home)
    print()
    print('ULTRA AWAY:', ultra_away)
    print('SUPER AWAY:', super_away)
    print('HUGE AWAY:', huge_away)
    print('STRONG AWAY:', strong_away)
    print('LITE AWAY:', lite_away)
    print('EQUAL AWAY:', equal_away)






