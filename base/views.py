from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import stripe

def home(request):
    publishable_key = settings.STRIPE_PUBLIC_KEY
    context={
        'publishable_key':publishable_key
    }
    return render(request, 'base/home.html', context)


def Payment_Submit(request):
    # Getting post requests values
    stripeToken = request.POST.get('stripeToken')
    payment_amount = request.POST.get('payment_amount', 1)
    print(stripeToken, payment_amount)

    secret_key = settings.STRIPE_SECRET_KEY
    stripe.api_key = secret_key
    try:
        customer = stripe.Customer.create(
            email='guest@domain.com',
            description='Someone paid from your website.',
            source=stripeToken
        )
        amount = float(payment_amount)
        charge = stripe.Charge.create(
            amount=int(amount * 100),
            currency="aud",
            customer=customer,
            description="Payment for My website",
        )
        messages.success(request, 'Payment was Successfull !!')

    except stripe.error.CardError as e:
        messages.info(request, f"{e.error.message}")
        return redirect('home')

    except stripe.error.RateLimitError as e:
        messages.info(request, f"{e.error.message}")
        return redirect('home')
    except stripe.error.InvalidRequestError as e:
        messages.info(request, "Invalid Request !")
        return redirect('home')
    except stripe.error.AuthenticationError as e:
        messages.info(request, "Authentication Error !!")
        return redirect('home')
    except stripe.error.APIConnectionError as e:
        messages.info(request, "Check Your Connection !")
        return redirect('home')
    except stripe.error.StripeError as e:
        messages.info(request, "There was an error please try again !")
        return redirect('home')
    except Exception as e:
        messages.info(request, "A serious error occured we were notified !")
        return redirect('home')
    return redirect('home')






def payment_success(request):
    messages.success(request, 'Payment Success')
    return render(request, 'base/home.html')

def payment_failure(request):
    messages.error(request, 'Payment Failure')
    return render(request, 'base/home.html')

