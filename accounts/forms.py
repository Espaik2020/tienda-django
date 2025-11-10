from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "display_name", "avatar",
            "phone", "gamer_tag", "favorite_platform", "birth_date",
            "street", "district", "city", "state", "zipcode",
            "newsletter_ok",
        ]
        labels = {
            "display_name": "Nombre a mostrar",
            "avatar": "Foto de perfil",
            "phone": "Teléfono",
            "gamer_tag": "Gamer tag",
            "favorite_platform": "Plataforma favorita",
            "birth_date": "Fecha de nacimiento",
            "street": "Calle",
            "district": "Colonia",
            "city": "Ciudad",
            "state": "Estado",
            "zipcode": "CP",
            "newsletter_ok": "Quiero recibir ofertas y novedades",
        }
        widgets = {
            "display_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Tu nombre público",
                "autocomplete": "off",
            }),
            "avatar": ClearableFileInput(attrs={
                "class": "form-control",      # <-- hace visible el file input
                "accept": "image/*",
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej. 444-123-4567",
                "autocomplete": "tel",
            }),
            "gamer_tag": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Tu alias gamer",
                "autocomplete": "off",
            }),
            "favorite_platform": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "PlayStation / Xbox / Nintendo / PC",
            }),
            "birth_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
            }),
            "street": forms.TextInput(attrs={"class": "form-control"}),
            "district": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "zipcode": forms.TextInput(attrs={"class": "form-control"}),
            "newsletter_ok": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegura estilo consistente en tema oscuro y limpia help_texts
        for name, field in self.fields.items():
            if name == "newsletter_ok":
                continue  # checkbox conserva su clase
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " form-control").strip()
            field.help_text = ""
