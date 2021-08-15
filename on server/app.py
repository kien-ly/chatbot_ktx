from flask import Flask, request , render_template
import requests,os 
import json
import config, voicebot, dbconfig, chatbot




app = Flask(__name__)
app.config['SECRET_KEY'] = '51dc30af-b37c-4b8a-90ea-4f32d6be3c62'

#Function to access the Sender API
#def callSendAPI(senderPsid, response):
    # # print("ffffffjgnkdfnfvgsfdkfvndslkgbdfkgndlfgnldfngvdfnvkdnvdfnvlmdnvdknvksdhvkd")
    # PAGE_ACCESS_TOKEN = config.PAGE_ACCESS_TOKEN

    # payload = {
    # 'recipient': {'id': senderPsid},
    # 'message': response,
    # 'messaging_type': 'RESPONSE',
    # }
    
    # headers = {'content-type': 'application/json'}
    # #files = {'filedata': ('answer', open('./static/answer.mp3', 'wb+'), 'audio/mp3') }
    # files = {
    #     'filedata': ('answer', open('./static/answer.mp3', 'rb'), 'audio/mp3')
    # }

    # #response = requests.post(url, data=payload, files=files)
    

    # url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
   
    # with open("tmp.txt", 'w+') as f:
    #     json.dump(str(payload), f)
    # # print(f"post value: {payload}")
    # r = requests.post(url, data=payload, headers=headers, files=files)
    # print(r.text)
    # print("id"+ senderPsid)

    # PAGE_ACCESS_TOKEN = config.PAGE_ACCESS_TOKEN

    # payload = {
    #     'recipient': '{"id":5347857931951582}',
    #     'message': '{"attachment":{"type":"audio", "payload":{}}}'
    # }
    # files = {
    #     'filedata': ('answer', open('./static/answer.mp3', 'rb'), 'audio/mp3')
    # }
    # url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)

    # r = requests.post(url, data=payload, files=files)
    # print(r.text)

#Function for handling a message from MESSENGER
def handleMessage(senderPsid, receivedMessage):

    #with open("sample.json", 'w+') as f:
    #    json.dump(receivedMessage, f, indent=2, ensure_ascii=False)
    
    #check if received message contains text
    print('We entered the HANDLE MESSAGE FUNCTION')
    if 'text' in receivedMessage:
        def callSendAPI(senderPsid, response):
            PAGE_ACCESS_TOKEN = config.PAGE_ACCESS_TOKEN

            payload = {
                'recipient': {'id': senderPsid},
                'message': response,
                'messaging_type': 'RESPONSE'
            }
            headers = {'content-type': 'application/json'}
            url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)

            
            r = requests.post(url, json=payload, headers=headers)
        print('TEXT does exist in the RECEIVER MESSAGE')

        toSend = receivedMessage['text']

        #The Chatbot function ------------------------
        
        def chatbotResponse():
            answer, type_num = chatbot.chatbot_response(toSend)
            print(f"answer: {answer}")
            return answer

        print('The Chatbot Response is: {}'.format(chatbotResponse()))

        response = {"text": chatbotResponse()}    
        callSendAPI(senderPsid, response)        
    else:
        def callSendAPI(senderPsid, return_msg):
            PAGE_ACCESS_TOKEN = config.PAGE_ACCESS_TOKEN

            payload = {
                'recipient': '{"id":' + senderPsid + '}',
                'message': '{"attachment":{"type":"audio", "payload":{}}}'
            }
            files = {
                'filedata': ('answer', open('./static/answer.mp3', 'rb'), 'audio/mp3')
            }
            url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)  
            r = requests.post(url, data=payload, files=files)
        
        return_msg = voicebot.voicebot(receivedMessage['attachments'][0]['payload']['url'])
        
        callSendAPI(senderPsid, return_msg)
    
    # else:
    #     response = {"text": 'Chatbot này chỉ nhận tin nhắn vs tin nhắn âm thanh thôi'}
    #     callSendAPI(senderPsid, response)
 



@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route('/getbot')
def get_bot_response():
    userText = request.args.get('msg')
    answer, type_num =  chatbot.chatbot_response(userText)
    data = {'answer': answer, 'type':type_num}
    return json.dumps(data, ensure_ascii=False)

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))

@app.route("/voicebot")
def get_record():
    # NOTE: Tam thoi commnet
    # voicebot.voicebot()
    # id_file = dir_last_updated('./static')
    return id_file

@app.route('/webhook', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        #do something.....
        VERIFY_TOKEN = "my_flower_token"

        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            print(mode)
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            print(token)
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            print(challenge)

        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('WEBHOOK VERIFIED')

                challenge = request.args.get('hub.challenge')

                return challenge, 200
            else:
                return 'ERROR', 403

        return 'SOMETHING', 200

    if request.method == 'POST':
        #do something.....
        VERIFY_TOKEN = "my_flower_token"

        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            print(mode)
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            print(token)
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            print(challenge)

        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('WEBHOOK VERIFIED')

                challenge = request.args.get('hub.challenge')

                return challenge, 200
            else:
                return 'ERROR', 403



        #do something else
        data = request.data
        body = json.loads(data.decode('utf-8'))

        if 'message' not in body['entry'][0]['messaging'][0] or  'is_echo' in body['entry'][0]['messaging'][0]['message']:
            return 'Nothing happens', 200

        with open("incoming_send.txt", 'a+') as f:
            f.write(str(body) + '\n')

        if 'object' in body and body['object'] == 'page':
            entries = body['entry']
            for entry in entries:
                webhookEvent = entry['messaging'][0]
                

                senderPsid = webhookEvent['sender']['id']
                print('Sender PSID: {}'.format(senderPsid))


                if 'message' in webhookEvent:
                    handleMessage(senderPsid, webhookEvent['message'])
                    

                return 'EVENT_RECEIVED', 200
        else:
            return 'ERROR', 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
