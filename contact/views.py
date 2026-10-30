from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import ContactForm


class ContactView(FormView):
    """
    Display and process the SGnG customer contact form.
    """

    template_name = "contact/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact:contact")

    def form_valid(self, form):
        """
        Process a valid submission.

        Email delivery will be configured separately for
        production. For Phase I, validation and successful
        submission feedback demonstrate the required
        contact workflow.
        """

        messages.success(
            self.request,
            (
                "Thank you for contacting SGnG. "
                "Your message was received successfully."
            ),
        )

        return super().form_valid(form)
