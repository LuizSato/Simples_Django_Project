def serializer_multiples(serializer, data):
    comments_serialized = serializer(data, many=True)
    return comments_serialized.data