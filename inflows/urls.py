from django.urls import path
from . import views

urlpatterns = [
    path("inflows/list", views.InflowListView.as_view(), name="inflow_list"),
    path("inflows/create", views.InflowCreateView.as_view(), name="inflow_create"),
    path(
        "inflows/<int:pk>/detail",
        views.InflowDetailView.as_view(),
        name="inflow_detail",
    ),
    path(
        "api/v1/inflows/",
        view=views.InflowListCreateApiView.as_view(),
        name="inflow-list-create-api-view",
    ),
    path(
        "api/v1/inflows/<int:pk>/",
        view=views.InflowRetrieveApiView.as_view(),
        name="inflow-retrieve-api-view",
    ),
]
