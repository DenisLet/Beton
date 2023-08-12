import re
data = ['1ST', 'HALF', '1', '-', '1', '"35"', '0', '-', '1', 'Trojak', 'M.', '"45"', '1', '-', '1', 'Meter', 'M.', '(Penalty)', '2ND', 'HALF', '2', '-', '1', '"50"', '2', '-', '1', 'Krajcek', 'K.', '"78"', '3', '-', '1', 'Horvat', 'M.', '"87"', '3', '-', '2', 'Rezic', 'I.', '(Penalty)<$>PRE-MATCH', 'ODDS', '1', '-', 'X', '-', '2', '-', '1', '2.49', 'X', '3.19', '2', '2.67', 'BET365', '-', 'Click', 'to', 'see', 'if', 'you', 'qualify', 'for', 'New', 'Customer', 'offer', 'Check', 'bet365.com', 'for', 'latest', 'offers', 'and', 'details.', 'Geo-variations', 'and', 'T&Cs', 'apply.', '18+', '1xBET', '-', '100%', 'deposit', 'bonus', 'up', 'to', '€100']
goal_times = []  # Список для хранения кортежей (счет, время)
score_changes = []
match = data[5:]
often_scores = ['10','01','11','12','21','22','20','02']
for i, el in enumerate(match):
    try:
        print()

        score_change = match[i]+match[i+2]

        goal_minute = match[i-1].replace('"','')
        if el.isdigit() and match[i+1] == '-' and match[i+2].isdigit() and goal_minute!= 'HALF':
            if '+' in goal_minute:
                if goal_minute[0] =='4':
                    goal_minute = 45
                else:
                    goal_minute = 90
            goal_times.append((score_change, int(goal_minute)))
    except:
        break

print(goal_times)
print()
lst= [[('10', 26), ('11', 66), ('21', 75)],
[('10', 21), ('11', 41), ('12', 46)],
[('01', 79)],
[('01', 23)],
[('01', 6), ('11', 18), ('12', 32), ('22', 45), ('32', 59), ('33', 90)],
[('01', 50), ('02', 79)],
[('10', 16), ('20', 59), ('30', 72), ('40', 79)],
[('10', 18), ('11', 37), ('21', 61), ('22', 64)],
[('01', 14), ('02', 22), ('03', 37), ('13', 82), ('23', 90)],
[('01', 30), ('02', 47), ('12', 53), ('13', 62), ('14', 90)]]

print('10' > '2')
