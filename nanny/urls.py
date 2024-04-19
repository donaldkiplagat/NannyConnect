from django.conf.urls import url,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^about',views.about,name='about'),
    url(r'^contact',views.contact,name='contact'),
    url(r'^nannies',views.nannies,name='nannies'),
    url(r'^pricing',views.pricing,name='pricing'),
    # url(r'^services',views.services,name='services'),
    url(r'^testimonial',views.testimonial,name='testimonial'),
    url(r'^inquiry_received',views.inquiry_received,name='inquiry_received'),
    url(r'^search/',views.search_results,name='search_results'),
    url(r'^book_nanny/(\d+)',views.book_nanny,name='book_nanny'),
    url('order_history/(\d+)',views.order_history,name='order_history'),
    url(r'^process-payment/', views.process_payment, name='process_payment'),
    url(r'^payment_done/', views.payment_done, name='payment_done'),
    url(r'^payment_cancelled/', views.payment_canceled, name='payment_cancelled'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
