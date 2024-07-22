from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'  # Ruta a tu plantilla personalizada
    success_url = reverse_lazy('password_reset_done')  # URL de redirección después de enviar el correo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí puedes configurar las variables protocol y domain
        context['protocol'] = 'https'  # Puedes establecer 'http' o 'https' según tu entorno de producción
        context['domain'] = 'ppppp.ppp'  # O usa un dominio fijo, e.g., 'example.com'
        return context
    