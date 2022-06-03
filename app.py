
# web app development
# flask (for small-scale app), django (suitable for website dev)


from flask import Flask, request, abort

from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('9zxW+3ibcAsniMoFPsWaUGcnF0VubtUh8IDTxgWO7vffyS7xWWUVj43meITfsEolhl80oiZ/h3hbdtKhkVdd35yG54KzHArdD2gxzxIez4EAbepbJwYzqvONMv9uMFlejeUFMhHlsWRD7N0SHcoZBwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0d09da511c2b3322ef6bde0ddc869e0c')


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
	msg = event.message.text
	r = 'Sorry, I don\'t understand.'

	if msg in ['Hi', 'hi']:
		r = 'Hi!'
	elif msg == 'Have you had dinner yet?':
		r = 'Not yet.'
	elif msg == 'Who are you?':
		r = 'I am a chat robot.'
	elif 'Booking' in msg:
		r = 'You wanna book a table, right?'

	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=r))


if __name__ == "__main__":
	app.run()