from django.contrib.auth.forms import UserCreationForm
from leads.models import Agent

from django.contrib.auth import get_user_model
User = get_user_model()


class AgentCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
        )