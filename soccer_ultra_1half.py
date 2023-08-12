from sheet_with_often_scores import soccer_first_half_often
import re

file_name = "leagues_soccer_made/Ykkonen.txt"
to_doc = file_name.split('/')[1]

def check_scores_and_odds(file_name):

    with open(file_name, 'r') as file:
        data = file.read()
        matches = data.split('\n')
        results_list = []
        lst_list = []

        for num,match in enumerate(matches):
            try:
                if num > 4800:
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

            except:
                continue

    return results_list


clear_results = check_scores_and_odds(file_name)

cases_ultra_h = cases_super_h = cases_huge_h = 0
cases_null_ultra_h = cases_null_super_h = cases_null_huge_h = 0
cases_ultra_a = cases_super_a = cases_huge_a = 0
cases_null_ultra_a = cases_null_super_a = cases_null_huge_a = 0


for match in clear_results:
        half1_res = (match[0], match[1])
        half2_res = sum([match[2], match[3]])
        k1 = match[4]
        k2 = match[5]
        if 1 < k1 <= 1.15:
            cases_null_ultra_h += 1
            if half1_res == (0, 0):
                cases_ultra_h += 1

        if 1.1 < k1 <= 1.25:
            cases_null_super_h += 1
            if half1_res == (0, 0):
                cases_super_h += 1

        if 1.25 < k1 <= 1.5:
            cases_null_huge_h += 1
            if half1_res == (0, 0):
                cases_huge_h += 1

        if 1 < k2 <= 1.3:
            cases_null_ultra_a += 1
            if half1_res == (0, 0):
                cases_ultra_a += 1

        if 1.1 < k2 <= 1.25:
            cases_null_super_a += 1
            if half1_res == (0, 0):
                cases_super_a += 1

        if 1.25 < k2 <= 1.5:
            cases_null_huge_a += 1
            if half1_res == (0, 0):
                cases_huge_a += 1



print(len(clear_results))
try:
    print('ULTRA HOME %: ', cases_ultra_h,cases_null_ultra_h, round((cases_null_ultra_h - cases_ultra_h)*100/cases_null_ultra_h,1))
    print('SUPER HOME %: ', cases_super_h,cases_null_super_h, round((cases_null_super_h - cases_super_h)*100/cases_null_super_h,1))
    print('HUGE HOME %: ', cases_huge_h,cases_null_huge_h, round((cases_null_huge_h - cases_huge_h)*100/cases_null_huge_h,1))
except:
    True


print()
try:
    print('ULTRA AWAY %: ', cases_ultra_a,cases_null_ultra_a, round((cases_null_ultra_a - cases_ultra_a)*100/cases_null_ultra_a,1))
    print('SUPER AWAY %: ', cases_super_a,cases_null_super_a, round((cases_null_super_a - cases_super_a)*100/cases_null_super_a,1))
    print('HUGE AWAY %: ', cases_huge_a,cases_null_huge_a, round((cases_null_huge_a - cases_huge_a)*100/cases_null_huge_a,1))
except:
    True

print()
print(to_doc)
if round((cases_null_ultra_h - cases_ultra_h)*100/cases_null_ultra_h,1) >87:
    print('ULTRA HOME %: ', cases_ultra_h,cases_null_ultra_h, round((cases_null_ultra_h - cases_ultra_h)*100/cases_null_ultra_h,1))
if round((cases_null_super_h - cases_super_h)*100/cases_null_super_h,1)>85:
    print('SUPER HOME %: ', cases_super_h, cases_null_super_h,
          round((cases_null_super_h - cases_super_h) * 100 / cases_null_super_h, 1))
if round((cases_null_huge_h - cases_huge_h)*100/cases_null_huge_h,1)> 80:
    print('HUGE HOME %: ', cases_huge_h, cases_null_huge_h,
          round((cases_null_huge_h - cases_huge_h) * 100 / cases_null_huge_h, 1))
if round((cases_null_ultra_a - cases_ultra_a)*100/cases_null_ultra_a,1)>87:
    print('ULTRA AWAY %: ', cases_ultra_a, cases_null_ultra_a,
          round((cases_null_ultra_a - cases_ultra_a) * 100 / cases_null_ultra_a, 1))
if round((cases_null_super_a - cases_super_a)*100/cases_null_super_a,1)>85:
    print('SUPER AWAY %: ', cases_super_a, cases_null_super_a,
          round((cases_null_super_a - cases_super_a) * 100 / cases_null_super_a, 1))
if round((cases_null_huge_a - cases_huge_a)*100/cases_null_huge_a,1) >80:
    print('HUGE AWAY %: ', cases_huge_a, cases_null_huge_a,
          round((cases_null_huge_a - cases_huge_a) * 100 / cases_null_huge_a, 1))