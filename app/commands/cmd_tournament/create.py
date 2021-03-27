import random

from faker import Faker


def create(args, context):
    """Create a new Tournament."""
    tournament_view = context["tournament_view"]
    tournament_model = context["tournament_model"]

    error_view = context["error_view"]

    fields = [
        {"name": "name", "value": None, "special": None},
        {"name": "location", "value": None, "special": None},
        {"name": "date", "value": None, "special": None},
        {"name": "turns", "value": None, "special": None},
        {"name": "players", "value": None, "special": select_players},
        {"name": "time_control", "value": None, "special": None},
        {"name": "description", "value": None, "special": None},
    ]

    for f_index, field in enumerate(fields):
        tournament_view.render_questions(fields, "Creating a Tournament")

        f_name = field["name"]
        f_special = field["special"]

        if f_special:
            value = f_special(context, fields)
        else:
            value = input(f"-> {f_name}: ")

        if not value:
            err_message = f"Missing value for : {f_name}\nvalue has been randomized."
            error_view.generic_error(message=err_message)
            value = generate_fake(f_name)

        if value == "*":
            value = generate_fake(f_name)

        fields[f_index]["value"] = value

    # params = {field["name"]: field["value"] for field in fields}
    tournament_view.render_created_tournament(fields, "Created Tournament")


def select_players(context, fields):
    error_view = context["error_view"]
    player_view = context["player_view"]
    player_model = context["player_model"]
    tournament_view = context["tournament_view"]

    selected_players = []

    id_list = lambda: [p.doc_id for p in selected_players]
    players = player_model.find_many(None, None)

    tournament_view.render_player_selection(players, fields, "Available Player(s)")

    while len(selected_players) != 8:
        player_list = [p for p in players if p.doc_id not in id_list()]
        tournament_view.render_player_selection(player_list, fields, "Available Player(s)")

        print("Selected players:", [p["first_name"] for p in selected_players])

        value = input("Please select a player by its ID: ")

        if value == "*":
            value = str(random.choice([idx.doc_id for idx in player_list]))

        if not value.isdigit():
            error_view.generic_error("Only Numbers are allowed")
            continue

        player = player_model.find_one(id=int(value))

        if player.doc_id in id_list():
            error_view.generic_error("Player already added to the list")
            continue

        selected_players.append(player)

    tournament_view.render_player_selection(selected_players, fields, "Selected Players")
    input("Press enter to continue...")

    return [player.doc_id for player in selected_players]


def generate_fake(field):
    """Generate Fake data using a given type"""
    fake = Faker()

    params = {}
    random_turns = random.randint(1, 4)

    params["name"] = fake.name()
    params["players"] = [i for i in range(8)]
    params["location"] = ", ".join(fake.address().split("\n"))
    params["date"] = fake.date().replace("-", "/")
    params["turns"] = random_turns
    params["time_control"] = random.choices(["blitz", "bullet"])
    params["description"] = fake.paragraph(nb_sentences=1)

    return params[field]
