convert = {
    'type': 'object',
    'properties': {
        'message': {
            'type': 'object',
            'properties': {
                'data': {'type': 'string'}
            },
            'required': ['data']
        },
    },
    'required': ['message']
}
