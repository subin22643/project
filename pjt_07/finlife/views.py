from django.shortcuts import render
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import requests
from .models import DepositProducts, DepositOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer

BASE_URL = 'https://finlife.fss.or.kr/finlifeapi/'

@api_view(['GET'])
def index(request):
    URL = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth' : settings.API_KEY,
        # 금융회사 코드 : 은행
        'topFinGrpNo' : '020000',
        'pageNo' : 1
    }
    response = requests.get(URL, params=params).json()
    return JsonResponse({ 'response' : response })

# requests 모듈을 활용하여
# 정기예금 상품 목록 데이터를 가져와
# 정기예금 상품 목록, 옵션 목록을 DB에 저장
@api_view(['GET'])
def save_deposit_products(request):
    URL = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth' : settings.API_KEY,
        # 금융회사 코드 : 은행
        'topFinGrpNo' : '020000',
        'pageNo' : 1
    }
    response = requests.get(URL, params=params).json()
    base_response = response['result']['baseList']
    option_response = response['result']['optionList']
    
    for base in base_response:
        save_data = {
            'fin_prdt_cd' : base.get('fin_prdt_cd'),
            'kor_co_nm' : base.get('kor_co_nm'),
            'fin_prdt_nm' : base.get('fin_prdt_nm'),
            'etc_note' : base.get('etc_note'),
            'join_deny' : base.get('join_deny'),
            'join_member' : base.get('join_member'),
            'join_way' : base.get('join_way'),
            'spcl_cnd' : base.get('spcl_cnd'),
        }
        serializer = DepositProductsSerializer(data = save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
    for option in option_response:
        prdt_cd = option.get('fin_prdt_cd')
        product = DepositProducts.objects.get(fin_prdt_cd = prdt_cd)        
        save_data = {
            'fin_prdt_cd' : option.get('fin_prdt_cd'),
            'intr_rate_type_nm' : option.get('intr_rate_type_nm'),
            'intr_rate' : option.get('intr_rate'),
            'intr_rate2' : option.get('intr_rate2'),
            'save_trm' : option.get('save_trm'),
        }
        serializer = DepositOptionsSerializer(data = save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=product)
    return JsonResponse({ "message": "okay"})


# GET : 전체 정기예금 상품 목록 반환
# POST : 상품 데이터 삽입
@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({ "message": "이미 있는 데이터이거나, 데이터가 잘못 입력되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(products, many=True)
        return Response(serializer.data)


# 특정 상품의 옵션 리스트 반환
@api_view(['GET'])
def deposit_products_options(request, fin_prdt_cd):
    product = DepositProducts.objects.get(fin_prdt_cd = fin_prdt_cd)
    option = product.deposit_options.all()
    serializer = DepositOptionsSerializer(option, many = True)
    return Response(serializer.data)


# 가입 기간에 상관없이
# 금리가 가장 높은 상품과 해당 상품의 옵션 리스트 출력
@api_view(['GET'])
def top_rate(request):
    options = DepositOptions.objects.all()
    rates = []
    for option in options:
        rates.append(option.intr_rate2)
    max_rate = max(rates)

    option = DepositOptions.objects.get(intr_rate2=max_rate)
    product = DepositProducts.objects.get(fin_prdt_cd=option.fin_prdt_cd)
    data = {
        "deposit_product": DepositProductsSerializer(product).data,
        "options": DepositOptionsSerializer(option).data,
    }
    
    return Response(data)