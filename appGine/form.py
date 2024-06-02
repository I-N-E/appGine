from django import forms
from django.forms import ModelForm 
from django.contrib.auth.models import User
from .models import DataUser,BlockPost

class FormUser(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','last_login','date_joined','is_active','is_staff']
        widgets = {
            'last_login':forms.TextInput(attrs={
                'readonly':'readonly',
                'style':'border: none'
            }),
            'date_joined':forms.TextInput(attrs={
                'readonly':'readonly',
                'style':'border: none'
            }),
            'is_active':forms.CheckboxInput(attrs={
                'disabled':'disabled'
            }),
            'is_staff':forms.CheckboxInput(attrs={
                'disabled':'disabled'
            })
        }

class Formdatauser(ModelForm):
    class Meta:
        model = DataUser
        fields = ['bio','picture','phone','birthday','sex','location']
        widgets = {
            'picture':forms.FileInput(attrs={
                'onchange':'submit',
                'style':'width: 325px;'
            }),
            'birthday':forms.DateInput(attrs={
                'type':'date'
            }),
            'phone':forms.NumberInput(attrs={
                'type':'number'
            })
        }

class FormPost(ModelForm):
    class Meta:
        model = BlockPost
        fields = ['title','post','picture_post']
        widgets = {
            'title':forms.TextInput(attrs={
                'id':'createPost_head'
            }),
            'post':forms.Textarea(attrs={
                'id':'createPost_body',  
            }),
            'picture_post':forms.FileInput(attrs={
                'onchange':'submit',
                'style':'width: 520px;'
            })
        }