# Deletes session variable 'last_search' when user leaves Add New page
# Was used to navigate through search results
class LastSearchCleaner:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.get_full_path().startswith('/new/') and request.session.get('last_search', None):
            del request.session['last_search']

        response = self.get_response(request)
        return response
