import random
import string
from faker import Faker
from app01.models import AsUser


class creatUsers(object):

    def __init__(self, count):
        self.count = count

    def creat_user(self):
        user_list = []
        num_list = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                    "147", "150", "151", "152", "153", "155", "156", "157", "158", "159",
                    "185", "187", "188", "189"]
        fake = Faker("en-us")
        for i in range(1, self.count):
            user_obj = AsUser(name=fake.name(),
                              email=''.join([random.choice(string.digits) for i in range(random.randint(8, 11))]) +
                                    random.choice(['@163.com', '@gmail.com', '@qq.com']),
                              phone=random.choice(num_list) + ''.join(random.choice('0123456789') for i in range(8)),
                              password=''.join(random.sample(string.ascii_letters + string.digits, 12)),
                              age=random.randint(18, 25),
                              gender=random.choice(['1', '2']),
                              status=0,
                              )
            user_list.append(user_obj)
        AsUser.objects.bulk_create(user_list)
        return user_list
