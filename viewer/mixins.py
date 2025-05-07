from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_staff:
            return True
        raise PermissionDenied("Nemáte oprávnění k této akci.")
