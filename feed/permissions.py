from django.shortcuts import redirect


def required(condition):
    def required_authenticated(func):
        def inner(request, *args, **kwargs):
            assert condition in ['authenticated', 'superuser', 'staff'],\
                "Condition should be one of: ['authenticated', 'superuser', 'staff']"
            if condition == 'authenticated':
                if not request.user.is_authenticated:
                    return redirect('/user/signin/')
            elif condition == 'superuser':
                if not request.user.is_superuser:
                    return redirect('/user/signin/')
            elif condition == 'staff':
                if not request.user.is_staff:
                    return redirect('/user/signin/')
            return func(request, *args, **kwargs)
        return inner
    return required_authenticated
