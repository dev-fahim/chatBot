import sys
from flask import Flask, request, render_template
from utils import wit_response
from pymessenger import Bot, Element, Button

from pprint import pprint

app = Flask(__name__)

# Facebook apps link:   https://developers.facebook.com/apps/2222049801408664/dashboard/
FB_ACCESS_TOKEN = "EAAJOK2fOTBIBACHgdFdaWuRNZAxTVRBmZAy6gUDUXQyeT8sAZCycRkz7gTHldq7gz05eorylViQGOXOCnfW8PYEXpNcfs6pVb6szcqe7hRwqDLR4crN1ctsW2s0wamgJQiSGShzLTZCPP2ijOiCPUEXarhwarX5tURmBZCZAXYsoZAdrxsoIL5e"

bot = Bot(FB_ACCESS_TOKEN)

VERIFICATION_TOKEN = "hello"


@app.route('/', methods=['GET'])
def verify():
    # Web hook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return render_template("index.html")


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    # **Necessary Code that extract json data facebook send**
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    # add for image reply
                    elif 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['attachments']

                    else:
                        messaging_text = 'no text'

                    response = None
                    entity, value = wit_response(messaging_text)

                    if entity == 'greetings':
                        response = [
                            {
                                "type":"web_url",
                                "url":"https://www.messenger.com",
                                "title":"Visit Messenger"
                            }
                        ]
                        bot.send_button_message(sender_id, "Hello", response)

                    elif entity == 'Ad_sense_income':
                        response = " Do you want to know how to start income using Adsense?"
                        bot.send_text_message(sender_id, response)

                    elif entity == 'yes':
                        response = {
                            "attachment": {
                                  "type": "template",
                                  "payload": {
                                    "template_type": "list",
                                    "top_element_style": "compact",
                                    "elements": [
                                      {
                                        "title": "Classic T-Shirt Collection",
                                        "subtitle": "See all our colors",
                                        "image_url": "https://peterssendreceiveapp.ngrok.io/img/collection.png",          
                                        "buttons": [
                                          {
                                            "title": "View",
                                            "type": "web_url",
                                            "url": "https://peterssendreceiveapp.ngrok.io/collection",
                                            "messenger_extensions": "true",
                                            "webview_height_ratio": "tall",
                                            "fallback_url": "https://peterssendreceiveapp.ngrok.io/"            
                                          }
                                        ]
                                      },
                                      {
                                        "title": "Classic White T-Shirt",
                                        "subtitle": "See all our colors",
                                        "default_action": {
                                          "type": "web_url",
                                          "url": "https://peterssendreceiveapp.ngrok.io/view?item=100",
                                          "messenger_extensions": "false",
                                          "webview_height_ratio": "tall"
                                        }
                                      },
                                      {
                                        "title": "Classic Blue T-Shirt",
                                        "image_url": "https://peterssendreceiveapp.ngrok.io/img/blue-t-shirt.png",
                                        "subtitle": "100% Cotton, 200% Comfortable",
                                        "default_action": {
                                          "type": "web_url",
                                          "url": "https://peterssendreceiveapp.ngrok.io/view?item=101",
                                          "messenger_extensions": "true",
                                          "webview_height_ratio": "tall",
                                          "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                                        },
                                        "buttons": [
                                          {
                                            "title": "Shop Now",
                                            "type": "web_url",
                                            "url": "https://peterssendreceiveapp.ngrok.io/shop?item=101",
                                            "messenger_extensions": "true",
                                            "webview_height_ratio": "tall",
                                            "fallback_url": "https://peterssendreceiveapp.ngrok.io/"            
                                          }
                                        ]        
                                      }
                                    ],
                                     "buttons": [
                                      {
                                        "title": "View More",
                                        "type": "postback",
                                        "payload": "payload"            
                                      }
                                    ]  
                                  }
                                }
                            }
                        bot.send_message(sender_id, response)

                    elif entity == 'phone_number':
                        response = "Thank you for giving your phone number. please fill the form so we can start working with you. https://sites.google.com/view/income-guru/"
                        bot.send_text_message(sender_id, response)

                    elif entity == 'about_business':
                        response = "Of course. tell me what you want to know."
                        bot.send_text_message(sender_id, response)

                    elif entity == 'assist_me':
                        response = "I am here. Ask your question dear."
                        bot.send_text_message(sender_id, response)

                    elif entity == 'recommend':
                        response = "My recommendation will start earning with Adsense."
                        bot.send_text_message(sender_id, response)

                    elif entity == 'thanks':
                        response = [
                            {
                                "type":"web_url",
                                "url":"https://www.messenger.com",
                                "title":"Visit Messenger"
                            }
                        ]
                        bot.send_button_message(sender_id, "Hello", response)

                    if response == None:
                        response = [
                            {
                                "title": "Hello",
                                "image_url": "https://images.pexels.com/photos/1893609/pexels-photo-1893609.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
                            },
                        ]
                        bot.send_generic_message(sender_id, response)

    return "ok", 200


@app.route('/Privacy-Policy')
def privacy_policy():
    return render_template("Privacy-Policy.html")


def log(message):
    # previously it was print now I just Use Petty Print
    pprint(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(port=80, use_reloader=True)