from django.urls import path
from . import views
app_name="events"

urlpatterns=[
    # TODO: Add event list URL.
    # path("",views.event_list,name="event_list"),
    path('', views.event_list, name='event_list'),

    # TODO: Add event detail URL.
    # path("event/<int:event_id>/",views.event_detail,name="event_detail"),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    # TODO: Add login/logout URLs.
    # path("login/",views.user_login,name="login"),
    # path("logout/",views.user_logout,name="logout"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # TODO: Add registration URL.
    # path("event/<int:event_id>/register/",views.register_event,name="register_event"),
    path('event/<int:event_id>/register/', views.register_event, name='register_event'),
    # TODO: Add create/edit/delete URLs.
    path('event/create/', views.create_event, name='create_event'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
]
