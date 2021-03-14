import random

from faker import Faker


def create(args, context):
    tournament_view = context["tournament_view"]
    tournament_model = context["tournament_model"]

    error_view = context["error_view"]

    params = {}
    fields = [
        {"name": "name", "value": None, "special": None},
        {"name": "location", "value": None, "special": None},
        {"name": "date", "value": None, "special": None},
        {"name": "turns", "value": None, "special": None},
        {"name": "players", "value": None, "special": select_players},
        {"name": "time_control", "value": None, "special": None},
        {"name": "description", "value": None, "special": None},
    ]

    for field in fields:
        tournament_view.render_questions(fields, title="Creating Tournament")

        f_name = field["name"]
        f_special = field["special"]

        if f_special:
            value = f_special()
        else:
            value = input(f"-> {field}: ")

        if not value:
            error_view.generic_error(message=f"Missing value for : {field}")
            continue

        if value == "*":
            value = generate_fake(field)

        params[f_name] = value

    tournament_view.render_questions(params, title="Creating Tournament")


def select_players(context):
    player_view = context["player_view"]
    player_model = context["player_model"]
    tournament_view = context["tournament_view"]

    selected_players = []

    id_list = lambda: [p.doc_id for p in selected_players]
    players = player_model.find_many(None, None)

    tournament_view.render_player_selection(players, "Registred Player(s)")


    # tournament = tournament_model(**params)
    # saved_tournament = tournament.save()

    # tournament_view.render_created_tournament(saved_tournament, title="Created Tournament")

    # def apply_players(value=8):
    #     while len(selected_players) != int(value):
    #         player_list = [p for p in players if p.doc_id not in id_list()]
    #         player_view.render_multiple_players(player_list, title="Available Players")
    #         print("Selected players:", [p["first_name"] for p in selected_players])
    #         selected = input("Please select a player by its ID: ")
    #         if not selected.isdigit():
    #             error_view.generic_error("Only Numbers are allowed")
    #             continue
    #         player = player_model.find_one(id=int(selected))
    #         if player.doc_id in id_list():
    #             error_view.generic_error("Player already added to the list")
    #             continue
    #         selected_players.append(player)
    #         player_list = [p for p in players if p.doc_id not in id_list()]
    #         player_view.render_multiple_players(player_list, title="Available Players")
    #     player_view.render_multiple_players(selected_players, title="Selected Players")

    # for question in params.keys():
    #     apply_question = params[question]
    #     value = input(f"-> {question}: ")
    #     value = generate_fake(question) if value == "*" else apply_question(value)
    #     params[question] = value
    # print(params)


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
