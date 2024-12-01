from django.apps import AppConfig


# class VinelandConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'vineland'

class VinelandConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vineland'
    verbose_name = 'Test Vineland'

    def ready(self):
        # Import ici pour éviter les imports circulaires
        from django.contrib.admin.apps import AdminConfig

        # Personnalisation de l'admin
        AdminConfig.default_site = 'vineland.admin.VinelandAdminSite'