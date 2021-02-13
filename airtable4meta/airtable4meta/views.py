from django.shortcuts import render

from tparser.models import Psychotherapist


def show_mainpage(request):
    
    psychotherapist_content = []

    for psychotherapist in Psychotherapist.objects.all():

        psychotherapist_description = {
            'name': psychotherapist.name,
            'photo': psychotherapist.image.url,
            'methods' : [
                obj.method for obj in psychotherapist.tag.all()
            ]
        }
        psychotherapist_content.append(psychotherapist_description)

    print(psychotherapist_content)



    return render(request, 'index.html', context={'all_psychotherapist' : psychotherapist_content})
