import random

from faker import Faker


def create(args, context):
    """Create a new Player."""
    fields = [
        {"name": "first_name", "value": None, "special": None},
        {"name": "last_name", "value": None, "special": None},
        {"name": "birthday", "value": None, "special": None},
        {"name": "sexe", "value": None, "special": None},
        {"name": "rank", "value": None, "special": None},
    ]

    action = args.pop(0) if len(args) else None

    if action == "*":
        create_multiple_players(context, fields)
    else:
        create_single_player(args, context, fields)


def create_single_player(args, context, fields):
    player_model = context["player_model"]
    player_view = context["player_view"]
    error_view = context["error_view"]

    for f_index, field in enumerate(fields):
        player_view.render_questions(fields, "Creating a Player")

        f_name = field["name"]
        f_special = field["special"]

        if f_special:
            value = f_special(context, fields)
        else:
            value = input(f"-> {f_name}: ")

        if not value:
            error_view.missing_value(f_name, True)
            value = generate_fake(f_name)

        if value == "*":
            value = generate_fake(f_name)

        fields[f_index]["value"] = value

    params = {field["name"]: field["value"] for field in fields}
    new_player = player_model(**params)
    new_player = new_player.save()

    player_view.render_single_player(new_player, "Created Player")


def create_multiple_players(context, fields):
    player_list = []

    player_model = context["player_model"]
    player_view = context["player_view"]

    for i in range(8):
        params = {}

        for field in fields:
            f_name = field["name"]

            value = generate_fake(f_name)
            params[f_name] = value

        new_player = player_model(**params)
        new_player = new_player.save()

        player_list.append(new_player)

    player_view.render_multiple_players(player_list, "Registred Players")


def generate_fake(field):
    """Generate Fake data using a given type"""
    fake = Faker()

    params = {}
    random_rank = random.randint(1, 100)

    params["first_name"] = fake.first_name()
    params["last_name"] = fake.last_name()
    params["birthday"] = fake.date().replace("-", "/")
    params["sexe"] = random.choice(["Male", "Female"])
    params["rank"] = random_rank

    return params[field]
