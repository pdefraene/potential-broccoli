import numpy as np

from Agent import Agent
from PayoffMatrix import PayoffMatrix
from Plots import plot_probabilities_historic_average


def ask_agents(agents):
    # VERY IMPORTANT to return a tuple otherwise numpy multiD access doesn't work as intended
    return tuple(ag.choose_action() for ag in agents)


def compute_stimuli(agents, payoffs, supremi):
    assert len(agents) == len(payoffs) == len(supremi)
    return [ag.compute_stimulus(payoffs[i], supremi[i]) for i, ag in enumerate(agents)]


def get_supremi(agents, payoff_matrix):
    assert len(agents) == len(payoff_matrix)
    return [payoff_matrix.get_supremum(ag.aspiration_level) for ag in agents]


def update_agents_probabilities(agents, stimuli, choices):
    assert len(agents) == len(stimuli) == len(choices)
    return [ag.update_probabilities(stimuli[i], choices[i]) for i, ag in enumerate(agents)]


def update_agents_aspiration(agents, payoffs):
    assert len(agents) == len(payoffs)
    return [ag.update_aspiration(payoffs[i]) for i, ag in enumerate(agents)]


if __name__ == '__main__':
    decision_heuristic = "BM"
    learning_rate = 0.5

    habituation = 0
    p_fill = 0.5

    Prisoners_Dilemma_values = [[1, 3, 0, 4], 2]
    Chicken_Game_values = [[0, 3, 1, 4], 2]
    Stag_Hunt_values = [[1, 4, 0, 3], 2]

    game = Prisoners_Dilemma_values

    aspiration_level = game[1]

    nb_agents = 2
    nb_actions = 2
    agents_main = [Agent(decision_heuristic, learning_rate, aspiration_level,
                         habituation, p_fill) for _ in range(nb_agents)]
    payoff_matrix_main = PayoffMatrix(*game[0])

    nb_rep = 1
    nb_ep = 100

    probabilities_historic = np.empty((nb_rep, nb_ep, nb_agents, nb_actions), dtype=np.float64)

    for rep in range(nb_rep):
        print(f"Calculating {rep}/{nb_rep}")
        for t in range(nb_ep):
            choices_main = ask_agents(agents_main)
            payoffs_main = payoff_matrix_main.get_payoff_for_actions_list(choices_main)
            supremi_main = get_supremi(agents_main, payoff_matrix_main)
            stimuli_main = compute_stimuli(agents_main, payoffs_main, supremi_main)
            new_proba_main = update_agents_probabilities(agents_main, stimuli_main, choices_main)
            new_aspi_main = update_agents_aspiration(agents_main, payoffs_main)

            probabilities_historic[(rep, t)] = new_proba_main

    plot_probabilities_historic_average(probabilities_historic, nb_rep, payoff_matrix_main.matrix_values,
                                        aspiration_level, learning_rate, habituation, p_fill, game)
