def find_min_pledge(pledge_list):
    pledges_set = set(pledge_list)
    
    amount = 1
    while amount in pledges_set:
        amount += 1
    
    return amount

assert find_min_pledge([1, 3, 6, 4, 1, 2]) == 5
assert find_min_pledge([1, 2, 3]) == 4
assert find_min_pledge([-1, -3]) == 1
