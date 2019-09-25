from django.urls import path
from rental import views

urlpatterns = [
    path('api/price/<slug:fun>/<slug:quadrant>/<slug:p_type>/<int:active>', views.price_metrics, name='price_metrics'),
    path('api/ts/<slug:quadrant>/<slug:p_type>/<int:active>', views.time_series, name='time_series'),
    path('api/count/<slug:quadrant>/<slug:p_type>/<int:active>', views.listing_count, name='listing_count'),
    path('api/map_data', views.map_data, name='map_data'),
]
