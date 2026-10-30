from django import forms


class ContactForm(forms.Form):
    """
    Customer contact form for the Cinematic SGnG Marketplace.
    """

    name = forms.CharField(
        max_length=100,
        label="Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your name",
                "autocomplete": "name",
            }
        ),
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "you@example.com",
                "autocomplete": "email",
            }
        ),
    )

    subject = forms.CharField(
        max_length=150,
        label="Subject",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Product question or marketplace inquiry",
            }
        ),
    )

    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(
            attrs={
                "rows": 7,
                "placeholder": "Tell us about your question "
                    "or marketplace inquiry.",
            }
        ),
    )