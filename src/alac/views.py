from django.http import JsonResponse

def IndexHandler(request):
	domain = request.get_host()
	directions = {
		"status": "Server Healthy!",
		"movies": {
			"all movies": "http://{}/movie/all".format(domain),
			"quick movies": "http://{}/movie/quick/".format(domain),
			"retrieve movie": "http://{}/movie/retrieve/".format(domain),
			"update movie": "http://{}/movie/update/".format(domain)
		},
		"categories": {
			"all category": "http://{}/category/all/".format(domain),
			"quick category": "http://{}/category/quick/".format(domain)
		}
	}
	return JsonResponse(directions)