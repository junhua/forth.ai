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
**GET /v1/posts?status=0&page_id=1**

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
**GET /v1/posts/1/**

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

**PUT /v1/posts/1/**

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
**DELETE /v1/posts/1/**

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
