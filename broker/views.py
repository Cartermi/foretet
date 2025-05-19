from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from .forms import UserRegistrationForm, UserLoginForm, SetPasswordForm, PasswordResetForm
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from .models import *
from .forms import *
from django.http import HttpResponse

# Create your views here.

def index(request):
    context = {}
    return render (request, "broker/index.html", context)


def about(request):
    context = {}
    return render (request, "broker/about.html", context)


def contact(request):
    context = {}
    return render (request, "broker/contact.html", context)

def contact_us(request):
    context = {}
    return render (request, "broker/contact-us.html", context)

def education(request):
    context = {}
    return render (request, "broker/education.html", context)

def faq(request):
    context = {}
    return render (request, "broker/faq.html", context)

def news(request):
    kycs = Kyc.objects.filter(user=request.user)

    context = {'kycs': kycs}
    return render(request, "broker/news.html", context)


def privacy_policy(request):
    context = {}
    return render (request, "broker/privacy-policy.html", context)


def privacy(request):
    context = {}
    return render (request, "broker/privacy.html", context)


def terms_and_condition(request):
    context = {}
    return render (request, "broker/terms-and-condition.html", context)


def template_activate_account(request):
    context = {}
    return render (request, "broker/template-activate-account.html", context)
    
def support(request):
    context = {}
    return render (request, "broker/support.html", context)

def investments(request):
    context = {}
    return render (request, "broker/investments.html", context)

@login_required(login_url="login")
def change_avatar(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, "broker/change-avatar.html", context)

@login_required (login_url = "login")
def change_password(request):
    context = {}
    return render (request, "broker/change-password.html", context)

@login_required (login_url = "login")
def crypto(request):
    context = {}
    return render (request, "broker/crypto.html", context)

@login_required (login_url = "login")
def dashboard(request):
    context = {}
    return render (request, "broker/dashboard.html", context)

@login_required (login_url = "login")
def deposit(request):
    context = {}
    return render (request, "broker/deposit.html", context)

@login_required (login_url = "login")
def fund_transfer(request):
    context = {}
    return render (request, "broker/fund-transfer.html", context)

@login_required (login_url = "login")
def kyc_form(request):
    kyc, created = Kyc.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = KycForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = KycForm(instance=kyc)

    return render(request, 'broker/kyc-form.html', {'form': form})


@login_required (login_url = "login")
def kyc(request):
    context = {}
    return render (request, "broker/kyc.html", context)

@login_required (login_url = "login")
def market(request):
    context = {}
    return render (request, "broker/market.html", context)

@login_required(login_url="login")
def settings(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, "broker/settings.html", context)


@login_required (login_url = "login")
def signal(request):
    context = {}
    return render (request, "broker/signal.html", context)

@login_required (login_url = "login")
def trade_history(request):
    user = request.user

    wiretransfers = Wiretransfer.objects.filter(user=user)
    banktransfers = Banktransfer.objects.filter(user=user)
    bitcoins = Bitcoin.objects.filter(user=user)

    context = {'wiretransfers':wiretransfers, 'banktransfers':banktransfers, 'bitcoins':bitcoins}
    return render (request, "broker/trade-history.html", context)


def verify(request):
    context = {}
    return render (request, "broker/verify.html", context)

@login_required(login_url="login")
def withdrawal_info(request):
    account, created = Account.objects.get_or_create(user=request.user)
    form = AccountForm(instance=account)

    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES, instance=account)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, "broker/withdrawal-info.html", context)

@login_required (login_url = "login")
def withdrawal(request):
    context = {}
    return render (request, "broker/withdrawal.html", context)

@user_not_authenticated
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.is_active=True
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('login')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name="broker/register.html",
        context={"form": form}
        )


@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("dashboard")

@user_not_authenticated
def custom_login(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("dashboard")

        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                
                messages.error(request, error) 

    form = UserLoginForm()

    return render(
        request=request,
        template_name="broker/login.html",
        context={"form": form}
        )

@login_required (login_url = "login")
def reset_password( request):
    return render (request, 'broker/reset-password.html') 


@user_not_authenticated
def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("broker/template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('login')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="broker/reset-password.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'broker/change-password.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("login")


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('login')



def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("broker/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def template_activate_account(request):
    context = {}
    return render (request, "broker/template-activate-account.html", context)


@login_required (login_url = "login")
def pin(request):
    context = {}
    return render (request, "broker/pin.html", context)


@login_required (login_url = "login")
def processing(request):
    return render (request, "broker/processing.html")


@login_required (login_url = "login")
def bitcoin_payout(request):
    user = request.user

    bitcoins = user.bitcoin_set.all()

    if request.method == 'POST':
        data = request.POST
        name = request.POST.get('name')
        transaction = request.POST.get('transaction')
        wallet = request.POST.get('wallet')
        gateway = request.POST.get('gateway')
        amount = request.POST.get('amount')
        charge = request.POST.get('charge')
        status = request.POST.get('status')
        time = request.POST.get('time')


        bitcoin, created = Bitcoin.objects.get_or_create(
            user=user,
            name=name,
            transaction=transaction,
            wallet=wallet,
            gateway=gateway,
            amount=amount,
            charge=charge,
            status=status,
            time=time
            )
        
        return redirect('pin')

    context = {'bitcoins':bitcoins}   
    return render (request, "broker/bitcoin_payout.html", context)

@login_required (login_url = "login")
def wire_transfer_payout(request):
    user = request.user

    wiretransfers = user.wiretransfer_set.all()

    if request.method == 'POST':
        data = request.POST
        name = request.POST.get('name')
        transaction = request.POST.get('transaction')
        bank = request.POST.get('bank')
        accountnumber = request.POST.get('accountnumber')
        gateway = request.POST.get('gateway')
        swift = request.POST.get('swift')
        amount = request.POST.get('amount')
        charge = request.POST.get('charge')
        status = request.POST.get('status')
        time = request.POST.get('time')


        wiretransfer, created = Wiretransfer.objects.get_or_create(
            user=user,
            name=name,
            bank=bank,
            transaction=transaction,
            accountnumber=accountnumber,
            gateway=gateway,
            swift=swift,
            amount=amount,
            charge=charge,
            status=status,
            time=time
            )
       
        return redirect('pin')

    context = {'wiretransfers': wiretransfers}
    return render (request, "broker/wire_transfer_payout.html", context)


@login_required (login_url = "login")
def bank_transfer_payout(request):
    user = request.user

    banktransfers = user.banktransfer_set.all()

    if request.method == 'POST':
        data = request.POST
        name = request.POST.get('name')
        transaction = request.POST.get('transaction')
        bank = request.POST.get('bank')
        accountnumber = request.POST.get('accountnumber')
        gateway = request.POST.get('gateway')
        swift = request.POST.get('swift')
        amount = request.POST.get('amount')
        charge = request.POST.get('charge')
        status = request.POST.get('status')
        time = request.POST.get('time')


        banktransfer, created = Banktransfer.objects.get_or_create(
            user=user,
            name=name,
            bank=bank,
            transaction=transaction,
            accountnumber=accountnumber,
            gateway=gateway,
            swift=swift,
            amount=amount,
            charge=charge,
            status=status,
            time=time
            )

        return redirect('pin')

    context = {'banktransfers': banktransfers} 
    return render (request, "broker/bank_transfer_payout.html", context)
