SUBJECT_ALL = ('语文', '数学', '英语', '物理', '化学', '生物', '历史', '政治', '地理')
SUBJECT_MAJOR = SUBJECT_ALL[:3]


class StatusCode():
    SUCCESS = 0
    INVALID_METHOD = 1
    # Argument: 参数输入后的合法性检测
    INVALID_ARGUMENT = 2
    # Type: 参数输入后的类型检测
    INVALID_TYPE = 3
    DUPLICATE_DATA = 4
    NONE_DATA = 5
