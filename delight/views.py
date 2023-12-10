# views.py
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .models import Program


def crawl_and_display(request):
    url = "https://delight.duksung.ac.kr/ko/program/all/list/all/2"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    detail_divs = soup.find_all('div', class_='detail')
    content_divs = soup.find_all('div', class_='hit')
    link_data_list = []

    ul_tag = soup.find('ul', class_='columns-4')
    li_tags = ul_tag.find_all('li') if ul_tag else []

    for li_tag in li_tags:
        a_tag = li_tag.find('a')
        if a_tag:
            link_content = a_tag.get('href')
            link_data_list.append({
                'link_content': link_content
            })

    detail_data_list = []
    content_data_list = []

    for detail_div in detail_divs:
        b_content = detail_div.find('b').text.strip() if detail_div.find('b') else None
        label_content = detail_div.find('label').text.strip() if detail_div.find('label') else None
        time_content = detail_div.find('time').text.strip() if detail_div.find('time') else None

        # 수정된 부분
        hit_span = detail_div.find('span', class_='hit')
        hit_content = int(hit_span.text.strip()[:-5]) if hit_span else None

        detail_data_list.append({
            'b_content': b_content,
            'label_content': label_content,
            'time_content': time_content,
            'hit_content': hit_content
        })

    for content_div in content_divs:
        hit_span = content_div.find('span', class_='hit')
        hit_content = int(hit_span.text.strip()[:-5]) if hit_span else None

        content_data_list.append({
            'hit_content': hit_content
        })

    min_length = min(len(detail_data_list), len(content_data_list), len(link_data_list))

    # 기존의 데이터를 모두 삭제
    Program.objects.all().delete()

    for i in range(min_length):
        detail_data = detail_data_list[i]
        content_data = content_data_list[i]
        link_data = link_data_list[i]

        # 가장 최근 데이터만 저장
        Program.objects.create(
            b_content=detail_data['b_content'],
            label_content=detail_data['label_content'],
            time_content=detail_data['time_content'],
            hit_content=content_data['hit_content'],
            link_content=link_data['link_content']
        )

    data_list = Program.objects.all()
    # QuerySet에 대한 정렬을 진행
    sorted_list = Program.objects.all().order_by('-hit_content')

    # 가장 높은 3개의 hit_content를 가진 링크를 얻어오기
    top_links1 = [item.link_content for item in sorted_list[:1]]
    top_links2 = [item.link_content for item in sorted_list[1:2]]
    top_links3 = [item.link_content for item in sorted_list[2:3]]
    print(top_links1)
    print(top_links2)
    print(top_links3)
    # 페이징
    paginate_by = 6  # 페이지당 보여질 아이템 수
    page_kwarg = "page"

    paginator = Paginator(data_list, 6)  # Set the number of items per page

    page = request.GET.get(page_kwarg, 1)  # 이 부분 추가

    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)

    return render(
        request,
        'delight/display_data.html',
        {'data_list': data_list, 'sorted_list': sorted_list, 'top_links1': top_links1, 'top_links2': top_links2,
         'top_links3': top_links3, 'page_kwarg': page_kwarg}
    )
