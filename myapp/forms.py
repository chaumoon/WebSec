from django import forms

class loginForm(forms.Form):
    username = forms.CharField(label="Tên đăng nhập", max_length=100)
    password = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput)

class registerForm(forms.Form):
    username = forms.CharField(label="Tên đăng nhập", max_length=100)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    check_pass = password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        check_pass = cleaned_data.get("check_pass")
        if password and check_pass and password != check_pass:
            raise forms.ValidationError("Mật khẩu không khớp!")
        return cleaned_data

class forgotForm(forms.Form):
    username = forms.CharField(label="Tên đăng nhập", max_length=100)
    email = forms.EmailField(label="Email")