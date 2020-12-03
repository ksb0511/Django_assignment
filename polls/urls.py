from django.urls import path

from . import views

# 실제 장고 프로젝트를 할 경우, 여러개의 app이 있을 것임. 그럴 때를 대비해 URLconf에 이름공간을 추가함. app_name을 추가하여 애플리케이션의 이름공간을 설정
# 이렇게 설정해주고, html 파일을 이름공간으로 나눠진 상세 뷰를 가리키도록 변경해준다.
app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

# path() 호출을 추가하여 새로운 뷰들을 poll.urls 모듈로 연결
# 두번째, 세번째 패턴의 경로 문자열에서 일치하는 패턴들의 이름을 pk로 변경


