from django.utils import translation

class LanguageSwitcherMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.GET.get("lang")

        if lang:
            request.session["lang"] = lang

        lang = request.session.get("lang", "en")
        translation.activate(lang)
        request.LANGUAGE_CODE = lang

        response = self.get_response(request)
        return response
