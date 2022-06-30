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
    def __init__(self, nccs, n_cards):
        self.n_cards = n_cards
        self.nccs = nccs
        self.rule_2_table = [[False, False, False] for i in range(nccs.get_number(2, 0))]
        self.checks_needed = len(self.rule_2_table) * 3
        self.checks_set = 0

    def add_hand(self, hand):
        n_cards_in_hand = len(hand)
        n_cards_not_in_hand = self.n_cards - n_cards_in_hand

        cards_not_in_hand = [x for x in range(self.n_cards) if x not in hand]
        
        # pre-allocate a list for the checks
        max_n_new_checks = n_cards_in_hand * n_cards_not_in_hand + (n_cards_not_in_hand - 1) * n_cards_not_in_hand // 2
        new_checks = [None for i in range(max_n_new_checks)]
        n_new_checks = 0

        pairs = [(not_in_hand_card, hand_card, 0) if not_in_hand_card < hand_card else (hand_card, not_in_hand_card, 2) for hand_card in hand for not_in_hand_card in cards_not_in_hand]
        pairs += [(cards_not_in_hand[i], cards_not_in_hand[j], 1) for i in range(n_cards_not_in_hand) for j in range(i + 1, n_cards_not_in_hand)]

        for card0, card1, table_col_idx in pairs:
            table_row_idx = self.nccs.get_index([card0, card1])
            if not self.rule_2_table[table_row_idx][table_col_idx]:
                new_checks[n_new_checks] = (table_row_idx, table_col_idx)
                n_new_checks = n_new_checks + 1
        
        new_checks = new_checks[:n_new_checks]

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


nA, nB, nC = [3, 3, 1]
ncards = nA + nB + nC
max_overlap = nA - nC - 1
nccs = NCCS(ncards)
r1 = Rule_1(nccs, max_overlap, ncards, nA)
r2 = Rule_2(nccs, ncards)

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