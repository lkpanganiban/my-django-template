from django import forms
from .models import FileSet, Files, Group


class FileSetForm(forms.Form):
    group_access = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = FileSet
        fields = (
            "group_access",
            "tags"
        )
