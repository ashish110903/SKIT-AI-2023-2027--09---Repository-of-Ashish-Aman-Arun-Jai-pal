def paginate_query(query, page: int = 1, page_size: int = 50):
    return query.offset((page - 1) * page_size).limit(page_size).all()
