from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselColumn,
                            CarouselTemplate, MessageAction, URIAction, ImageCarouselColumn, ImageCarouselTemplate,
                            ImageSendMessage, ConfirmTemplate,ButtonsTemplate)
import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "確認樣板":
        confirm_template = TemplateSendMessage(
            alt_text='Confirm template',
            template= ConfirmTemplate(
            text = 'Drink coffee',
            actions= [
                MessageAction(
                              label= 'Yes',
                              text= 'Yes',),

                MessageAction(label = 'No',
                              text = 'No'
                              ),
                    ]

                )

            )
        line_bot_api.reply_message(event.reply_token, confirm_template)
    if event.message.text == '按鈕模板':
        buttons_template = TemplateSendMessage(
            alt_text = 'button template',
            template = ButtonsTemplate(
            
                thumbnail_image_url = 'https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',

                title = "Brown cafe",

                actions = [

                    MessageAction(
                                  
                        label= '咖啡好處',
                        text = "讓你有精神"

                    ),
                    MessageAction(
            
                        label= "321",
                        url = "https://www.mrbrown.com.tw/"
                    ),
                 ] 
            )
        )
    line_bot_api.reply_message(event.reply_token,buttons_template)

    if event.message.text == '卷軸模板':
        carousel_template = TemplateSendMessage(
            alt_text = 'carousel template',
            template = CarouselTemplate(
                columns = [
                    CarouselColumn(
                        thumbnail_image_url= "https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg",
                        title = "This is Menu1",
                        text = "Menu 1",
                        actions = [
                            MessageAction(
                            label = "咖啡好處",
                            text = "有精神"                                                     
                            ),
                            URIAction(
                                label = "伯朗咖啡",
                                url = "https://www.mrbrown.com.tw/",
                                ),
                            ],
                        ),
                    CarouselColumn(
                        thumbnail_image_url = "https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg",
                        title = "This is menu 2",
                        actions = [
                            MessageAction(
                                label = "咖啡好處",
                                text = "有精神",
                            ),
                            URIAction(
                                label = "伯朗咖啡",
                                url = "https://www.mrbrown.com.tw/",
                            )
                        ]
                    )
                ]
            )                
        )
    
    line_bot_api.reply_message(event.reply_token,carousel_template)


if __name__ == "__main__":
    app.run()
