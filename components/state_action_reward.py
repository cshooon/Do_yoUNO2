import pandas as pd
import numpy as np
import itertools


def states():
    """TODO: Comment this function"""

    # Normal cards
    norm_cards = {"RED": 2, "GRE": 2, "BLU": 2, "YEL": 2}
    spec_cards = {"SKI": 1, "REV": 1, "PL2": 1}
    wild_cards = {"PL4": 1, "COL": 1}

    # Special cards
    norm_cards_play = {"RED#": 1, "GRE#": 1, "BLU#": 1, "YEL#": 1}
    spec_cards_play = {"SKI#": 1, "REV#": 1, "PL2#": 1}

    # Combine dictionaries
    states_dict = {
        **norm_cards,
        **spec_cards,
        **wild_cards,
        **norm_cards_play,
        **spec_cards_play
    }
    states = [["RED", "GRE", "BLU", "YEL"]]

    for val in states_dict.values():
        aux = range(0, val + 1)
        states.append(aux)

    # Conduct all combinations
    states = list(itertools.product(*states))
    states_all = list()

    for i in range(len(states)):
        if (
                states[i][1] >= states[i][10] and
                states[i][2] >= states[i][11] and
                states[i][3] >= states[i][12] and
                states[i][4] >= states[i][13] and
                states[i][5] >= states[i][14] and
                states[i][6] >= states[i][15] and
                states[i][7] >= states[i][16]
        ):
            states_all.append(states[i])

    return states_all


def actions():
    """TODO: Comment this function"""

    actions_all = [
        "RED", "GRE", "BLU", "YEL", "SKI",
        "REV", "PL2", "PL4", "COL"
    ]
    return actions_all


def rewards(states, actions):
    """Calculate rewards for given states and actions.
    Assigns higher rewards for states closer to winning (fewer cards remaining),
    aiming for diverse rewards and encouraging quick game completion."""

    R = np.zeros((len(states), len(actions)))
    # 카드 수에 따라 다양한 보상을 할당합니다.
    states_t = [sum(states[i][1:10]) for i in range(len(states))]  # 카드의 총 수를 계산합니다.

    for i in range(len(states)):
        if states_t[i] == 0:
            R[i] = 1  # 모든 카드를 다 사용했을 때 (게임 종료)
        elif states_t[i] <= 2:
            R[i] = 0.5  # 카드가 2장 이하일 때
        elif states_t[i] <= 5:
            R[i] = 0.25  # 카드가 5장 이하일 때
        elif states_t[i] <= 8:
            R[i] = 0.12   # 카드가 8장 이하일 때
        else:
            R[i] = 0.06   # 그 외의 경우 (많은 카드가 남아 있을 때)

    R = pd.DataFrame(
        data=R,
        columns=actions,
        index=states)

    return R
