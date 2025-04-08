from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from rest_framework import generics
from .models import Product
from brands.models import Brand
from categories.models import Category
from . import forms, models, serializers
from app import metrics


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"
    paginate_by = 10
    permission_required = "products.view_product"

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get("title")
        category = self.request.GET.get("category")
        brand = self.request.GET.get("brand")
        serie_number = self.request.GET.get("serie_number")
        if title:
            queryset = queryset.filter(title__icontains=title)
        if category:
            queryset = queryset.filter(category__id=category)
        if brand:
            queryset = queryset.filter(brand__id=brand)
        if serie_number:
            queryset = queryset.filter(serie_number__icontains=serie_number)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["brands"] = Brand.objects.all()
        context["product_metrics"] = metrics.get_product_metrics()
        return context


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    template_name = "product_create.html"
    form_class = forms.ProductModelForm
    success_url = reverse_lazy("product_list")
    permission_required = "products.add_product"


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    template_name = "product_detail.html"
    permission_required = "products.view_product"


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = "product_update.html"
    form_class = forms.ProductModelForm
    success_url = reverse_lazy("product_list")
    permission_required = "products.change_product"


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = "product_delete.html"
    success_url = reverse_lazy("product_list")
    permission_required = "products.delete_product"


class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ProductRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
