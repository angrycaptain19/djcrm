import random

from django.core.mail import send_mail
from django.shortcuts import render, reverse
from django.views import generic

from leads.models import Agent
from .forms import AgentCreateForm
from .mixins import OrganisorAndLoginRequiredMixin


class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    model = Agent
    template_name = 'agents/agent_list.html'

    def get_queryset(self):
        organisation = self.request.user.userprofile

        return self.model.objects.filter(organisation=organisation)


class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    form_class = AgentCreateForm
    template_name = 'agents/agent_create.html'
    
    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(str(random.randint(0, 10000)))
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        send_mail(
            subject='You are invited to be an agent',
            message='You were added as an agent on DJCRM. Please come login to start working',
            from_email=self.request.user.email,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    model = Agent
    template_name = 'agents/agent_detail.html'
    context_object_name = 'agent'


class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    model = Agent
    form_class = AgentCreateForm
    template_name = 'agents/agent_update.html'


class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    model = Agent
    template_name = 'agents/agent_delete.html'

    def get_success_url(self):
        return reverse('agents:agent-list')