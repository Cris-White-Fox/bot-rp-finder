from dataclasses import dataclass, field
from typing import List
from enum import Enum
from myapp import models


ALL_PROFILES_VIEWED = "Вы просмотрели все анкеты, попробуйте поискать позже"

class Activity(Enum):
    DEFAULT = 1
    TRUE = 2
    FALSE = 3
    ACTION = 4


class MenuID(Enum):
    PROFILE = 1
    CHANGE_TEXT_VIEW = 2
    CHANGE_TEXT_SAVE = 3
    CHANGE_IMG_VIEW = 4
    CHANGE_IMG_SAVE = 5
    SEARCH = 6
    DISLIKE = 7
    LIKE = 8
    MUTUAL = 9


@dataclass
class Image:
    iid: str
    url: str = None


@dataclass
class Button:
    text: str
    menu: MenuID
    activity: Activity
    info: dict = field(default_factory=dict)


@dataclass
class Message:
    uid: int
    text: str = ''
    profile: models.Profile = None
    menu: MenuID = None
    info: dict = field(default_factory=dict)
    images: List[Image] = field(default_factory=list)
    buttons: List[Button] = field(default_factory=list)


def format_images(profile):
    return [Image(img.image_id, img.url) for img in profile.image_set.all()]


def profile_view(msg):
    return Message(
        uid=msg.uid,
        text=f"Ваша анкета:\n\n {msg.profile.text}" if msg.profile.text else "Заполните анкету",
        images=format_images(msg.profile),
        menu=MenuID.PROFILE,
        buttons=[
            Button(
                text="Описание",
                menu=MenuID.CHANGE_TEXT_VIEW,
                activity=Activity.DEFAULT,
            ),
            Button(
                text="Изображения",
                menu=MenuID.CHANGE_IMG_VIEW,
                activity=Activity.DEFAULT,
            ),
            Button(
                text="Искать анкеты",
                menu=MenuID.SEARCH if msg.profile.text else MenuID.PROFILE,
                activity=Activity.ACTION if msg.profile.text else Activity.FALSE,
            ),
        ]
    )


def change_text_save(msg):
    msg.profile.change_text(msg.text)
    return profile_view(msg)


def change_text_view(msg):
    return Message(
        uid=msg.uid,
        text="Отправь новый текст анкеты",
        menu=MenuID.CHANGE_TEXT_SAVE,
        buttons=[
            Button(
                text="Назад",
                menu=MenuID.PROFILE,
                activity=Activity.DEFAULT,
            ),
        ]
    )


def change_img_save(msg):
    msg.profile.change_images(msg.images)
    return profile_view(msg)


def change_img_view(msg):
    return Message(
        uid=msg.uid,
        text="Отправь новые изображения",
        menu=MenuID.CHANGE_IMG_SAVE,
        buttons=[
            Button(
                text="Назад",
                menu=MenuID.PROFILE,
                activity=Activity.DEFAULT,
            ),
        ]
    )


def like_view(msg):
    if subject := msg.info.get("subject"):
        msg.profile.like(models.Profile.objects.get(uid=subject))
    return search_view(msg)


def dislike_view(msg):
    if subject := msg.info.get("subject"):
        msg.profile.dislike(models.Profile.objects.get(uid=subject))
    return search_view(msg)


def search_view(msg):
    mutual_count = len(msg.profile.get_new_mutual())
    found_profile = msg.profile.get_next_profile()
    print('found_profile', found_profile)

    if not found_profile:
        return Message(
            uid=msg.uid,
            text=ALL_PROFILES_VIEWED,
            menu=MenuID.SEARCH,
            buttons=[
                Button(
                    text="Повторная попытка",
                    menu=MenuID.SEARCH,
                    activity=Activity.DEFAULT,
                ),
                Button(
                    text="Моя анкета",
                    menu=MenuID.PROFILE,
                    activity=Activity.DEFAULT,
                ),
                Button(
                    text="Взаимные лайки" + (f" ({mutual_count})" if mutual_count else ""),
                    menu=MenuID.MUTUAL,
                    activity=Activity.TRUE if mutual_count else Activity.DEFAULT,
                ),
            ]
        )

    return Message(
        uid=msg.uid,
        text=found_profile.text,
        images=format_images(found_profile),
        menu=MenuID.SEARCH,
        buttons=[
            Button(
                text="лайк",
                menu=MenuID.LIKE,
                info={"subject": found_profile.uid},
                activity=Activity.TRUE,
            ),
            Button(
                text="следующая",
                menu=MenuID.DISLIKE,
                info={"subject": found_profile.uid},
                activity=Activity.FALSE,
            ),
            Button(
                text="Моя анкета",
                menu=MenuID.PROFILE,
                activity=Activity.DEFAULT,
            ),
            Button(
                text="Взаимные лайки" + (f" ({mutual_count})" if mutual_count else ""),
                menu=MenuID.MUTUAL,
                activity=Activity.TRUE if mutual_count else Activity.DEFAULT,
            ),
        ]
    )


def show_mutual_view(msg):
    mutual_list = msg.profile.get_new_mutual()
    mutual_count = len(mutual_list)
    if not mutual_count:
        return Message(
            uid=msg.uid,
            text=ALL_PROFILES_VIEWED,
            menu=MenuID.MUTUAL,
            buttons=[
                Button(
                    text="Назад",
                    menu=MenuID.SEARCH,
                    activity=Activity.DEFAULT,
                ),
            ]
        )

    mutual_profile = mutual_list.first()
    mutual_count -= 1
    return Message(
        uid=msg.uid,
        text=mutual_profile.text,
        images=format_images(mutual_profile),
        menu=MenuID.MUTUAL,
        buttons=[
            Button(
                text=f"Следующая анкета ({mutual_count})",
                menu=MenuID.MUTUAL,
                activity=Activity.TRUE if mutual_count else Activity.DEFAULT,
            ),
            Button(
                text="Назад",
                menu=MenuID.SEARCH,
                activity=Activity.DEFAULT,
            ),
        ]
    )


routs = {
    MenuID.PROFILE: profile_view,
    MenuID.SEARCH: search_view,
    MenuID.MUTUAL: show_mutual_view,
    MenuID.LIKE: like_view,
    MenuID.DISLIKE: dislike_view,
    MenuID.CHANGE_TEXT_VIEW: change_text_view,
    MenuID.CHANGE_TEXT_SAVE: change_text_save,
    MenuID.CHANGE_IMG_VIEW: change_img_view,
    MenuID.CHANGE_IMG_SAVE: change_img_save,
}


def manage(msg):
    msg.profile, created = models.Profile.objects.get_or_create(uid=msg.uid)
    msg.profile.update_activity()
    if created:
        return routs[MenuID.PROFILE](msg)
    else:
        return routs[msg.menu](msg)
