from django.urls import path
from . import views

urlpatterns = [
    path("categories/list/", views.CategoryListView.as_view(), name="category_list"),
    path(
        "categories/create/", views.CategoryCreateView.as_view(), name="category_create"
    ),
    path(
        "categories/<int:pk>/detail/",
        views.CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "categories/<int:pk>/update/",
        views.CategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "categories/<int:pk>/delete/",
        views.CategoryDeleteView.as_view(),
        name="category_delete",
    ),
    path(
        "api/v1/categories/",
        view=views.CategoryListCreateApiView.as_view(),
        name="category-list-create-api-view",
    ),
    path(
        "api/v1/categories/<int:pk>/",
        view=views.CategoryRetrieveUpdateDestroyAPIView.as_view(),
        name="category-retrieve-update-destroy-api-view",
    ),
]
