def ratings_for(obj):
    ratings = {}

    if hasattr(obj, 'username'):
        # If we're getting the ratings for a user, we're looking at all the
        # different quotes they rated.
        def key(quote_obj):
            return quote_obj.quote.pk

    else:
        # If we're getting ratings fora quote, we're looking at all the
        # different users that rated it.
        def key(quote_obj):
            return quote_obj.user.pk

    for vq in obj.viewedquote_set.all():
        ratings[key(vq)] = 1
    for fq in obj.favoritequote_set.all():
        ratings[key(fq)] = 5
    return ratings
