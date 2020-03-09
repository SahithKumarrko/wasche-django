import cv2
import json
import requests
import pyzbar.pyzbar as pyzbar
import pyqrcode
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

user = {"cred":{"email":""},"data":{}}



api_key = 'acc_24f50e74ddbaf36'
api_secret = 'c234ca7dec045a9235ecb19e8dbf7a3b'
import requests

  
def process_image_and_detect_imagga(file):
  acc=50
  response = requests.post(
      'https://api.imagga.com/v2/tags?limit=10',
      auth=(api_key, api_secret),
      files={'image': open("photo.jpg", 'rb')})

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
              return ["Lower Wear",txt]
            
        elif i["tag"]["en"] in c2["Upper Wear"]:
          if i["confidence"]>=acc:
            f=True
            txt = "\nDetected   :  " + i["tag"]["en"] + "\n\nConfidence  :  "  +  str(i["confidence"]) + "\nUpper Wear"
            return ["Upper Wear",txt]
        
        elif i["tag"]["en"] in c2["Inner Wear"]:
          if i["confidence"]>=acc:
            f=True
            txt = "\nDetected   :  " + i["tag"]["en"] + "\n\nConfidence  :  "  +  str(i["confidence"]) + "\nInner Wear"
            return ["Inner Wear",txt]
        
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
              return ["Other",txt]
              
        if f==True:
          break
        else:
          acc = acc-5
        if acc<=10:
          break
  else:
    return []
  return []

  
def detect_user(img):
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
            user["data"]["t"] = tot
            user["msg"] = "Your order has been processed."
            user["data"]["start"] = False
            user["title"] = "Order Details"
            req = requests.post("https://wasche-services.herokuapp.com/dashboard/update/",data={"user":json.dumps(user)})

            # print(req)
						
						# print_image("qrcode.png")
					
          tot = 0
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

          req = requests.post("https://wasche-services.herokuapp.com/dashboard/update_new/",data={"user":json.dumps(user)})
          # print(req)
          req = req.json()
          user["date"] = req["date"]
          user["time"] = req["time"]
          return True
      except Exception as exp:
        return "Error while finding data : " + exp 
  return False

def process_image():
  
  if user["cred"]["email"]!="":
    result = process_image_and_detect_imagga("photo.jpg")
    # print(result)
    global tot
    if len(result)>0:
      # for i,j in classes.items():
      #   if result in j:
          # predicted = i
      tot = tot + 1
      # found = True
      data = user["cred"]
      # data["data"] = i
      data["data"] = result[0]
      
      qr = pyqrcode.create(json.dumps(data))
      qr.png("qrcode.png",scale=8)
      
      # text = "Detected {} => {}".format(result,i)

      # cv2.putText(frame, text, (10, 10),
      #     cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

      user["data"][result[0]] = user["data"][result[0]] + 1
      return result[1]
  return ""

tot = 0
try:
  c_d=0
#   print("Starting  Cam  : \n")
  text="Searching for User : "
  c = cv2.VideoCapture(0)
  
  print("Starting  Cam  : \n")
  
  print(text,"\n")
  while(True):
    # take_photo()
    r,f = c.read()
    cv2.imwrite("photo.jpg",f)
    cv2.imshow("Frame", f)
	
    img = cv2.imread("photo.jpg")
    
    c_d = c_d + 1
    # print(c_d)
    if user["cred"]["email"]!="" and c_d==10:
      print("changing")
      t2 = "Searching for clothes..."
      print(t2)
    if(detect_user(img)==True):
      t = "User : " + user["cred"]["email"]
      print(t)
    tex = process_image()
    # print("Found : "+tex)
    if tex!="":
      c_d=0
      t = tex
      print(t)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
  
except Exception as exp:
  print(exp)