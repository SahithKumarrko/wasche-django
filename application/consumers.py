from channels.generic.websocket import AsyncWebsocketConsumer
import json
from user.models import User
from contracts.models import Contracts
from channels.db import database_sync_to_async
from application.views import check_cookie
from tracking_system.models import Tracker
class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        # data  = check_cookie()
        # print(self.scope['url_'])
        self.uname = ""
        if "wasche" in self.scope["cookies"]:
            print("yes")
            data=self.scope["cookies"]['wasche']
            import json
            data=data.replace("'","\"")
            data=json.loads(data)
            
            self.uname=data["e"]
        print(self.uname)
        # print(dir(self.scope.cookie))
        self.room_group_name="Notvalid"

        print("connecting  :  "+str(self.uname))
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # print(self.uname)
        if(self.uname!=""):
            self.colname = await self.check_user()
            if self.room_name=="notifications":
                self.room_group_name = 'noti_%s' % self.colname
            else:
                return
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        

    async def disconnect(self, close_code):
        # Leave room group
        print("disconnecting")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("recieved web_socket msg")
        text_data_json = json.loads(text_data)
        message = text_data_json['data']
        type_msg = ""
        if "type" in message:
            print(message["type"])
            if message["type"] == "notify" or message["type"] == "tracking":
                type_msg = message["type"]
            else:
                return
        if type_msg=="notify":
            await self.save_notification(message)
        if type_msg == "tracking":
            await self.update_tracking(message)

        # print(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': "notify_message",
                'data': message
            }
        )

    # Receive message from room group
    async def notify_message(self, event):
        message = event['data']
        print("recieved chat msg  :  ")
        # print(message)
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'data': message
        }))
    
    @database_sync_to_async
    def check_user(self):
        u = User.objects.filter(email=self.uname)
        
        col = u[0].contract_name
        coln = col.contract_name
        coln = "_".join(coln.split(" "))
        print(coln)
        # print(col)
        return coln
    @database_sync_to_async
    def save_notification(self,msg):
        try:
            u = User.objects.filter(email=self.uname)
            from user.models import Notifications
            n = Notifications(email=u,sent_from=msg["from"],title=msg["title"],msg=msg["msg"])
            n.save()
        except Exception as e:
            print("Error occured while saving notification :  ",e)
    @database_sync_to_async
    def update_tracking(self,msg):
        try:
            u = User.objects.filter(email=self.uname)
            from user.models import Notifications
            t = Tracker.objects.filter(email=u,on_going=True)
            # if len(t)!=0:
            #     td = 

        except Exception as e:
            print("Error occured while saving notification :  ",e)
       
        # col = Contracts.objects.get(email)
        # if(u.is_active):
        #     print("active")
        #     return True
        # else:
        #     return False
        