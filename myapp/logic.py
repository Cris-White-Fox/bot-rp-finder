from dataclasses import dataclass, field
from typing import List


@dataclass
class Image:
    iid: str
    url: str


@dataclass
class Message:
    uid: int
    msg: str
    img: List[Image] = field(default_factory=list)
    button: dict = None


def func1(msg):
    return 1


def func2(msg):
    return 2


def func3(msg):
    return 3


routs = {
    "m1": func1,
    "m2": func2,
    "m3": func3,
}


def manage(msg):
    return routs.get(msg.button.get('mid', 'm1'), func1)(msg)


if __name__ == '__main__':
    print(manage(Message(123, '123', button={"mid": "m2", "data": 123})))
