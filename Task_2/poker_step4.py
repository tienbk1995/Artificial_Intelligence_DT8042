import statistics
from Task_2.poker_step1 import RandomAgent
from Task_2.poker_step2 import FixedAgent
from Task_2.poker_step3 import play_game


def run_experiment(agent1, agent2, n_games=100):
    """n_games games chalata hai (har game 50 hands).
    Return: har game ka bankroll difference (agent1 - agent2) ki list"""
    diffs = []
    for _ in range(n_games):
        b1, b2, _hist = play_game(agent1, agent2)
        diffs.append(b1 - b2)
    return diffs


def summarize(name1, name2, diffs):
    mean = statistics.mean(diffs)
    std = statistics.stdev(diffs)
    wins1 = sum(1 for d in diffs if d > 0)
    wins2 = sum(1 for d in diffs if d < 0)
    print(f"{name1} vs {name2} ({len(diffs)} games, 50 hands each)")
    print(f"  Mean difference ({name1} - {name2}): {mean:.2f}")
    print(f"  Std deviation                    : {std:.2f}")
    print(f"  Games won: {name1} = {wins1}, {name2} = {wins2}")


if __name__ == "__main__":
    random_agent = RandomAgent()
    fixed_agent = FixedAgent()

    diffs = run_experiment(random_agent, fixed_agent, n_games=100)
    summarize("Random", "Fixed", diffs)