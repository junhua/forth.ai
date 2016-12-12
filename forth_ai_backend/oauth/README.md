 status:
 0 -- PENDING
 1 -- SENT = (0, 1)
 type:
 0 -- ME
 1 -- PAGE = (0, 1)


# POST api
## Create
**POST /v1/posts/**  

Header: Authorization: jwt <token_retrieved>  

{
	"publish_date": "2017-01-12 23:13:08",
    "themes":[],
    "keywords":[],
	"content":"hello world",
    "type": 2,  (0-repost, 1 images, 2 text)
    "pages":[{"id":1},{"id":2}]
}

**Response**

Status 201 Created

{
    "post_id": "1"
}

## Retrive List
**GET /v1/posts?status=pending&page_id=1**

Header: Authorization: jwt <token_retrieved>

**Response**

Status 200 OK

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

## Retrive detail
**GET /v1/posts/1/**

Header: Authorization: jwt <token_retrieved>

**Response**

Status 200 OK

{
"id": 1,
"content": "hello world",
"date_create": "2017-01-12 23:13:08",
"date_publish":"2017-01-13 23:13:08",
"status":"pending"
}



## Update

**PUT /v1/posts/1/**

Header: Authorization: jwt <token_retrieved>

{
    "content":"Bye world",
    "publish_date":"2017-01-19 23:13:08",
    "themes": [1111,111],
    "keywords": [2222,222]
}

**Response**

Status 200 OK

{
    "post_id": "1",
    "content": "hello world",
}

## Delete
**DELETE /v1/posts/1/**

Header: Authorization: jwt <token_retrieved>

**Response**

HTTP_204_NO_CONTENT



#Page api

## Retrive pages
**GET /v1/pages/**

Header: Authorization: jwt <token_retrieved>

**Response**

Status 200 OK

[
  {
    "id": 1,
    "name": "mark0",
    "provider": "facebook",
    "avatar":"http://....",
    "extra_data":"{extra_data_in_json_format}"
  },
  {
    "id": 2,
    "name": "mark1",
    "provider": "facebook",
    "avatar":"http://....",
    "extra_data":{
    ....
    }
  }
]
