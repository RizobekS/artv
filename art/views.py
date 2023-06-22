from django.http import HttpResponseRedirect
from django.utils import translation
from django.shortcuts import redirect


def set_language_from_url(request, user_language):
	translation.activate(user_language)
	request.session[translation.LANGUAGE_SESSION_KEY] = user_language

	if "uz" in request.META.get('HTTP_REFERER'):
		response = request.META.get(
			'HTTP_REFERER').replace('/uz', '/' + user_language)
	if "ru" in request.META.get('HTTP_REFERER'):
		response = request.META.get(
			'HTTP_REFERER').replace('ru', user_language)
	if "en" in request.META.get('HTTP_REFERER'):
		response = request.META.get(
			'HTTP_REFERER').replace('en', user_language)
	if "zh-cn" in request.META.get('HTTP_REFERER'):
		response = request.META.get(
			'HTTP_REFERER').replace('zh-cn', user_language)

	return HttpResponseRedirect(response)


def robots(request):
	return redirect('static/robots.txt')
