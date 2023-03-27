from django.test import TestCase
from datetime import datetime, timedelta
from myapp import models
from myapp import logic


class UpdateClientsTest(TestCase):
    def setUp(self):
        self.p1, _ = models.Profile.objects.get_or_create(uid=1)
        self.p2, _ = models.Profile.objects.get_or_create(
            uid=2,
            defaults={'last_activity': datetime.today() - timedelta(days=1)}
        )
        self.p3, _ = models.Profile.objects.get_or_create(
            uid=3,
            defaults={'last_activity': datetime.today() - timedelta(days=1)}
        )

    def test_1(self):
        self.p2.update_activity()
        assert self.p2 == self.p1.get_next_profile()

        i = models.Interaction(initiator=self.p1, subject=self.p2, result=True)
        i.save()
        assert self.p3 == self.p1.get_next_profile()

        i = models.Interaction(initiator=self.p1, subject=self.p3, result=False)
        i.save()
        assert None == self.p1.get_next_profile()

        self.p2.profile_changed()
        assert self.p2 == self.p1.get_next_profile()


def get_next_button(result, menu_id):
    return next(btn for btn in result.buttons if btn.menu == menu_id)


class FullLogicTest(TestCase):
    def test(self):
        # first user message
        result = logic.manage(logic.Message(
            uid=1,
            text='start',
        ))
        assert result.menu == logic.MenuID.PROFILE
        assert logic.MenuID.SEARCH not in [btn.menu for btn in result.buttons]
        assert result.uid == 1
        assert models.Profile.objects.get(uid=1) != None

        # change profile text
        next_button = get_next_button(result, logic.MenuID.CHANGE_TEXT_VIEW)
        result = logic.manage(logic.Message(
            uid=1,
            text=next_button.text,
            menu=next_button.menu,
            info=next_button.info,
        ))
        assert result.menu == logic.MenuID.CHANGE_TEXT_SAVE

        new_text = "Описание профиля"
        result = logic.manage(logic.Message(
            uid=1,
            text=new_text,
            menu=logic.MenuID.CHANGE_TEXT_SAVE,
        ))
        assert result.menu == logic.MenuID.PROFILE
        assert models.Profile.objects.get(uid=1).text == new_text

        # first user search
        next_button = get_next_button(result, logic.MenuID.SEARCH)
        result = logic.manage(logic.Message(
            uid=1,
            text=next_button.text,
            menu=next_button.menu,
            info=next_button.info,
        ))
        assert result.menu == logic.MenuID.SEARCH
        assert result.text == logic.ALL_PROFILES_VIEWED

        # second user message
        result = logic.manage(logic.Message(
            uid=2,
            text='Пирвет',
        ))
        assert result.menu == logic.MenuID.PROFILE
        assert result.uid == 2
        assert models.Profile.objects.get(uid=2) != None

        # change second profile text
        next_button = get_next_button(result, logic.MenuID.CHANGE_TEXT_VIEW)
        result = logic.manage(logic.Message(
            uid=2,
            text=next_button.text,
            menu=next_button.menu,
            info=next_button.info,
        ))
        assert result.menu == logic.MenuID.CHANGE_TEXT_SAVE

        new_text_2 = "Описание второго профиля"
        result = logic.manage(logic.Message(
            uid=2,
            text=new_text_2,
            menu=logic.MenuID.CHANGE_TEXT_SAVE,
        ))
        assert result.menu == logic.MenuID.PROFILE
        assert models.Profile.objects.get(uid=2).text == new_text_2

        # second user search
        next_button = get_next_button(result, logic.MenuID.SEARCH)
        result = logic.manage(logic.Message(
            uid=2,
            text=next_button.text,
            menu=next_button.menu,
            info=next_button.info,
        ))
        assert result.menu == logic.MenuID.SEARCH
        assert result.text == new_text

        next_button = get_next_button(result, logic.MenuID.LIKE)
        result = logic.manage(logic.Message(
            uid=2,
            text=next_button.text,
            menu=next_button.menu,
            info=next_button.info,
        ))
        assert result.menu == logic.MenuID.SEARCH
        assert result.text == logic.ALL_PROFILES_VIEWED
        assert logic.MenuID.LIKE not in [btn.menu for btn in result.buttons]

        # first user search again
        next_button = get_next_button(result, logic.MenuID.SEARCH)
        result = logic.manage(logic.Message(
            uid=1,
            text=next_button.text,
            menu=next_button.menu,
            info=next_button.info,
        ))
        assert result.menu == logic.MenuID.SEARCH
        assert result.text == new_text_2

        next_button = get_next_button(result, logic.MenuID.LIKE)
        result = logic.manage(logic.Message(
            uid=1,
            text=next_button.text,
            menu=next_button.menu,
            info=next_button.info,
        ))
        assert result.menu == logic.MenuID.SEARCH
        assert result.text == logic.ALL_PROFILES_VIEWED

        next_button = get_next_button(result, logic.MenuID.MUTUAL)
        result = logic.manage(logic.Message(
            uid=1,
            text=next_button.text,
            menu=next_button.menu,
            info=next_button.info,
        ))
        assert result.menu == logic.MenuID.MUTUAL
        assert result.text == new_text_2









