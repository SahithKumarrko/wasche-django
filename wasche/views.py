from PIL import Image
import cv2
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pyzbar.pyzbar as pyzbar
from django.shortcuts import render
from delivery_executives.models import Deliver_Executive
import json
import base64
import io
import numpy as np
import os
import requests
import pyqrcode
# import keras
# from keras.preprocessing import image
# from keras.applications import imagenet_utils
# from keras.applications.mobilenet import preprocess_input
# from keras.applications import MobileNet
# import win32print
# import win32ui
from PIL import ImageWin
# import cv2

#mobile = keras.applications.mobilenet.MobileNet()


root_url = "http://wasche-services.herokuapp.com"
root_url = "http://localhost:8000"
tot = 0
classes = {
    "Upper Wear":[
"jersey",
"military_uniform",
"stole",
"sweatshirt",
"trench_coat"
    ],
    "Lower Wear":[
"hoopskirt",
"jean",
"miniskirt",
"overskirt"
    ],
    "Inner Wear":[
        "bikini",
        "brassiere",
        "swimming_trunks",
        "diaper"
    ],
    "Other":[
        "apron",
        "bath_towel",
        # "bow_tie",
        "cardigan",
        "doormat",
        "fur_coat",
        "handkerchief",
        "lab_coat",
        "maillot",
        "mitten",
        "velvet",
        "neck_brace",
        "vestment",
        "guacamole",
        "pajama",
        "poncho",
        "quilt",
        "theater_curtain",
        "sarong",
        "shower_curtain",
        "sock",
        "suit"
    ],
    "Full Wear":[
        "gown",
        "kimono"
    ]
}

c2 = {
	"Lower Wear":[
	"leg",
	"jean",
	"jeans",
	"trouser",
	"pants",
	"denim",
	"standing"
	],
	"Inner Wear":[
	"pantie",
	"lingerie",
	"diaper",
	"top",
	"undergarment",
	"bra",
	"brassiere",
	"protective garment"
	
	],
	"Upper Wear":[
	"suit",
	"jacket",
	"jersey",
	"bulletproof vest",
	"apron",
	"shirt","sleeve","top","t-shirt"
	],
	"Other":[
	"womans's clothing",
	"tie",
	"garment",
	"fashion",
	"dress",
	"clothing",
	"clothes",
	"full",
	"outfit",
	"dressed"
	]
	
}
api_key = 'acc_24f50e74ddbaf36'
api_secret = 'c234ca7dec045a9235ecb19e8dbf7a3b'

# def process_image_and_detect(imagepath):
  
  
#   img = image.load_img(img_path, target_size=(299, 299))
#   x = image.img_to_array(img)
#   timg = cv2.cvtColor(x,cv2.COLOR_BGR2GRAY)
#   c = timg>=90
#   if np.count_nonzero(c)>=42000:
    

#     x = np.expand_dims(x, axis=0)
#     x = preprocess_input(x)

#     preds = minsr.predict(x)
#     preds =  decode_predictions(preds, top=3)[0][0]
#     if preds[2]>0.5:
#       for i,j in classes.items():
#         if preds[1] in j:
#           txt = "\nDetected   :  " + preds[1] + "\n\nConfidence  :  "  +  str(preds[2]) + "\n" + i
#           return [i,txt]
#   else:
#     return []
#   return []

def process_image_and_detect_imagga(filename):
  acc=50
  response = requests.post(
      'https://api.imagga.com/v2/tags?limit=10',
      auth=(api_key, api_secret),
      files={'image': open(filename, 'rb')})

  res = response.json()
  if "result" in res:
    res = res["result"]["tags"]
    f=False
    while True:
      for i in res:
        if (i["tag"]["en"] in c2["Lower Wear"]):
          if i["confidence"]>=acc:
            if not (i["tag"]["en"]=="standing" and i["confidence"]>=44):						
              f=True
              txt = "\nDetected   :  " + i["tag"]["en"] + "\n\nConfidence  :  "  +  str(i["confidence"]) + "\nLower Wear"
              return ["Lower Wear",i["confidence"]]
            
        elif i["tag"]["en"] in c2["Upper Wear"]:
          if i["confidence"]>=acc:
            f=True
            txt = "\nDetected   :  " + i["tag"]["en"] + "\n\nConfidence  :  "  +  str(i["confidence"]) + "\nUpper Wear"
            return ["Upper Wear",i["confidence"]]
        
        elif i["tag"]["en"] in c2["Inner Wear"]:
          if i["confidence"]>=acc:
            f=True
            txt = "\nDetected   :  " + i["tag"]["en"] + "\n\nConfidence  :  "  +  str(i["confidence"]) + "\nInner Wear"
            return ["Inner Wear",i["confidence"]]
        
      if f==True:
        break
      else:
        acc = acc-5
      if acc<=10:
        break
    acc=50
    if f==False:
      while True:
        for i in res:
          if i["tag"]["en"] in c2["Other"]:
            if i["confidence"]>=acc:
              f=True
              txt = "\nDetected   :  " + i["tag"]["en"] + "\n\nConfidence  :  "  +  str(i["confidence"]) + "\nOther"
              return ["Other",i["confidence"]]
              
        if f==True:
          break
        else:
          acc = acc-5
        if acc<=10:
          break
  else:
    return []
  return []


@csrf_exempt
def p1(request):
    path = os.path.abspath(".") + "\\wasche\\" + request.POST["path"]
    path = path.replace("\\","/")
    print(path)
    # img = Image.open(request.POST["path"])
    img = cv2.imread(path)
    img = cv2.resize(img,(140,140))
    print(img.shape)
    decoded = pyzbar.decode(img)
    print(decoded)
    if len(decoded)>=1:
        dd = decoded[0].data.decode('utf-8')
        
        if "wasche-services" in dd:
            ddd = json.loads(dd)
            ddd = ddd["wasche-services"] 
            res = requests.post(root_url+"/api/notify_initial/",data={"data":json.dumps({"name":ddd["name"],"id":ddd["id"],"type":"initial","msg":"Hey Laundrer, The Delivery Executive is on his way make sure you have your clothes ready.","title":"Notification"})})
            if res.text=="Success":
                print("Successs")
                de = Deliver_Executive.objects.get(id=int(ddd["id"]),name = ddd["name"])
                cn = de.contract_name.contract_name
                return HttpResponse(json.dumps({"name":ddd["name"],"dest":cn}))
            else:
                print("There was an error please contact the technical department.")
                return HttpResponse("There was an error please contact the technical department.")
        else:
            return HttpResponse("Not Found")

    else:
        return HttpResponse("Not Found")

def process(request):
    return render(request,"process.html")

def process2(request):
    return render(request,"process2.html")


def process_image(user,filename):
  
  if user["cred"]["email"]!="":
    result = process_image_and_detect_imagga(filename)
    print(result)
    if len(result)>0:
      # for i,j in classes.items():
      #   if result in j:
          # predicted = i
      # found = True
      data = user["cred"]
      # data["data"] = i
      data["data"] = result[0]
      
      qr = pyqrcode.create(json.dumps(data))
      qr.png("qrcode_"+ str(user["data"]["t"]) + "_" + result[0] +".png",scale=8)
      
      # text = "Detected {} => {}".format(result,i)

      # cv2.putText(frame, text, (10, 10),
      #     cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
      user["data"]["t"] = user["data"]["t"] + 1
      user["data"][result[0]] = user["data"][result[0]] + 1
      return result
  return ""
  
def detect_user(img,user):
  decoded = pyzbar.decode(img)
  print("calling")
  print(decoded)
  if len(decoded) >= 1:
    dd = decoded[0].data.decode('utf-8')
    # print("saasddssad")
    print(dd)
    if "email" in dd:
      dd = json.loads(dd)
      try:
        if dd["email"] != user["cred"]["email"]:
          if user["cred"]["email"]!="":
            user["type"] = "po"
            user["data"]["p"] = True
            user["data"]["t"] = user["data"]["t"] + 1
            user["msg"] = "Your order has been processed."
            user["data"]["start"] = False
            user["title"] = "Order Details"
            req = requests.post(root_url+"/dashboard/update/",data={"user":json.dumps(user)})

            # print(req)
						
						# print_image("qrcode.png")
    
          user["data"] = {"Upper Wear":0,"Lower Wear":0,"Inner Wear":0,"Other":0,"Full Wear":0}
          user["cred"]["email"] = dd["email"]
          user["cred"]["contract_name"] = dd["contract_name"]
          user["cred"]["contract_address"] = dd["contract_address"]
          user["cred"]["first_name"] = dd["first_name"]
          user["cred"]["last_name"] = dd["last_name"]
          user["cred"]["gender"] = dd["gender"]
          user["type"] = "co"
          user["data"]["start"] = True
          user["data"]["s"]=0
          user["data"]["c"]=0
          user["data"]["f"]=0
          user["data"]["t"] = 0
          # text = "User  :  {}".format(user["cred"]["email"])

          # cv2.putText(img, text, (10, 10),
          # cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
          print(user)
          req = requests.post(root_url+"/dashboard/update_new/",data={"user":json.dumps(user)})
          # print(req)
          print(req.text)
          req = req.json()
          user["date"] = req["date"]
          user["time"] = req["time"]
          return True
      except Exception as exp:
        return "Error while finding data : " + exp 
  return False


@csrf_exempt
def search_user(request):
    imgstr = json.loads(request.POST["data"])
    imgstr = imgstr["img"]
    imgstr = imgstr.replace(" ","+")
    image_bytes = io.BytesIO(base64.b64decode(imgstr))
    im = Image.open(image_bytes)
    im.save("qr.png")
    user =  json.loads(request.POST["user"])
    arr = np.array(im)[:,:]
    print(arr.shape)
    u = detect_user(arr,user)
    if u==True:
        return HttpResponse(json.dumps({"user":user}))
    return HttpResponse("no")

@csrf_exempt
def detect_cloth(request):
    path = os.path.abspath(".") + "/" + request.POST["path"]
    path = path.replace("\\","/")
    user = json.loads(request.POST["user"])
    print(path)
    result = process_image(user,path)
    res = "Not Detected"
    if result!="":
        res = "{}  -  {:.2f}%".format(result[0],result[1])
        # res = result[0] + "  -  " + str(result[1])
    return HttpResponse(json.dumps({"user":user,"res":res}))
    
@csrf_exempt
def complete_order(request):
    users = json.loads(request.POST["user"])
    for user in users:
        try:
            user["type"] = "pd"
            user["data"]["p"] = False
            user["data"]["s"] = user["data"]["t"]
            user["data"]["c"] = 1
            user["msg"] = "Your order has completed. It may reach you in another 2 hours."
            user["data"]["start"] = False
            user["title"] = "Order Details"
            req = requests.post(root_url+"/dashboard/update/",data={"user":json.dumps(user)})
        except Exception as exp:
            print("Error :  ",exp)

    return HttpResponse("complete")




from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
def upload_detect(request):
  res = "Not Detected"
  try:
    # file_to_up = request.FILES["image"]
    image = request.FILES['image']
    # print(file_to_up)
    print(request.FILES)
    tmp_file = os.path.join("", image.name)
    path = default_storage.save(tmp_file, ContentFile(image.read()))
    print(path)
    result = process_image_and_detect_imagga("media/"+path)
    print(result)
    if len(result)>0:
      if result!="":
          return HttpResponse(json.dumps({"c":result[0],"a":"{0:.2f}".format(result[1]),"path":path}))
          # res = result[0] + "  -  " + str(result[1])
  except Exception as err:
    print(err)
    

  return HttpResponse(json.dumps({"c":res,"path":path}))

def detect_file_url(request):
  return render(request,"detector.html")
