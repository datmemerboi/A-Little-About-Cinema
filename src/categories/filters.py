def DirectorFilters(query, opr, val):
	if opr == "is" or opr == "equals":
		query = query.filter(director = val)
	elif opr == "in" or opr == "contains":
		query = query.filter(director__icontains = val)
	elif opr == "is not" or opr == "not equal":
		query = query.filter(director__ne = val)
	elif opr == "not in" or opr == "not contain":
		query = query.exclude(director__icontains = val)
	return query

def LanguageFilters(query, opr, val):
	if opr == "is" or opr == "equals":
		query = query.filter(language = val)
	elif opr == "in" or opr == "contains":
		query = query.filter(language__icontains = val)
	elif opr == "is not" or opr == "not equal":
		query = query.filter(language__ne = val)
	elif opr == "not in" or opr == "not contain":
		query = query.exclude(language__icontains = val)
	return query

def YearFilters(query, opr, val):
	if opr == "is" or opr == "equals":
		query = query.filter(year = val)
	elif opr == "in" or opr == "contains":
		query = query.filter(year__icontains = val)
	elif opr == "is not" or opr == "not equal":
		query = query.filter(year__ne = val)
	elif opr == "not in" or opr == "not contain":
		query = query.exclude(year__icontains = val)
	elif opr == "before":
		query = query.filter(year__lt = val)
	elif opr == "after":
		query = query.filter(year__gt = val)
	elif opr == "from":
		query = query.filter(year__gte = val)
	elif opr == "to":
		query = query.filter(year__lte = val)
	return query

def CastFilters(query, opr, val):
	if opr == "in" or opr == "contains":
		query = query.filter(cast__icontains = val)
	elif opr == "not in" or opr == "not contain":
		query = query.exclude(cast__icontains = val)
	return query

def KeywordFilters(query, opr, val):
	if opr == "in" or opr == "contains":
		query = query.filter(keywords__icontains = val)
	elif opr == "not in" or opr == "not contain":
		query = query.exclude(keywords__icontains = val)
	return query

def SingleConditionFilter(query, key, opr, val):
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

def MultiConditionFilter(query, conditions):
	for con in conditions:
		query = SingleConditionFilter(query, con['key'], con['operator'], con['value'])
	return query