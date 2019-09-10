def merge_lists(lists):
    merges = []
    for item in lists:
        if type(item) is list:
            merges += item
    return merges
