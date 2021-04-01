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

    show_actions = lambda: context["main_view"].display_actions(actions=actions)

    if not action or action not in actions.keys():
        return show_actions()

    execute = actions[action]
    state = execute(data, context, actions)

    if state == 0:
        return show_actions()


def find_all(data, context, actions):
    """Find all the players that has been registred"""
    player_list = context["player_model"].find_many(None, None)
    context["player_view"].render_multiple_players(player_list, "Registred Player(s)")


def findby_id(player_id, context, actions):
    """Find one player by its Id"""

    if not player_id or not player_id.isdigit():
        context["error_view"].generic_error(message="id must be a number")
        return 0

    found_player = context["player_model"].find_one(id=int(player_id))

    if not found_player:
        context["error_view"].generic_error(message=f"player id [{player_id}] not found")
        return 0

    context["player_view"].render_single_player(found_player, "Found Player")


def findby_name(player_name, context, actions):
    """Find many player by name (last name)"""
    found_players = context["player_model"].find_many("last_name", player_name)

    if not found_players:
        context["error_view"].generic_error(message=f"No players with name of [{player_name}] has been found")
        return 0

    context["player_view"].render_multiple_players(found_players, "Found Player(s)")


def findby_rank(player_rank, context, actions):
    """Find many players by rank"""

    if not player_rank or not player_rank.isdigit():
        context["error_view"].generic_error(message="rank must be a number")
        return 0

    found_players = context["player_model"].find_many("rank", player_rank)

    if not found_players:
        context["error_view"].generic_error(message=f"player with [{player_rank}] rank not found")
        return 0

    context["player_view"].render_multiple_players(found_players, "Found Player(s)")