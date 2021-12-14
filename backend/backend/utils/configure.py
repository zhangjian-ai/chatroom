import re

# 员工职级
GRADE = [(0, "总经理"), (1, "技术总监"), (2, "部门经理"), (3, "技术专家"), (4, "高级职工"), (5, "中级职工"), (6, "初级职工"), (7, "实习生")]

# 房间主题分类
THEME = ["科技前沿", "娱乐八卦", "党政新风", "街电吐槽", "低息贷款", "半夜相亲"]

# 所有有效的配置信息
ITEMS = {item[0]: item[1] for item in filter(lambda item: re.match("^[A-Z]+$", item[0]), locals().items())}
