import telegram


def telegramSendMessage(month: str, day: str, siteNumber: int, camping: str):
    chat_token = "1752254532:AAHM8-RftUAr3V5KRJ2SzaBp41G8JTTeHIE"
    bot = telegram.Bot(token=chat_token)
    telegramMessageText = camping + ': ' + month + ' ' + day + \
        '일 ' + str(siteNumber) + '개 예약 가능'
    bot.sendMessage(chat_id="-564369831", text=telegramMessageText)  # Official
    # bot.sendMessage(chat_id="1003456250", text=telegramMessageText)  # Test
