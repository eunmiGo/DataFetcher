# datafetcher
Project Code : **Open Social Crawler**


## Instruction
데이터 포털/마켓, 블로그, 뉴스 등 웹 페이지의 내용 데이터를 끌어올 수 있는 모듈
블로그 크롤링의 경우 페이지 내용의 키워드를 뽑아 함께 저장함
A module that can bring up content data on web pages such as data portals/markets, blogs, and news.


## Contribution Guide

Airflow 실행 - webserver/scheduler 실행
```
airflow webserver &
airflow scheduler &
```


## Clone Guide
```
git clone https://github.com/ThirdActiveDataExTech/DataFetcher.git
```



## Developer Setting
```
서버
- airflow 서버
- crawling file 저장 DB(minio)
- file metadata 저장 DB(postgresql)
- config_template.py setting
```