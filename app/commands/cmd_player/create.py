import random

from faker import Faker


def create(args, context):
    """Create a new Player."""
    questions = ["first_name", "last_name", "birthday", "sexe", "rank"]
    action = args.pop(0) if len(args) else None

    if action == "*":
        create_multiple_players(context, questions)
    else:
        create_single_player(args, context, questions)


def create_single_player(args, context, questions):
    params = {}

    player_model = context["player_model"]
    player_view = context["player_view"]

    for question in questions:
        value = input(f"-> {question}: ")
        value = generate_fake(question) if value == "*" else value

        params[question] = value

    new_player = player_model(**params)
    new_player = new_player.save()

    player_view.render_single_player(new_player, title="Created Player")


def create_multiple_players(context, questions):
    player_list = []

    player_model = context["player_model"]
    player_view = context["player_view"]

    for i in range(8):
        params = {}

        for question in questions:
            value = generate_fake(question)
            params[question] = value

        new_player = player_model(**params)
        new_player = new_player.save()

        player_list.append(new_player)

    player_view.render_multiple_players(player_list=player_list, title="Registred Players")


def generate_fake(field):
    """Generate Fake data using a given type"""
    fake = Faker()

    params = {}
    random_rank = random.randint(1, 100)
    random_sexe = random.randint(1, 100)

    params["first_name"] = fake.first_name()
    params["last_name"] = fake.last_name()
    params["birthday"] = fake.date().replace("-", "/")
    params["sexe"] = random.choice(["Male", "Female"])
    params["rank"] = random_rank

    return params[field]
