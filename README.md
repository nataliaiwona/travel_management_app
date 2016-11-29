

Trippy is a travel management application that allows users to keep track of their past and future travel destinations. This app allows users to customize a map of the world with pins that represent cities. A user can add, edit or remove a pin, and can designate what type of pin to use for a city. Color-coded pins help the user distinguish between a city a user wants to visit, has visited and wants to go back, or has visited but never wants to return. Trippy --the app that gives globetrotters a high-level view of their travels.🌍


# Trippy #

![Trippy Landing Page](/static/assets/landing.png)

## Table of Contents

* [Tech Stack](#tech-stack)
* [Features](#features)
* [Setup/Installation](#installation)
* [To-Do](#future)
* [License](#license)

## <a name="tech-stack"></a>Tech Stack

__Frontend:__ HTML5, Javascript💖, jQuery, Bootstrap <br/>
__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy, bcrypt <br/>
__APIs:__ Google Maps, Google Places <br/>

## <a name="features"></a>Features 

Search for city to add pin to map (green: wish list, blue: want to go back, red: never going back). Edit and remove pin. 
User account registration not required.
  
![Logged out](/static/assets/signup.png)
![Login](/static/assets/login.png)
<br/><br/><br/>
Register or login to add a pin.
  
![Add Pin](/static/assets/autocomplete.png)
![City Added](/static/assets/cityadded.png)
<br/><br/><br/>
Add pins to your map.
  
![Edit Pin](/static/assets/editpin.png)
<br/><br/><br/>
Edit and remove pins from your map.


####Requirements:

- Install PostgreSQL
- Python 2.7
- Google Maps and Google Places API keys

To have this app running on your local computer, please follow the below steps:

Clone repository:
```
$ git clone https://github.com/nataliaiwona/trippy-hackbright-project.git
```
Create a virtual environment:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Get your own secret key for [Google Maps](https://developers.google.com/maps/documentation/javascript/get-api-key) and [Google Places](https://developers.google.com/places/web-service/get-api-key). Save them to a file `secrets.sh`. Your file should look something like this:
```
APP_KEY = 'xyz'
GOOGLE_MAPS_API_KEY = 'abc'
GOOGLE_PLACES_API_KEY = 'abc'

```
Create database 'travels'.
```
$ createdb travels
```
Create your database tables and seed example data.
```
$ python model.py
```
Run the app from the command line.
```
$ python server.py
```
If you want to use SQLAlchemy to query the database, run in interactive mode
```
$ python -i model.py
```

## <a name="future"></a>TODO✨
* Add notes feature to each city
* Add ability for users to upload photos to city
* Add year visited and number of visits, create timeline of travels
* Filter by type of pin
* Allow map-sharing
* Add another API to give recommendations based on city (ex Yelp API)

## <a name="license"></a>License

The MIT License (MIT)
Copyright (c) 2016 [Natalia Brokaw](https://www.linkedin.com/in/natalia-brokaw)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.