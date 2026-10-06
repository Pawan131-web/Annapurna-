from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CategoryForm
from .models import Category


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_queryset(self):
        qs = Category.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'categories/category_detail.html'
    context_object_name = 'category'


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:list')

    def form_valid(self, form):
        messages.success(self.request, f'Category "{form.instance.name}" created.')
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:list')

    def form_valid(self, form):
        messages.success(self.request, f'Category "{form.instance.name}" updated.')
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'categories/category_confirm_delete.html'
    success_url = reverse_lazy('categories:list')

    def form_valid(self, form):
        messages.success(self.request, 'Category deleted.')
        return super().form_valid(form)
