from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from writer.models import Article
from .models import Subscription
from account.models import CustomUser
from .paypal import *


@login_required(login_url='my-login')
def client_dashboard(request):
    try:
        subDetails = Subscription.objects.get(user=request.user)
        subscriptionPlan = subDetails.subscription_plan
    except:
        subscriptionPlan = "None"

    context = {'subPlan': subscriptionPlan}
    return render(request, 'client/client-dashboard.html', context=context)
    

@login_required(login_url='my-login')
def browse_articles(request):
    try:
        subDetails = Subscription.objects.get(user=request.user, is_active=True)
    except:
        return redirect('subscription-locked')
    
    currentSubscriptionPlan = subDetails.subscription_plan
    
    if currentSubscriptionPlan == "Standard":
        articles = Article.objects.all().filter(is_premium=False)
    elif currentSubscriptionPlan == "Premium":
        articles = Article.objects.all()

    context = {'allClientArticles': articles}

    return render(request, 'client/browse-articles.html', context=context)


@login_required(login_url='my-login')
def subscription_locked(request):
    return render(request, 'client/subscription-locked.html')


@login_required(login_url='my-login')
def subscription_plans(request):
    return render(request, 'client/subscription-plans.html')


@login_required(login_url='my-login')
def client_account_management(request):
    try:
        subDetails = Subscription.objects.get(user=request.user)

        subscription_id = subDetails.paypal_subscription_id

        context = {'SubscriptionID': subscription_id}

        return render(request, 'client/account-management.html', context)
    except:
        return render(request, 'client/account-management.html')


@login_required(login_url='my-login')
def create_subscription(request, subID, plan):
    custom_user = CustomUser.objects.get(email=request.user)

    firstName = custom_user.first_name
    lastName = custom_user.last_name

    full_name = firstName + " " + lastName

    selected_sub_plan = plan

    if selected_sub_plan == "Standard":
        sub_cost = "4.99"
    elif selected_sub_plan == "Premium":
        sub_cost = "9.99"

    subscription = Subscription.objects.create(
        subscriber_name=full_name, 
        subscription_plan=selected_sub_plan, 
        subscription_cost=sub_cost,
        paypal_subscription_id=subID,
        is_active=True,
        user=request.user 
    )

    context = {
        'SubscriptionPlan': selected_sub_plan
    }

    return render(request, 'client/create-subscription.html', context)


@login_required(login_url='my-login')
def delete_subscription(request, subID):
    # Delete Subscription from Paypal
    access_token = get_access_token()
    cancel_subscription_paypal(access_token, subID)

    # Delete a subscription from Django (application side)
    subscription = Subscription.objects.get(user=request.user, paypal_subscription_id=subID)

    subscription.delete()

    return render(request, 'client/delete-subscription.html')
