from django import forms


class AddCommentForm(forms.Form):
    """ Add Comment Form Definition """

    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Add your comment here"}),
    )
