ALAC API
=
Two modules in ALAC
- [Movie](#Movie)
- [Category](#Category)

### Index / Health
```GET /```

#### Response
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
</pre>
<pre>
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
### Create Movie
```POST /movie/new/```

#### Headers
<table>
  <thead>
    <tr>
      <th>Header</th>
      <th>Value</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Authorization</td>
      <td>Token</td>
      <td>the Django user OAuth token created locally</td>
    </tr>
  </tbody>
</table>

#### Request Body
Required fields: **title**, **director**, **year**, **language**
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
#### Response
**Status 201** Created

<details><summary>Sample</summary>
<pre>
curl --location --request POST 'localhost:9090/movie/new/' \
--header 'Authorization: Token <YOUR_AUTH_TOKEN>' \
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
</pre>
<pre>
201 Created
</pre>
</details>

### Create Multiple Movies
```POST /movie/new/```

#### Headers
<table>
  <thead>
    <tr>
      <th>Header</th>
      <th>Value</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Authorization</td>
      <td>Token</td>
      <td>the Django user OAuth token created locally</td>
    </tr>
  </tbody>
</table>

#### Request Body
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

#### Response
**Status 201** Created

<details><summary>Sample</summary>
<pre>
curl --location --request POST 'localhost:9090/movie/new/' \
--header 'Authorization: Token <YOUR_AUTH_TOKEN>' \
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
</pre>
<pre>
201 Created
</pre>
</details>

### List Movies
```GET /movie/all/```

#### Query Parameters
<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Data Type</th>
      <th>Description</th>
      <th>Default value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>quick</td>
      <td>Boolean</td>
      <td>Returns a concise list of objects instead of the entire movie object</td>
      <td><code>false</code></td>
    </tr>
    <tr>
      <td>limit</td>
      <td>Number</td>
      <td>To limit the number of records returned</td>
      <td><code>null</code></td>
    </tr>
  </tbody>
</table>

#### Response
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
</pre>
<pre>
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

### Retrieve Single Movie
```GET /movie/retrieve/```

#### Query Parameters
<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Data Type</th>
      <th>Description</th>
      <th>Required</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>id</td>
      <td>String</td>
      <td>ID of the movie to retrieve</td>
      <td><code>true</code></td>
    </tr>
  </tbody>
</table>

#### Response
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
</pre>
<pre>
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

### Retrieve Multiple Movies
```POST /movie/retrieve/```

#### Request Body
Required fields: **id**
```
{

	id*:			[ String ]
}
```
#### Response
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
</pre>
<pre>
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

### Update Movie
```PUT /movie/update/```

#### Headers
<table>
  <thead>
    <tr>
      <th>Header</th>
      <th>Value</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Authorization</td>
      <td>Token</td>
      <td>the Django user OAuth token created locally</td>
    </tr>
  </tbody>
</table>

#### Request Body
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
#### Response
**Status 200**

<details><summary>Sample</summary>
<pre>
curl --location --request PUT 'localhost:9090/movie/update/' \
--header 'Authorization: Token <YOUR_AUTH_TOKEN>' \
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
</pre>
<pre>
200 OK
</pre>
</details>

### Delete Movie
```DELETE /movie/delete/```
#### Headers
<table>
  <thead>
    <tr>
      <th>Header</th>
      <th>Value</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Authorization</td>
      <td>Token</td>
      <td>the Django user OAuth token created locally</td>
    </tr>
  </tbody>
</table>

#### Query Parameters
<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Data Type</th>
      <th>Description</th>
      <th>Required</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>id</td>
      <td>String</td>
      <td>ID of the movie to delete</td>
      <td><code>true</code></td>
    </tr>
  </tbody>
</table>

#### Response
**Status 200**

<details><summary>Sample</summary>
<pre>
curl --location --request DELETE 'localhost:9090/movie/delete/?id=Inglourious%20Basterds%20(2009)' \
--header 'Authorization: Token <YOUR_AUTH_TOKEN>'
</pre>
<pre>
200 OK
</pre>
</details>

### Truncate Movies
```DELETE /movie/truncate/```

#### Headers
<table>
  <thead>
    <tr>
      <th>Header</th>
      <th>Value</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Authorization</td>
      <td>Token</td>
      <td>the Django user OAuth token created locally</td>
    </tr>
  </tbody>
</table>

#### Response
**Status 200**

<details><summary>Sample</summary>
<pre>
curl --location --request DELETE 'localhost:9090/movie/truncate/' \
--header 'Authorization: Token <YOUR_AUTH_TOKEN>'
</pre>
<pre>
200 OK
</pre>
</details>

## Category
### Create Category
```POST /category/new/```

#### Headers
<table>
  <thead>
    <tr>
      <th>Header</th>
      <th>Value</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Authorization</td>
      <td>Token</td>
      <td>the Django user OAuth token created locally</td>
    </tr>
  </tbody>
</table>

#### Request Body
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
#### Response
**Status 201**

<details><summary>Sample</summary>
<pre>
curl --location --request POST 'localhost:9090/category/new/' \
--header 'Authorization: Token <YOUR_AUTH_TOKEN>' \
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
</pre>
<pre>
201 Created
</pre>
</details>

### List Categories
```GET/category/all/```

#### Query Parameters
<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Data Type</th>
      <th>Description</th>
      <th>Default value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>quick</td>
      <td>Boolean</td>
      <td>Returns a concise list of objects instead of the entire category object</td>
      <td><code>false</code></td>
    </tr>
    <tr>
      <td>limit</td>
      <td>Number</td>
      <td>To limit the number of records returned</td>
      <td><code>null</code></td>
    </tr>
  </tbody>
</table>

#### Response
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
</pre>
<pre>
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

### Retrieve Category
```GET /category/retrieve/```

#### Query Parameter
<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Data Type</th>
      <th>Description</th>
      <th>Required</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>id</td>
      <td>Number</td>
      <td>ID of the category to retrieve</td>
      <td><code>true</code></td>
    </tr>
  </tbody>
</table>

#### Response
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
</pre>
<pre>
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

### Sync Category
```PUT /cateogry/sync/```
#### Headers
<table>
  <thead>
    <tr>
      <th>Header</th>
      <th>Value</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Authorization</td>
      <td>Token</td>
      <td>the Django user OAuth token created locally</td>
    </tr>
  </tbody>
</table>

#### Query Parameters
<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Data Type</th>
      <th>Description</th>
      <th>Required</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>id</td>
      <td>Number</td>
      <td>ID of the category to sync</td>
      <td><code>true</code></td>
    </tr>
  </tbody>
</table>

#### Response
**Status 200**

<details><summary>Sample</summary>
<pre>
curl --location --request PUT 'localhost:9090/category/sync/?id=1' \
--header 'Authorization: Token <YOUR_AUTH_TOKEN>'
</pre>
<pre>
200 OK
</pre>
</details>

### Clear Category List
```PUT /category/clear/```
#### Headers
<table>
  <thead>
    <tr>
      <th>Header</th>
      <th>Value</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Authorization</td>
      <td>Token</td>
      <td>the Django user OAuth token created locally</td>
    </tr>
  </tbody>
</table>

#### Query Parameters
<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Data Type</th>
      <th>Description</th>
      <th>Required</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>id</td>
      <td>Number</td>
      <td>ID of the category to clear list</td>
      <td><code>true</code></td>
    </tr>
  </tbody>
</table>

#### Response
**Status 200**

<details><summary>Sample</summary>
<pre>
curl --location --request PUT 'localhost:9090/category/clear/?id=1' \
--header 'Authorization: Token <YOUR_AUTH_TOKEN>'
</pre>
<pre>
200 OK
</pre>
</details>

### Edit Category
```PUT /category/edit/```

#### Request Body
```
{
	id*:			Number
}
```
#### Response
**Status 200**

<details><summary>Sample</summary>
<pre>
curl --location --request POST 'localhost:9090/category/new/' \
--header 'Authorization: Token <YOUR_AUTH_TOKEN>' \
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
</pre>
<pre>
200 OK
</pre></details>
