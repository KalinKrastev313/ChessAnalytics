from django.shortcuts import render


def HomePageView(request):
    return render(request, template_name='common/home-page.html')


def Error404(request, exception):
    return render(request, template_name='404-error.html', status=404)


def Error500(request):
    return render(request, template_name='500-error.html', status=500)
