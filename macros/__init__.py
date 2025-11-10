"""Macro actions for game automation"""

from .basic_actions import tap_macro, swipe_macro, input_macro
from .game_actions import (
    close_game,
    open_game,
    launch_instance,
    clone_instance,
    close_instance,
    delete_instance,
    tap_if_regular_summon,
)

__all__ = [
    'tap_macro',
    'swipe_macro',
    'input_macro',
    'close_game',
    'open_game',
    'launch_instance',
    'clone_instance',
    'close_instance',
    'delete_instance',
    'tap_if_regular_summon',
]