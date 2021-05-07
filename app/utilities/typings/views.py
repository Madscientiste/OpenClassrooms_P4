from typing import TypedDict

from app.views import main, error, player, tournament


class Views(TypedDict):
    main: main.View
    error: error.View
    player: player.View
    tournament: tournament.View
