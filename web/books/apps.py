from django.apps import AppConfig

class BooksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "books"

    def ready(self):
        # import signals to register them
        import books.signals  # noqa
