import csv
import re

def_dict = {
  'Base': 13,
  'Aerials won': 1.9,
  'Aerials lost': -1.5,
  'Tackles': 2.7,
  'Dribbled past': -1.6,
  'Interceptions': 2.7,
  'Clearances': 1.1,
  'Conceded': -5,
  'Fouls': -0.6,
  'Offsides': -0.6,
  'Own goals': -3.5,
  'Error led to shot': -5,
  'Error lead to goal': -5,
  'Passes': 1 / 9,
  'Missed passes': -1 / 4.5,
  'KP': 2.5,
  'Dribbles won': 2.5,
  'Dribbles lost': -0.8,
  'Blocked shots': 1.1,
  'BCC': 1.5,
  'Crosses': 1.2,
  'Shots off': 0.5,
  'Shots blocked': 0.5,
  'Shots on': 2.5,
  'Woodwork': 3,
  'Minutes played': 1 / 30,
  'Goals': 10,
  'Assists': 8,
  'Clearance off line': 3,
  'Red cards': -5,
  'Penalty miss': -5,
  'Penalty committed': -5
}

mid_dict = {
  'Base': 7,
  'Aerials won': 1.63,
  'Aerials lost': -1.5,
  'Tackles': 2.6,
  'Dribbled past': -1.2,
  'Interceptions': 2.5,
  'Clearances': 1.1,
  'Conceded': -2,
  'Team goals': 2,
  'Fouls': -0.55,
  'Offsides': -0.55,
  'Own goals': -3.3,
  'Error led to shot': -5,
  'Error lead to goal': -5,
  'Passes': 1 / 6.65,
  'Missed passes': -1 / 3.2,
  'KP': 2.5,
  'Dribbles won': 2.9,
  'Dribbles lost': -0.8,
  'Blocked shots': 1.1,
  'BCC': 1.5,
  'Crosses': 1.2,
  'Shots off': 0.25,
  'Shots blocked': 0.25,
  'Shots on': 2.2,
  'Woodwork': 3,
  'Minutes played': 1 / 30,
  'Goals': 10,
  'Assists': 8,
  'Clearance off line': 3,
  'Red cards': -5,
  'Penalty miss': -5,
  'Penalty committed': -5
}

att_dict = {
  'Base': 5,
  'Aerials won': 1.4,
  'Aerials lost': -0.4,
  'Tackles': 2.6,
  'Dribbled past': -1,
  'Interceptions': 2.7,
  'Clearances': 0.8,
  'Team goals': 3,
  'Fouls': -0.5,
  'Offsides': -0.5,
  'Own goals': -3,
  'Error led to shot': -5,
  'Error lead to goal': -5,
  'Passes': 1 / 6,
  'Missed passes': -1 / 8,
  'KP': 2.5,
  'Dribbles won': 3,
  'Dribbles lost': -1,
  'Blocked shots': 0.8,
  'BCC': 1.5,
  'Crosses': 1.2,
  'Shots off': -0.3,
  'Shots blocked': -0.3,
  'Shots on': 3,
  'Woodwork': 3,
  'Minutes played': 1 / 30,
  'Goals': 10,
  'Assists': 8,
  'Clearance off line': 3,
  'Red cards': -5,
  'Penalty miss': -5,
  'Penalty committed': -5
}

base_dict = {"GKP": 'L', "DEF": def_dict, "MID": mid_dict, "ATT": att_dict}


def calc_gkp(lst, tg, conc):
  score = 0
  score += 20 - (conc * 5)
  score += brackets(
    lst[lst.index('Aerial duels (won)') + 1])[0] * 1.9 - brackets(
      lst[lst.index('Aerial duels (won)') + 1])[1] * 1.5
  score += check(lst, 'Total tackles') * 2.7
  score -= 2 * check(lst, 'Dribbled past') * 0.8
  score += check(lst, 'Interceptions') * 2.7
  score += check(lst, 'Clearances') * 1.1
  score += check(lst, 'Fouls') * 0.6 - (check(
    lst, 'Error led to shot') * 5) - (check(lst, 'Error led to goal') * 5)
  score += slashes(lst[lst.index('Accurate passes') + 1])[0] * (1 / 6) - slashes(
    lst[lst.index('Accurate passes') + 1])[1] * (1 / 12)
  score += check(lst, 'Key passes') * 2.5
  score += brackets(
    lst[lst.index('Dribble attempts (succ.)') + 1])[0] * 2.5 - brackets(
      lst[lst.index('Dribble attempts (succ.)') + 1])[1] * 0.8
  score += check(lst, 'Blocked shots') * 1.1
  score += int(lst[lst.index('Minutes played') + 1][:-1]) * (1 / 30)
  score += check(lst, 'Penalty committed') * -5
  score += check(lst, 'Penalties saved') * 8
  score += check(lst, 'Penalty shootout saves') * 4
  score += check(lst, 'Penalty shootout saves') * 4
  score += check(lst, 'Saves') * 1.5
  score += check(lst, 'Saves from inside box') * 1.25
  score += check(lst, 'High claims') * 1.75
  return round(score, 2)


def calc_def(lst, tg, conc):
  score = 0
  score += brackets(
    lst[lst.index('Aerial duels (won)') + 1])[0] * 1.9 - brackets(
      lst[lst.index('Aerial duels (won)') + 1])[1] * 1.5
  score += check(lst, 'Total tackles') * 2.7
  score -= 2 * check(lst, 'Dribbled past') * 0.8
  score += check(lst, 'Interceptions') * 2.7
  score += check(lst, 'Clearances') * 1.1
  score += 10 - (conc * 5)
  score += 3 - (check(lst, 'Fouls') * 0.6) - (check(lst, 'Offsides') * 0.6) - (
    check(lst, 'Own goals') * 3.5) - (check(lst, 'Error led to shot') * 5) - (
      check(lst, 'Error led to goal') * 5)
  score += slashes(lst[lst.index('Accurate passes') + 1])[0] * (1 / 9) - slashes(
    lst[lst.index('Accurate passes') + 1])[1] * (1 / 4.5)
  score += check(lst, 'Key passes') * 2.5
  score += brackets(
    lst[lst.index('Dribble attempts (succ.)') + 1])[0] * 2.5 - brackets(
      lst[lst.index('Dribble attempts (succ.)') + 1])[1] * 0.8
  score += check(lst, 'Blocked shots') * 1.1
  score += check(lst, 'Big chances created') * 1.5
  score += brackets(lst[lst.index('Crosses (acc.)') + 1])[0] * 1.2
  score += check(lst, 'Shots off target') * 0.5
  score += check(lst, 'Shots blocked') * 0.5
  score += check(lst, 'Shots on target') * 2.5
  score += check(lst, 'Hit woodwork') * 3
  score += int(lst[lst.index('Minutes played') + 1][:-1]) * (1 / 30)
  score += check(lst, 'Goals') * 10
  score += check(lst, 'Assists') * 8
  score += check(lst, 'Clearance off line') * 3
  score += check(lst, 'Red card') * -4
  score += check(lst, 'Penalty miss') * -5
  score += check(lst, 'Penalty committed') * -5
  return round(score, 2)


def calc_mid(lst, tg, conc):
  score = 0
  score += brackets(
    lst[lst.index('Aerial duels (won)') + 1])[0] * 1.63 - brackets(
      lst[lst.index('Aerial duels (won)') + 1])[1] * 1.5
  score += check(lst, 'Total tackles') * 2.6
  score -= 2 * check(lst, 'Dribbled past') * 0.6
  score += check(lst, 'Interceptions') * 2.5
  score += check(lst, 'Clearances') * 1.1
  score += 4 + (tg * 2) - (conc * 2)
  score += 3 - (check(lst, 'Fouls') * 0.55) - (
    check(lst, 'Offsides') * 0.55) - (check(lst, 'Own goals') * 3.3) - (check(
      lst, 'Error led to shot') * 5) - (check(lst, 'Error led to goal') * 5)
  score += slashes(lst[lst.index('Accurate passes') + 1])[0] * (
    1 / 6.65) - slashes(lst[lst.index('Accurate passes') + 1])[1] * (1 / 3.2)
  score += check(lst, 'Key passes') * 2.5
  score += brackets(
    lst[lst.index('Dribble attempts (succ.)') + 1])[0] * 2.9 - brackets(
      lst[lst.index('Dribble attempts (succ.)') + 1])[1] * 0.8
  score += check(lst, 'Blocked shots') * 1.1
  score += check(lst, 'Big chances created') * 1.5
  score += brackets(lst[lst.index('Crosses (acc.)') + 1])[0] * 1.2
  score += check(lst, 'Shots off target') * 0.25
  score += check(lst, 'Shots blocked') * 0.25
  score += check(lst, 'Shots on target') * 2.2
  score += check(lst, 'Hit woodwork') * 3
  score += int(lst[lst.index('Minutes played') + 1][:-1]) * (1 / 30)
  score += check(lst, 'Goals') * 10
  score += check(lst, 'Assists') * 8
  score += check(lst, 'Clearance off line') * 3
  score += check(lst, 'Red card') * -4
  score += check(lst, 'Penalty miss') * -5
  score += check(lst, 'Penalty committed') * -5
  return round(score, 2)


def calc_att(lst, tg, conc):
  score = 0
  score += brackets(
    lst[lst.index('Aerial duels (won)') + 1])[0] * 1.4 - brackets(
      lst[lst.index('Aerial duels (won)') + 1])[1] * 0.4
  score += check(lst, 'Total tackles') * 2.6
  score -= 2 * check(lst, 'Dribbled past') * 0.5
  score += check(lst, 'Interceptions') * 2.7
  score += check(lst, 'Clearances') * 0.8
  score += (tg * 3)
  score += 5 - (check(lst, 'Fouls') * 0.5) - (check(lst, 'Offsides') * 0.5) - (
    check(lst, 'Own goals') * 3) - (check(lst, 'Error led to shot') *
                                    5) - (check(lst, 'Error led to goal') * 5)
  score += slashes(lst[lst.index('Accurate passes') + 1])[0] * (1 / 6) - slashes(
    lst[lst.index('Accurate passes') + 1])[1] * (1 / 8)
  score += check(lst, 'Key passes') * 2.5
  score += brackets(
    lst[lst.index('Dribble attempts (succ.)') + 1])[0] * 3 - brackets(
      lst[lst.index('Dribble attempts (succ.)') + 1])[1] * 1
  score += check(lst, 'Blocked shots') * 0.8
  score += check(lst, 'Big chances created') * 1.5
  score += brackets(lst[lst.index('Crosses (acc.)') + 1])[0] * 1.2
  score += check(lst, 'Shots off target') * -0.3
  score += check(lst, 'Shots blocked') * -0.3
  score += check(lst, 'Shots on target') * 3
  score += check(lst, 'Hit woodwork') * 3
  score += int(lst[lst.index('Minutes played') + 1][:-1]) * (1 / 30)
  score += check(lst, 'Goals') * 10
  score += check(lst, 'Assists') * 8
  score += check(lst, 'Clearance off line') * 3
  score += check(lst, 'Red card') * -4
  score += check(lst, 'Penalty miss') * -5
  score += check(lst, 'Penalty committed') * -5
  return round(score, 2)


def brackets(text):
  return [
    int(text[text.index('(') + 1:len(text) - 1]),
    int(text[:text.index(' ')]) - int(text[text.index('(') + 1:len(text) - 1])
  ]


def brac_perc(text):
  base = float(text[:text.index('(') - 1])
  perc = float(text[text.index('(') + 1:text.index('%')])
  if perc == 0.0:
    bad = 0
  else:
    bad = (base / (perc / 100)) - base
  return [base, bad]


def slashes(text):
  return [
    int(text[:text.index('/')]),
    int(text[text.index('/') + 1:text.index(' ')]) -
    int(text[:text.index('/')])
  ]


def check(lst, text):
  if text in lst:
    return float(lst[lst.index(text) + 1])
  else:
    return 0


def check_dict(dictionary, text):
  if text in dictionary.keys():
    return dictionary[text]
  else:
    return 0


def get_participant_points(num_players):
  with open('CalcSheet.csv', mode='r') as file:
    d = csv.reader(file)
    data = []
    for lines in d:
      for text in lines:
        if "SUB" in text.upper():
          data.append(text[:-4])
        elif text != '':
          data.append(text)
    # print(data)
    # print()

  participant_dict = {}
  with open('ParticipantTeams.csv', mode='r') as file:
    print()
    print("MISSING PLAYERS:")
    d = csv.reader(file)
    player_lst = []
    point_lst = []
    key = "Süle XI"
    for lines in d:
      # if len(lines) > 0:
      # print("Line: ", lines)
      for text in lines:
        text = re.sub('\s', ' ', text)
        text = re.sub('\.', '.', text)
        if text[-1] == ' ':
          text = text[:-1]
        # print("text: ", text)
        if (text[0] == '*'):
          participant_dict[key] = [player_lst, point_lst]
          key = text[1:]
          player_lst, point_lst = [], []
        if text in data:
          # print(text, "in data!")
          player_lst.append(text)
          point_lst.append(data[data.index(text) + 1])
        else:
          print(text)
      participant_dict[key] = [player_lst, point_lst]

    for k, v in participant_dict.items():
      point_lst, player_lst = (list(reversed(list(t))) for t in zip(*sorted(zip(map(int, v[1]), v[0]))))
      master_lst = [[w1, w2] for w1, w2 in zip(player_lst, point_lst)]
      for i in range(len(master_lst)):
        if "Keeps" in master_lst[i][0]:
          master_lst.insert(0, master_lst.pop(i))
      participant_dict[k] = master_lst

    # print()
    # print(participant_dict)
    # print()
  points = 0
  counter = 0
  point_lst = []
  player_lst = []
  with open('ParticipantPoints.csv', mode='w') as file:
    w = csv.writer(file)
    for k in participant_dict.keys():
      w.writerow([k])
      for v in participant_dict[k]:
        w.writerow(v)
        if counter < num_players:
          points += round(float(v[1]))
          counter += 1
      w.writerow(["POINTS:", points])
      w.writerow([''])
      point_lst.append(points)
      player_lst.append(k)
      points = 0
      counter = 0
    point_lst, player_lst = (list(reversed(list(t)))
                             for t in zip(*sorted(zip(point_lst, player_lst))))

    print()
    print("STANDINGS:")
    for i in range(len(player_lst)):
      print(f"{i+1}) {player_lst[i]}: {point_lst[i]}")


def get_calculated_points(points_dict):
  with open('CalculatedPoints.csv', mode='r') as file:
    data = csv.reader(file)
    new = []
    for lines in data:
      new.append(lines)
    # print(new)

    old_len = len(new[0])
    i = 0
    for k, v in points_dict.items():
      if i >= len(new):
        lst1 = [''] * old_len
        # print(lst1)
        lst2 = [k, v, '']
        # print(lst2)
        new.append(lst1 + lst2)
        i += 1
        continue
      else:
        new[i].extend([k, v, ''])
        i += 1

    if i < len(new) - 1:
      for t in range(i, len(new)):
        new[t].extend(['', '', ''])
    print(new)

  with open('CalculatedPoints.csv', mode='w') as file:
    w = csv.writer(file)
    for item in new:
      w.writerow(item)


def quick_sim(calc_dict, save):
  # opening the CSV file
  with open('Quicksim.csv', mode='r') as file:

    # reading the CSV file
    quick_data = csv.reader(file)
    new = []
    for lines in quick_data:
      new.append(lines[0])

  quick_data = []
  lst = []
  for i in range(len(new) - 1):
    if (new[i + 1] == 'Minutes played' and i > 1):
      # lst.append(new[i])
      quick_data.append(lst)
      lst = [new[i]]
      continue
    lst.append(new[i])
    if i == len(new) - 2:
      lst.append(new[i + 1])
      quick_data.append(lst)

  # print(quick_data)
  # print()

  print("SCORES FROM QUICKSIM: ")

  with open('CalcSheet.csv', mode='w') as file:
    w = csv.writer(file)
    for i in range(len(quick_data)):
      score = calc_dict[quick_data[i][-3].upper()](quick_data[i],
                                                   int(quick_data[i][-2]),
                                                   int(quick_data[i][-1]))
      print(f"{quick_data[i][0]}:", score)

      if save:
        w.writerow([quick_data[i][0], round(score)])


def avg_points(calc_dict):
  # opening the CSV file
  with open('AvgPoints.csv', mode='r') as file:

    # reading the CSV file
    quick_data = csv.reader(file)
    new = []
    for lines in quick_data:
      new.append(lines[0])
  # print(new)

  avg_data = []
  lst = []
  for i in range(len(new) - 1):
    if (new[i + 1] == 'Total played' and i > 1):
      # lst.append(new[i])
      avg_data.append(lst)
      lst = [new[i]]
      continue
    lst.append(new[i])
    if i == len(new) - 2:
      lst.append(new[i + 1])
      avg_data.append(lst)

  # print(avg_data)
  # print()

  print("SCORES FROM AVG_POINTS: ")
  # print()

  for i in range(len(avg_data)):
    pos_dict = base_dict[avg_data[i][-3].upper()]
    tg = float(lst[-2])
    conc = float(lst[-1])
    lst = avg_data[i]
    games = int(lst[lst.index('Total played') + 1])
    score = pos_dict['Base']
    score += brac_perc(
      lst[lst.index('Aerial duels won') + 1])[0] * pos_dict['Aerials won']
    score += brac_perc(
      lst[lst.index('Aerial duels won') + 1])[1] * pos_dict['Aerials lost']
    score += check(lst, 'Tackles per game') * pos_dict['Tackles']
    score += check(lst, 'Dribbled past per game') * pos_dict['Dribbled past']
    score += check(lst, 'Interceptions per game') * pos_dict['Interceptions']
    score += check(lst, 'Clearances per game') * pos_dict['Clearances'] * 1.25
    score += check(lst, 'Fouls') * pos_dict['Fouls']
    score += check(lst, 'Own goals') / games * pos_dict['Own goals']
    score += check(lst, 'Offsides') * pos_dict['Offsides']
    score += check(lst,
                   'Error led to shot') / games * pos_dict['Error led to shot']
    score += check(
      lst, 'Error led to goal') / games * pos_dict['Error lead to goal']
    score += check(lst, 'Red cards') / games * pos_dict['Red cards']
    score += brac_perc(
      lst[lst.index('Accurate per game') + 1])[0] * pos_dict['Passes']
    score += brac_perc(
      lst[lst.index('Accurate per game') + 1])[1] * pos_dict['Missed passes']
    score += check(lst, 'Key passes') * pos_dict['KP']
    score += check(lst, 'Big chances created') / games * pos_dict['BCC']
    score += brac_perc(
      lst[lst.index('Succ. dribbles') + 1])[0] * pos_dict['Dribbles won']
    score += brac_perc(
      lst[lst.index('Succ. dribbles') + 1])[1] * pos_dict['Dribbles lost']
    score += brac_perc(
      lst[lst.index('Acc. crosses') + 1])[0] * pos_dict['Crosses']
    score += (check(lst, 'Shots per game') -
              check(lst, 'Shots on target per game')) * pos_dict['Shots off']
    score += check(lst, 'Shots on target per game') * pos_dict['Shots on']
    score += check(lst, 'Goals per game') * pos_dict['Goals']
    score += check(lst, 'Assists') / games * pos_dict['Assists']
    score += check(lst, 'Minutes per game') * pos_dict['Minutes played']
    score += check(
      lst, 'Penalties committed') / games * pos_dict['Penalty committed']
    score += tg * check_dict(pos_dict, 'Team goals')
    score += conc * check_dict(pos_dict, 'Conceded')

    print(f'{lst[0]}: {round(score,2)}')
