ALAC API
=
Two modules in ALAC
- [Movie](##Movie)
- [Category](##Category)

## Movie
**Create Movie**
```
Endpoint: /movie/new/
Method: POST
Request Body: {
	title*:			String,
	director*:		String,
	year*:			Number,
	language*:		String,
	short_title:	String,
	cast:			[String],
	poster_url:		String,
	status:			Number,
	why_watch_it:	String,
	keywords:		[String]
}
Response: Status 201
```

**Create Multiple Movies**
```
Endpoint: /movie/new/
Method: POST
Request Body: {
	records*: [{
		title*:			String,
		director*:		String,
		year*:			Number,
		language*:		String,
		short_title:	String,
		cast:			[String],
		poster_url:		String,
		status:			Number,
		why_watch_it:	String,
		keywords:		[String]
	}]
}
Response: Status 201
```

**List Movies**
```
Endpoint: /movie/all/
Method: GET
Params: quick=<Boolean>, limit=<Number>
Response: [{
	title:			String,
	director:		String,
	year:			Number,
	language:		String,
	short_title:	String,
	cast:			[String],
	poster_url:		String,
	status:			Number,
	why_watch_it:	String,
	keywords:		[String],
	created_at:		ISO timestamp
}]
```

**Retrieve Single Movie**
```
Endpoint: /movie/retrieve/
Method: GET
Param: id*=<String>
Response: {
	title:			String,
	director:		String,
	year:			Number,
	language:		String,
	short_title:	String,
	cast:			[String],
	poster_url:		String,
	status:			Number,
	why_watch_it:	String,
	keywords:		[String],
	created_at:		ISO timestamp
}
```

**Retrieve Multiple Movies**
```
Endpoint: /movie/retrieve/
Method: GET
Request Body: {
	id*:			[String]
}
Response: [{
	title:			String,
	director:		String,
	year:			Number,
	language:		String,
	short_title:	String,
	cast:			[String],
	poster_url:		String,
	status:			Number,
	why_watch_it:	String,
	keywords:		[String],
	created_at:		ISO timestamp
}]
```

**Update Movie**
```
Endpoint: /movie/update/
Method: PUT
Request Body: {
	id*:			String
	title:			String,
	director:		String,
	year:			Number,
	language:		String,
	short_title:	String,
	cast:			[String],
	poster_url:		String,
	status:			Number,
	why_watch_it:	String,
	keywords:		[String]
}
Response: Status 200
```

**Delete Movie**
```
Endpoint: /movie/delete/
Method: DELETE
Params: id*=<String>
Response: Status 200
```
**Truncate Movies**
```
Endpoint: /movie/truncate/
Method: DELETE
Response: Status 200
```

## Category
**Create Category**
```
Endpoint: /category/new/
Method: POST
Request Body: {
	name*:			String,
	description:	String,
	condition*: {
		key*:		String,
		value*:		String
	},
	movie_list:		[String]
}
Response: Status 201
```

**List Categories**
```
Endpoint: /category/all/
Method: GET
Params: quick=<Boolean>, meta=<Boolean>, limit=<Number>
Response:[{
	id:				Number
	name:			String,
	description:	String,
	condition: {
		key:		String,
		value:		String
	},
	movie_list:		[String],
	meta:			{JSON},
	created_at:		ISO timestamp
}]
```

**Retrieve Category**
```
Endpoint: /category/retrieve/
Method: GET
Params: id*=<Number>
Response:{
	id:				Number
	name:			String,
	description:	String,
	condition: {
		key:		String,
		value:		String
	},
	movie_list:		[String],
	meta:			{JSON},
	created_at:		ISO timestamp
}
```

**Sync Category**
```
Endpoint: /cateogry/sync/
Method: PUT
Params: id*=<Number>
Response: Status 200
```

**Clear Category List**
```
Endpoint: /category/clear/
Method: PUT
Params: id*=<Number>
Response: Status 200
```