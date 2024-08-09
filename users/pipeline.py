def get_username(strategy, details, user=None, *args, **kwargs):
    if user:
        return {"username": user.username}
    else:
        return {"username": details['username']}
