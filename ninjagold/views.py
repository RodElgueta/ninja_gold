from typing import Counter
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, localtime, strftime
from django.utils.crypto import get_random_string
from random import randint

# Create your views here.
users = [{"name":"rodrigo","password":"1234"},
{"name":"rodrigo2","password":"4321"},
{"name":"rodrigo3","password":"1324"}]



def login(request):
    
    
    
    if request.method == 'GET':
        return render(request, 'index.html')
    
    else:
        name_from_form = request.POST['name']
        pass_from_form = request.POST['password']
        request.session['name'] = request.POST['name']
        
        for dict in range(len(users)):
            
            if request.POST['name'] == users[dict]['name'] and request.POST['password'] == users[dict]['password']:

                return redirect('/parameters')
            else:
                context = {"message":"Wrong Username or Password"}
                return render(request,"index.html",context)

def logout(request):
    
    del request.session['name']
    
    
    return redirect('')

def reset(request):

    request.session['turns'] = 0
    request.session['gold'] = 0
    request.session['activities'] = []

    return redirect('/ninja_gold')

def ninja_gold(request):
    gold = request.session.get('gold',0)
    
    if 'gold' not in request.session:
        request.session['gold'] = 0
    

        
    if 'turns' not in request.session:
        request.session['turns'] = 0


    context = {'gold':request.session['gold'],
        'Turns':request.session['parameter'],
        'MaxGold':request.session['parameter2']
        }
    
    return render(request,"ninja_gold.html",context)

def set_defaults(request):

    if 'turns' not in request.session:
        request.session['turns'] = 0

    if 'parameter' not in request.session:
        request.session['parameter'] = 10
    
    if 'parameter2' not in request.session:
        request.session['parameter2'] = 250
    
    if 'activities' not in request.session:
        request.session['activities'] = []


def procces_money(request):
    turns = request.session.get('turns',0)
    Maxturns = int(request.session.get('parameter',10))
    Agold = request.session.get('gold',0)
    MaxGold = int(request.session.get('parameter2',240))

    set_defaults(request)

    gold = 0 
    
    if request.POST['place'] == 'farm':
        gold = randint(10,20)
        request.session['turns'] += 1
        
    
    elif request.POST['place'] == 'cave':
        gold = randint(5,10)
        request.session['turns'] += 1
    
    elif request.POST['place'] == 'house':
        gold = randint(2,5)
        request.session['turns'] += 1
    
    else:
        gold = randint(-50,50)
        request.session['turns'] += 1

    request.session['gold'] += gold
    
    if gold > 0:
        request.session['activities'].insert(0,{
            'text': f"Got {gold} Gold in {request.POST['place']}",
            'gold': gold
        })
        
    else:
        request.session['activities'].insert(0,{
            'text': f"Lost {gold} Gold in Casino",
            'gold': gold
        })
    request.session.save()

    if Agold >= MaxGold:
        request.session['msg'] = "Congratz u Won"
        request.session['img'] =  "https://img.freepik.com/free-vector/pixel-art-luxury-treasure-pile_150088-456.jpg?size=626&ext=jpg&ga=GA1.2.501542633.1626566400"
        return redirect('/end')

    elif turns >= Maxturns:
        request.session['msg'] = "Game Over"
        request.session['img'] = "https://www.8bitish.com/wp-content/uploads/2019/05/change_bridge_animated.gif"
        return redirect('/end')

    return redirect('/ninja_gold')

def parameters(request):
    if request.method == 'GET':
        return render(request, 'parameters.html')
    
    else:

        request.session['parameter'] = request.POST['parameter']
        request.session['parameter2'] = request.POST['parameter2']
    
        return redirect('/ninja_gold')

def end(request):
    reset(request)
    return render(request,'end.html')