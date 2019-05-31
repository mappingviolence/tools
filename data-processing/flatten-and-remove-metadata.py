import json, os

def lambda_try(func):
    try:
        value = func()
        return value if value is not None else "" 
    except (AttributeError, TypeError):
        return ""

def format_date(date):
    date_str = ''
    year = date.get('year')
    month = date.get('month')
    day = date.get('day')
    mod = date.get('modifier')
    if year is None:
        return None
    elif month is None and mod is None:
        return str(year)
    elif month is None and mod is not None:
        return str(mod) + ' ' + str(year)
    elif day is None and mod is None:
        return str(year) + ' ' + str(month)
    elif day is None and mod is not None:
        return str(year) + ' ' + str(mod) + ' ' + str(month)
    elif day is not None and mod is None:
        return str(year) + ' ' + str(month) + ' ' + str(day)
    elif day is not None and mod is not None:
        return str(year) + ' ' + str(month) + ' ' + str(mod) + ' ' + str(day)
    else:
        return None

field_breakdowns = [
    ('title', lambda x: lambda_try(lambda: x.get('__data').get('title').get('value'))),
    ('description', lambda x: lambda_try(lambda: x.get('__data').get('description').get('value'))),
    ('date', lambda x: lambda_try(lambda: format_date(x.get('__data').get('date').get('value')))),
    ('location', lambda x: lambda_try(lambda: x.get('__data').get('location').get('value').get('coordinates'))),
    ('locationRationale', lambda x: lambda_try(lambda: x.get('__data').get('locationRationale').get('value'))),
    ('victims', lambda x: list(map(lambda lst: '|'.join(lst), lambda_try(lambda: list(map(lambda person: list(map(lambda identity: identity.get('category') + ':' + identity.get('value'), person.get('identities'))), x.get('__data').get('victims')))) or []))),
    ('aggressors', lambda x: list(map(lambda lst: '|'.join(lst), lambda_try(lambda: list(map(lambda person: list(map(lambda identity: identity.get('category') + ':' + identity.get('value'), person.get('identities'))), x.get('__data').get('aggressors')))) or []))),
    ('tags', lambda x: lambda_try(lambda: str(list(map(lambda source: source.get('value'), x.get('__data').get('tags')))))),
    ('primarySources', lambda x: lambda_try(lambda: str(list(map(lambda source: source.get('value'), x.get('__data').get('primarySources')))))),
    ('secondarySources', lambda x: lambda_try(lambda: str(list(map(lambda source: source.get('value'), x.get('__data').get('secondarySources')))))),
    ('researchNotes', lambda x: lambda_try(lambda: x.get('__data').get('researchNotes').get('value'))),
]

with open('data.json', 'r') as file:
    data = json.load(file)

    processed_data = [{"_id": doc.get('_id')} for doc in data]

    data_data = [{"__data": doc.get('data')} for doc in data]

    for (field, field_func) in field_breakdowns:
        [processed_data[i].update({field:field_func(doc)}) for i, doc in list(enumerate(data_data))]

with open('flattened-data.json', 'w') as file:
    json.dump(processed_data, file)