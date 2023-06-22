from playwright.sync_api import sync_playwright
import re

s = [

['Finished', 'South', 'Sudan', 'Gambia', '2', '3', '(1)', '(1)', '6.21', '3.56', '1.70'],
['Finished', 'Sao', 'Tome', 'and', 'Principe', 'Guinea', 'Bissau', '0', '1', '(0)', '(0)', '18.30', '8.58', '1.14'],
['Finished', 'Guinea', 'Egypt', '1', '2', '(1)', '(1)', '4.99', '2.70', '2.10'],
['After', 'ET', 'Netherlands', 'Croatia', '2', '4', '(1)', '(0)', '2', '2', '1.75', '3.60', '4.75'],
['Finished', 'Saoura', 'U21', 'Kabylie', 'U21', '2', '1', '(0)', '(1)', '1.65', '3.71', '4.86'],
['Finished', 'Atl.', 'Tucuman', 'Godoy', 'Cruz', '2', '1', '(1)', '(0)', '2.25', '3.00', '3.60'],
['Finished', 'Gimnasia', 'L.P.', 'Huracan', '1', '0', '(0)', '(0)', '2.90', '2.75', '2.88'],
['Finished', 'Patronato', 'Almirante', 'Brown', '0', '1', '(0)', '(0)', '1.95', '3.20', '4.33'],
['Finished', 'Midland', 'Puerto', 'Nuevo', '2', '1', '(1)', '(0)', '1.74', '3.34', '5.18'],
['Finished', 'Aldosivi', 'San', 'Martin', 'S.J.', '0', '1', '(0)', '(0)', '3.12', '3.01', '2.38'],
['Finished', 'Velez', 'Sarsfield', '2', 'Racing', 'Club', '2', '3', '0', '(2)', '(0)', '1.62', '3.60', '5.75'],
['Finished', 'El', 'Porvenir', 'W', 'River', 'Plate', 'W', '0', '3', '(0)', '(1)', '11.20', '5.10', '1.28'],
['Finished', 'Oman', 'Tajikistan', '1', '1', '(1)', '(1)', '1.88', '3.34', '4.39'],
['Finished', 'Turkmenistan', 'Uzbekistan', '0', '2', '(0)', '(0)', '16.20', '7.38', '1.16'],
['Cancelled', 'BSK', 'Banja', 'Luka', 'Modrica', '-', '-', '-', '-', '-'],
['Finished', 'Nevesinje', 'Drina', 'Zvornik', '1', '0', '(0)', '(0)', '-', '-', '-'],
['Finished', 'Oratorio', 'Macapa', '0', '1', '(0)', '(1)', '1.12', '10.00', '13.70'],
['Finished', 'Arturo', 'Fernandez', 'Vial', 'Iberia', '0', '1', '(0)', '(0)', '1.69', '3.37', '5.51'],
['Finished', 'Domazlice', 'Zizkov', '0', '0', '(0)', '(0)', '4.43', '4.30', '1.64'],
['Finished', 'Lisen', 'B', 'Boskovice', '2', '1', '(2)', '(1)', '-', '-', '-'],
['Finished', 'Sparta', 'Brno', 'Ratiskovice', '6', '3', '(3)', '(0)', '-', '-', '-'],
['Finished', 'Ostrov', 'Nejdek', '7', '0', '(4)', '(0)', '-', '-', '-'],
['Finished', 'Cerveny', 'Kostelec', 'Kostelec', 'n.', 'O.', '2', '0', '(2)', '(0)', '-', '-', '-'],
['Finished', 'Holice', 'Ceska', 'Trebova', '1', '2', '(1)', '(0)', '-', '-', '-'],
['Finished', 'America', 'de', 'Quito', 'Ind.', 'Juniors', '3', '2', '(2)', '(0)', '2.90', '2.97', '2.58'],
['Finished', 'Nueve', 'de', 'Octubre', 'Imbabura', '4', '2', '(3)', '(1)', '2.09', '3.24', '3.55'],
['Finished', 'Tamya', 'Fayoum', '1', '4', '-', '-', '-'],
['Finished', 'Al', 'Magd', 'Gomhoriat', 'Shebin', '2', '1', '(0)', '(0)', '-', '-', '-'],
['Finished', 'Alexandria', 'SC', 'Abu', 'Qir', 'Semad', '2', '1', '(0)', '(0)', '2.44', '3.14', '2.80'],
['Finished', 'Dekernes', 'Baladiyat', 'El', 'Mahalla', '0', '4', '(0)', '(3)', '-', '-', '-'],
['Finished', 'El', 'Dabaa', 'Salloum', '0', '1', '(0)', '(1)', '1.62', '3.72', '5.17'],
['Finished', 'El', 'Olympi', 'Pioneers', '0', '2', '(0)', '(0)', '2.25', '3.10', '3.21'],
['Finished', 'Kafr', 'El', 'Sheikh', 'Al', 'Hammam', '1', '0', '(1)', '(0)', '-', '-', '-'],
['Finished', 'Nabarouh', 'Proxy', '1', '3', '(0)', '(1)', '4.99', '3.54', '1.68'],
['Finished', 'Tanta', 'El', 'Mansoura', '2', '1', '(0)', '(1)', '-', '-', '-'],
['Finished', 'Flora', 'W', 'Polva', 'Lootos', 'W', '9', '0', '(5)', '(0)', '-', '-', '-'],
['Finished', 'Bavaria', '(Am)', '(Ger)', 'Galicia', '(Am)', '(Esp)', '0', '1', '(0)', '(1)', '-', '-', '-'],
['Finished', 'Belgrade', '(Am)', '(Srb)', 'Lisboa', '(Am)', '(Por)', '2', '1', '(1)', '(0)', '-', '-', '-'],
['Finished', 'Dolny', 'Slask', '(Am)', '(Pol)', 'Zlin', '(Am)', '(Cze)', '0', '0', '(0)', '(0)', '-', '-', '-'],
['Finished', 'Ireland', '(Am)', '(Eur)', 'Zenica-Doboj', 'Canton', '(Am)', '(Bih)', '1', '1', '(0)', '(1)', '-', '-', '-'],
['Finished', 'Kyzyltash', 'Alushta', '4', '3', '(2)', '(0)', '-', '-', '-'],
['Finished', 'TSK', 'Simferopol', 'Rubin', 'Yalta', '3', '1', '(0)', '(0)', '-', '-', '-'],
['Finished', 'FC', 'Sevastopol', 'Chernomorets', 'Sevastopol', '5', '1', '(4)', '(0)', '-', '-', '-'],
['Finished', 'Ocean', 'Kerch', 'Sparta-KT', '1', '0', '(0)', '(0)', '-', '-', '-'],
['Finished', 'An', 'der', 'Fahner', 'Hohe', 'MSV', 'Neuruppin', '6', '0', '(4)', '(0)', '-', '-', '-'],
['After', 'Pen.', 'TUS', 'Dietkirchen', 'Bornheim', 'GW', '2', '1', '(0)', '(0)', '1', '1', '-', '-', '-'],
['Finished', 'Grossaspach', 'TuS', 'Koblenz', '2', '2', '(0)', '(0)', '1.93', '3.64', '3.64'],
['Finished', 'Giouchtas', 'Kampaniakos', '1', '1', '(1)', '(0)', '1.91', '3.39', '3.97'],
['Finished', 'Kozani', 'FC', 'Tilikratis', 'L.', '1', '0', '(1)', '(0)', '1.19', '6.50', '9.30'],
['Finished', 'Vissel', 'Kobe', 'Nagano', '3', '1', '(2)', '(1)', '1.17', '7.50', '10.00'],
['Finished', 'Chabab', 'Mohammedia', 'Maghreb', 'Fez', '3', '0', '(1)', '(0)', '1.80', '2.88', '4.50'],
['Finished', 'Difaa', 'El', 'Jadidi', 'Mouloudia', 'Oujda', '0', '1', '(0)', '(0)', '2.40', '2.60', '3.25'],
['Finished', 'FAR', 'Rabat', 'Olympique', 'Khouribga', '1', '0', '(0)', '(0)', '1.29', '4.20', '10.00'],
['Finished', 'Hassania', 'Agadir', 'Wydad', '0', '0', '(0)', '(0)', '6.50', '3.50', '1.50'],
['Finished', 'Moghreb', 'Tetouan', 'Jeunesse', 'Sportive', 'Soualem', '1', '2', '(1)', '(2)', '2.00', '3.10', '3.50'],
['Finished', 'Olympique', 'de', 'Safi', 'FUS', 'Rabat', '0', '1', '(0)', '(0)', '2.75', '2.55', '2.80'],
['Finished', 'Raja', 'Casablanca', 'Berkane', '2', '1', '(1)', '(0)', '1.67', '3.40', '5.00'],
['Finished', 'Union', 'Touarga', 'IR', 'Tanger', '2', '2', '(1)', '(2)', '4.00', '3.25', '1.80'],
['Finished', 'SteDoCo', 'VVSB', '1', '0', '(1)', '(0)', '2.60', '3.74', '2.39'],
['Finished', 'Gateway', 'Utd.', 'Crown', 'FC', '1', '0', '(0)', '(0)', '-', '-', '-'],
['Finished', 'Ijebu', 'Joy', 'Cometh', '3', '1', '(1)', '(1)', '-', '-', '-'],
['Finished', 'Sporting', 'Lagos', 'Smart', 'City', '4', '0', '(1)', '(0)', '1.36', '4.20', '9.40'],
['Finished', 'Swit', 'Skolwin', 'Cartusia', 'Kartuzy', '0', '2', '(0)', '(0)', '1.53', '4.22', '5.80'],
['Finished', 'Rakow', '2', 'Gornik', 'Zabrze', '2', '3', '2', '(0)', '(0)', '1.68', '4.97', '3.77'],
['Postponed', 'FC', 'Johansen', 'Mighty', 'Blackpool', '-', '-', '-', '-', '-'],
['Postponed', 'Freetown', 'City', 'Bo', 'Rangers', '-', '-', '-', '-', '-'],
['Postponed', 'Luawa', 'Diamond', 'Stars', '-', '-', '-', '-', '-'],
['Postponed', 'SLIFA', 'Old', 'Edwardians', '-', '-', '-', '-', '-'],
['Finished', 'Wusum', 'Stars', 'Bai', 'Bureh', 'Warriors', '5', '0', '(2)', '(0)', '-', '-', '-'],
['Postponed', 'Wusum', 'Stars', 'Kamboi', 'Eagles', '-', '-', '-', '-', '-'],
['Finished', 'Ariana', 'Angelholm', '1', '0', '(0)', '(0)', '1.46', '4.75', '5.81'],
['Finished', 'Korsnas', 'Sandviken', '0', '6', '(0)', '(1)', '-', '-', '-'],
['Finished', 'Kalmar', 'W', 'Rosengard', 'W', '0', '5', '(0)', '(5)', '25.00', '10.80', '1.04'],
['Finished', 'Vittsjo', 'W', 'Pitea', 'W', '3', '1', '(0)', '(0)', '2.44', '3.38', '2.66'],
['Finished', 'Veres-Rivne', 'MFC', 'Metalurh', '6', '1', '(3)', '(0)', '1.39', '4.29', '9.60'],
['Finished', 'LNZ', 'Cherkasy', 'Inhulets', '2', '1', '(2)', '(0)', '2.75', '2.90', '2.90'],
['Finished', 'New', 'England', 'Revolution', 'II', 'New', 'York', 'City', 'II', '1', '0', '(0)', '(0)', '2.08', '3.94', '2.90'],
['Finished', 'Albany', 'Rush', 'Vermont', 'Green', '0', '2', '(0)', '(0)', '8.18', '6.14', '1.28'],
['Finished', 'Virginia', 'Beach', 'Christos', '4', '0', '(2)', '(0)', '-', '-', '-'],
['Finished', 'Wake', 'FC', 'West', 'Virginia', '2', '2', '(1)', '(2)', '2.84', '3.92', '2.17'],
['Finished', 'Asheville', 'City', 'Bantams', '3', '0', '(2)', '(0)', '1.57', '4.61', '4.61'],
['Finished', 'Houston', 'FC', 'AHFC', 'Royals', '1', '2', '(1)', '(0)', '3.26', '4.28', '1.89'],
['Finished', 'Tennessee', 'Southern', 'Soccer', 'Academy', '2', '0', '(1)', '(0)', '1.58', '4.32', '4.89'],
['Finished', 'Tampa', 'Bay', 'U23', 'Florida', 'Elite', '0', '0', '(0)', '(0)', '4.28', '3.50', '1.72'],
['Finished', 'Swan', 'City', 'Brevard', 'SC', '1', '1', '(0)', '(1)', '-', '-', '-'],
['Finished', 'New', 'Jersey', 'Copa', 'Westchester', '2', '0', '(0)', '(0)', '1.58', '4.65', '4.31'],
['Finished', 'Mozambique', 'Malawi', '1', '1', '(0)', '(0)', '-', '-', '-'],
['Finished', 'Romania', 'U17', 'Austria', 'U17', '3', '0', '(0)', '(0)', '-', '-', '-'],
['Finished', 'Latvia', 'U19', 'Lithuania', 'U19', '3', '0', '(2)', '(0)', '-', '-', '-'],
['Finished', 'Pakistan', 'Kenya', '0', '1', '(0)', '(1)', '-', '-', '-'],
['Finished', 'Indonesia', 'Palestine', '0', '0', '(0)', '(0)', '2.30', '3.20', '3.00'],
['Finished', 'Netherlands', 'U21', 'Japan', 'U22', '0', '0', '(0)', '(0)', '-', '-', '-'],
['Finished', 'Malaysia', 'Solomon', 'Islands', '4', '1', '(2)', '(1)', '1.20', '6.50', '13.00'],
['Finished', 'Togo', 'Lesotho', '2', '0', '(2)', '(0)', '-', '-', '-'],
['Finished', 'Mauritius', 'Djibouti', '1', '3', '(1)', '(0)', '1.84', '3.48', '4.45'],
['Finished', 'United', 'Arab', 'Emirates', 'U23', 'Jordan', 'U23', '1', '2', '(1)', '(0)', '2.60', '2.90', '2.60'],
['Finished', 'D.R.', 'Congo', 'Uganda', '1', '0', '(1)', '(0)', '2.15', '2.88', '3.40'],
['Finished', 'Finland', 'U19', 'Estonia', 'U19', '2', '1', '(0)', '(0)', '-', '-', '-'],
['Finished', 'Albania', 'U19', 'Kosovo', 'U19', '1', '0', '(0)', '(0)', '2.27', '3.30', '2.81'],
['Finished', 'Iran', 'U23', 'Syria', 'U23', '3', '1', '(3)', '(1)', '1.50', '3.40', '6.50'],
['Finished', 'Yemen', 'U23', 'Oman', 'U23', '0', '3', '(0)', '(1)', '8.50', '4.00', '1.36'],
['Finished', 'Necaxa', '(Mex)', 'Celaya', '(Mex)', '2', '0', '-', '-', '-']
]




# for line in s:
#     home_coef, draw_coef, away_coef = [float(i) if '.' in i else 0 for i in line[-3:]]
#     print(line)
#     try:
#         team1_1half, team2_1half = re.findall(r'\(\d\)', ' '.join(line))
#         mark = line.index(team1_1half)
#         if 'After' not in line:
#             team1_all = int(line[mark - 2])
#             team2_all = int(line[mark - 1])
#         else:
#             team1_all = int(line[mark + 2])
#             team2_all = int(line[mark + 3])
#
#         team1_1half = int(team1_1half.strip('()'))
#         team2_1half = int(team2_1half.strip('()'))
#
#     except:
#         team1_1half, team2_1half, team1_all, team2_all = -1, -1, -1, -1
#     print(team1_1half, team2_1half, team1_all, team2_all)
# results = [(1, 1, 2, 2), (1, 2, 2, 2), (0, 0, 1, 0), (3, 0, 4, 1), (0, 0, 0, 0), (1, 2, 2, 3)]
#
# score_dict = {}
#
# for match in results:
#     first_half_score = (match[0], match[1])
#     second_half_goals = (match[2], match[3])
#
#     if first_half_score not in score_dict:
#         score_dict[first_half_score] = [1, 0, 0]
#     else:
#         score_dict[first_half_score][0] += 1
#
#     if second_half_goals[0] == 1:
#         score_dict[first_half_score][1] += 1
#     if second_half_goals[0] > 1:
#         score_dict[first_half_score][2] += 1
#
# score_dict = {key: tuple(value) for key, value in score_dict.items()}
#
# print(score_dict)


# coefs = (6, 3, 1.49)
# is_favorite = True if 1<coefs[0] < 1.5 or 1<coefs[2]<1.5 else False
# print(is_favorite)