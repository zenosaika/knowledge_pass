from django.shortcuts import render
import requests
import json

def homepage(req):
    context = {}
    return render(req, 'PathFinder/homepage.html', context)

def search_results(request):
    query = request.GET.get('q')  # Get the query from the URL parameter
    if query:
        api_url = f"http://127.0.0.1:8081/search?q={query}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            results = response.json()

            html = results['html']
            sankey_data = results['sankey_data']

        except requests.exceptions.RequestException as e:
            error_message = f"Error contacting job search API: {e}"
            results = {"error": error_message}  # Return the error message to the template

    else:
        results = None # no query

    context = {
        'query': query,
        'results': html,
        'sankey_data': json.dumps({'data':sankey_data}),
    }

    return render(request, 'PathFinder/search_results.html', context)