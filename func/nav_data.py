
def walk_dict(collect):
    if isinstance(collect,(list,tuple)):
        for item in collect:
            yield item
    else:
        yield collect
        if collect.get('children'):
            for child in collect.get('children'):
                yield child