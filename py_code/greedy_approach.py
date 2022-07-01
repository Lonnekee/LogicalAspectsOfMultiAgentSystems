class NCCS:
    def __init__(self, n_cards):
        nccs = [[] for i in range(n_cards)]
        nccs[1] = [n_cards - i for i in range(n_cards + 1)]
        for ncinc in range(2, len(nccs)):
            nccs[ncinc] = [sum(nccs[ncinc-1][i+1:]) for i in range(n_cards - ncinc + 2)]
        self.nccs = nccs

    def get_number(self, number_of_cards_in_the_combination, minimum_starting_number):
        return self.nccs[number_of_cards_in_the_combination][minimum_starting_number]

    def get_index(self, comb):
        nccs = self.nccs
        lc = len(comb)
        combinations_after = 0
        for i in range(lc):
            v = comb[i]
            combinations_after += nccs[lc-i][v + 1]
        idx = nccs[lc][0] - 1 - combinations_after
        return idx

def get_combs(n_cards):
    n_digits = n_cards
    combs = [[] for i in range(n_digits)]
    combs[0] = [[[]] for i in range(n_digits)]
    for i in range(1, n_digits):
        combs[i] = [[[j] + x for j in range(k + 1, n_digits) for x in combs[i-1][j]] for k in range(n_digits)]

    combs = [[[j] + comb for j in range(n_digits) for comb in combs[i][j]] for i in range(n_digits)]
    return combs

class Rule_1:
    def __init__(self, nccs, max_overlap, n_cards, cards_per_hand):
        self.n_cards = n_cards
        self.nccs = nccs
        self.cards_per_comb = max_overlap + 1
        self.rule_1_table = [False for i in range(nccs.get_number(self.cards_per_comb, 0))]
        self.comb_idcs_list = get_combs(cards_per_hand)[self.cards_per_comb-1]

    def add_hand(self, hand):
        checks = [None] * len(self.comb_idcs_list)
        for i, comb_idcs in enumerate(self.comb_idcs_list):
            comb = [hand[comb_idx] for comb_idx in comb_idcs]
            table_idx = self.nccs.get_index(comb)
            if self.rule_1_table[table_idx]:
                return (False, [])
                
            checks[i] = table_idx

        for check in checks:
            self.rule_1_table[check] = True

        return (True, checks)

    def remove_checks(self, checks):
        for row_idx, col_idx in checks:
            self.rule_1_table[row_idx][col_idx] = False


class Rule_2:
    def __init__(self, nccs, n_cards, C_hand_size):
        self.n_cards = n_cards
        self.nccs = nccs
        self.rule_2_table = [[False] * (C_hand_size + 2) for i in range(nccs.get_number(C_hand_size + 1, 0))]
        self.checks_needed = len(self.rule_2_table) * 3
        self.checks_set = 0
        self.C_hand_size = C_hand_size

    def add_hand(self, hand):
        n_cards_in_hand = len(hand)
        n_cards_not_in_hand = self.n_cards - n_cards_in_hand

        cards_not_in_hand = [x for x in range(self.n_cards) if x not in hand]

        possible_checks = []

        # all possible combinations of the values 0 to n_cards_not_in_hand
        # we can use this to get all possible combinations of the cards not in hand
        comb_idcs_list_list = get_combs(n_cards_not_in_hand)
        
        # for the combinations with one card from the hand, we only need combinations of length C_hand_size
        comb_idcs_list = comb_idcs_list_list[self.C_hand_size-1]

        for comb_indcs in comb_idcs_list:
            comb = [cards_not_in_hand[idx] for idx in comb_indcs]
            i = 0
            for card_in_hand in hand:
                while i < len(comb) and comb[i] < card_in_hand:
                    # print(i, comb, card_in_hand)
                    i += 1
                comb_ = comb[:i] + [card_in_hand] + comb[i:]
                row_idx = self.nccs.get_index(comb_)
                col_idx = i + 1
                # print(comb_)
                possible_checks.append((row_idx, col_idx))

        # for the combinations with only not-in-hand cards, we need combinations with length C_hand_size + 1
        comb_idcs_list = comb_idcs_list_list[self.C_hand_size]

        for comb_indcs in comb_idcs_list:
            comb = [cards_not_in_hand[idx] for idx in comb_indcs]
            row_idx = self.nccs.get_index(comb)
            col_idx = 0
            possible_checks.append((row_idx, col_idx))

        new_checks = [pc for pc in possible_checks if not self.rule_2_table[pc[0]][pc[1]]]

        self.set_checks(new_checks, True)

        return (self.satisfied(), new_checks)

    def set_checks(self, checks_list, truth_value):
        n_checks = len(checks_list)
        self.checks_set += n_checks if truth_value else - n_checks
        for table_row_idx, table_col_idx in checks_list:
            self.rule_2_table[table_row_idx][table_col_idx] = truth_value

    def satisfied(self):
        return self.checks_set == self.checks_needed

    def remove_checks(self, checks):
        self.set_checks(checks, False)


nA, nB, nC = [3,3,1]
ncards = nA + nB + nC
max_overlap = nA - nC - 1
nccs = NCCS(ncards)
r1 = Rule_1(nccs, max_overlap, ncards, nA)
r2 = Rule_2(nccs, ncards, nC)

possible_hands = get_combs(ncards)[nA - 1]

presented_options = []

for hand in possible_hands:
    allowed, _ = r1.add_hand(hand)
    if not allowed:
        continue
    succ, _ = r2.add_hand(hand)
    presented_options.append(hand)
    if succ:
        print('solution found! (greedy approach)')
        for opt in presented_options:
            print('\t{}'.format(opt))
        exit(0)

print('no solution (greedy approach)')
exit(-1)
