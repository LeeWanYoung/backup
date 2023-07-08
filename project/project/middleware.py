from django.middleware.csrf import CsrfViewMiddleware

class CustomCsrfMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        # POST 요청에 대해서만 CSRF 보호 기능을 적용합니다.
        if request.method == 'POST':
            return super().process_view(request, callback, callback_args, callback_kwargs)