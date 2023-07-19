from django.shortcuts import render


def HomePageView(request):
    return render(request, template_name='common/home-page.html')
