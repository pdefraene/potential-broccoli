import numpy as np


def actions_list_to_index(actions_list):
    return 0 if actions_list[0] == 'C' else 1, 0 if actions_list[1] == 'C' else 1


class PayoffMatrix:
    def __init__(self, r_value, s_value, t_value, p_value, **kwargs):
        self.matrix = np.empty(shape=(2, 2, 2), dtype=np.float)
        self.matrix[0, 0, 0] = self.matrix[0, 0, 1] = r_value
        self.matrix[1, 1, 0] = self.matrix[1, 1, 1] = p_value

        self.matrix[0, 1, 0] = self.matrix[1, 0, 1] = s_value
        self.matrix[0, 1, 1] = self.matrix[1, 0, 0] = t_value

    def get_payoff_for_actions_list(self, actions_list):
        return self.matrix[actions_list_to_index(actions_list)]

    def __str__(self):
        res = '\n'
        res += " |    C     |     D    |\n"
        res += "-|----------|----------|\n"
        res += 'C|    ' + str(self.matrix[0,0,1]).rjust(5) + " |     " + str(self.matrix[0,1, 1]).rjust(5) + '|\n'
        res += ' |' + str(self.matrix[0,0,0]).ljust(10) + "|" + str(self.matrix[0,1,0]).ljust(10) + '|\n'
        res += "-|----------|----------|\n"
        res += 'D|    ' + str(self.matrix[1, 0, 1]).rjust(5) + " |     " + str(self.matrix[1, 1, 1]).rjust(5) + '|\n'
        res += ' |' + str(self.matrix[1, 0, 0]).ljust(10) + "|" + str(self.matrix[1, 1, 0]).ljust(10) + '|\n'
        res += "-----------------------\n"
        return res


if __name__ == '__main__':
    payoff_matrix = PayoffMatrix(-0.5, -10, 0, -5)
    print(f'Payoff matrix is {payoff_matrix}')
    actions_test = [['C', 'C'], ['C', 'D'], ['D', 'C'], ['D', 'D']]
    for actions in actions_test:
        payoff = payoff_matrix.get_payoff_for_actions_list(actions)
        print(f'Combination of actions {actions} yielded payoffs of {payoff[0]} for player 0 ({actions[0]}), and '
              f'{payoff[1]} for player 1 ({actions[0]})')
