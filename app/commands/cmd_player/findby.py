def findby(args, context):
    """Find a Player by ID, Rank or first_name."""

    action = args.pop(0) if len(args) else None
    data = args.pop(0) if len(args) else None

    actions = {
        "*": find_all,
        "id": findby_id,
        "name": findby_name,
        "rank": findby_rank,
    }

    if not action or action not in actions.keys():
        return context["error_view"].missing_action(actions=actions)

    execute = actions[action]
    execute(data, context)


def find_all(data, context):
    """Find all the players that has been registred"""
    player_list = context["player_model"].find_many(None, None)
    context["player_view"].render_multiple_players(player_list, "Registred Player(s)")


def findby_id(player_id, context):
    """Find one player by its Id"""
    found_player = context["player_model"].find_one(id=int(player_id))
    context["player_view"].render_single_player(found_player, "Found Player")


def findby_name(player_name, context):
    """Find many player by name (first name)"""
    found_players = context["player_model"].find_many("first_name", player_name)
    context["player_view"].render_multiple_players(found_players, "Found Player(s)")


def findby_rank(player_rank, context):
    """Find many players by rank"""
    found_players = context["player_model"].find_many("rank", player_rank)
    context["player_view"].render_multiple_players(found_players, "Found Player(s)")