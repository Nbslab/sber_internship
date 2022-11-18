import random

EDGES = {1: [[2, 300], [4, 150], [7, 220]],
         2: [[1, 100], [5, 520], [10, 110]],
         3: [[4, 340]],
         4: [[1, 150], [3, 340]],
         5: [[2, 520]],
         7: [[1, 220]],
         9: [[10, 230]],
         10: [[2, 110], [9, 230]]
         }

FREQS = {1: 1234,
         2: 1505,
         3: 900,
         4: 2345,
         5: 378,
         6: 2998,
         7: 5421,
         8: 1323,
         9: 708,
         10: 1283
         }


def get_absent():
    cnt = random.randint(1, 4)
    absent = random.sample(list(FREQS.keys()), cnt)
    return absent


def get_basket():
    cnt = random.randint(1, 5)
    basket = random.sample(list(FREQS.keys()), cnt)
    return basket


def get_edges_recs(basket: list) -> list:
    recs_list = []
    for value in basket:
        if value in EDGES:
            possible_recs = EDGES[value]
            recs_list.append(possible_recs)
    return recs_list


def get_freq_recs(recs: list, n_items: int, basket_list: list,
                  absent_list: list) -> list:
    absent_local = absent_list[:]
    for value in recs:
        if value[0] not in absent_local:
            absent_local.append(value[0])
    sorted_freqs = sorted(FREQS.items(), key=lambda kv: kv[1], reverse=True)
    sorted_freqs = list(map(list, sorted_freqs))
    sorted_freqs = recs_basket_filter(sorted_freqs, absent_local)
    sorted_freqs = recs_basket_filter(sorted_freqs, basket_list)
    sorted_freqs = sorted_freqs[:n_items]
    return sorted_freqs


def recs_absent_filter(recs: list, absent_list: list) -> list:
    filtered_recs = []
    for value in recs:
        for subrecs in value:
            if subrecs[0] not in absent_list:
                filtered_recs.append(subrecs)
    return filtered_recs


def recs_basket_filter(recs: list, basket_list: list) -> list:
    filtered_recs = []
    for value in recs:
        if value[0] not in basket_list:
            filtered_recs.append(value)
    return filtered_recs


def preprocess_recs(recs: list, basket_list: list, absent_list: list) -> list:
    recs_absent = recs_absent_filter(recs, absent_list)
    recs_basket = recs_basket_filter(recs_absent, basket_list)
    totals = {}
    for k, v in recs_basket:
        totals[k] = totals.get(k, 0) + v
    return [list(t) for t in totals.items()]


def fill_recs(recs: list, basket_list: list, absent_list: list) -> list:
    recs = sorted(recs, key=lambda x: int(x[1]), reverse=True)
    if len(recs) < 4:
        len_diff = 4 - len(recs)
        recs_by_freq = get_freq_recs(recs, len_diff, basket_list, absent_list)
        for value in recs_by_freq:
            recs.append(value)
        return recs
    elif len(recs) > 4:
        while len(recs) > 4:
            recs.pop()
        return recs
    elif len(recs) == 4:
        return recs


def let_from_basket(recs: list, n_items: int, basket: list, absent_list: list) -> list:
    post_recs = get_edges_recs(basket)
    absent_local = absent_list[:]
    for value in recs:
        if value[0] not in absent_local:
            absent_local.append(value[0])
    post_recs_absent = recs_absent_filter(post_recs, absent_local)
    post_recs_absent = sorted(post_recs_absent, key=lambda x: int(x[1]), reverse=True)
    if len(post_recs_absent) >= n_items:
        result_fillers = post_recs_absent[:n_items]
        return result_fillers
    else:
        savers_list = []
        for key in FREQS.keys():
            if key not in absent_local:
                savers_list.append([key, FREQS[key]])
        savers_list = sorted(savers_list, key=lambda x: int(x[1]), reverse=True)
        if len(post_recs_absent) == 0:
            return savers_list[:n_items]
        else:
            savers_list = savers_list[:n_items-len(post_recs_absent)]
            for saver in savers_list:
                post_recs_absent.append(saver)
            return post_recs_absent


def initiate_recs(baskets: list, absent_list: list) -> dict:
    result = {}
    for i in range(5):
        raw_recs = get_edges_recs(baskets[i])
        filter_recs = preprocess_recs(raw_recs, baskets[i], absent_list)
        full_recs = fill_recs(filter_recs, baskets[i], absent_list)
        if len(full_recs) < 4:
            len_diff = 4 - len(full_recs)
            filler = let_from_basket(full_recs, len_diff, baskets[i], absent_list)
            for value in filler:
                full_recs.append(value)
        result[i] = [baskets[i], full_recs]
    return result


if __name__ == '__main__':
    random.seed(444)
    absent = get_absent()

    baskets = []
    for _ in range(5):
        baskets.append(get_basket())
    result_recs = initiate_recs(baskets, absent)
    print('absent', '\n', absent, '\n', '-' * 25)
    print('basket : recs', )
    for i in result_recs:
        tmp_list = []
        for value in result_recs[i][1]:
            tmp_list.append(value[0])
        print(result_recs[i][0], ':', tmp_list)
