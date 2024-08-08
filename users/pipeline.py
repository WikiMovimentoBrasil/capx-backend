def get_username(details, user=None):
    if user:
        return {"username": user.username}
    else:
        return {"username": details['username']}
