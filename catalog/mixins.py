from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)


class StaffRequiredMixin(
    LoginRequiredMixin,
    UserPassesTestMixin,
):
    """
    Allow access only to authenticated active staff users.

    Anonymous users are redirected to Login.
    Authenticated nonstaff users receive HTTP 403.
    """

    raise_exception = True
    permission_denied_message = (
        "Staff access is required to manage products."
    )

    def test_func(self):
        user = self.request.user

        return (
            user.is_authenticated
            and user.is_active
            and user.is_staff
        )