from django.contrib import sitemaps
from django.core.urlresolvers import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['register', 'terms', 'tutorial', 'about', 'login', 'objekti',
                ('objekti', 'novi'), ('objekti', 'zemun'), ('objekti', 'centar'),
                ('objekti', 'kosa'), ('objekti', 'palilula')]

    def location(self, item):
        if isinstance(item, str):
            return reverse(item)
        elif isinstance(item, tuple):
            item_name, item_arg = item
            return reverse(item_name, args=(item_arg,))