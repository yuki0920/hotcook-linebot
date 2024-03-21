import os

from gpt import call_gpt

from flask import Flask, request, abort

import ngrok

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)


access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
configuration = Configuration(access_token=access_token)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
handler = WebhookHandler(channel_secret)

port = int(os.getenv("PORT") or "8080")


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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    message = event.message.text
    app.logger.info(f"Received message: {message}")

    answer = call_gpt(message)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=answer)]
            )
        )


def forward():
    listener = ngrok.forward(port, authtoken_from_env=True)
    print(f"Ingress established at {listener.url()}")


if __name__ == "__main__":
    if os.getenv("ENV") == "development":
        forward()

    app.run(debug=True, host="0.0.0.0", port=port)
