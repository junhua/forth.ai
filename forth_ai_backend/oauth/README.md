# Admin can view all user profiles
rest-auth/profiles/ (GET)
Header: Authorization - jwt admin_token

# Admin can create a user profile
rest-auth/create/ (POST)
Header: Authorization - jwt admin_token
data:
{
    "username": "11",
    "email": "1@11.com",
    "password1": "123456789",
    "password2": "123456789"
}