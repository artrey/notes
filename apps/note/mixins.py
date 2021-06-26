from django.contrib.auth.mixins import UserPassesTestMixin


class OwnerOrAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        user = self.request.user
        obj = self.get_object()
        return user.is_superuser or user.is_staff or user == obj.author


class OwnerOrAdminOrPublicRequiredMixin(OwnerOrAdminRequiredMixin):
    def test_func(self) -> bool:
        if super().test_func():
            return True
        note = self.get_object()
        return note.is_public
