from django.views.generic import DetailView, ListView, TemplateView, View
from django.shortcuts import render
from django.conf import settings
from home.models import Page, Section, Article, Image, Faq
from django.utils.translation import get_language

class AboutView(ListView):
    """A view to return the about page and show all sections"""
    model = Page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = Page.objects.get(slug='about')
        if self.request.htmx:
            context['section'] = Section.objects.get(
                id=self.request.GET['name'])
            context['articles'] = Article.objects.filter(
                section=context['section'])
            if Image.objects.filter(articles__in=context['articles']).exists():
                context['images'] = Image.objects.filter(
                    articles__in=context['articles'])
            elif Image.objects.filter(sections=context['section']).exists():
                context['images'] = Image.objects.filter(
                    sections=context['section'])
            return context
        else:
            context['sections'] = Section.objects.filter(page=context['page'])
        return context
    
    def get_template_names(self):
        if self.request.htmx:
            return 'includes/about_items.html'
        return 'pages/about.html'
    

class PageDetailView(DetailView):
    """ A view to show individual image with details """
    model = Page

    def get_slug_field(self) -> str:
        if get_language() == 'no':
            return 'slug_no'
        return super().get_slug_field()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.htmx:
            context['section'] = Section.objects.get(
                id=self.request.GET['name'])
            context['articles'] = Article.objects.filter(
                section=context['section'])
            if Image.objects.filter(articles__in=context['articles']).exists():
                context['images'] = Image.objects.filter(
                    articles__in=context['articles'])
            elif Image.objects.filter(sections=context['section']).exists():
                context['images'] = Image.objects.filter(
                    sections=context['section'])
            if self.object.name == 'faq':
                context['object_list'] = Faq.objects.all()
            return context
        else:
            context['sections'] = Section.objects.filter(page=self.object)
            return context

    def get_template_names(self):
        page_name = self.object.name
        if self.request.htmx:
            return f"includes/{page_name}_items.html"
        return 'pages/about.html'
