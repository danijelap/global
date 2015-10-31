from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings as msettings

admin.autodiscover()

urlpatterns = i18n_patterns("",
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    ("^admin/", include(admin.site.urls)),
)

if settings.USE_MODELTRANSLATION:
    urlpatterns += patterns('',
        url('^i18n/$', 'django.views.i18n.set_language', name='set_language'),
    )

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url("^beograd/?$", direct_to_template, {"template": "base.html"}, name="home"),
    ("^%s/" % settings.SITE_PREFIX, include("mezzanine.urls")),
    url(r'^', include('nekretnine.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
