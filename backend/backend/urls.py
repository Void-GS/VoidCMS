from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# PROJECT VIEWS
from voidcms.drf.views.clientViews import LoginView, LogoutView, RegisterView, GetAuthUserView, ClientsView
from voidcms.drf.views.cartViews import CartView
from voidcms.drf.views.settingsViews import SettingsView
from voidcms.drf.views.socialViews import SocialView
from voidcms.drf.views.categoryViews import CategoryView, CategoryPositionView
from voidcms.drf.views.productViews import ProductView, ProductPromotedView
from voidcms.drf.views.imageViews import ImageView
from voidcms.drf.views.pageViews import PageView
from voidcms.drf.views.cartViews import CartView
from voidcms.drf.views.orderViews import OrderView
from voidcms.drf.views.searchViews import SearchView
from voidcms.drf.views.backupViews import BackupView






urlpatterns = [
    # Backups
    path("settings/backup", BackupView.as_view(), name="backup-restore"),
    # Settings
    path("settings", SettingsView.as_view(), name="settings"),
    path('settings/<int:pk>', SettingsView.as_view(), name='settings-detail'),
    path("socials", SocialView.as_view(), name="socials"),
    path('socials/<int:pk>', SocialView.as_view(), name='social-detail'),
    # Users
    path("clients", ClientsView.as_view(), name='clients'),
    path('clients/<int:pk>', ClientsView.as_view(), name='clients-detail'),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("register", RegisterView.as_view(), name="register"),
    path("session", GetAuthUserView.as_view(), name="get-user"),
    path("cart", CartView.as_view(), name='cart'),
    # Orders
    path("orders", OrderView.as_view(), name='order'),
    path('orders/<int:pk>', OrderView.as_view(), name='order-detail'),
    # Pages
    path('pages', PageView.as_view(), name='page-list'),
    path('pages/<int:pk>', PageView.as_view(), name='page-detail'),
    # Categories
    path('categories', CategoryView.as_view(), name='category-list'),
    path('categories/<int:pk>', CategoryView.as_view(), name='category-detail'),
    path('categories/<int:pk>/position', CategoryPositionView.as_view(), name='category-positioning'),

    # Products
    path('products', ProductView.as_view(), name='product-list'),
    path('products/<int:pk>', ProductView.as_view(), name='product-detail'),
    path('products/promoted', ProductPromotedView.as_view(), name='products-promoted'),
    # Images
    path('images/<int:pk>', ImageView.as_view(), name='image-detail'),
    # Search
    path('search', SearchView.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
