

def default_error_status_handler(data, error):
    if data:
        return 200
    elif not error:
        return 404
    else:
        return 400