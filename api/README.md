# POST API

**Status:**

0 -- PENDING  
1 -- SENT

**Type:**

0 -- REPOST  
1 -- IMAGES  
2 -- TEXT  

## Create
**POST /v1/posts/**  

Headers  
Authorization: "jwt token_retrieved"

Body
```json
{
	"publish_date": "2017-01-12T23:13:08Z",
    "publish_now":false,
    "themes": [],
    "keywords": [],
	"content": "hello world",
    "type": 2,
    "pages":[
        {"id": 1},
        {"id": 2}
    ]
}
```


**Response**

Status 201 Created

Body
```json
{
    "posts": [
        {
            "id": 49,
            "publish_date": "2017-01-12T23:13:08Z",
            "status": 0,
            "type": 2,
            "themes": [],
            "keywords": [],
            "content": "hello world",
            "page": 1
        }
    ]
}
```


## Publish an existing post
**POST /v1/posts/{id}/existed_post**  

Headers  
Authorization: "jwt token_retrieved"

Body
```json
{
    "publish_now": true,
    "pages":[
        {"id": 1}
    ]
}
```


**Response**

Status 201 Created

Body
```json
{
    "id": 49,
    "publish_date": "2017-01-12T23:13:08Z",
    "status": 0,
    "type": 2,
    "themes": [],
    "keywords": [],
    "content": "hello world"
}
```


## Retrive List
**GET /v1/posts?status=0&page=1**

Headers  
Authorization: "jwt token_retrieved"

**Response**

Status 200 OK

Body
```json
[
    {
        "id": 25,
        "publish_date": "2016-12-11T04:29:00Z",
        "status": 0,
        "type": 2,
        "themes": [],
        "keywords": [],
        "content": "hello world"
    },
    {
        "id": 26,
        "publish_date": "2016-12-11T05:00:42Z",
        "status": 0,
        "type": 2,
        "themes": [],
        "keywords": [],
        "content": "hello world"
    }
]
```


## Retrive detail
**GET /v1/posts/{id}/**

Headers  
Authorization: "jwt token_retrieved"

**Response**

Status 200 OK

Body
```json
{
    "id": 1,
    "content": "hello world",
    "date_created": "2017-01-12T23:13:08Z",
    "publish_date": "2017-01-13T23:13:08Z",
    "status": 0,
    "pages": [
        {"id": 1},
        {"id": 2}
    ]
}
```


## Update

**PUT /v1/posts/{id}/**

Headers  
Authorization: "jwt token_retrieved"

Body
```json
{
    "content": "Bye world",
    "publish_date": "2017-01-19T23:13:08Z"
}
```
**Response**

Status 200 OK

Body
```json
{
    "id": 1,
    "content": "hello world",
    "date_created": "2017-01-12T23:13:08Z",
    "publish_date": "2017-01-19T23:13:08Z",
    "status": 0,
    "pages": [
        {"id": 1},
        {"id": 2}
    ]
}
```


## Delete
**DELETE /v1/posts/{id}/**

Headers  
Authorization: "jwt token_retrieved"

**Response**

Status 204 NO CONTENT



#Page API

**Type:**

0 -- ACCOUNT  
1 -- PAGE 

## Retrive pages
**GET /v1/pages/**

Headers  
Authorization: "jwt token_retrieved"

**Response**

Status 200 OK

Body
```json
[
  {
    "id": 1,
    "name": "mark0",
    "provider": "facebook",
    "avatar": "http://....",
    "type": 0,
    "extra_data": "{extra_data_in_json_format}"
  },
  {
    "id": 2,
    "name": "mark1",
    "provider": "facebook",
    "type": 1
    "avatar": "http://....",
    "extra_data": "{extra_data_in_json_format}"
  }
]
```


## Retrive 
**POST /v1/link/**  

Body
```json
{
    "url": "http://haipo1023.baijia.baidu.com/article/730304"
}
```


**Response**

Status 200 OK

Body
```json
{
    "images": [
        {
            "url": "http://h.hiphotos.baidu.com/news/crop%3D0%2C136%2C1280%2C768%3Bw%3D638/sign=8d441e4fd0f9d72a032b4a5de91a0405/ac4bd11373f08202cda7eb4f42fbfbedab641b8c.jpg",
            "width": 638,
            "height": 383
        }
    ],
    "origin_url": "http://lihao.baijia.baidu.com/article/730325",
    "description": "按citibike的数据，用户平均骑行时间为16.13分钟，换成中国用户这个数据只多不少，原因很简单，在火爆房地产的支撑下，中国城市的市域面积一直在高速扩张中，以马上要修出七环路的北京为例，市域面积1.64万平方公里，上海6340平方公里，都比纽约的798平方公里大出N倍，城市大意味着用户的生活圈也更加宽泛。",
    "title": "滴滴未来的商业闭环：力保短途需求，对抗共享单车？--百度百家"
}  "title": "互联网发展到今天，知识无法直接变现是最大的耻辱--百度百家"
}
```