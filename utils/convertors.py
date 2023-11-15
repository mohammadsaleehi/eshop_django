def group_list(custom_list: list, size: int = 4) -> list:
    my_list = []
    for i in range(0, len(custom_list), size):
        my_list.append(custom_list[i:i + size])
    return my_list
