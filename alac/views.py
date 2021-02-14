from django.http import JsonResponse

def IndexHandler(request):
	domain = request.get_raw_uri().strip('/')
	directions = {
		"healthy": True,
		"movies": {
			"all movies": "{}/movie/all".format(domain),
			"quick movies": "{}/movie/all?quick=true".format(domain),
			"retrieve movie": "{}/movie/retrieve/?id=".format(domain),
			"update movie": "{}/movie/update/".format(domain)
		},
		"categories": {
			"all category": "{}/category/all/".format(domain),
			"quick category": "{}/category/all?quick=true".format(domain),
			"meta category": "{}/category/all?meta=true".format(domain),
			"retrieve category": "{}/category/retrieve?id=".format(domain)
		},
		"API documentation": "https://github.com/datmemerboi/A-Little-About-Cinema/blob/main/API%20Documentation.md"
	}
	return JsonResponse(directions)