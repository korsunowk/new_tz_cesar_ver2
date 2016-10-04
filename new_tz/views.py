from django.shortcuts import redirect
from django.http import JsonResponse
from CesarCrypt.CesarCrypting import CesarCrypting
from django.views.generic import View


cesarCrypting = CesarCrypting()


class CesarCryptingView(View):
    @staticmethod
    def encrypt(request):
        text = request.POST.get('text', False)
        key = int(request.POST.get('key', False))

        if text and key:
            return JsonResponse({
                'finaltext': cesarCrypting.encrypting(text, key)
            })
        else:
            return redirect('/')

    @staticmethod
    def decrypt(request):
        text = request.POST.get('text', False)
        key = int(request.POST.get('key', False))
        if text and key:
            return JsonResponse({
                'finaltext': cesarCrypting.decrypting(text, key)
            })
        else:
            return redirect('/')

    @staticmethod
    def find(request):
        mytext = request.POST.get('mytext', False)
        if mytext:
            if cesarCrypting.find_text(mytext):
                return JsonResponse(
                    {
                        'enc': 'false'
                    }
                )
            else:
                for i in range(1, 27):
                    if cesarCrypting.find_text(cesarCrypting.decrypting(mytext, i)):
                        return JsonResponse(
                            {
                                'enc': 'true',
                                'word': cesarCrypting.decrypting(mytext, i),
                                'key': i
                            }
                        )
                return JsonResponse({'enc': 'dont_know'})
        else:
            return redirect('/')
