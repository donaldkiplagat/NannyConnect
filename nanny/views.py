from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from .models import pro_skills, Location, Nanny, Rate, Report
from .forms import ContactForm, FilterNannies, BookNanny
from django.core.mail import send_mail, BadHeaderError

from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    nannies = Nanny.objects.all()[:4]

    return render(request,'index.html',{"nannies":nannies})

def about(request):

    return render(request,'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name':form.cleaned_data['first_name'],
                'last_name':form.cleaned_data['last_name'],
                'email_address':form.cleaned_data['email_address'],
                'message':form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'admin@example.com',['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("inquiry_received")
    form = ContactForm()

    return render(request,'contact.html',{'form':form})

def nannies(request):
    nannies = Nanny.objects.all()

    return render(request,'nannies.html',{"nannies":nannies})

def profile(request):

    return render(request,'profile.html')

def pricing(request):
    nannies = Nanny.objects.all()

    return render(request,'pricing.html',{"nannies":nannies})

def services(request):

    return render(request,'services.html')

def testimonial(request):

    return render(request,'testimonial.html')

def inquiry_received(request):

    return render(request,'inquiry_received.html')

@login_required(login_url='/accounts/login')
def order_history(request, client_id):
    reports = Report.filter_reports(client_id)

    print(reports)
    return render(request,'orders.html',{"reports":reports})

@login_required(login_url='/accounts/login')
def book_nanny(request, nanny_id):
    current_user = request.user
    nanny = Nanny.objects.get(id=nanny_id)


    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % ((nanny.rate.rate*nanny.min_hours)/116),
        'item_name': nanny.first_name,
        # 'invoice': (nanny.rate*10),
        'currency_code': 'USD',


    }
    try:
        nanny = Nanny.objects.get(id=nanny_id)
    except:
        raise ObjectDoesNotExist()

    form = PayPalPaymentsForm(initial=paypal_dict)


    report_instance = Report.objects.create(payment_status="Completed",nanny_first_name=nanny.first_name,nanny_last_name=nanny.last_name,nanny_phonenumber=nanny.phonenumber,nanny_rate=str(nanny.rate),total_cost=(nanny.rate.rate*nanny.min_hours),client_id=current_user.id,client_first_name=current_user.first_name,client_last_name=current_user.last_name,booked_hours=nanny.min_hours)



    return render(request,"book_nanny.html",{"nanny":nanny, 'form':form})

def search_results(request):

    if 'location' in request.GET and request.GET["location"] and 'skill' in request.GET and request.GET["skill"] and 'rate' in request.GET and request.GET["rate"]:
        search_term = request.GET.get("location")
        skill_search = request.GET.get("skill")
        rate_search = request.GET.get("rate")
        filtered_nannies = Nanny.filter_nannies(search_term, skill_search, rate_search).distinct()
        message=f"{search_term} and {skill_search} and {rate_search}"

        print(filtered_nannies)
        print(skill_search)

        return render(request,'filtered_nannies.html',{"message":message,"filtered_nannies":filtered_nannies})

    else:
        message = "You haven't searched for any term"
        return render(request,'filtered_nannies.html',{"message":message})


#Paypal views
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
        #...
        #...

            cart.clear(request)

            request.session['order_id'] = o.id
            return redirect('process_payment')


    else:
        form = CheckoutForm()
        return render(request, 'ecommerce_app/checkout.html', locals())

def process_payment(request):
    nanny = Nanny.objects.get(id=1)

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % 2,
        'item_name': 'Nanny',
        'invoice': str("Total Amount: 400"),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),

    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'ecommerce_app/process_payment.html', {'form': form})

@csrf_exempt
def payment_done(request):
    return render(request,'ecommerce_app/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'ecommerce_app/payment_cancelled.html')
