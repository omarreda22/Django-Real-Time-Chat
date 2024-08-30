from django import forms

from .models import ChatMessage


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ["message"]

    def __init__(self, *args, **kwargs):
        super(ChatMessageForm, self).__init__(*args, **kwargs)

        self.fields["message"].widget.attrs["placeholder"] = "Type your message..."
