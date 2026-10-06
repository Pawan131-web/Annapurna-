import json
from urllib.parse import urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView


def authenticate_user(request, identifier, password):
    if not identifier or not password:
        return None
    identifier = identifier.strip()
    # 1. Try direct exact match first
    user = authenticate(request, username=identifier, password=password)
    if user:
        return user
    # 2. Try candidate users matching case-insensitively or by email
    candidates = User.objects.filter(username__iexact=identifier) | User.objects.filter(email__iexact=identifier)
    if '@' in identifier:
        prefix = identifier.split('@')[0]
        candidates = candidates | User.objects.filter(username__iexact=prefix)

    for candidate in candidates.distinct():
        user = authenticate(request, username=candidate.username, password=password)
        if user:
            return user
    return None


@method_decorator(csrf_exempt, name='dispatch')
class ShopLoginView(View):
    """
    Direct Admin Portal Authentication View.
    Accepts login from the frontend store modal (JSON fetch or Form POST),
    authenticates store admins, initializes their session, and redirects/responds
    with the direct admin dashboard URL.
    """

    def get_frontend_base_url(self, request):
        frontend_base = getattr(settings, 'FRONTEND_URL', 'http://127.0.0.1:8000')
        referer = request.META.get('HTTP_REFERER', '')
        if referer:
            parsed = urlparse(referer)
            if '8000' in parsed.netloc or '5500' in parsed.netloc or 'localhost' in parsed.netloc or '127.0.0.1' in parsed.netloc:
                path = parsed.path if parsed.path and parsed.path != '/' else ''
                return f"{parsed.scheme}://{parsed.netloc}{path}"
        return frontend_base

    def get(self, request, *args, **kwargs):
        next_url = request.GET.get('next', '/dashboard/')
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            return HttpResponseRedirect(next_url)

        frontend_target = self.get_frontend_base_url(request)
        delimiter = '&' if '?' in frontend_target else '?'
        redirect_url = f"{frontend_target}{delimiter}admin_login=1&next={next_url}"
        return HttpResponseRedirect(redirect_url)

    def post(self, request, *args, **kwargs):
        is_json = False
        data = {}

        if request.content_type and 'application/json' in request.content_type:
            is_json = True
            try:
                data = json.loads(request.body.decode('utf-8'))
            except (ValueError, UnicodeDecodeError):
                data = {}
        else:
            data = request.POST.dict()

        identifier = data.get('identifier') or data.get('username') or data.get('email', '')
        password = data.get('password', '')
        next_url = data.get('next') or request.GET.get('next') or '/dashboard/'

        if not identifier or not password:
            msg = 'Please provide both username/email and password.'
            if is_json or request.headers.get('Accept') == 'application/json':
                return JsonResponse({'success': False, 'message': msg}, status=400)
            frontend_target = self.get_frontend_base_url(request)
            delimiter = '&' if '?' in frontend_target else '?'
            return HttpResponseRedirect(f"{frontend_target}{delimiter}admin_login=1&error=missing_fields")

        user = authenticate_user(request, identifier, password)

        if user is None:
            msg = 'Invalid username or password. Please verify your admin credentials.'
            if is_json or request.headers.get('Accept') == 'application/json':
                return JsonResponse({'success': False, 'message': msg}, status=401)
            frontend_target = self.get_frontend_base_url(request)
            delimiter = '&' if '?' in frontend_target else '?'
            return HttpResponseRedirect(f"{frontend_target}{delimiter}admin_login=1&error=invalid_credentials")

        if not user.is_active:
            msg = 'Your administrator account is inactive. Please contact system support.'
            if is_json or request.headers.get('Accept') == 'application/json':
                return JsonResponse({'success': False, 'message': msg}, status=403)
            return HttpResponseRedirect(f"{self.get_frontend_base_url(request)}?admin_login=1&error=inactive")

        if not (user.is_staff or user.is_superuser):
            msg = 'Access denied. You need store administrator privileges to enter the admin portal.'
            if is_json or request.headers.get('Accept') == 'application/json':
                return JsonResponse({'success': False, 'message': msg}, status=403)
            return HttpResponseRedirect(f"{self.get_frontend_base_url(request)}?admin_login=1&error=forbidden")

        # Authenticate session
        auth_login(request, user)

        # Build absolute dashboard redirect URL
        if not next_url.startswith('http'):
            if not next_url.startswith('/'):
                next_url = '/' + next_url
            dashboard_url = request.build_absolute_uri(next_url)
        else:
            dashboard_url = next_url

        if is_json or request.headers.get('Accept') == 'application/json':
            return JsonResponse({
                'success': True,
                'message': 'Authentication successful. Redirecting to admin portal...',
                'redirect_url': dashboard_url,
                'dashboard_url': request.build_absolute_uri('/dashboard/'),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email or f"{user.username}@annapurnastore.com",
                    'name': user.get_full_name() or user.username.title(),
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser
                }
            })

        return HttpResponseRedirect(dashboard_url)


@method_decorator(csrf_exempt, name='dispatch')
class ShopLogoutView(View):
    """
    Admin Logout View. Clears session and redirects directly to the store home page.
    """

    def get_frontend_base_url(self, request):
        return getattr(settings, 'FRONTEND_URL', 'http://127.0.0.1:8000').rstrip('/') + '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        frontend_target = self.get_frontend_base_url(request)
        return redirect(frontend_target)

    def post(self, request, *args, **kwargs):
        auth_logout(request)
        frontend_target = self.get_frontend_base_url(request)
        if request.headers.get('Accept') == 'application/json' or (request.content_type and 'application/json' in request.content_type):
            return JsonResponse({'success': True, 'message': 'Logged out successfully', 'redirect_url': frontend_target})
        return redirect(frontend_target)


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)


class UserListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 15

    def get_queryset(self):
        qs = User.objects.select_related('profile').all().order_by('-is_superuser', '-is_staff', 'username')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(username__icontains=q) |
                Q(email__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        all_users = User.objects.all()
        ctx['total_users'] = all_users.count()
        ctx['active_users'] = all_users.filter(is_active=True).count()
        ctx['admin_users'] = all_users.filter(Q(is_superuser=True) | Q(profile__role='admin')).count()
        return ctx


class UserCreateView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '').strip()
        role = request.POST.get('role', 'staff').strip().lower()
        is_active = request.POST.get('is_active') == 'on' or request.POST.get('is_active') == 'true'

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return redirect('accounts:user_list')

        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" is already taken. Please choose another.')
            return redirect('accounts:user_list')

        is_admin = (role == 'admin')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=is_admin,
            is_active=is_active
        )

        from .models import Profile
        Profile.objects.update_or_create(
            user=user,
            defaults={'role': Profile.Role.ADMIN if is_admin else Profile.Role.STAFF}
        )

        messages.success(request, f'User "{username}" created successfully with {role.title()} privileges.')
        return redirect('accounts:user_list')


class UserToggleStatusView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            messages.error(request, 'You cannot deactivate your own account.')
            return redirect('accounts:user_list')

        user.is_active = not user.is_active
        user.save()
        status_text = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'User "{user.username}" has been {status_text}.')
        return redirect('accounts:user_list')


class UserDeleteView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            messages.error(request, 'You cannot delete your own account.')
            return redirect('accounts:user_list')

        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" has been removed.')
        return redirect('accounts:user_list')

