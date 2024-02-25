from bs4 import BeautifulSoup
import pandas as pd
import argparse

from course import Course, CourseLoader


def main(source_file_path: str, choice_list: list[str]):
    with open(source_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    main_content_div = soup.find("div", id="main-content")
    courses = main_content_div.find("table").find("tbody").find_all("tr")

    results = []
    course_loader = None
    for course in courses:
        fields = course.find_all("td")
        if len(fields) == 18:
            # 新的course
            if course_loader is not None:
                results.append(course_loader.load_item())
            course_loader = CourseLoader(Course())
            course_loader.add_value("index", fields[0])
            course_loader.add_value("department", fields[1])
            course_loader.add_value("id", fields[2])
            course_loader.add_value("name", fields[3])
            course_loader.add_value("type", fields[4])
            course_loader.add_value("discipline", fields[5])
            hour_credit = fields[6].get_text(strip=True)
            course_loader.add_value("hours", int(hour_credit.split("/")[0]))
            course_loader.add_value("credits", float(hour_credit.split("/")[1]))
            course_loader.add_value("limit_cnt", fields[7])
            course_loader.add_value("chosen_cnt", fields[8])
            arrange = (fields[9], fields[10], fields[11])
            course_loader.add_value("arrange", arrange)
            course_loader.add_value("teach_method", fields[12])
            course_loader.add_value("exam_method", fields[13])
            course_loader.add_value("chair_professor", fields[14])
            course_loader.add_value("teacher", fields[15])
            course_loader.add_value("assistant", fields[16])
            course_loader.add_value("remote_learning", fields[17])
        elif len(fields) == 3:
            arrange = (fields[0], fields[1], fields[2])
            course_loader.add_value("arrange", arrange)
        else:
            raise Exception("Unknown Format")
    if course_loader is not None:
        results.append(course_loader.load_item())

    chosen_course_list = list(
        filter(lambda course: course["id"] in choice_list, results)
    )

    formatted_chosen_course_list = []
    for course in chosen_course_list:
        course_name = course["name"]
        teachers = []
        if course.get("chair_professor"):
            teachers.append(course["chair_professor"])
        if course.get("teacher"):
            teachers.append(course["teacher"])
        if course.get("assistant"):
            teachers.append(course["assistant"])
        for _class in course["arrange"]:
            formatted_course = {
                "课程名称": course_name,
                "星期": _class[1],
                "开始节数": _class[2][0],
                "结束节数": _class[2][-1],
                "老师": "，".join(teachers),
                "地点": _class[3],
                "周数": _class[0],
            }
            formatted_chosen_course_list.append(formatted_course)

    df = pd.DataFrame(formatted_chosen_course_list)
    df.to_csv("chosen_courses.csv", index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file_path", type=str)
    parser.add_argument("--choice_list", nargs="*", default=[])
    args = parser.parse_args()
    main(args.source_file_path, args.choice_list)

# python generate_csv.py content.html --choice_list 180203085412P2001H 180088010108MX004H 180207040200MX009H 180207040200MX001H 180086083500P3001H 180086081203P3006H
