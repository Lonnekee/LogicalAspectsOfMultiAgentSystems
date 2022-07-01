def get_combs(n_cards_in_comb, n_cards_total):
    if n_cards_in_comb == 0:
        return [[]]
    combs = [[] for i in range(n_cards_total)]
    combs[0] = [[[]] for i in range(n_cards_total)]
    for i in range(1, n_cards_total):
        combs[i] = [[[j] + x for j in range(k + 1, n_cards_total) for x in combs[i-1][j]] for k in range(n_cards_total)]
    combs = [[[j] + comb for j in range(n_cards_total) for comb in combs[i][j]] for i in range(n_cards_total)]
    return combs[n_cards_in_comb - 1]

class Table:
    def __init__(self, n_cards_in_comb, n_cards_total, n_columns):
        self.n_cards_in_comb = n_cards_in_comb
        self.n_cards_total = n_cards_total
        self.n_columns = n_columns

        all_possible_combs = get_combs(n_cards_in_comb, n_cards_total)
        self.table = {str(comb): [None] * n_columns for comb in all_possible_combs}

        self.n_rows = len(all_possible_combs)

    def is_valid_idx(self, comb, col_idx):
        if comb not in self.table:
            print('Combination {} not in table keys {}'.format(comb, self.table.keys()))
            exit(-1)
        if col_idx >= len(self.table[comb]):
            print('Col_idx {} too high for self.table[{}] (length: {})'.format(col_idx, comb, len(self.table[comb])))
            exit(-2)

    def get(self, comb, col_idx):
        comb = str(comb)
        self.is_valid_idx(comb, col_idx)
        return self.table[comb][col_idx]

    def set(self, comb, col_idx, value):
        comb = str(comb)
        self.is_valid_idx(comb, col_idx)
        self.table[comb][col_idx] = value

    def set_list(self, comb_col_idx_pairs, value):
        for comb, col_idx in comb_col_idx_pairs:
            self.set(comb, col_idx, value)

    def get_size(self):
        return self.n_rows * self.n_columns

class Rule_1:
    def __init__(self, n_cards_in_hand, n_cards_in_comb, n_cards_total):
        self.table = Table(n_cards_in_comb, n_cards_total, 1)
        self.all_possible_index_combs = get_combs(n_cards_in_comb, n_cards_in_hand)

    def add_hand(self, hand):
        checks = [None] * len(self.all_possible_index_combs)
        
        for i, index_comb in enumerate(self.all_possible_index_combs):
            comb = [hand[idx] for idx in index_comb]
            if self.table.get(comb, 0):
                return (False, [])
            checks[i] = (comb, 0)

        self.table.set_list(checks, True)

        return (True, checks)

    def remove_checks(self, checks):
        self.table.set_list(checks, False)
            
class Rule_2:
    def __init__(self, n_cards_in_hand, n_cards_C, n_cards_total):
        self.n_cards_total = n_cards_total

        n_cards_in_comb = n_cards_C + 1
        n_columns = n_cards_C + 2
        self.table = Table(n_cards_in_comb, n_cards_total, n_columns)

        n_cards_not_in_hand = n_cards_total - n_cards_in_hand

        self.all_possible_index_combs_for_with_hand_card = get_combs(n_cards_C, n_cards_not_in_hand)
        self.all_possible_index_combs_for_without_hand_card = get_combs(n_cards_C + 1, n_cards_not_in_hand)

        self.checks_set = 0
        self.checks_needed = self.table.get_size()

    def add_hand(self, hand):
        possible_checks = []

        cards_not_in_hand = [x for x in range(self.n_cards_total) if x not in hand]

        if self.all_possible_index_combs_for_with_hand_card != []:
            for idx_comb in self.all_possible_index_combs_for_with_hand_card:
                comb = [cards_not_in_hand[idx] for idx in idx_comb]
                hand_card_insertion_idx = 0
                for card_in_hand in hand:
                    while hand_card_insertion_idx < len(comb) and comb[hand_card_insertion_idx] < card_in_hand:
                        hand_card_insertion_idx += 1
                    
                    # insert hand card in combinaton of non-hand cards
                    comb_ = comb[:hand_card_insertion_idx] + [card_in_hand] + comb[hand_card_insertion_idx:]
                    possible_checks.append((comb_, hand_card_insertion_idx + 1))
        else:
            possible_checks = [(card_in_hand, 1) for card_in_hand in hand]

        for idx_comb in self.all_possible_index_combs_for_without_hand_card:
            comb = [cards_not_in_hand[idx] for idx in idx_comb]
            possible_checks.append((comb, 0))

        new_checks = [pc for pc in possible_checks if not self.table.get(pc[0], pc[1])]

        self.set_checks(new_checks, True)

        return (self.satisfied(), new_checks)

    def set_checks(self, checks_list, truth_value):
        n_checks = len(checks_list)
        self.checks_set += n_checks if truth_value else - n_checks
        self.table.set_list(checks_list, truth_value)

    def satisfied(self):
        return self.checks_set == self.checks_needed

    def remove_checks(self, checks):
        self.set_checks(checks, False)

def run_greedy_search(n_cards_A, n_cards_B, n_cards_C, true_hand):
    n_cards_total = n_cards_A + n_cards_B + n_cards_C
    max_overlap = n_cards_A - n_cards_C - 1

    if max_overlap < 0:
        return (False, [])

    r1 = Rule_1(n_cards_A, max_overlap + 1, n_cards_total)
    r2 = Rule_2(n_cards_A, n_cards_C, n_cards_total)

    r1.add_hand(true_hand)
    r2.add_hand(true_hand)

    presented_options = [(None, true_hand, None, None)]

    possible_hands = get_combs(n_cards_A, n_cards_total)
    i = 0
    while True:
        while i < len(possible_hands):
            # possibly add hand possible_hands[i]
            hand = possible_hands[i]
        
            # are we allowed to add this decoy hand to our list of options according to rule 1?
            allowed, checks1 = r1.add_hand(hand)
            if not allowed:
                i += 1
                continue

            # after adding this hand to our list of options, does rule 2 tell us we successfully created enough insecurity for Cath?
            succ, checks2 = r2.add_hand(hand)

            presented_options.append((i, hand, checks1, checks2))
            if succ:
                return (True, [po[1] for po in presented_options])
            i += 1
            
        removed_hand = presented_options[-1]
        presented_options = presented_options[:-1]
        if len(presented_options) == 0:
            # we removed the true hand because no solution exists with the true hand.
            break
        r1.remove_checks(removed_hand[2])
        r2.remove_checks(removed_hand[3])
        i = removed_hand[0] + 1
    return (False, [])

if __name__ == "__main__":
    from sys import argv
    
    if len(argv) < 2 or not (len(argv) != 4 or len(argv) != 4 + int(argv[1])):
        print("not the right amount of arguments.\nuse: python3 {} n_cards_A n_cards_B n_cards_C [true cards of A]".format(argv[0]))
        exit(0)

    args = [int(a) for a in argv[1:]]

    if any([a < 0 for a in args]):
        print("please don't be so negative: it makes Python sad")
        exit(0)

    n_cards_A, n_cards_B, n_cards_C = args[:3]

    if len(args) > 3:
        n_total = n_cards_A + n_cards_B + n_cards_C
        if any([a >= n_total for a in args]):
            print("please use cards from 0 to {} only".format(n_total - 1))
            exit(0)
        true_hand_A = args[3:]
    else:
        true_hand_A = list(range(n_cards_A))

    succ, options = run_greedy_search(n_cards_A, n_cards_B, n_cards_C, true_hand_A)
    
    if succ:
        print('solution found! (greedy approach)')
        for opt in options:
            print('\t{}'.format(opt))
    else:
        print('no solution (greedy approach)')
