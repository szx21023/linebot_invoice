from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage
)
import json

def how_to_respond_postback(event, line_bot_api):
    if event.postback.data == 'instructions':
        FlexMessage = json.load(open('./templates/instructions.json', 'r',encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))

    elif event.postback.data == 'current_number':
        text = '這期號碼\n特別獎: \n14872301, \n特獎: \n37250799, \n頭獎: \n71086085, \n53645821, \n46626911, \n增開六獎: \n916'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))

    elif event.postback.data == 'money_special':
        text = '恭喜獲得 10,000,000 元！'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))

    elif event.postback.data == 'money_1':
        text = '恭喜獲得 200,000 元！'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))

    elif event.postback.data == 'money_2':
        text = '恭喜獲得 40,000 元！'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))

    elif event.postback.data == 'money_3':
        text = '恭喜獲得 10,000 元！'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))

    elif event.postback.data == 'money_4':
        text = '恭喜獲得 4,000 元！'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))

    elif event.postback.data == 'money_5':
        text = '恭喜獲得 1,000 元！'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))

    elif event.postback.data == 'money_6':
        text = '恭喜獲得 200 元！'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))

    elif event.postback.data == 'money_0':
        text = '恭喜獲得 0 元！'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.postback.data))