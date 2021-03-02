def find(context):
    """Find a Player by ID, Rank or first_name."""
    player_list = context["player_model"].find_many(None, None)
    context["player_view"].render_multiple_players(player_list=player_list, title="Registred Players")
