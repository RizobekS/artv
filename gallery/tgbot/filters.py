import telebot


def filters(bot, chat_id):
    # filter for checking whether user is Admin or Creator
    class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
        key = 'is_admin'

        @staticmethod
        def check(message: telebot.types.Message):
            return bot.get_chat_member(message.chat.id, message.from_user.id).status in ('administrator', 'creator')

    # filter for checking whether is in the assigned group
    class IsGroup(telebot.custom_filters.SimpleCustomFilter):
        key = 'is_group'

        @staticmethod
        def check(message: telebot.types.Message):
            return bot.get_chat(message.chat.id).id == int(chat_id)

    bot.add_custom_filter(IsAdmin())
    bot.add_custom_filter(IsGroup())