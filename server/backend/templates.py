from backend.models import Template


class Messages():
    START_MESSAGE_HANDLER = Template.messages.get(id=1).gettext()
    MENU = Template.messages.get(id=2).gettext()
    VIDEOS_PER_DAY_LIMIT_EXCEEDED = Template.messages.get(id=9).gettext()
    CURRENCY = Template.messages.get(id=10).gettext()
    BONUS_RECEIVED = Template.messages.get(id=14).gettext()
    NOT_SO_FAST = Template.messages.get(id=15).gettext()
    PROFILE = Template.messages.get(id=16).gettext()
    FUND_WITHDRAWAL = Template.messages.get(id=19).gettext()
    REFERAL = Template.messages.get(id=22).gettext()
    STATISTICS = Template.messages.get(id=23).gettext()
    REFERAL_LINK = Template.messages.get(id=24).gettext()
    SUPPORT = Template.messages.get(id=26).gettext()


class Keys():
    EARN = Template.keys.get(id=3).gettext()
    PROFILE = Template.keys.get(id=4).gettext()
    FUND_WITHDRAWAL = Template.keys.get(id=5).gettext()
    REFERALS = Template.keys.get(id=6).gettext()
    GET_BONUS = Template.keys.get(id=11).gettext()
    FINISH = Template.keys.get(id=12).gettext()
    SEE_MORE = Template.keys.get(id=13).gettext()
    MENU = Template.keys.get(id=17).gettext()
    STATISTICS = Template.keys.get(id=18).gettext()
    GET_PAID = Template.keys.get(id=20).gettext()
    WATCH_VIDEO = Template.keys.get(id=21).gettext()
    SUPPORT = Template.keys.get(id=25).gettext()


class Smiles():
    PREV = Template.smiles.get(id=7).gettext()
    NEXT = Template.smiles.get(id=8).gettext()
