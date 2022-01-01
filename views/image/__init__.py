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
from PIL import Image
from .model import predict_of_invoice
import json

match_d = {'特別獎': './templates/card_special.json', 
    '特獎': './templates/card_special.json', 
    '頭獎': './templates/card_1.json', 
    '二獎': './templates/card_2.json', 
    '三獎': './templates/card_3.json', 
    '四獎': './templates/card_4.json', 
    '五獎': './templates/card_5.json', 
    '六獎': './templates/card_6.json', 
    '沒中獎': './templates/card.json'}

def read_image_by_id(line_bot_api, message_id):
    message_content = line_bot_api.get_message_content(message_id)
    file_path = f'/home/herry/{message_id}.jpg'
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    return Image.open(file_path)

def how_to_respond_image_message(event, line_bot_api):
    message_id = event.message.id
    img = read_image_by_id(line_bot_api, message_id)
    date, predict_number = predict_of_invoice(img)
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