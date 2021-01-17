def DirectorFilters(query, opr, val):
	if opr == "is" or opr == "equals":
		return query.filter(director = val)
	elif opr == "in" or opr == "contains":
		return query.filter(director__in = val)
	elif opr == "is not" or opr == "not equal":
		return query.filter(director__ne = val)
	elif opr == "not in" or opr == "not contain":
		return query.exclude(director__in = val)
	return query

def LanguageFilters(query, opr, val):
	if opr == "is" or opr == "equals":
		return query.filter(language = val)
	elif opr == "in" or opr == "contains":
		return query.filter(language__in = val)
	elif opr == "is not" or opr == "not equal":
		return query.filter(language__ne = val)
	elif opr == "not in" or opr == "not contain":
		return query.exclude(language__in = val)
	return query

def YearFilters(query, opr, val):
	if opr == "is" or opr == "equals":
		return query.filter(year = int(val))
	elif opr == "in" or opr == "contains":
		return query.filter(year__in = int(val))
	elif opr == "is not" or opr == "not equal":
		return query.filter(year__ne = int(val))
	elif opr == "not in" or opr == "not contain":
		return query.exclude(year__in = int(val))
	elif opr == "before":
		return query.filter(year__lt = int(val))
	elif opr == "after":
		return query.filter(year__gt = int(val))
	elif opr == "from":
		return query.filter(year__gte = int(val))
	elif opr == "to":
		return query.filter(year__lte = int(val))
	return query

def CastFilters(query, opr, val):
	if opr == "in" or opr == "contains":
		return query.filter(cast__icontains = val)
	elif opr == "not in" or opr == "not contain":
		return query.exclude(cast__icontains = val)
	return query

def KeywordFilters(query, opr, val):
	if opr == "in" or opr == "contains":
		return query.filter(keywords__icontains = val)
	elif opr == "not in" or opr == "not contain":
		return query.exclude(keywords__icontains = val)
	return query

def SingleCondition(query, key, opr, val):
	if key == "director":
		return DirectorFilters(query, opr, val)
	elif key == "language":
		return LanguageFilters(query, opr, val)
	elif key == "year":
		return YearFilters(query, opr, val)
	elif key == "cast":
		return CastFilters(query, opr, val)
	elif key == "keywords":
		return KeywordFilters(query, opr, val)

def MultiCondition(query, conditions):
	for con in conditions:
		query = SingleCondition(query, con['key'], con['operator'], con['value'])
	return query

def ApplyFiltersToQuery(query, filters):
	print(dict(filters))
	if not filters:
		return query
	for key, val in filters.items():
		if key.lower() == 'recommended' and bool(val):
			query = query.filter(status__gt = 0)
		elif key.lower() == 'watchable' and bool(val):
			query = query.filter(status__gte = 0)
		elif key.lower() == 'language':
			query = query.filter(language = val)
		elif key.lower() == 'director':
			query = query.filter(director = val)
		elif key.lower() == 'cast':
			query = query.filter(cast__icontains = val)
		elif key.lower() == 'year':
			query = query.filter(year = int(val))
		elif key.lower() == 'keywords':
			for word in val:
				query = query.filter(keywords__icontains = word)
	return query