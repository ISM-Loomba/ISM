import numpy as np
import pandas as pd

df = pd.read_csv('data2.csv', delim_whitespace=True, index_col=0)
print(df)

IPM = np.empty(df.shape, dtype=int)

size = len(df.columns)
i = 0
for index, row in df.iterrows():
    size = len(df.columns)
    while size > 0:

        if i == size - 1:
            IPM[size - 1][i] = 1
        elif pd.isnull(row[str(size)]):
            break
        else:
            if row[str(size)].lower() == 'v':
                IPM[i][size - 1] = 1
                IPM[size - 1][i] = 0
            elif row[str(size)].lower() == 'a':
                IPM[i][size - 1] = 0
                IPM[size - 1][i] = 1
            elif row[str(size)].lower() == 'x':
                IPM[i][size - 1] = 1
                IPM[size - 1][i] = 1
            elif row[str(size)].lower() == 'o':
                IPM[i][size - 1] = 0
                IPM[size - 1][i] = 0

        size -= 1
    i += 1


frm = pd.DataFrame(columns=['Parameter', 'Reachability_set', 'Level'], dtype=np.int8)

for i, row in enumerate(IPM):
    sub_list = []
    for index, val in enumerate(row):
        if val == 1:
            sub_list.append(index + 1)

    frm = frm.append({'Parameter': i + 1, 'Reachability_set': set(sub_list)}, ignore_index=True)

Antecedent_set = {}

for i, column in enumerate(IPM.T):
    sub_list = []
    for index, val in enumerate(column):
        if val == 1:
            sub_list.append(index + 1)

    Antecedent_set[i + 1] = set(sub_list)
    # frm[frm['Parameter'] == i+1]['Antecedent_set'] = set(sub_list)

Intersection_set = {}

for index, Antecedent in Antecedent_set.items():
    [val] = frm[frm['Parameter'] == index]['Reachability_set'].values
#print(val)
    Intersection_set[index] = Antecedent.intersection(val)


Antecedent = pd.DataFrame(list(Antecedent_set.items()), columns=['Parameter', 'Antecedent_set'])
Intersection = pd.DataFrame(list(Intersection_set.items()), columns=['Parameter', 'Intersection_set'])

frm = frm.merge(Antecedent, on='Parameter')
frm = frm.merge(Intersection, on='Parameter')



# frm['Intersection_set'] = [a.intersection(b) for a, b in zip(frm.Reachability_set, frm.Antecedent_set)]

#frm[frm['Intersection_set'] == frm['Reachability_set']].Level = 1

level = 1
removed_numbers = []
size =len(frm.index)
while len(removed_numbers) < len(frm.index):
    removed_numbers += frm[frm.Reachability_set == frm.Intersection_set]['Parameter'].tolist()
    frm.loc[frm.Reachability_set == frm.Intersection_set, 'Level'] = level




    for i in frm.index:

        if frm.at[i,'Parameter'] in removed_numbers:
            frm.at[i,'Intersection_set'] = None
            continue
        else:
            Reachablility_temp = frm.at[i,'Reachability_set']
            Reachablility_temp = [d for d in Reachablility_temp if d not in removed_numbers]
            frm.at[i,'Reachability_set'] =  set(Reachablility_temp)
            Antecedent_temp = frm.at[i,'Antecedent_set']
            Antecedent_temp = [d for d in Antecedent_temp if d not in removed_numbers]
            frm.at[i, 'Antecedent_set'] = set(Antecedent_temp)
            frm.at[i,'Intersection_set'] = set(Antecedent_temp).intersection(set(Reachablility_temp))





    level += 1



print(frm)


