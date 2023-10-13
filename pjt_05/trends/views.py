from django.shortcuts import render


# 키워드 저장 및 keyword.html 렌더링
def keyword(request):
    return render(request, 'trends/keyword.html')

# 키워드 삭제 및 keyword.html로 리다이렉션
def keyword_detail():
    pass

# 크롤링 수행 및 결과 개수 출력
def crawling():
    pass

# 크롤링 수행 및 결과 개수 막대 그래프로 출력
def crawling_histogram():
    pass

# 지난 1년을 기준으로
# 크롤링 수행 및 결과 개수 막대 그래프 출력
def crawling_advanced():
    pass