# from corsheaders.signals import check_request_enabled
#
# from core.models import ApiKey
#
#
# def cors_allow_api_clients(sender, request, **kwargs):
#     return ApiKey.objects.filter(host=request.headers["origin"]).exists() and request.path.startswith("/api/")
#
#
# check_request_enabled.connect(cors_allow_api_clients)
