from django import forms
from recipe.models import Ohje, Comment

class AddRecipeForm(forms.ModelForm):

    class Meta:
        model = Ohje
        fields = ["title", "dish", "cooking_time", "ingredients", "body", "image"]

class UpdateRecipeForm(forms.ModelForm):

    class Meta:
        model = Ohje
        fields = ["title", "dish", "cooking_time", "ingredients", "body", "image"]

        def save(self, commit=True):
            ohje = self.instance

            ohje.title = self.cleaned_data["title"]
            ohje.dish = self.cleaned_data["dish"]
            ohje.cooking_time = self.cleaned_data["cooking_time"]
            ohje.ingredients = self.cleaned_data["ingredients"]
            ohje.body = self.cleaned_data["body"]

            if self.cleaned_data['image']:
                ohje.image=self.cleaned_data["image"]

            if commit:
                ohje.save()
            return ohje


class AddCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["author", "text"]
