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
from tools.crawl import reward
import json
import logging

match_d = {'特別獎': './templates/card_special.json', 
    '特獎': './templates/card_special.json', 
    '頭獎': './templates/card_1.json', 
    '二獎': './templates/card_2.json', 
    '三獎': './templates/card_3.json', 
    '四獎': './templates/card_4.json', 
    '五獎': './templates/card_5.json', 
    '六獎': './templates/card_6.json', 
    '沒中獎': './templates/card.json'}

def parser_information(text):
    date, predict_number = text.split(' ')
    return date, predict_number

def how_to_respond_text_message(event, line_bot_api):
    date, predict_number = parser_information(event.message.text)
    message = reward(date, predict_number)

    if message in match_d:
        card_json = json.load(open(match_d[message], 'r',encoding='utf-8'))
        card_json['body']['contents'][1]['text'] = f'日期: {date}'
        card_json['body']['contents'][2]['text'] = f'發票號碼: {predict_number}'
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', card_json))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message))