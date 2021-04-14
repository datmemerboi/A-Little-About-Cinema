ALAC API
=
Two modules in ALAC
- [Movie](#Movie)
- [Category](#Category)

#### Index / Health
Endpoint: `/`

Method: GET

Response:
```
{
	healthy:		Boolean,
	movies:			{ JSON },
	categories:		{ JSON }
}
```

<details><summary>Sample</summary>
<pre>
curl --location --request GET 'localhost:9090'

{
	"healthy": true,
	"movies": {
		"all movies": "http://localhost:9090/movie/all",
		"quick movies": "http://localhost:9090/movie/all?quick=true",
		"retrieve movie": "http://localhost:9090/movie/retrieve/?id=id",
		"update movie": "http://localhost:9090/movie/update/"
	},
	"categories": {
		"all category": "http://localhost:9090/category/all/",
		"quick category": "http://localhost:9090/category/all?quick=true",
		"meta category": "http://localhost:9090/category/all?meta=true",
		"retrieve category": "http://localhost:9090/category/retrieve?id=1"
	},
	"API documentation": "https://github.com/datmemerboi/A-Little-About-Cinema/blob/main/API%20Documentation.md"
}
</pre>
</details>

## Movie
#### Create Movie

Endpoint: `/movie/new/`

Method: POST

Headers:
- Authorization: Token
  - Django user OAuth token

Request Body:
```
{
	title*:			String,
	director*:		[ String ],
	year*:			Number,
	language*:		String,
	short_title:	String,
	cast:			[ String ],
	poster_url:		String,
	status:			Number,
	why_watch_it:	String,
	keywords:		[ String ]
}
```
Response: Status 201

<details><summary>Sample</summary>
<pre>
curl --location --request POST 'localhost:9090/movie/new/' \
--header 'Authorization: Token YOUR_AUTH_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Inglourious Basterds",
    "director": "Quentin Tarantino",
    "year": 2009,
    "status": 2,
    "cast": [
        "Brad Pitt",
        "Christoph Waltz",
        "Melanie Laurent"
    ],
    "language": "English",
    "why_watch_it": "- Possibly the best WW2 movie - Christoph Waltz won an Oscar for Best Supporting Actor",
    "keywords": [
        "war",
        "action",
        "funny",
        "violent"
    ]
}'


201 Created
</pre>
</details>

#### Create Multiple Movies

Endpoint: `/movie/new/`

Method: POST

Headers:
- Authorization: Token
  - Django user OAuth token

Request Body:
```
{
	records*: [{
		title*:			String,
		director*:		[ String ],
		year*:			Number,
		language*:		String,
		short_title:	String,
		cast:			[ String ],
		poster_url:		String,
		status:			Number,
		why_watch_it:	String,
		keywords:		[ String ]
	}]
}
```
Response: Status 201

<details><summary>Sample</summary>
<pre>
curl --location --request POST 'localhost:9090/movie/new/' \
--header 'Authorization: Token YOUR_AUTH_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
	records: [
		{
			"title": "Inglourious Basterds",
		    "director": "Quentin Tarantino",
		    "year": 2009,
		    "status": 2,
		    "cast": [
		        "Brad Pitt",
		        "Christoph Waltz",
		        "Melanie Laurent"
		    ],
		    "language": "English",
		    "why_watch_it": "- Possibly the best WW2 movie - Christoph Waltz won an Oscar for Best Supporting Actor",
		    "keywords": [
		        "war",
		        "action",
		        "funny",
		        "violent"
		    ]
		}
	]
}'

201 Created
</pre>
</details>

#### List Movies
Endpoint: `/movie/all/`

Method: GET

Parameters:
- quick
  - datatype: Boolean
  - Returns a concise list of objects instead of the entire movie object
- limit
  - datatype: Number
  - To limit the number of records returned

Response:
```
[{
	title:			String,
	director:		[ String ],
	year:			Number,
	language:		String,
	short_title:	String,
	cast:			[ String ],
	poster_url:		String,
	status:			Number,
	why_watch_it:	String,
	keywords:		[ String ],
	created_at:		ISO timestamp
}]
```
<details><summary>Sample</summary>
<pre>
curl --location --request GET 'localhost:9090/movie/all/'

[
	{
        "id": "Inglourious Basterds (2009)",
        "title": "Inglourious Basterds",
        "director": [
            "Quentin Tarantino"
        ],
        "year": 2009,
        "language": "English",
        "short_title": null,
        "cast": [
            "Brad Pitt",
            "Christoph Waltz",
            "Melanie Laurent"
        ],
        "poster_url": null,
        "status": 2,
        "why_watch_it": "- Possibly the best WW2 movie - Christoph Waltz won an Oscar for Best Supporting Actor",
        "keywords": [
            "war",
            "action",
            "funny",
            "violent"
        ],
        "created_at": "2021-04-13T15:54:14.657173Z"
    }
]
</pre>
</details>

#### Retrieve Single Movie
Endpoint: `/movie/retrieve/`

Method: GET

Parameters:
- **id**
  - datatype: String
  - required parameter
  - ID of the movie to retrieve

Response:
```
{
	title:			String,
	director:		[ String ],
	year:			Number,
	language:		String,
	short_title:	String,
	cast:			[ String ],
	poster_url:		String,
	status:			Number,
	why_watch_it:	String,
	keywords:		[ String ],
	created_at:		ISO timestamp
}
```

<details><summary>Sample</summary>
<pre>
curl --location --request GET 'localhost:9090/movie/retrieve/?id=Inglourious%20Basterds%20(2009)'

{
    "id": "Inglourious Basterds (2009)",
    "title": "Inglourious Basterds",
    "director": [
        "Quentin Tarantino"
    ],
    "year": 2009,
    "language": "English",
    "short_title": null,
    "cast": [
        "Brad Pitt",
        "Christoph Waltz",
        "Melanie Laurent"
    ],
    "poster_url": null,
    "status": 2,
    "why_watch_it": "- Possibly the best WW2 movie - Christoph Waltz won an Oscar for Best Supporting Actor",
    "keywords": [
        "war",
        "action",
        "funny",
        "violent"
    ],
    "created_at": "2021-04-13T15:54:14.657173Z"
}
</pre>
</details>

#### Retrieve Multiple Movies
Endpoint: `/movie/retrieve/`

Method: POST

Request Body:
```
{

	id*:			[ String ]
}
```
Response:
```
[{
	title:			String,
	director:		[ String ],
	year:			Number,
	language:		String,
	short_title:	String,
	cast:			[ String],
	poster_url:		String,
	status:			Number,
	why_watch_it:	String,
	keywords:		[ String ],
	created_at:		ISO timestamp
}]
```

<details><summary>Sample</summary>
<pre>
curl --location --request POST 'localhost:9090/movie/retrieve/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": [
        "Inglourious Basterds (2009)"
    ]
}'

[
    {
        "id": "Inglourious Basterds (2009)",
        "title": "Inglourious Basterds",
        "director": [
            "Quentin Tarantino"
        ],
        "year": 2009,
        "language": "English",
        "short_title": null,
        "cast": [
            "Brad Pitt",
            "Christoph Waltz",
            "Melanie Laurent"
        ],
        "poster_url": null,
        "status": 2,
        "why_watch_it": "- Possibly the best WW2 movie - Christoph Waltz won an Oscar for Best Supporting Actor",
        "keywords": [
            "war",
            "action",
            "funny",
            "violent"
        ],
        "created_at": "2021-04-13T15:54:14.657173Z"
    }
]
</pre>
</details>

#### Update Movie
Endpoint: `/movie/update/`

Method: PUT

Headers:
- Authorization: Token
  - Django user OAuth token

Request Body:
```
{
	id*:			String
	title:			String,
	director:		[ String ],
	year:			Number,
	language:		String,
	short_title:	String,
	cast:			[ String ],
	poster_url:		String,
	status:			Number,
	why_watch_it:	String,
	keywords:		[ String ]
}
```
Response: Status 200

<details><summary>Sample</summary>
<pre>
curl --location --request PUT 'localhost:9090/movie/update/' \
--header 'Authorization: Token YOUR_AUTH_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "Inglourious Basterds (2009)",
    "title": "Inglourious Basterds",
    "director": "Quentin Tarantino",
    "year": 2009,
    "status": 2,
    "cast": [
        "Brad Pitt",
        "Christoph Waltz",
        "Melanie Laurent",
        "Diane Kruger"
    ],
    "language": "English",
    "why_watch_it": "- Possibly the best WW2 movie - Christoph Waltz won an Oscar for Best Supporting Actor",
    "keywords": [
        "war",
        "action",
        "funny",
        "violent"
    ]
}'

200 OK
</pre>
</details>

#### Delete Movie
Endpoint: `/movie/delete/`

Method: DELETE

Headers:
- Authorization: Token
  - Django user OAuth token

Parameters:
- **id**
  - datatype: String
  - required parameter
  - ID of movie record to delete

Response: Status 200

<details><summary>Sample</summary>
<pre>
curl --location --request DELETE 'localhost:9090/movie/delete/?id=Inglourious%20Basterds%20(2009)' \
--header 'Authorization: Token YOUR_AUTH_TOKEN'
</pre>
</details>

#### Truncate Movies
Endpoint: `/movie/truncate/`

Method: DELETE

Headers:
- Authorization: Token
  - Django user OAuth token

Response: Status 200

<details><summary>Sample</summary>
<pre>
curl --location --request DELETE 'localhost:9090/movie/truncate/' \
--header 'Authorization: Token YOUR_AUTH_TOKEN'

200 OK
</pre>
</details>

## Category
#### Create Category
Endpoint: `/category/new/`

Method: POST

Headers:
- Authorization: Token
  - Django user OAuth token

Request Body:
```
{
	name:			String,
	description:	String,
	condition*: {
		key*:		String,
		operator*:	String,
		value*:		String
	},
	movie_list:		[ String ]
}
```
Response: Status 201

<details><summary>Sample</summary>
<pre>
curl --location --request POST 'localhost:9090/category/new/' \
--header 'Authorization: Token YOUR_AUTH_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "English Movies",
    "conditions": [
        {
            "key": "language",
            "operator": "is",
            "value": "English"
        }
    ]
}'

201 Created
</pre>
</details>

#### List Categories
Endpoint: `/category/all/`

Method: GET

Parameters:
- quick
  - datatype: Boolean
  - Returns a concise list of objects instead of the entire category object
- meta
  - datatype: Boolean
  - Returns the meta data of the category object
- limit
  - datatype: Number
  - To limit the number of records returned

Response:
```
[{
	id:				Number
	name:			String,
	description:	String,
	condition: {
		key:		String,
		operator:	String,
		value:		String
	},
	movie_list:		[ String ],
	meta:			{ JSON },
	created_at:		ISO timestamp
}]
```

<details><summary>Sample</summary>
<pre>
curl --location --request GET 'localhost:9090/category/all/'

[
    {
        "id": 1,
        "name": "English Movies",
        "description": null,
        "conditions": [
            {
                "key": "language",
                "value": "English",
                "operator": "is"
            }
        ],
        "movie_list": [],
        "meta": null,
        "created_at": "2021-04-14T15:19:07.953570Z"
    }
]
</pre>
</details>

#### Retrieve Category
Endpoint: `/category/retrieve/`

Method: GET

Parameters:
- **id**
  - datatype: Number
  - required parameter
  - ID of the category to retrieve

Response:
```
{
	id:				Number
	name:			String,
	description:	String,
	condition: {
		key:		String,
		value:		String
	},
	movie_list:		[ String ],
	meta:			{JSON},
	created_at:		ISO timestamp
}
```
<details><summary>Sample</summary>
<pre>
curl --location --request GET 'localhost:9090/category/retrieve/?id=1'

{
    "id": 1,
    "name": "English Movies",
    "description": null,
    "conditions": [
        {
            "key": "language",
            "value": "English",
            "operator": "is"
        }
    ],
    "movie_list": [],
    "meta": null,
    "created_at": "2021-04-14T15:19:07.953570Z"
}
</pre>
</details>

#### Sync Category
Endpoint: `/cateogry/sync/`

Method: PUT

Headers:
- Authorization: Token
  - Django user OAuth token

Parameters:
- **id**
  - datatype: Number
  - required parameter
  - ID of the category to sync

Response: Status 200

<details><summary>Sample</summary>
<pre>
curl --location --request PUT 'localhost:9090/category/sync/?id=1' \
--header 'Authorization: Token YOUR_AUTH_TOKEN'

200 OK
</pre>
</details>

#### Clear Category List
Endpoint: `/category/clear/`

Method: PUT

Headers:
- Authorization: Token
  - Django user OAuth token

Parameters:
- **id**
  - datatype: Number
  - required parameter
  - ID of the category to clear list

Response: Status 200

<details><summary>Sample</summary>
<pre>
curl --location --request PUT 'localhost:9090/category/clear/?id=1' \
--header 'Authorization: Token YOUR_AUTH_TOKEN'

200 OK
</pre>
</details>

#### Edit Category
Endpoint: `/category/edit/`

Method: PUT

Request Body:
```
{
	id*:			Number
}
```
Response: Status 200

<details><summary>Sample</summary>
<pre>
curl --location --request POST 'localhost:9090/category/new/' \
--header 'Authorization: Token YOUR_AUTH_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
	"id": "1"
    "name": "English Movies",
    "description": "A list of all english movies",
    "conditions": [
        {
            "key": "language",
            "operator": "is",
            "value": "English"
        }
    ]
}'

200 OK
</pre></details>