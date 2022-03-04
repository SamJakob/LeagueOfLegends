import sys

import league_of_legends

if __name__ == '__main__':
    sys.stdout.write('\rWaiting for game start.  [....]')
    game, wait_time = league_of_legends.wait_for_local_game(
        on_poll=lambda poll_wait_time: sys.stdout.write(
            f'\rWaiting for game start.  [{"{:.1f}".format(poll_wait_time)}s]'
        )
    )

    print(f'\rWaiting for game start.  [DONE: ({"{:.1f}".format(wait_time)}s)]')
    print(f'\tCurrent player: {game.active_player_summoner} ({game.active_player.champion})')
    print(f'\tTeammates:')
    for ally in game.active_player_allies:
        print(f'\t\t{ally.summoner} ({ally.champion}) – {ally.level}')
    print(f'\tEnemies:')
    for enemy in game.active_player_enemies:
        print(f'\t\t{enemy.summoner} ({enemy.champion}) – {enemy.level}')
