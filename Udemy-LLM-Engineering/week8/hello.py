import modal
from modal import App, Image

# Setup

# create a modal app name hello 
app = modal.App("hello")

# set up os image which will be debian and perform pip install requests
image = Image.debian_slim().pip_install("requests")

# Hello!

@app.function(image=image)
def hello() -> str:
    import requests
    
    response = requests.get('https://ipinfo.io/json')
    data = response.json()
    city, region, country = data['city'], data['region'], data['country']
    return f"Hello from {city}, {region}, {country}!!"

# New - added thanks to student Tue H.!
@app.function(image=image, region="eu")
def hello_europe() -> str:
    import requests
    
    response = requests.get('https://ipinfo.io/json')
    data = response.json()
    city, region, country = data['city'], data['region'], data['country']
    return f"Hello from {city}, {region}, {country}!!"
