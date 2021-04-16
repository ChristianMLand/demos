from django.shortcuts import render, HttpResponse, redirect
from random import randint

gold_map = {#dictionary that maps locations to the range of gold you can earn
    "farm" : (10,20),
    "cave" : (5,10),
    "house" : (2,5),
    "casino" : (-50,50),
}

def index(request):
    if "gold" not in request.session:#initialize session variables
        request.session["activities"] = []
        request.session["gold"] = 0
    return render(request,"index.html",{"gold_map":gold_map})

def process_money(request, location=""):#allow for passing location through url (get request)
    if request.method == "POST":#allow for passing location through post request
        location = request.POST["location"]
    if location in gold_map:#only perform logic if recieved a valid location
        amount = randint(*gold_map[location])#unpack tuple into it's individual values and pass them as arguments
        request.session["activities"].append(f"Earned {amount} gold from the {location}!")
        request.session["gold"] += amount
    return redirect('/')

def reset(request):
    request.session.flush();#clear session completely
    return redirect('/')