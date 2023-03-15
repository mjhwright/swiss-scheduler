import copy
import networkx as nx
import numpy as np
import pandas as pd

def initialise(players):
    return pd.DataFrame(zip(players.values(), [0 for i in range(len(players))], [0 for i in range(len(players))]), columns = ['Player', 'W', 'Points']), np.diag(1000 * np.ones(len(players)))

def pair(absentees, players, standings, C):
    standings.attrs['R'] += 1

    if (len(players) - len(absentees)) % 2:
        D = copy.copy(C[:-1, :-1])

    else:
        D = copy.copy(C)

    id = [id for id, player in players.items() if player in absentees]
    D[id] = 10000
    D[:, id] = 10000

    ebunch = []

    for i in range(len(D)):
        for j in range(len(D)):
            if i < j:
                ebunch.append((i, j, D[i, j]))

    G = nx.Graph()
    G.add_nodes_from(np.arange(len(D)))
    G.add_weighted_edges_from(ebunch)
    pairings = nx.algorithms.matching.min_weight_matching(G)
    pairings = [list(pairing) for pairing in pairings if (pairing[0] not in id and pairing[1] not in id)]

    for pairing in pairings:
        if standings.at[pairing[0], 'W'] > standings.at[pairing[1], 'W']:
            pairing.reverse()

    print(f"ROUND {standings.attrs['R']}")
    print('-' * 20)
    print(*[players[w] + ' - ' + players[b] for [w, b] in pairings], sep = '\n')
    print('-' * 20)

    return pairings

def score(pairings, players, results, standings, C):
    for pairing, result in zip(pairings, results):
        if result == 'W':
            standings.at[pairing[0], 'Points'] += 3
            standings.at[pairing[1], 'Points'] += 1

        if result == 'B':
            standings.at[pairing[0], 'Points'] += 1
            standings.at[pairing[1], 'Points'] += 3

        if result == '=':
            standings.at[pairing[0], 'Points'] += 2
            standings.at[pairing[1], 'Points'] += 2

        standings.at[pairing[0], 'W'] += 1
        C[pairing[0], pairing[1]] = 1000
        C[pairing[1], pairing[0]] = 1000

    for i in range(len(C)):
        for j in range(len(C)):
            if C[i, j] < 1000:
                C[i, j] = (standings.at[i, 'Points'] - standings.at[j, 'Points']) ** 2

    return standings, C

def main():
    players = {
        0: 'Carlsen',
        1: 'Kasparov',
        2: 'Fischer',
        3: 'Anand',
        4: 'Ivanchuk',
        5: 'Shirov',
        6: 'Capablanca',
        7: 'Alekhine',
        8: 'Anderssen',
        9: 'Staunton',
        10: 'COACH'
    }

    standings, C = initialise(players)
    standings.attrs = {'R': 0}

    # Round 1
    absentees = []
    pairings = pair(absentees, players, standings, C)

    results = ['W', 'B', 'W', 'W', '=']
    standings, C = score(pairings, players, results, standings, C)

    # Round 2
    absentees = ['Fischer']
    pairings = pair(absentees, players, standings, C)

    results = ['W', 'B', 'B', 'B', 'B']
    standings, C = score(pairings, players, results, standings, C)

    # Round 3
    absentees = ['Alekhine', 'Capablanca']
    pairings = pair(absentees, players, standings, C)

    results = ['B', 'B', '=', 'W']
    standings, C = score(pairings, players, results, standings, C)

    # print(standings.sort_values('Points', ascending = False))

if __name__ == '__main__':
    main()
