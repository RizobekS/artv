from django.urls import path

from . import views

# namespace
app_name = "general"
urlpatterns = [
    path('partners', views.PartnersView.as_view(), name='partners_page'),
    path('aac', views.AacView.as_view(), name='aac_page'),
    path('aocv', views.AocvView.as_view(), name='aocv_page'),
    path('auctionrules', views.AuctionRulesView.as_view(), name='auctionrules_page'),
    path('about/<int:id>/', views.AboutDetail.as_view(), name="about_detail_page"),
    path('about/experts/', views.ExpertsView.as_view(), name="experts_page"),
    path('about/team/', views.TeamMemberExtraView.as_view(), name="team_page"),
    path('artists/', views.Artists.as_view(), name="artists_page"),
    path('artists/<int:id>/', views.ArtistDetail.as_view(), name="artists_detail_page"),
    path('artists/craftmanship/<slug:slug>/', views.CraftmanshipView.as_view(), name="craftmanship_page"),
    path('catalog/', views.Catalog.as_view(), name="catalog_page"),
    path('catalog/<slug:slug>/', views.catalog_detail, name="catalog_detail_page"),
    path('auctions/', views.Auctions.as_view(), name="auctions_page"),
    path('auction/<slug:slug>/', views.AuctionDetail.as_view(), name="auctions_detail_page"),
    path('profile/', views.profile, name="profile_page"),

    path('gallery/', views.gallery_details, name="gallery_page"),
    path('gallery/<int:pk>/',
         views.gallery_details,
         name="gallery_detail_page"),

    path('gallery-api/', views.gallery_details_api, name="gallery_api"),
    path('gallery-api/2/', views.gallery_applied_art_api, name="gallery_details_api"),
    path('gallery-api/<int:pk>/', views.gallery_details_api, name="gallery_details_api"),


    path('blog/', views.Blog.as_view(), name="blog_page"),
    path('blog/<slug:slug>/', views.BlogDetail.as_view(), name="blog_detail_page"),
    path('services/', views.ServicesView.as_view(), name="services_page"),
    path('services/<slug:slug>/',
         views.ServicesDetail.as_view(),
         name="services_detail_page"),
    path('contact/', views.contact_page, name="contact_page"),

    path('cart/', views.cart_page, name="cart_page"),
    path('order/', views.order_page, name="order_page"),
    path('favorites/', views.favorites_page, name="favorites_page"),
    path('history/', views.history_page, name="history_page"),
    path('search/', views.search, name="search"),
    path('search-api/', views.search_api, name="search_api"),
    path('sell/', views.sell, name="sell_page"),
    path('types/', views.GenresView.as_view(), name="genres_page"),
    path('types/<slug:slug>/', views.GenresDetailView.as_view(), name="genres_detail_page"),
    path('applied-types/', views.AppliedArtTypesView.as_view(), name="applied_types_page"),
    path('applied-types/<int:num>/', views.appliedart_types_detail, name="applied_types_detail_page"),

    path('robot/', views.robot, name="robot")
]
