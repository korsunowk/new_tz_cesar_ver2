from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from new_tz.forms import Form
from django.http import JsonResponse

def encrypting(normaltext, key):
    cesartext = ''
    it=0
    for i in normaltext.lower():
        try:
            int(i)            #проверка символа на число
            cesartext += i
        except:
            if i == ' ':            #проверка на пробел в тексте
                cesartext += ' '
            else:
                if alphabet.find(i) >= 0:      		#проверка на входимость в алфавит
                    letter = alphabet.find(i)+key
                    if letter >25:
                        letter -= 26
                    if normaltext[it].isupper():
                        cesartext += chr(letter+97).upper()       
                    else:
                        cesartext += chr(letter+97)
                else:                               #если нет в алфавите, то символ не изменяется
                    cesartext += i
            it+=1
    return cesartext

def decrypting(cesartext, key):
    normaltext = ''
    it=0
    for i in cesartext.lower():
        try:
            int(i)                  #проверка символа на число
            normaltext += i
        except:
            if i == ' ':                #проверка на пробел в тексте
                normaltext += ' '
            else:
                if alphabet.find(i) >= 0:               #проверка на входимость в алфавит
                    letter = alphabet.find(i)-key
                    if letter < 0:
                        letter +=26
                    if cesartext[it].isupper():
                        normaltext += chr(letter+97).upper()
                    else:
                        normaltext += chr(letter+97)
                else:                                   #если нет в алфавите, то символ не изменяется
                    normaltext += i
            it+=1
    return normaltext

def find_text(text):
    for word in text.split(' '):
        if word in eng_slovar:                  #поиск слова из введенного текста в словаре
            return True
    return False

def index(request):
    args = {}
    args.update(csrf(request))
    args['form'] = Form()
    global alphabet
    global eng_slovar
    alphabet = ''
    eng_slovar = set()
    for i in range(97,123):     #97-123 - англ алфавит
        alphabet+=(chr(i))		#создание списка алфавита

    eng_slovar1 = open("static/eng_slovar.txt","r")   #cоздание множества словаря слов
    for line in eng_slovar1:
        for i in line.split(' '):
            eng_slovar.add(i)

    return render_to_response('index.html',args)

@csrf_exempt
def encrypt(request):                   #шифрование
    if request.method == 'POST':
        return JsonResponse(
            {
                'finaltext': encrypting
                (
                    request.POST.get('text',''),
                    int(request.POST.get('key',''))
                )
            }
        )
    else:
        return redirect('/')

@csrf_exempt
def decrypt(request):                   #дешифратор
    if request.method == 'POST':
        return JsonResponse(
            {
                'finaltext': decrypting
                (
                    request.POST.get('text',''),
                    int(request.POST.get('key',''))
                )
            }
        )
    else:
        return redirect('/')

@csrf_exempt
def find(request):                      #поиск введенного текста в словаре
    if request.method == 'POST':
        mytext = request.POST.get('mytext','')
        if find_text(mytext):                   #проверка на незашифрованный текст
            return JsonResponse(
                {
                    'enc':'false'
                }
            )
        for i in range(1,27):                   #поиск зашифрованного текта
            if find_text(decrypting(mytext,i)):
                return JsonResponse(
                    {
                        'enc':'true',
                        'word':decrypting(mytext,i),
                        'key':i
                    }
                )
        return JsonResponse({'enc':'dont_know'})
    else:
        return redirect('/')
