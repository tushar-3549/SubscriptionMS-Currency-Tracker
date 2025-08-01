import requests
from datetime import timedelta, date
from django.db import transaction
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Plan, Subscription, ExchangeRateLog
from .serializers import PlanSerializer, SubscriptionSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe(request):
    plan_id = request.data.get('plan_id')
    try:
        plan = Plan.objects.get(id=plan_id)
        with transaction.atomic():
            end_date = date.today() + timedelta(days=plan.duration_days)
            subscription = Subscription.objects.create(
                user=request.user,
                plan=plan,
                end_date=end_date,
                status='active'
            )
            return Response(SubscriptionSerializer(subscription).data, status=201)
    except Plan.DoesNotExist:
        return Response({"error": "Plan not found"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_subscriptions(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    serializer = SubscriptionSerializer(subscriptions, many=True)
    return Response(serializer.data)



def subscription_list(request):
    subscriptions = Subscription.objects.select_related('user', 'plan').all()
    return render(request, 'subscriptions/subscription_list.html', {'subscriptions': subscriptions})




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_subscription(request):
    sub_id = request.data.get('subscription_id')
    try:
        subscription = Subscription.objects.get(id=sub_id, user=request.user)
        subscription.status = 'cancelled'
        subscription.save()
        return Response({'status': 'cancelled'})
    except Subscription.DoesNotExist:
        return Response({"error": "Subscription not found"}, status=404)

@api_view(['GET'])
@permission_classes([AllowAny])
def exchange_rate(request):
    base = request.GET.get('base', 'USD')
    target = request.GET.get('target', 'BDT')
    url = f"https://open.er-api.com/v6/latest/{base}"
    res = requests.get(url)
    data = res.json()
    rate = data['rates'].get(target)
    if rate:
        ExchangeRateLog.objects.create(base_currency=base, target_currency=target, rate=rate)
        return Response({'rate': rate})
    return Response({'error': 'Rate not found'}, status=400)