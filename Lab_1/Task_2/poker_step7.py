"""
Task 2 - Step 7: Comparison of all agents (table of all matchups)

"""
import statistics

from poker_step1 import RandomAgent
from poker_step2 import FixedAgent
from poker_step3 import play_game
from poker_step5 import ReflexAgent
from poker_step6 import MemoryAgent

AGENTS = {
    "Random": RandomAgent,
    "Fixed": FixedAgent,
    "Reflex": ReflexAgent,
    "Memory": MemoryAgent,
}


def matchup(cls1, cls2, n_games=100):
    """Play n_games games with new agents for every game.
    Returns the mean and std of the bankroll difference and the win rate (%) of agent 1."""
    diffs = []
    wins = 0
    for _ in range(n_games):
        b1, b2, _hist = play_game(cls1(), cls2())
        diffs.append(b1 - b2)
        if b1 > b2:
            wins += 1
    return statistics.mean(diffs), statistics.stdev(diffs), wins / n_games * 100


if __name__ == "__main__":
    names = list(AGENTS)
    w = 16
    mean_table = {}
    win_table = {}

    # Play every agent against every other agent
    for r in names:
        for c in names:
            if r != c:
                m, s, wr = matchup(AGENTS[r], AGENTS[c])
                mean_table[(r, c)] = (m, s)
                win_table[(r, c)] = wr

    print("Mean difference (row - column), +- std\n")
    print(f"{'':<8}" + "".join(f"{n:^{w}}" for n in names))
    print("-" * (8 + w * len(names)))
    for r in names:
        row = f"{r:<8}"
        for c in names:
            if r == c:
                cell = "-"
            else:
                m, s = mean_table[(r, c)]
                cell = f"{m:+.1f} +- {s:.0f}"
            row += f"{cell:^{w}}"
        print(row)

    print("\nWin rate % (percentage of games the row agent beat the column agent)\n")
    print(f"{'':<8}" + "".join(f"{n:^{w}}" for n in names))
    print("-" * (8 + w * len(names)))
    for r in names:
        row = f"{r:<8}"
        for c in names:
            cell = "-" if r == c else f"{win_table[(r, c)]:.0f}%"
            row += f"{cell:^{w}}"
        print(row)

    # Final ranking: average over all opponents
    print("\nFINAL RANKING (average over all opponents)\n")
    summary = []
    for r in names:
        others = [c for c in names if c != r]
        avg_diff = statistics.mean(mean_table[(r, c)][0] for c in others)
        avg_win = statistics.mean(win_table[(r, c)] for c in others)
        summary.append((r, avg_diff, avg_win))

    summary.sort(key=lambda x: x[1], reverse=True)
    print(f"{'Rank':<6}{'Agent':<10}{'Avg diff':>12}{'Avg win %':>12}")
    for i, (name, d, wr) in enumerate(summary, 1):
        print(f"{i:<6}{name:<10}{d:>+12.1f}{wr:>11.0f}%")

    print(f"\nWinner: {summary[0][0]}")
