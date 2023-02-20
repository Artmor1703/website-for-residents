from django import forms
from django.contrib import admin
from .models import *
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('apartment', 'fio', 'email', 'telenum',  'quadrature',  'is_admin')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('apartment', 'fio', 'email', 'telenum',  'quadrature',  'is_admin')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('apartment', 'fio', 'email', 'telenum',  'quadrature',  'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal info', {'fields': ('fio', 'telenum', 'email',)}),
        ('Apartment', {'fields': ('apartment', 'quadrature',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('apartment', 'quadrature', 'password1', 'password2'),
        }),
    )
    search_fields = ('apartment',)
    ordering = ('apartment',)
    filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)
admin.site.register(News)
admin.site.register(Feedback)


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'title',

    )


class ChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'question',
    )
    list_filter = ('question',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'question',
        'choice',
    )
    list_filter = ('user',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
