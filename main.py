from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
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

from config import ACCESS_TOKEN, SECRET
from views.follow import how_to_respond_follow
from views.image import how_to_respond_image_message
from views.postback import how_to_respond_postback
from views.text import how_to_respond_text_message
import json

app = Flask(__name__)
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    how_to_respond_text_message(event, line_bot_api)

@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    how_to_respond_image_message(event, line_bot_api)

@handler.add(PostbackEvent)
def handle_message(event):
    how_to_respond_postback(event, line_bot_api)

@handler.add(FollowEvent)
def handle_follow(event):
    how_to_respond_follow(event, line_bot_api)

if __name__ == "__main__":
    app.run(debug=True)
