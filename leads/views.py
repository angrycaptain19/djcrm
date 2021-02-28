from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from agents.views import OrganisorAndLoginRequiredMixin
from .models import Lead, Agent, Category
from .forms import (
    LeadModelForm,
    CustomUserCreationForm,
    LeadAssignAgentForm,
    LeadCategoryUpdateForm
)


class SignupView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'


class LeadListView(LoginRequiredMixin, generic.ListView):
    model = Lead
    template_name = 'leads/lead_list.html'

    def get_queryset(self):
        return get_user_objects(self.request.user, super().get_queryset())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'leads': context['object_list'].filter(agent__isnull=False),
            'leads_unassigned': context['object_list'].filter(agent__isnull=True)
        })

        return context


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    model = Lead
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        return get_user_objects(self.request.user, super().get_queryset())


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    model = Lead
    form_class = LeadModelForm
    template_name = 'leads/lead_create.html'
    success_url = reverse_lazy('leads:lead-list')

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(
            subject=f'The new Lead has been created',
            message='Go to site to see the Lead',
            from_email='test@test.com',
            recipient_list=['test2@test.com']
        )

        return super().form_valid(form)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    model = Lead
    form_class = LeadModelForm
    template_name = 'leads/lead_update.html'

    def get_queryset(self):
        return get_user_objects(self.request.user, super().get_queryset())


class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    model = Lead
    template_name = 'leads/lead_delete.html'
    success_url = reverse_lazy('leads:lead-list')

    def get_queryset(self):
        return get_user_objects(self.request.user, super().get_queryset())


class LeadAssigneAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = 'leads/lead_assign_agent.html'
    form_class = LeadAssignAgentForm
    success_url = reverse_lazy('leads:lead-list')

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request
        })

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'lead': Lead.objects.get(id=self.kwargs['pk'])
        })
        
        return context

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super().form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = 'leads/categorsy_list.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        unassigned_leads = get_user_objects(
            user,
            Lead.objects.filter(category__isnull=True)
        )
        context = super().get_context_data(**kwargs)
        context.update({
            'unassigned_leads_count': unassigned_leads.count()
        })
        
        return context


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Category
    template_name = 'leads/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context.update({
            'leads': get_user_objects(user, self.get_object().leads.all())
        })
        
        return context


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Lead
    form_class = LeadCategoryUpdateForm
    template_name = 'leads/category_update.html'

    def get_queryset(self):
        return get_user_objects(self.request.user, super().get_queryset())
    


def get_user_objects(user, objects):
    if user.is_organisor:
        return objects.filter(organisation=user.userprofile)
    else:
        queryset = objects.filter(organisation=user.agent.organisation)
        queryset = queryset.filter(agent__user=user)

    return queryset