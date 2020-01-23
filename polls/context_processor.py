def votes(request):
	if request.user.is_authenticated:
		votes = request.user.datevoted_set.order_by('-date_voted')
		if votes:
			return {'votes_list': votes}
		else:
			return {'message': 'Вы пока не проголосовали'}
	else:
		return {'message': 'Сначала войлите в аккаунт'}