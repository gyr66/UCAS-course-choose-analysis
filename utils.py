day_map = {
    "周一": 1,
    "周二": 2,
    "周三": 3,
    "周四": 4,
    "周五": 5,
    "周六": 6,
    "周日": 7,
}


def parse_week(week_info: str):
    """
    第2,4-5,8-13周 => [2, 4, 5, 8, 9, 10, 11, 12, 13]
    """
    week_list = []
    week_info = week_info[1:-1]
    week_info_splited_list = week_info.split(",")
    for item in week_info_splited_list:
        if "-" not in item:
            week_list.append(int(item))
        else:
            item_splited_list = item.split("-")
            start_week = int(item_splited_list[0])
            end_week = int(item_splited_list[1])
            week_list += list(range(start_week, end_week + 1))
    return week_list


def parse_time(time_info: str):
    global day_map
    day = day_map[time_info[:2]]
    classes_info = time_info[3:-1]
    classes_info_splited_list = classes_info.split("-")
    start_class = int(classes_info_splited_list[0])
    end_class = int(classes_info_splited_list[1])
    class_list = list(range(start_class, end_class + 1))
    return (day, class_list)


def generate_arrange(arrange_info):
    arrange = []
    try:
        week_list = parse_week(arrange_info[0])
        time = parse_time(arrange_info[1])
    except:
        return None
    for week in week_list:
        arrange.append((week, *time, arrange_info[2]))
    return arrange


if __name__ == "__main__":
    t = ("第3-5周", "周二(7-8)", "教二楼204")
    print(generate_arrange(t))
