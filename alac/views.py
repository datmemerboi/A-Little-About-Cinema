from django.http import JsonResponse

def IndexHandler(request):
	domain = request.get_host()
	directions = {
		"healthy": True,
		"movies": {
			"all movies": "http://{}/movie/all".format(domain),
			"quick movies": "http://{}/movie/all?quick=true".format(domain),
			"retrieve movie": "http://{}/movie/retrieve/?id=".format(domain),
			"update movie": "http://{}/movie/update/".format(domain)
		},
		"categories": {
			"all category": "http://{}/category/all/".format(domain),
			"quick category": "{}/category/all?quick=true".format(domain),
			"meta category": "http://{}/category/all?meta=true".format(domain),
			"retrieve category": "http://{}/category/retrieve?id=".format(domain)
		},
		"API documentation": "https://github.com/datmemerboi/A-Little-About-Cinema/API%20Documentation.md"
	}
	return JsonResponse(directions)