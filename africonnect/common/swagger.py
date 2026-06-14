class SwaggerSafeMixin:

    def is_swagger(self):

        return getattr(self, "swagger_fake_view", False)

    def safe_user(self):

        user = getattr(self.request, "user", None)

        if not user or not user.is_authenticated:
            return None

        return user

    def safe_supplier(self):

        user = self.safe_user()

        if not user:
            return None

        return getattr(user, "supplier_profile", None)

    def empty_queryset(self, model):

        return model.objects.none()
