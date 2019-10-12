from django.urls import path
from rental import views

urlpatterns = [
    path(
        "api/price/<slug:fun>/<slug:quadrant>/<slug:community>/<slug:p_type>/<int:active>",
        views.price_metrics,
        name="price_metrics",
    ),
    path(
        "api/ts/<slug:quadrant>/<slug:community>/<slug:p_type>/<int:active>",
        views.time_series,
        name="time_series",
    ),
    path(
        "api/scatter/<slug:quadrant>/<slug:community>/<slug:p_type>/<int:active>",
        views.scatter_data,
        name="scatter_data",
    ),
    path(
        "api/count/<slug:quadrant>/<slug:community>/<slug:p_type>/<int:active>",
        views.listing_count,
        name="listing_count",
    ),
    path(
        "api/market/<slug:quadrant>/<slug:community>/<slug:p_type>/<int:active>",
        views.market_share,
        name="market_share",
    ),
    path("api/map/<slug:quadrant>/<slug:community>/<slug:p_type>/<int:active>",
        views.map_data, name="map_data"),
        
    path("api/community_list", views.community_list, name="community_list"),
]
