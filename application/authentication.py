# from rest_framework.authentication import BaseAuthentication
# from rest_framework.exceptions import AuthenticationFailed
# from rest_framework_simplejwt.tokens import UntypedToken
# from rest_framework_simplejwt.exceptions import TokenError
# from rest_framework import HTTP_HEADER_ENCODING
# from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
# from rest_framework_simplejwt.authentication import JWTAuthentication

# class CustomJWTAuthentication(JWTAuthentication):
#     def authenticate(self, request):
#         header = self.get_header(request)

#         if header is None:
#             return None

#         raw_token = self.get_raw_token(header)
#         validated_token = self.get_validated_token(raw_token)
#         user = self.get_user(validated_token)

#         self.enforce_blacklist(raw_token)

#         return (user, validated_token)

#     def enforce_blacklist(self, token):
#         if isinstance(token, UntypedToken):
#             return

#         try:
#             token_str = token.decode('utf-8') 
#             if BlacklistedToken.objects.filter(token=token_str).exists():
#                 raise AuthenticationFailed('Token is blacklisted')
#         except TokenError:
#             raise AuthenticationFailed('Invalid token')