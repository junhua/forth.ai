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
	"publish_date": "2017-01-12 23:13:08",
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

Status  
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
**GET /v1/posts?status=pending&page_id=1**

Headers  
Authorization: "jwt token_retrieved"

**Response**

Status  
Status 200 OK

Body
```json
[
    {
        "id": 25,
        "publish_date": "2016-12-11T04:29:00.486919Z",
        "status": 0,
        "type": 2,
        "themes": [],
        "keywords": [],
        "content": "hello world"
    },
    {
        "id": 26,
        "date_publish": "2016-12-11T05:00:42.646724Z",
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

Status  
Status 200 OK

Body
```json
{
    "id": 1,
    "content": "hello world",
    "date_create": "2017-01-12 23:13:08",
    "date_publish": "2017-01-13 23:13:08",
    "status": "pending"
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
    "publish_date": "2017-01-19 23:13:08",
    "themes": [1111,111],
    "keywords": [2222,222]
}
```
**Response**

Status  
Status 200 OK

Body
```json
{
    "id": 40,
    "publish_date": "2017-01-19T23:13:08Z",
    "themes": [
        "1111",
        "111"
    ],
    "keywords": [
        "2222",
        "222"
    ],
    "content": "Bye world"
}
```
## Delete
**DELETE /v1/posts/1/**

Headers  
Authorization: "jwt token_retrieved"

**Response**

Status  
HTTP_204_NO_CONTENT



#Page API

## Retrive pages
**GET /v1/pages/**

Headers  
Authorization: "jwt token_retrieved"

**Response**

Status  
Status 200 OK

Body
```json
[
  {
    "id": 1,
    "name": "mark0",
    "provider": "facebook",
    "avatar": "http://....",
    "extra_data": "{extra_data_in_json_format}"
  },
  {
    "id": 2,
    "name": "mark1",
    "provider": "facebook",
    "avatar": "http://....",
    "extra_data": "{extra_data_in_json_format}"
  }
]
```
