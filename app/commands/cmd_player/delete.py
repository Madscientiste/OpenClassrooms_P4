def delete(args, context):
    """Delete a Player by ID."""
    player_model = context["player_model"]
    player_view = context["player_view"]
    error_view = context["error_view"]
    sub_commands = context["sub_commands"]

    player_id = args.pop(0) if len(args) else None

    if not player_id or not player_id.isdigit():
        error_view.generic_error(message="id must be a number")
        context["main_view"].display_actions(actions=sub_commands)
        return

    deleted_player = player_model.delete_one(id=int(player_id))

    if not deleted_player:
        error_view.generic_error(message=f"player id [{player_id}] not found")
        context["main_view"].display_actions(actions=sub_commands)
        return


    player_view.render_single_player(deleted_player, "Deleted Player")
