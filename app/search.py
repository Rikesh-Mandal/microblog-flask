from flask import current_app
from elasticsearch.exceptions import ConnectionError

def add_to_index(index,model):
    if not current_app.elasticsearch:
        return
    payload={}
    for field in model.__searchable__:
        payload[field]=getattr(model, field)
    try:
        current_app.elasticsearch.index(index=index, id=model.id, document=payload)
    except ConnectionError:
        current_app.logger.warning(
            'Elasticsearch is unavailable. '
            'Skipping indexing for %s id=%s',
            index,
            model.id
        )



def remove_from_index(index,model):
    if not current_app.elasticsearch:
        return
    try:
        current_app.elasticsearch.delete(index=index, id=model.id)
    except ConnectionError:
        current_app.logger.warning(
            'Elasticsearch is unavailable. '
            'Skipping indexing for %s id=%s',
            index,
            model.id
        )



def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    try:
        search = current_app.elasticsearch.search(
            index=index,
            query={'multi_match': {'query': query, 'fields': ['*']}},
            from_=(page - 1) * per_page,
            size=per_page
        )
    except ConnectionError:
        current_app.logger.warning(
            'Elasticsearch is unavailable. '
            'Search request could not be completed.'
        )
        return [], 0
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
    
