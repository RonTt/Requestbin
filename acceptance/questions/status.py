
class StatusQuestions(object):
    @classmethod
    def is_ok(cls, status) -> bool:
        return status == 200
