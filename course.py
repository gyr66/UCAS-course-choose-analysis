from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Compose

from utils import generate_arrange


class Course(Item):
    index = Field()  # 序号
    department = Field()  # 开课单位
    id = Field()  # 课程编码
    name = Field()  # 课程名称
    type = Field()  # 课程属性
    discipline = Field(
        input_processor=Compose(
            lambda item: item.get_text(strip=True)
            if item.find("div") == None
            else item.find("div").get_text(strip=True),
        )
    )  # 所属学科/专业
    hours = Field(input_processor=TakeFirst())  # 课时
    credits = Field(input_processor=TakeFirst())  # 学分
    limit_cnt = Field(
        output_processor=Compose(TakeFirst(), lambda item: int(item))
    )  # 限选
    chosen_cnt = Field(
        output_processor=Compose(TakeFirst(), lambda item: int(item))
    )  # 已选
    arrange = Field(
        input_processor=Compose(
            lambda lst: [td.get_text(strip=True) for td in lst], generate_arrange
        ),
        output_processor=lambda lst: sorted(lst, key=lambda x: (x[0], x[1])),
    )  # 排课安排，[(周次, 星期, [节次列表], 教室), ...]
    teach_method = Field()  # 授课方式
    exam_method = Field()  # 考试方式
    chair_professor = Field()  # 首席教授
    teacher = Field()  # 主讲教授
    assistant = Field()  # 助教
    remote_learning = Field(
        output_processor=Compose(TakeFirst(), lambda item: True if item == "是" else "否")
    )  # 是否远程教学
    sort_key = Field()


class CourseLoader(ItemLoader):
    default_input_processor = Compose(
        TakeFirst(), lambda item: item.get_text(strip=True)
    )
    default_output_processor = TakeFirst()


if __name__ == "__main__":
    course = Course()
    course_loader = CourseLoader(course)
    course_loader.add_value("arrange", ("第3-5周", "周二(7-8)", "教二楼204"))
    course_loader.add_value("arrange", ("第2周", "周一(7-8)", "教二楼204"))
    print(course_loader.load_item())
