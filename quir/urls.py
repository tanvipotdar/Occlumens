from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
import views
#from views import NetworkView

urlpatterns = [
	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^search/$', views.search_screen, name="search"),
    url(r'^load_data/$', views.load_data, name = "load_data"),
    url(r'^search/create_network/$', views.create_network, name="create_network"),
    url(r'^search/expand/$', views.node_click, name="expand"),
    url(r'^search/create_network/info$', views.information, name="info"),
    url(r'^search/recommendations/$', views.get_recs, name="recommendations"),
    url(r'^search/save/$', views.saveToDB, name="save"),
    url(r'^search/ret/$', views.retreive_session, name="retreive")
]