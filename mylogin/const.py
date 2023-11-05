SUBJECT_ALL = ('语文', '数学', '英语', '物理', '化学', '生物', '历史', '政治', '地理')
SUBJECT_MAJOR = SUBJECT_ALL[:3]


class StatusCode():
    SUCCESS = 0
    INVALID_METHOD = 1
    INVALID_ARGUMENT = 2
    DUPLICATE_DATA = 3
