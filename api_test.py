import requests
import shutil


response = requests.get("https://randomfox.ca/floof/")
fox = response.json()
with open("fox_img.jpg", "wb") as file:
    shutil.copyfileobj(fox["image"], file)
    
print(fox["image"])