import smtplib 

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
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
        Send a validated SGnG contact inquiry through the 
        configured email backend.
        """

        name = form.cleaned_data["name"]
        visitor_email = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        message = form.cleaned_data["message"]

        email_subject = f"SGnG Contact Inquiry: {subject}"

        email_body = (
            "A new message was submitted through the "
            "Cinematic SGnG Marketplace contact form.\n\n"
            f"Name: {name}\n"
            f"Email: {visitor_email}\n"
            f"Subject: {subject}\n\n"
            "Message:\n"
            f"{message}\n"
        )

        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL],
            reply_to=[visitor_email],
        )

        try:
            sent_count = email.send(fail_silently=False)
        except (
            smtplib.SMTPException,
            OSError,
        ):
            form.add_error(
                None,
                (
                    "Your message could not be sent at this time. "
                    "Please verify the email configuration or try "
                    "again later."
                ),
            )

            return self.form_invalid(form)

        if sent_count != 1:
            form.add_error(
                None,
                (
                    "The email service did not confirm delivery. "
                    "Please try again."
                ),
            )

            return self.form_invalid(form)

        messages.success(
            self.request,
            (
                "Thank you for contacting SGnG. "
                "Your message was received successfully."
            ),
        )

        return super().form_valid(form)
