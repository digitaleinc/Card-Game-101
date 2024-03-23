def calculate_score(hand):
    score = 0
    minus_points = 0

    for card in hand:
        rank = card[0]
        if rank.isdigit():
            if rank == '9':
                score += 0
            else:
                score += int(rank)
        elif rank in ['J', 'Q', 'K']:
            score += 10
        elif rank == 'A':
            score += 11

    if score == 0:
        for card in hand:
            rank = card[0]
            suit = card[1]
            if rank == 'Q':
                if suit == 'spades':
                    minus_points = 20
                else:
                    minus_points = 40

    score -= minus_points
    return score


def check_scores(scores):
    if scores[0] == 101:
        scores[0] = 0
    if scores[1] == 101:
        scores[1] = 0
    if scores[2] == 101:
        scores[2] = 0
    if scores[3] == 101:
        scores[3] = 0
    return scores


def save_results(winners, scores, players):
    with open("results.txt", "w") as file:
        file.write("Результати гри:\n")
        file.write("----------------\n")
        for i, player in enumerate(players):
            file.write(f"Гравець {player.name}: {scores[i]} очок\n")
        file.write("----------------\n")
        file.write("Переможці:\n")
        file.write("----------------\n")
        for winner in winners:
            file.write(f"Гравець {players[winner - 1].name}\n")


def determine_winner(final_scores):
    min_score = min(final_scores)
    winners = [i + 1 for i, score in enumerate(final_scores) if score == min_score]
    return winners, final_scores


def is_game_over(scores):
    max_score = max(scores)
    if max_score > 101:
        return True
    else:
        return False
