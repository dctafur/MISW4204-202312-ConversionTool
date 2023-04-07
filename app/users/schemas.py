login = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['username', 'password']
}

sign_up = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password1': {'type': 'string'},
        'password2': {'type': 'string'},
        'email': {'type': 'string'}
    },
    'required': ['username', 'password1', 'password2', 'email']
}
