# Problem 54: Poker hands

## Problem

In the card game poker, a hand consists of five cards and are ranked, from lowest to highest, in the following way:

- **High Card:** Highest value card.
- **One Pair:** Two cards of the same value.
- **Two Pairs:** Two different pairs.
- **Three of a Kind:** Three cards of the same value.
- **Straight:** All cards are consecutive values.
- **Flush:** All cards of the same suit.
- **Full House:** Three of a kind and a pair.
- **Four of a Kind:** Four cards of the same value.
- **Straight Flush:** All cards are consecutive values of same suit.
- **Royal Flush:** Ten, Jack, Queen, King, Ace, in same suit.

The cards are valued in the order:
2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.

If two players have the same ranked hands then the rank made up of the highest value wins; for example, a pair of eights beats a pair of fives (see example 1 below). But if two ranks tie, for example, both players have a pair of queens, then highest cards in each hand are compared (see example 4 below); if the highest cards tie then the next highest cards are compared, and so on.

Consider the following five hands dealt to two players:
| Hand | Player 1 | Player 2 | Winner |
|---|---|---|---|
| 1 | 5H 5C 6S 7S KD<br>Pair of Fives | 2C 3S 8S 8D TD<br>Pair of Eights | Player 2 |
| 2 | 5D 8C 9S JS AC<br>Highest card Ace | 2C 5C 7D 8S QH<br>Highest card Queen | Player 1 |
| 3 | 2D 9C AS AH AC<br>Three Aces | 3D 6D 7D TD QD<br>Flush with Diamonds | Player 2 |
| 4 | 4D 6S 9H QH QC<br>Pair of Queens, highest card Nine | 3D 6D 7H QD QS<br>Pair of Queens, highest card Seven | Player 1 |
| 5 | 2H 2D 4C 4D 4S<br>Full House with Three Fours | 3C 3D 3S 9S 9D<br>Full House with Three Threes | Player 1 |

The file, `poker.txt`, contains one-thousand random hands dealt to two players. Each line of the file contains ten cards (separated by a single space): the first five are Player 1's cards and the last five are Player 2's cards. You can assume that all hands are valid (no invalid characters or repeated cards), each player's hand is in no specific order, and in each hand there is a clear winner.

How many hands does Player 1 win?


## Implementation


```python
from collections import defaultdict
from pathlib import Path
import abc
from dataclasses import dataclass
from typing import Protocol, Type
from typing import Self


# Solution
CARD_VALUE_POSITION = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}

class Card:
    def __init__(self, card_text: str):
        self.value: str = card_text[0]
        self.value_pos: int = CARD_VALUE_POSITION[self.value]
        self.suit: str = card_text[1]

    def __lt__(self, other):
        return self.value_pos < other.value_pos

    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, Card) and self.value == value.value
    
    def __repr__(self) -> str:
        return f"{self.value}{self.suit}"


def compare_card_values(cards1: list[Card], cards2: list[Card]) -> int:
    zipped_cards = zip(sorted(cards1, reverse=True), sorted(cards2, reverse=True))
    for c1, c2 in zipped_cards:
        if c1 < c2:
            return -1
        if c1 > c2:
            return 1
    return 0

def group_matching_cards(cards: list[Card]) -> dict[str, list[Card]]:
    groups = defaultdict(lambda: [])
    for card in cards:
        groups[card.value].append(card)
    return groups


def are_cards_consecutive(cards: list[Card]) -> bool:
    positions = [c.value_pos for c in cards]

    # Handle special case with A, 2, 3, ...
    if 2 in positions and 14 in positions:
        positions.remove(14)
        positions.append(1)
    
    sorted_positions = sorted(positions)
    i = 0
    while i < len(sorted_positions) - 1:
        if sorted_positions[i+1] - sorted_positions[i] != 1:
            return False
        i+=1
    return True


def are_cards_from_same_suit(cards: list[Card]) -> bool:
    suit = None
    for card in cards:
        if suit is None:
            suit = card.suit
        elif suit != card.suit:
            return False
    return True
            


class NotValidHandForCards(Exception):
    def __init__(self, *args: object):
        return


@dataclass(kw_only=True)
class PokerHand(abc.ABC):
    rank: int
    ranked_cards: list[Card]
    non_ranked_cards: list[Card]

    @abc.abstractclassmethod
    def from_cards(cls, cards: list[Card]) -> Self: ...

    def compare(self, other: PokerHand) -> int:
        if self.rank < other.rank:
            return -1
        if self.rank > other.rank:
            return 1
        ranked_card_values = compare_card_values(self.ranked_cards, other.ranked_cards)
        if ranked_card_values != 0:
            return ranked_card_values
        return compare_card_values(self.non_ranked_cards, other.non_ranked_cards)


@dataclass(kw_only=True)
class HighCard(PokerHand):
    rank: int = 1

    @classmethod
    def from_cards(cls, cards: list[Card]) -> Self:
        return cls(ranked_cards=[], non_ranked_cards=cards)


@dataclass(kw_only=True)
class OnePair(PokerHand):
    rank: int = 2
    
    @classmethod
    def from_cards(cls, cards: list[Card]) -> Self:
        groups = group_matching_cards(cards)
        pair_value = None
        for group_value, group_cards in groups.items():
            if len(group_cards) == 2:
                pair_value = group_value
                break
        if pair_value is None:
            raise NotValidHandForCards()
        return cls(ranked_cards=[c for c in cards if c.value == pair_value], non_ranked_cards=[c for c in cards if c.value != pair_value])


@dataclass(kw_only=True)
class TwoPairs(PokerHand):
    rank: int = 3

    @classmethod
    def from_cards(cls, cards: list[Card]) -> Self:
        groups = group_matching_cards(cards)
        first_pair_value = None
        second_pair_value = None
        for group_value, group_cards in groups.items():
            if len(group_cards) == 2:
                if first_pair_value is None:
                    first_pair_value = group_value
                else:
                    second_pair_value = group_value
                    break
        if second_pair_value is None:
            raise NotValidHandForCards()
        return cls(
            ranked_cards=[c for c in cards if c.value in (first_pair_value, second_pair_value)], 
            non_ranked_cards=[c for c in cards if c.value not in (first_pair_value, second_pair_value)],
        )


@dataclass(kw_only=True)
class ThreeOfAKind(PokerHand):
    rank: int = 4

    @classmethod
    def from_cards(cls, cards: list[Card]) -> Self:
        groups = group_matching_cards(cards)
        ranked_value = None
        for group_value, group_cards in groups.items():
            if len(group_cards) == 3:
                ranked_value = group_value
                break
        if ranked_value is None:
            raise NotValidHandForCards()
        return cls(ranked_cards=[c for c in cards if c.value == ranked_value], non_ranked_cards=[c for c in cards if c.value != ranked_value])


@dataclass(kw_only=True)
class Straight(PokerHand):
    rank: int = 5

    @classmethod
    def from_cards(cls, cards: list[Card]) -> Self:
        is_straight = are_cards_consecutive(cards)
        if not is_straight:
            raise NotValidHandForCards()
        return cls(ranked_cards=cards, non_ranked_cards=[])


@dataclass(kw_only=True)
class Flush(PokerHand):
    rank: int = 6

    @classmethod
    def from_cards(cls, cards: list[Card]) -> Self:
        same_suit = are_cards_from_same_suit(cards)
        if not same_suit:
            raise NotValidHandForCards()
        return cls(ranked_cards=cards, non_ranked_cards=[])


@dataclass(kw_only=True)
class FullHouse(PokerHand):
    rank: int = 7

    @classmethod
    def from_cards(cls, cards: list[Card]) -> Self:
        groups = group_matching_cards(cards)
        pair_value = None
        three_of_a_kind_value = None
        for group_value, group_cards in groups.items():
            if len(group_cards) == 2:
                pair_value = group_value
            elif len(group_cards) == 3:
                three_of_a_kind_value = group_value
        if pair_value is None or three_of_a_kind_value is None:
            raise NotValidHandForCards()
        return cls(
            ranked_cards=[c for c in cards if c.value in (pair_value, three_of_a_kind_value)],
            non_ranked_cards=[c for c in cards if c.value not in (pair_value, three_of_a_kind_value)],
        )


@dataclass(kw_only=True)
class FourOfAKind(PokerHand):
    rank: int = 8

    @classmethod
    def from_cards(cls, cards: list[Card]) -> Self:
        groups = group_matching_cards(cards)
        ranked_value = None
        for group_value, group_cards in groups.items():
            if len(group_cards) == 4:
                ranked_value = group_value
                break
        if ranked_value is None:
            raise NotValidHandForCards()
        return cls(ranked_cards=[c for c in cards if c.value == ranked_value], non_ranked_cards=[c for c in cards if c.value != ranked_value])


@dataclass(kw_only=True)
class StraightFlush(PokerHand):
    rank: int = 9

    @classmethod
    def from_cards(cls, cards: list[Card]) -> Self:
        is_straight = are_cards_consecutive(cards)
        is_same_suit = are_cards_from_same_suit(cards)
        if not is_straight or not is_same_suit:
            raise NotValidHandForCards()
        return cls(ranked_cards=cards, non_ranked_cards=[])


ALL_HAND_TYPES: list[Type[PokerHand]] = [
    StraightFlush,
    FourOfAKind,
    FullHouse,
    Flush,
    Straight,
    ThreeOfAKind,
    TwoPairs,
    OnePair,
    HighCard,
]


def get_hand_from_cards_text(cards_str_list: list[str]) -> PokerHand:
    cards = [Card(c) for c in cards_str_list]
    for hand_type in ALL_HAND_TYPES:
        try:
            return hand_type.from_cards(cards)
        except NotValidHandForCards:
            continue
    raise RuntimeError("This is not expected")


def parse_line_hands(line_str: str) -> tuple[PokerHand, PokerHand]:
    cards_str_list = line_str.strip().split(" ")
    p1_cards_str_list = cards_str_list[:5]
    p2_cards_str_list = cards_str_list[5:10]
    p1_hand = get_hand_from_cards_text(p1_cards_str_list)
    p2_hand = get_hand_from_cards_text(p2_cards_str_list)
    return p1_hand, p2_hand


def poker_hands() -> int:
    file_path = Path("poker.txt")
    p1_wins = 0
    with file_path.open("r") as f:
        for line_str in f.readlines():
            p1_hand, p2_hand = parse_line_hands(line_str)
            hand_result = p1_hand.compare(p2_hand)
            if hand_result > 0:
                print(f"{line_str} - P1 wins - P1 Hand: {p1_hand} ; P2 Hand: {p2_hand}")
                p1_wins+=1
            else:
                print(f"{line_str} - P1 does not win - P1 Hand: {p1_hand} ; P2 Hand: {p2_hand}")
    return p1_wins
# END solution


# Tests
def test_poker_hands():
    assert isinstance(get_hand_from_cards_text(["TS", "JD", "8S", "QS", "TH"]), OnePair)
    assert isinstance(get_hand_from_cards_text(["AS", "2S", "5S", "4S",  "3S"]), StraightFlush)
    assert isinstance(get_hand_from_cards_text(["6S", "2S", "5S", "4S",  "3S"]), StraightFlush)
    assert isinstance(get_hand_from_cards_text(["AS", "JS", "TS", "QS",  "KS"]), StraightFlush)
    assert isinstance(get_hand_from_cards_text(["AS", "2S", "TS", "4S",  "3S"]), Flush)
    assert isinstance(get_hand_from_cards_text(["6H", "6S", "6C", "KS",  "KH"]), FullHouse)
    print("All tests passed!")



from IPython.display import  Markdown

test_poker_hands()
solution = poker_hands()

Markdown(f"""
## Solution

How many hands does Player 1 win?: {solution}
""")
```

    All tests passed!
    8C TS KC 9H 4S 7D 2S 5D 3S AC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, TS, KC, 9H, 4S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 2S, 5D, 3S, AC])
    5C AD 5D AC 9C 7C 5H 8D TD KS
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[5C, AD, 5D, AC], non_ranked_cards=[9C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 5H, 8D, TD, KS])
    3H 7H 6S KC JS QH TD JC 2D 8S
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, 7H, 6S, KC, JS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, TD, JC, 2D, 8S])
    TH 8H 5C QS TC 9H 4D JC KS JS
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[TH, TC], non_ranked_cards=[8H, 5C, QS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JC, JS], non_ranked_cards=[9H, 4D, KS])
    7C 5H KC QH JD AS KH 4C AD 4S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 5H, KC, QH, JD]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[AS, 4C, AD, 4S], non_ranked_cards=[KH])
    5H KS 9C 7D 9H 8D 3S 5D 5C AH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9C, 9H], non_ranked_cards=[5H, KS, 7D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5D, 5C], non_ranked_cards=[8D, 3S, AH])
    6H 4H 5C 3H 2H 3S QH 5S 6S AS
     - P1 wins - P1 Hand: Straight(rank=5, ranked_cards=[6H, 4H, 5C, 3H, 2H], non_ranked_cards=[]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, QH, 5S, 6S, AS])
    TD 8C 4H 7C TC KC 4C 3H 7S KS
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[TD, TC], non_ranked_cards=[8C, 4H, 7C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KC, KS], non_ranked_cards=[4C, 3H, 7S])
    7C 9C 6D KD 3H 4C QS QC AC KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 9C, 6D, KD, 3H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QS, QC], non_ranked_cards=[4C, AC, KH])
    JC 6S 5H 2H 2D KD 9D 7C AS JS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2H, 2D], non_ranked_cards=[JC, 6S, 5H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, 9D, 7C, AS, JS])
    AD QH TH 9D 8H TS 6D 3S AS AC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, QH, TH, 9D, 8H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AS, AC], non_ranked_cards=[TS, 6D, 3S])
    2H 4S 5C 5S TC KC JD 6C TS 3C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5C, 5S], non_ranked_cards=[2H, 4S, TC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, JD, 6C, TS, 3C])
    QD AS 6H JS 2C 3D 9H KC 4H 8S
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QD, AS, 6H, JS, 2C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, 9H, KC, 4H, 8S])
    KD 8S 9S 7C 2S 3S 6D 6S 4H KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, 8S, 9S, 7C, 2S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6D, 6S], non_ranked_cards=[3S, 4H, KC])
    3C 8C 2D 7D 4D 9S 4S QH 4H JD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 8C, 2D, 7D, 4D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4S, 4H], non_ranked_cards=[9S, QH, JD])
    8C KC 7S TC 2D TS 8H QD AC 5C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, KC, 7S, TC, 2D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, 8H, QD, AC, 5C])
    3D KH QD 6C 6S AD AS 8H 2H QS
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[6C, 6S], non_ranked_cards=[3D, KH, QD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AD, AS], non_ranked_cards=[8H, 2H, QS])
    6S 8D 4C 8S 6C QH TC 6D 7D 9D
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[6S, 8D, 8S, 6C], non_ranked_cards=[4C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, TC, 6D, 7D, 9D])
    2S 8D 8C 4C TS 9S 9D 9C AC 3D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[8D, 8C], non_ranked_cards=[2S, 4C, TS]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[9S, 9D, 9C], non_ranked_cards=[AC, 3D])
    3C QS 2S 4H JH 3D 2D TD 8S 9H
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, QS, 2S, 4H, JH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, 2D, TD, 8S, 9H])
    5H QS 8S 6D 3C 8C JD AS 7H 7D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, QS, 8S, 6D, 3C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7H, 7D], non_ranked_cards=[8C, JD, AS])
    6H TD 9D AS JH 6C QC 9S KD JC
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, TD, 9D, AS, JH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, QC, 9S, KD, JC])
    AH 8S QS 4D TH AC TS 3C 3D 5C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AH, 8S, QS, 4D, TH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3C, 3D], non_ranked_cards=[AC, TS, 5C])
    5S 4D JS 3D 8H 6C TS 3S AD 8C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 4D, JS, 3D, 8H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, TS, 3S, AD, 8C])
    6D 7C 5D 5H 3S 5C JC 2H 5S 3D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[5D, 5H], non_ranked_cards=[6D, 7C, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5C, 5S], non_ranked_cards=[JC, 2H, 3D])
    5H 6H 2S KS 3D 5D JD 7H JS 8H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, 6H, 2S, KS, 3D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JD, JS], non_ranked_cards=[5D, 7H, 8H])
    KH 4H AS JS QS QC TC 6D 7C KS
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, 4H, AS, JS, QS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, TC, 6D, 7C, KS])
    3D QS TS 2H JS 4D AS 9S JC KD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, QS, TS, 2H, JS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, AS, 9S, JC, KD])
    QD 5H 4D 5D KH 7H 3D JS KD 4H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5H, 5D], non_ranked_cards=[QD, 4D, KH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, 3D, JS, KD, 4H])
    2C 9H 6H 5C 9D 6C JC 2D TH 9S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9H, 9D], non_ranked_cards=[2C, 6H, 5C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, JC, 2D, TH, 9S])
    7D 6D AS QD JH 4D JS 7C QS 5C
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 6D, AS, QD, JH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, JS, 7C, QS, 5C])
    3H KH QD AD 8C 8H 3S TH 9D 5S
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, KH, QD, AD, 8C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8H, 3S, TH, 9D, 5S])
    AH 9S 4D 9D 8S 4H JS 3C TC 8D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9S, 9D], non_ranked_cards=[AH, 4D, 8S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, JS, 3C, TC, 8D])
    2C KS 5H QD 3S TS 9H AH AD 8S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, KS, 5H, QD, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AH, AD], non_ranked_cards=[TS, 9H, 8S])
    5C 7H 5D KD 9H 4D 3D 2D KS AD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5C, 5D], non_ranked_cards=[7H, KD, 9H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, 3D, 2D, KS, AD])
    KS KC 9S 6D 2C QH 9D 9H TS TC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[KS, KC], non_ranked_cards=[9S, 6D, 2C]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[9D, 9H, TS, TC], non_ranked_cards=[QH])
    9C 6H 5D QH 4D AD 6D QC JS KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, 6H, 5D, QH, 4D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, 6D, QC, JS, KH])
    9S 3H 9D JD 5C 4D 9H AS TC QH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9S, 9D], non_ranked_cards=[3H, JD, 5C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, 9H, AS, TC, QH])
    2C 6D JC 9C 3C AD 9S KH 9D 7D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, 6D, JC, 9C, 3C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9S, 9D], non_ranked_cards=[AD, KH, 7D])
    KC 9C 7C JC JS KD 3H AS 3C 7D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JC, JS], non_ranked_cards=[KC, 9C, 7C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3H, 3C], non_ranked_cards=[KD, AS, 7D])
    QD KH QS 2C 3S 8S 8H 9H 9C JC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[QD, QS], non_ranked_cards=[KH, 2C, 3S]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[8S, 8H, 9H, 9C], non_ranked_cards=[JC])
    QH 8D 3C KC 4C 4H 6D AD 9H 9D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, 8D, 3C, KC, 4C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9H, 9D], non_ranked_cards=[4H, 6D, AD])
    3S KS QS 7H KH 7D 5H 5D JD AD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KS, KH], non_ranked_cards=[3S, QS, 7H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5H, 5D], non_ranked_cards=[7D, JD, AD])
    2H 2C 6H TH TC 7D 8D 4H 8C AS
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[2H, 2C, TH, TC], non_ranked_cards=[6H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8D, 8C], non_ranked_cards=[7D, 4H, AS])
    4S 2H AC QC 3S 6D TH 4D 4C KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4S, 2H, AC, QC, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4D, 4C], non_ranked_cards=[6D, TH, KH])
    4D TC KS AS 7C 3C 6D 2D 9H 6C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, TC, KS, AS, 7C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6D, 6C], non_ranked_cards=[3C, 2D, 9H])
    8C TD 5D QS 2C 7H 4C 9C 3H 9H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, TD, 5D, QS, 2C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9C, 9H], non_ranked_cards=[7H, 4C, 3H])
    5H JH TS 7S TD 6H AD QD 8H 8S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TS, TD], non_ranked_cards=[5H, JH, 7S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8H, 8S], non_ranked_cards=[6H, AD, QD])
    5S AD 9C 8C 7C 8D 5H 9D 8S 2S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, AD, 9C, 8C, 7C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8D, 8S], non_ranked_cards=[5H, 9D, 2S])
    4H KH KS 9S 2S KC 5S AD 4S 7D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KH, KS], non_ranked_cards=[4H, 9S, 2S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, 5S, AD, 4S, 7D])
    QS 9C QD 6H JS 5D AC 8D 2S AS
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[QS, QD], non_ranked_cards=[9C, 6H, JS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AC, AS], non_ranked_cards=[5D, 8D, 2S])
    KH AC JC 3S 9D 9S 3C 9C 5S JS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, AC, JC, 3S, 9D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9S, 9C], non_ranked_cards=[3C, 5S, JS])
    AD 3C 3D KS 3S 5C 9C 8C TS 4S
     - P1 wins - P1 Hand: ThreeOfAKind(rank=4, ranked_cards=[3C, 3D, 3S], non_ranked_cards=[AD, KS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5C, 9C, 8C, TS, 4S])
    JH 8D 5D 6H KD QS QD 3D 6C KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, 8D, 5D, 6H, KD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QS, QD], non_ranked_cards=[3D, 6C, KC])
    8S JD 6C 3S 8C TC QC 3C QH JS
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[8S, 8C], non_ranked_cards=[JD, 6C, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QC, QH], non_ranked_cards=[TC, 3C, JS])
    KC JC 8H 2S 9H 9C JH 8S 8C 9S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, JC, 8H, 2S, 9H]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[9C, 8S, 8C, 9S], non_ranked_cards=[JH])
    8S 2H QH 4D QC 9D KC AS TH 3C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QH, QC], non_ranked_cards=[8S, 2H, 4D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9D, KC, AS, TH, 3C])
    8S 6H TH 7C 2H 6S 3C 3H AS 7S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, 6H, TH, 7C, 2H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3C, 3H], non_ranked_cards=[6S, AS, 7S])
    QH 5S JS 4H 5H TS 8H AH AC JC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[5S, 5H], non_ranked_cards=[QH, JS, 4H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AH, AC], non_ranked_cards=[TS, 8H, JC])
    9D 8H 2S 4S TC JC 3C 7H 3H 5C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9D, 8H, 2S, 4S, TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3C, 3H], non_ranked_cards=[JC, 7H, 5C])
    3D AD 3C 3S 4C QC AS 5D TH 8C
     - P1 wins - P1 Hand: ThreeOfAKind(rank=4, ranked_cards=[3D, 3C, 3S], non_ranked_cards=[AD, 4C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, AS, 5D, TH, 8C])
    6S 9D 4C JS KH AH TS JD 8H AD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, 9D, 4C, JS, KH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AH, AD], non_ranked_cards=[TS, JD, 8H])
    4C 6S 9D 7S AC 4D 3D 3S TC JD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 6S, 9D, 7S, AC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3D, 3S], non_ranked_cards=[4D, TC, JD])
    AD 7H 6H 4H JH KC TD TS 7D 6S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, 7H, 6H, 4H, JH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TD, TS], non_ranked_cards=[KC, 7D, 6S])
    8H JH TC 3S 8D 8C 9S 2C 5C 4D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[8H, 8D], non_ranked_cards=[JH, TC, 3S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, 9S, 2C, 5C, 4D])
    2C 9D KC QH TH QS JC 9C 4H TS
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, 9D, KC, QH, TH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, JC, 9C, 4H, TS])
    QS 3C QD 8H KH 4H 8D TD 8S AC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QS, QD], non_ranked_cards=[3C, 8H, KH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8D, 8S], non_ranked_cards=[4H, TD, AC])
    7C 3C TH 5S 8H 8C 9C JD TC KD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 3C, TH, 5S, 8H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, 9C, JD, TC, KD])
    QC TC JD TS 8C 3H 6H KD 7C TD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TC, TS], non_ranked_cards=[QC, JD, 8C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, 6H, KD, 7C, TD])
    JH QS KS 9C 6D 6S AS 9H KH 6H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, QS, KS, 9C, 6D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6S, 6H], non_ranked_cards=[AS, 9H, KH])
    2H 4D AH 2D JH 6H TD 5D 4H JD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2H, 2D], non_ranked_cards=[4D, AH, JH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, TD, 5D, 4H, JD])
    KD 8C 9S JH QD JS 2C QS 5C 7C
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, 8C, 9S, JH, QD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, 2C, QS, 5C, 7C])
    4S TC 7H 8D 2S 6H 7S 9C 7C KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4S, TC, 7H, 8D, 2S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7S, 7C], non_ranked_cards=[6H, 9C, KC])
    8C 5D 7H 4S TD QC 8S JS 4H KS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, 5D, 7H, 4S, TD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 8S, JS, 4H, KS])
    AD 8S JH 6D TD KD 7C 6C 2D 7D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, 8S, JH, 6D, TD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7C, 7D], non_ranked_cards=[KD, 6C, 2D])
    JC 6H 6S JS 4H QH 9H AH 4C 3C
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[JC, 6H, 6S, JS], non_ranked_cards=[4H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, 9H, AH, 4C, 3C])
    6H 5H AS 7C 7S 3D KH KC 5D 5C
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[7C, 7S], non_ranked_cards=[6H, 5H, AS]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[KH, KC, 5D, 5C], non_ranked_cards=[3D])
    JC 3D TD AS 4D 6D 6S QH JD KS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JC, 3D, TD, AS, 4D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6D, 6S], non_ranked_cards=[QH, JD, KS])
    8C 7S 8S QH 2S JD 5C 7H AH QD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[8C, 8S], non_ranked_cards=[7S, QH, 2S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, 5C, 7H, AH, QD])
    8S 3C 6H 6C 2C 8D TD 7D 4C 4D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[6H, 6C], non_ranked_cards=[8S, 3C, 2C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4C, 4D], non_ranked_cards=[8D, TD, 7D])
    5D QH KH 7C 2S 7H JS 6D QC QD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5D, QH, KH, 7C, 2S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QC, QD], non_ranked_cards=[7H, JS, 6D])
    AD 6C 6S 7D TH 6H 2H 8H KH 4H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[6C, 6S], non_ranked_cards=[AD, 7D, TH]) ; P2 Hand: Flush(rank=6, ranked_cards=[6H, 2H, 8H, KH, 4H], non_ranked_cards=[])
    KS JS KD 5D 2D KH 7D 9C 8C 3D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KS, KD], non_ranked_cards=[JS, 5D, 2D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, 7D, 9C, 8C, 3D])
    9C 6D QD 3C KS 3S 7S AH JD 2D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, 6D, QD, 3C, KS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, 7S, AH, JD, 2D])
    AH QH AS JC 8S 8H 4C KC TH 7D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AH, AS], non_ranked_cards=[QH, JC, 8S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8H, 4C, KC, TH, 7D])
    JC 5H TD 7C 5D KD 4C AD 8H JS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5H, 5D], non_ranked_cards=[JC, TD, 7C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, 4C, AD, 8H, JS])
    KC 2H AC AH 7D JH KH 5D 7S 6D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AC, AH], non_ranked_cards=[KC, 2H, 7D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, KH, 5D, 7S, 6D])
    9S 5S 9C 6H 8S TD JD 9H 6C AC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9S, 9C], non_ranked_cards=[5S, 6H, 8S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, JD, 9H, 6C, AC])
    7D 8S 6D TS KD 7H AC 5S 7C 5D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 8S, 6D, TS, KD]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[7H, 5S, 7C, 5D], non_ranked_cards=[AC])
    AH QC JC 4C TC 8C 2H TS 2C 7D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AH, QC, JC, 4C, TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2H, 2C], non_ranked_cards=[8C, TS, 7D])
    KD KC 6S 3D 7D 2S 8S 3H 5S 5C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KD, KC], non_ranked_cards=[6S, 3D, 7D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5S, 5C], non_ranked_cards=[2S, 8S, 3H])
    8S 5D 8H 4C 6H KC 3H 7C 5S KD
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[8S, 8H], non_ranked_cards=[5D, 4C, 6H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KC, KD], non_ranked_cards=[3H, 7C, 5S])
    JH 8C 3D 3C 6C KC TD 7H 7C 4C
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3D, 3C], non_ranked_cards=[JH, 8C, 6C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7H, 7C], non_ranked_cards=[KC, TD, 4C])
    JC KC 6H TS QS TD KS 8H 8C 9S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JC, KC, 6H, TS, QS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8H, 8C], non_ranked_cards=[TD, KS, 9S])
    6C 5S 9C QH 7D AH KS KC 9S 2C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, 5S, 9C, QH, 7D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KS, KC], non_ranked_cards=[AH, 9S, 2C])
    4D 4S 8H TD 9C 3S 7D 9D AS TH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4D, 4S], non_ranked_cards=[8H, TD, 9C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, 7D, 9D, AS, TH])
    6S 7D 3C 6H 5D KD 2C 5C 9D 9C
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[6S, 6H], non_ranked_cards=[7D, 3C, 5D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9D, 9C], non_ranked_cards=[KD, 2C, 5C])
    2H KC 3D AD 3H QD QS 8D JC 4S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3D, 3H], non_ranked_cards=[2H, KC, AD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QD, QS], non_ranked_cards=[8D, JC, 4S])
    8C 3H 9C 7C AD 5D JC 9D JS AS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, 3H, 9C, 7C, AD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JC, JS], non_ranked_cards=[5D, 9D, AS])
    5D 9H 5C 7H 6S 6C QC JC QD 9S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[5D, 5C], non_ranked_cards=[9H, 7H, 6S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QC, QD], non_ranked_cards=[6C, JC, 9S])
    JC QS JH 2C 6S 9C QC 3D 4S TC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JC, JH], non_ranked_cards=[QS, 2C, 6S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, QC, 3D, 4S, TC])
    4H 5S 8D 3D 4D 2S KC 2H JS 2C
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[4H, 4D], non_ranked_cards=[5S, 8D, 3D]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[2S, 2H, 2C], non_ranked_cards=[KC, JS])
    TD 3S TH KD 4D 7H JH JS KS AC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[TD, TH], non_ranked_cards=[3S, KD, 4D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JH, JS], non_ranked_cards=[7H, KS, AC])
    7S 8C 9S 2D 8S 7D 5C AD 9D AS
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[8C, 8S], non_ranked_cards=[7S, 9S, 2D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AD, AS], non_ranked_cards=[7D, 5C, 9D])
    8C 7H 2S 6C TH 3H 4C 3S 8H AC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, 7H, 2S, 6C, TH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3H, 3S], non_ranked_cards=[4C, 8H, AC])
    KD 5H JC 8H JD 2D 4H TD JH 5C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JC, JD], non_ranked_cards=[KD, 5H, 8H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, 4H, TD, JH, 5C])
    3D AS QH KS 7H JD 8S 5S 6D 5H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, AS, QH, KS, 7H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5S, 5H], non_ranked_cards=[JD, 8S, 6D])
    9S 6S TC QS JC 5C 5D 9C TH 8C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9S, 6S, TC, QS, JC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5C, 5D], non_ranked_cards=[9C, TH, 8C])
    5H 3S JH 9H 2S 2C 6S 7S AS KS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, 3S, JH, 9H, 2S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, 6S, 7S, AS, KS])
    8C QD JC QS TC QC 4H AC KH 6C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QD, QS], non_ranked_cards=[8C, JC, TC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 4H, AC, KH, 6C])
    TC 5H 7D JH 4H 2H 8D JC KS 4D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, 5H, 7D, JH, 4H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, 8D, JC, KS, 4D])
    5S 9C KH KD 9H 5C TS 3D 7D 2D
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[9C, KH, KD, 9H], non_ranked_cards=[5S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5C, TS, 3D, 7D, 2D])
    5H AS TC 4D 8C 2C TS 9D 3H 8D
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, AS, TC, 4D, 8C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, TS, 9D, 3H, 8D])
    6H 8D 2D 9H JD 6C 4S 5H 5S 6D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, 8D, 2D, 9H, JD]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[6C, 5H, 5S, 6D], non_ranked_cards=[4S])
    AD 9C JC 7D 6H 9S 6D JS 9H 3C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, 9C, JC, 7D, 6H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9S, 9H], non_ranked_cards=[6D, JS, 3C])
    AD JH TC QS 4C 5D 9S 7C 9C AH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, JH, TC, QS, 4C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9S, 9C], non_ranked_cards=[5D, 7C, AH])
    KD 6H 2H TH 8S QD KS 9D 9H AS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, 6H, 2H, TH, 8S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9D, 9H], non_ranked_cards=[QD, KS, AS])
    4H 8H 8D 5H 6C AH 5S AS AD 8S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[8H, 8D], non_ranked_cards=[4H, 5H, 6C]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[AH, AS, AD], non_ranked_cards=[5S, 8S])
    QS 5D 4S 2H TD KS 5H AC 3H JC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 5D, 4S, 2H, TD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 5H, AC, 3H, JC])
    9C 7D QD KD AC 6D 5H QH 6H 5S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, 7D, QD, KD, AC]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[6D, 5H, 6H, 5S], non_ranked_cards=[QH])
    KC AH QH 2H 7D QS 3H KS 7S JD
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, AH, QH, 2H, 7D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 3H, KS, 7S, JD])
    6C 8S 3H 6D KS QD 5D 5C 8H TC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[6C, 6D], non_ranked_cards=[8S, 3H, KS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5D, 5C], non_ranked_cards=[QD, 8H, TC])
    9H 4D 4S 6S 9D KH QC 4H 6C JD
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[9H, 4D, 4S, 9D], non_ranked_cards=[6S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, QC, 4H, 6C, JD])
    TD 2D QH 4S 6H JH KD 3C QD 8C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 2D, QH, 4S, 6H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, KD, 3C, QD, 8C])
    4S 6H 7C QD 9D AS AH 6S AD 3C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4S, 6H, 7C, QD, 9D]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[AS, AH, AD], non_ranked_cards=[6S, 3C])
    2C KC TH 6H 8D AH 5C 6D 8S 5D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, KC, TH, 6H, 8D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5C, 5D], non_ranked_cards=[AH, 6D, 8S])
    TD TS 7C AD JC QD 9H 3C KC 7H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TD, TS], non_ranked_cards=[7C, AD, JC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QD, 9H, 3C, KC, 7H])
    5D 4D 5S 8H 4H 7D 3H JD KD 2D
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[5D, 4D, 5S, 4H], non_ranked_cards=[8H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 3H, JD, KD, 2D])
    JH TD 6H QS 4S KD 5C 8S 7D 8H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, TD, 6H, QS, 4S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8S, 8H], non_ranked_cards=[KD, 5C, 7D])
    AC 3D AS 8C TD 7H KH 5D 6C JD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AC, AS], non_ranked_cards=[3D, 8C, TD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, KH, 5D, 6C, JD])
    9D KS 7C 6D QH TC JD KD AS KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9D, KS, 7C, 6D, QH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KD, KC], non_ranked_cards=[TC, JD, AS])
    JH 8S 5S 7S 7D AS 2D 3D AD 2H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[7S, 7D], non_ranked_cards=[JH, 8S, 5S]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[AS, 2D, AD, 2H], non_ranked_cards=[3D])
    2H 5D AS 3C QD KC 6H 9H 9S 2C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, 5D, AS, 3C, QD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9H, 9S], non_ranked_cards=[KC, 6H, 2C])
    9D 5D TH 4C JH 3H 8D TC 8H 9H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9D, 5D, TH, 4C, JH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8D, 8H], non_ranked_cards=[3H, TC, 9H])
    6H KD 2C TD 2H 6C 9D 2D JS 8C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2C, 2H], non_ranked_cards=[6H, KD, TD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, 9D, 2D, JS, 8C])
    KD 7S 3C 7C AS QH TS AD 8C 2S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7S, 7C], non_ranked_cards=[KD, 3C, AS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, TS, AD, 8C, 2S])
    QS 8H 6C JS 4C 9S QC AD TD TS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 8H, 6C, JS, 4C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TD, TS], non_ranked_cards=[9S, QC, AD])
    2H 7C TS TC 8C 3C 9H 2D 6D JC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TS, TC], non_ranked_cards=[2H, 7C, 8C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 9H, 2D, 6D, JC])
    TC 2H 8D JH KS 6D 3H TD TH 8H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, 2H, 8D, JH, KS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TD, TH], non_ranked_cards=[6D, 3H, 8H])
    9D TD 9H QC 5D 6C 8H 8C KC TS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9D, 9H], non_ranked_cards=[TD, QC, 5D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8H, 8C], non_ranked_cards=[6C, KC, TS])
    2H 8C 3D AH 4D TH TC 7D 8H KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, 8C, 3D, AH, 4D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TH, TC], non_ranked_cards=[7D, 8H, KC])
    TS 5C 2D 8C 6S KH AH 5H 6H KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, 5C, 2D, 8C, 6S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KH, KC], non_ranked_cards=[AH, 5H, 6H])
    5S 5D AH TC 4C JD 8D 6H 8C 6C
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[5S, 5D], non_ranked_cards=[AH, TC, 4C]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[8D, 6H, 8C, 6C], non_ranked_cards=[JD])
    KC QD 3D 8H 2D JC 9H 4H AD 2S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, QD, 3D, 8H, 2D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JC, 9H, 4H, AD, 2S])
    TD 6S 7D JS KD 4H QS 2S 3S 8C
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 6S, 7D, JS, KD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, QS, 2S, 3S, 8C])
    4C 9H JH TS 3S 4H QC 5S 9S 9C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 9H, JH, TS, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9S, 9C], non_ranked_cards=[4H, QC, 5S])
    2C KD 9H JS 9S 3H JC TS 5D AC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9H, 9S], non_ranked_cards=[2C, KD, JS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, JC, TS, 5D, AC])
    AS 2H 5D AD 5H JC 7S TD JS 4C
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[AS, 5D, AD, 5H], non_ranked_cards=[2H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JC, JS], non_ranked_cards=[7S, TD, 4C])
    2D 4S 8H 3D 7D 2C AD KD 9C TS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, 4S, 8H, 3D, 7D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, AD, KD, 9C, TS])
    7H QD JH 5H JS AC 3D TH 4C 8H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JH, JS], non_ranked_cards=[7H, QD, 5H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 3D, TH, 4C, 8H])
    6D KH KC QD 5C AD 7C 2D 4H AC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[KH, KC], non_ranked_cards=[6D, QD, 5C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AD, AC], non_ranked_cards=[7C, 2D, 4H])
    3D 9D TC 8S QD 2C JC 4H JD AH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, 9D, TC, 8S, QD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JC, JD], non_ranked_cards=[2C, 4H, AH])
    6C TD 5S TC 8S AH 2C 5D AS AC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[TD, TC], non_ranked_cards=[6C, 5S, 8S]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[AH, AS, AC], non_ranked_cards=[2C, 5D])
    TH 7S 3D AS 6C 4C 7H 7D 4H AH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, 7S, 3D, AS, 6C]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[4C, 7H, 7D, 4H], non_ranked_cards=[AH])
    5C 2H KS 6H 7S 4H 5H 3D 3C 7H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5C, 2H, KS, 6H, 7S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3D, 3C], non_ranked_cards=[4H, 5H, 7H])
    3C 9S AC 7S QH 2H 3D 6S 3S 3H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 9S, AC, 7S, QH]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[3D, 3S, 3H], non_ranked_cards=[2H, 6S])
    2D 3H AS 2C 6H TC JS 6S 9C 6C
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2D, 2C], non_ranked_cards=[3H, AS, 6H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6S, 6C], non_ranked_cards=[TC, JS, 9C])
    QH KD QD 6D AC 6H KH 2C TS 8C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QH, QD], non_ranked_cards=[KD, 6D, AC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, KH, 2C, TS, 8C])
    8H 7D 3S 9H 5D 3H 4S QC 9S 5H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8H, 7D, 3S, 9H, 5D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, 4S, QC, 9S, 5H])
    2D 9D 7H 6H 3C 8S 5H 4D 3S 4S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, 9D, 7H, 6H, 3C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4D, 4S], non_ranked_cards=[8S, 5H, 3S])
    KD 9S 4S TC 7S QC 3S 8S 2H 7H
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, 9S, 4S, TC, 7S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 3S, 8S, 2H, 7H])
    TC 3D 8C 3H 6C 2H 6H KS KD 4D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3D, 3H], non_ranked_cards=[TC, 8C, 6C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KS, KD], non_ranked_cards=[2H, 6H, 4D])
    KC 3D 9S 3H JS 4S 8H 2D 6C 8S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3D, 3H], non_ranked_cards=[KC, 9S, JS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8H, 8S], non_ranked_cards=[4S, 2D, 6C])
    6H QS 6C TC QD 9H 7D 7C 5H 4D
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[6H, QS, 6C, QD], non_ranked_cards=[TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7D, 7C], non_ranked_cards=[9H, 5H, 4D])
    TD 9D 8D 6S 6C TC 5D TS JS 8H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[6S, 6C], non_ranked_cards=[TD, 9D, 8D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TC, TS], non_ranked_cards=[5D, JS, 8H])
    4H KC JD 9H TC 2C 6S 5H 8H AS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, KC, JD, 9H, TC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, 6S, 5H, 8H, AS])
    JS 9C 5C 6S 9D JD 8H KC 4C 6D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9C, 9D], non_ranked_cards=[JS, 5C, 6S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, 8H, KC, 4C, 6D])
    4D 8D 8S 6C 7C 6H 7H 8H 5C KC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[8D, 8S], non_ranked_cards=[4D, 6C, 7C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, 7H, 8H, 5C, KC])
    TC 3D JC 6D KS 9S 6H 7S 9C 2C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, 3D, JC, 6D, KS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9S, 9C], non_ranked_cards=[6H, 7S, 2C])
    6C 3S KD 5H TS 7D 9H 9S 6H KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, 3S, KD, 5H, TS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9H, 9S], non_ranked_cards=[7D, 6H, KH])
    3D QD 4C 6H TS AC 3S 5C 2H KD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, QD, 4C, 6H, TS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 3S, 5C, 2H, KD])
    4C AS JS 9S 7C TS 7H 9H JC KS
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, AS, JS, 9S, 7C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, 7H, 9H, JC, KS])
    4H 8C JD 3H 6H AD 9S 4S 5S KS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, 8C, JD, 3H, 6H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, 9S, 4S, 5S, KS])
    4C 2C 7D 3D AS 9C 2S QS KC 6C
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 2C, 7D, 3D, AS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, 2S, QS, KC, 6C])
    8S 5H 3D 2S AC 9D 6S 3S 4D TD
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, 5H, 3D, 2S, AC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9D, 6S, 3S, 4D, TD])
    QD TH 7S TS 3D AC 7H 6C 5D QC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TH, TS], non_ranked_cards=[QD, 7S, 3D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 7H, 6C, 5D, QC])
    TC QD AD 9C QS 5C 8D KD 3D 3C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QD, QS], non_ranked_cards=[TC, AD, 9C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3D, 3C], non_ranked_cards=[5C, 8D, KD])
    9D 8H AS 3S 7C 8S JD 2D 8D KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9D, 8H, AS, 3S, 7C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8S, 8D], non_ranked_cards=[JD, 2D, KC])
    4C TH AC QH JS 8D 7D 7S 9C KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, TH, AC, QH, JS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7D, 7S], non_ranked_cards=[8D, 9C, KH])
    9D 8D 4C JH 2C 2S QD KD TS 4H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9D, 8D, 4C, JH, 2C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, QD, KD, TS, 4H])
    4D 6D 5D 2D JH 3S 8S 3H TC KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, 6D, 5D, 2D, JH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3S, 3H], non_ranked_cards=[8S, TC, KH])
    AD 4D 2C QS 8C KD JH JD AH 5C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, 4D, 2C, QS, 8C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JH, JD], non_ranked_cards=[KD, AH, 5C])
    5C 6C 5H 2H JH 4H KS 7C TC 3H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5C, 5H], non_ranked_cards=[6C, 2H, JH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, KS, 7C, TC, 3H])
    3C 4C QC 5D JH 9C QD KH 8D TC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 4C, QC, 5D, JH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, QD, KH, 8D, TC])
    3H 9C JS 7H QH AS 7C 9H 5H JC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, 9C, JS, 7H, QH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, 7C, 9H, 5H, JC])
    2D 5S QD 4S 3C KC 6S 6C 5C 4C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, 5S, QD, 4S, 3C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6S, 6C], non_ranked_cards=[KC, 5C, 4C])
    5D KH 2D TS 8S 9C AS 9S 7C 4C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5D, KH, 2D, TS, 8S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9C, 9S], non_ranked_cards=[AS, 7C, 4C])
    7C AH 8C 8D 5S KD QH QS JH 2C
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[8C, 8D], non_ranked_cards=[7C, AH, 5S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QH, QS], non_ranked_cards=[KD, JH, 2C])
    8C 9D AH 2H AC QC 5S 8H 7H 2C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AH, AC], non_ranked_cards=[8C, 9D, 2H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 5S, 8H, 7H, 2C])
    QD 9H 5S QS QC 9C 5H JC TH 4H
     - P1 wins - P1 Hand: ThreeOfAKind(rank=4, ranked_cards=[QD, QS, QC], non_ranked_cards=[9H, 5S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, 5H, JC, TH, 4H])
    6C 6S 3H 5H 3S 6H KS 8D AC 7S
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[6C, 6S, 3H, 3S], non_ranked_cards=[5H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, KS, 8D, AC, 7S])
    AC QH 7H 8C 4S KC 6C 3D 3S TC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, QH, 7H, 8C, 4S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3D, 3S], non_ranked_cards=[KC, 6C, TC])
    9D 3D JS TH AC 5H 3H 8S 3S TC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9D, 3D, JS, TH, AC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3H, 3S], non_ranked_cards=[5H, 8S, TC])
    QD KH JS KS 9S QC 8D AH 3C AC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[KH, KS], non_ranked_cards=[QD, JS, 9S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AH, AC], non_ranked_cards=[QC, 8D, 3C])
    5H 6C KH 3S 9S JH 2D QD AS 8C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, 6C, KH, 3S, 9S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, 2D, QD, AS, 8C])
    6C 4D 7S 7H 5S JC 6S 9H 4H JH
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[7S, 7H], non_ranked_cards=[6C, 4D, 5S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JC, JH], non_ranked_cards=[6S, 9H, 4H])
    AH 5S 6H 9S AD 3S TH 2H 9D 8C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AH, AD], non_ranked_cards=[5S, 6H, 9S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, TH, 2H, 9D, 8C])
    4C 8D 9H 7C QC AD 4S 9C KC 5S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 8D, 9H, 7C, QC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, 4S, 9C, KC, 5S])
    9D 6H 4D TC 4C JH 2S 5D 3S AS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4D, 4C], non_ranked_cards=[9D, 6H, TC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, 2S, 5D, 3S, AS])
    2H 6C 7C KH 5C AD QS TH JD 8S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, 6C, 7C, KH, 5C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, QS, TH, JD, 8S])
    3S 4S 7S AH AS KC JS 2S AD TH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AH, AS], non_ranked_cards=[3S, 4S, 7S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, JS, 2S, AD, TH])
    JS KC 2S 7D 8C 5C 9C TS 5H 9D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, KC, 2S, 7D, 8C]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[5C, 9C, 5H, 9D], non_ranked_cards=[TS])
    7S 9S 4D TD JH JS KH 6H 5D 2C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7S, 9S, 4D, TD, JH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, KH, 6H, 5D, 2C])
    JD JS JC TH 2D 3D QD 8C AC 5H
     - P1 wins - P1 Hand: ThreeOfAKind(rank=4, ranked_cards=[JD, JS, JC], non_ranked_cards=[TH, 2D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, QD, 8C, AC, 5H])
    7S KH 5S 9D 5D TD 4S 6H 3C 2D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5S, 5D], non_ranked_cards=[7S, KH, 9D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 4S, 6H, 3C, 2D])
    4S 5D AC 8D 4D 7C AD AS AH 9C
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[4S, 4D], non_ranked_cards=[5D, AC, 8D]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[AD, AS, AH], non_ranked_cards=[7C, 9C])
    6S TH TS KS 2C QC AH AS 3C 4S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[TH, TS], non_ranked_cards=[6S, KS, 2C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AH, AS], non_ranked_cards=[QC, 3C, 4S])
    2H 8C 3S JC 5C 7C 3H 3C KH JH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, 8C, 3S, JC, 5C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3H, 3C], non_ranked_cards=[7C, KH, JH])
    7S 3H JC 5S 6H 4C 2S 4D KC 7H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7S, 3H, JC, 5S, 6H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4C, 4D], non_ranked_cards=[2S, KC, 7H])
    4D 7C 4H 9S 8S 6S AD TC 6C JC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[4D, 4H], non_ranked_cards=[7C, 9S, 8S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6S, 6C], non_ranked_cards=[AD, TC, JC])
    KH QS 3S TC 4C 8H 8S AC 3C TS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, QS, 3S, TC, 4C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8H, 8S], non_ranked_cards=[AC, 3C, TS])
    QD QS TH 3C TS 7H 7D AH TD JC
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[QD, QS, TH, TS], non_ranked_cards=[3C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7H, 7D], non_ranked_cards=[AH, TD, JC])
    TD JD QC 4D 9S 7S TS AD 7D AC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, JD, QC, 4D, 9S]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[7S, AD, 7D, AC], non_ranked_cards=[TS])
    AH 7H 4S 6D 7C 2H 9D KS JC TD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7H, 7C], non_ranked_cards=[AH, 4S, 6D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, 9D, KS, JC, TD])
    7C AH JD 4H 6D QS TS 2H 2C 5C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, AH, JD, 4H, 6D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2H, 2C], non_ranked_cards=[QS, TS, 5C])
    TC KC 8C 9S 4C JS 3C JC 6S AH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, KC, 8C, 9S, 4C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JS, JC], non_ranked_cards=[3C, 6S, AH])
    AS 7D QC 3D 5S JC JD 9D TD KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, 7D, QC, 3D, 5S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JC, JD], non_ranked_cards=[9D, TD, KH])
    TH 3C 2S 6H AH AC 5H 5C 7S 8H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, 3C, 2S, 6H, AH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5H, 5C], non_ranked_cards=[AC, 7S, 8H])
    QC 2D AC QD 2S 3S JD QS 6S 8H
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[QC, 2D, QD, 2S], non_ranked_cards=[AC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, JD, QS, 6S, 8H])
    KC 4H 3C 9D JS 6H 3S 8S AS 8C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, 4H, 3C, 9D, JS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8S, 8C], non_ranked_cards=[6H, 3S, AS])
    7H KC 7D JD 2H JC QH 5S 3H QS
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[7H, 7D], non_ranked_cards=[KC, JD, 2H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QH, QS], non_ranked_cards=[JC, 5S, 3H])
    9H TD 3S 8H 7S AC 5C 6C AH 7C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, TD, 3S, 8H, 7S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AC, AH], non_ranked_cards=[5C, 6C, 7C])
    8D 9H AH JD TD QS 7D 3S 9C 8S
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, 9H, AH, JD, TD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 7D, 3S, 9C, 8S])
    AH QH 3C JD KC 4S 5S 5D TD KS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AH, QH, 3C, JD, KC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5S, 5D], non_ranked_cards=[4S, TD, KS])
    9H 7H 6S JH TH 4C 7C AD 5C 2D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, 7H, 6S, JH, TH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 7C, AD, 5C, 2D])
    7C KD 5S TC 9D 6S 6C 5D 2S TH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, KD, 5S, TC, 9D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6S, 6C], non_ranked_cards=[5D, 2S, TH])
    KC 9H 8D 5H 7H 4H QC 3D 7C AS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, 9H, 8D, 5H, 7H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, QC, 3D, 7C, AS])
    6S 8S QC TD 4S 5C TH QS QD 2S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, 8S, QC, TD, 4S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QS, QD], non_ranked_cards=[5C, TH, 2S])
    8S 5H TH QC 9H 6S KC 7D 7C 5C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, 5H, TH, QC, 9H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7D, 7C], non_ranked_cards=[6S, KC, 5C])
    7H KD AH 4D KH 5C 4S 2D KC QH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KD, KH], non_ranked_cards=[7H, AH, 4D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5C, 4S, 2D, KC, QH])
    6S 2C TD JC AS 4D 6C 8C 4H 5S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, 2C, TD, JC, AS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4D, 4H], non_ranked_cards=[6C, 8C, 5S])
    JC TC JD 5S 6S 8D AS 9D AD 3S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[JC, JD], non_ranked_cards=[TC, 5S, 6S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AS, AD], non_ranked_cards=[8D, 9D, 3S])
    6D 6H 5D 5S TC 3D 7D QS 9D QD
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[6D, 6H, 5D, 5S], non_ranked_cards=[TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QS, QD], non_ranked_cards=[3D, 7D, 9D])
    4S 6C 8S 3S 7S AD KS 2D 7D 7C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4S, 6C, 8S, 3S, 7S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7D, 7C], non_ranked_cards=[AD, KS, 2D])
    KC QH JC AC QD 5D 8D QS 7H 7D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QH, QD], non_ranked_cards=[KC, JC, AC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7H, 7D], non_ranked_cards=[5D, 8D, QS])
    JS AH 8S 5H 3D TD 3H 4S 6C JH
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, AH, 8S, 5H, 3D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 3H, 4S, 6C, JH])
    4S QS 7D AS 9H JS KS 6D TC 5C
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4S, QS, 7D, AS, 9H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, KS, 6D, TC, 5C])
    2D 5C 6H TC 4D QH 3D 9H 8S 6C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, 5C, 6H, TC, 4D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, 3D, 9H, 8S, 6C])
    6D 7H TC TH 5S JD 5C 9C KS KD
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[TC, TH], non_ranked_cards=[6D, 7H, 5S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KS, KD], non_ranked_cards=[JD, 5C, 9C])
    8D TD QH 6S 4S 6C 8S KC 5C TC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, TD, QH, 6S, 4S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, 8S, KC, 5C, TC])
    5S 3D KS AC 4S 7D QD 4C TH 2S
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 3D, KS, AC, 4S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, QD, 4C, TH, 2S])
    TS 8H 9S 6S 7S QH 3C AH 7H 8C
     - P1 wins - P1 Hand: Straight(rank=5, ranked_cards=[TS, 8H, 9S, 6S, 7S], non_ranked_cards=[]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, 3C, AH, 7H, 8C])
    4C 8C TS JS QC 3D 7D 5D 7S JH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 8C, TS, JS, QC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7D, 7S], non_ranked_cards=[3D, 5D, JH])
    8S 7S 9D QC AC 7C 6D 2H JH KC
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, 7S, 9D, QC, AC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 6D, 2H, JH, KC])
    JS KD 3C 6S 4S 7C AH QC KS 5H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, KD, 3C, 6S, 4S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, AH, QC, KS, 5H])
    KS 6S 4H JD QS TC 8H KC 6H AS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 6S, 4H, JD, QS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, 8H, KC, 6H, AS])
    KH 7C TC 6S TD JC 5C 7D AH 3S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TC, TD], non_ranked_cards=[KH, 7C, 6S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JC, 5C, 7D, AH, 3S])
    3H 4C 4H TC TH 6S 7H 6D 9C QH
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[4C, 4H, TC, TH], non_ranked_cards=[3H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6S, 6D], non_ranked_cards=[7H, 9C, QH])
    7D 5H 4S 8C JS 4D 3D 8S QH KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 5H, 4S, 8C, JS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, 3D, 8S, QH, KC])
    3H 6S AD 7H 3S QC 8S 4S 7S JS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[3H, 3S], non_ranked_cards=[6S, AD, 7H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 8S, 4S, 7S, JS])
    3S JD KH TH 6H QS 9C 6C 2D QD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, JD, KH, TH, 6H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QS, QD], non_ranked_cards=[9C, 6C, 2D])
    4S QH 4D 5H KC 7D 6D 8D TH 5S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4S, 4D], non_ranked_cards=[QH, 5H, KC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 6D, 8D, TH, 5S])
    TD AD 6S 7H KD KH 9H 5S KC JC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, AD, 6S, 7H, KD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KH, KC], non_ranked_cards=[9H, 5S, JC])
    3H QC AS TS 4S QD KS 9C 7S KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, QC, AS, TS, 4S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KS, KC], non_ranked_cards=[QD, 9C, 7S])
    TS 6S QC 6C TH TC 9D 5C 5D KD
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[TS, 6S, 6C, TH], non_ranked_cards=[QC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5C, 5D], non_ranked_cards=[TC, 9D, KD])
    JS 3S 4H KD 4C QD 6D 9S JC 9D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[4H, 4C], non_ranked_cards=[JS, 3S, KD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9S, 9D], non_ranked_cards=[QD, 6D, JC])
    8S JS 6D 4H JH 6H 6S 6C KS KH
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[JS, JH], non_ranked_cards=[8S, 6D, 4H]) ; P2 Hand: FullHouse(rank=7, ranked_cards=[6H, 6S, 6C, KS, KH], non_ranked_cards=[])
    AC 7D 5D TC 9S KH 6S QD 6H AS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 7D, 5D, TC, 9S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6S, 6H], non_ranked_cards=[KH, QD, AS])
    AS 7H 6D QH 8D TH 2S KH 5C 5H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, 7H, 6D, QH, 8D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5C, 5H], non_ranked_cards=[TH, 2S, KH])
    4C 7C 3D QC TC 4S KH 8C 2D JS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 7C, 3D, QC, TC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4S, KH, 8C, 2D, JS])
    6H 5D 7S 5H 9C 9H JH 8S TH 7H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[5D, 5H], non_ranked_cards=[6H, 7S, 9C]) ; P2 Hand: Straight(rank=5, ranked_cards=[9H, JH, 8S, TH, 7H], non_ranked_cards=[])
    AS JS 2S QD KH 8H 4S AC 8D 8S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, JS, 2S, QD, KH]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[8H, 8D, 8S], non_ranked_cards=[4S, AC])
    3H 4C TD KD 8C JC 5C QS 2D JD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, 4C, TD, KD, 8C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JC, JD], non_ranked_cards=[5C, QS, 2D])
    TS 7D 5D 6C 2C QS 2H 3C AH KS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, 7D, 5D, 6C, 2C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 2H, 3C, AH, KS])
    4S 7C 9C 7D JH 6C 5C 8H 9D QD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7C, 7D], non_ranked_cards=[4S, 9C, JH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, 5C, 8H, 9D, QD])
    2S TD 7S 6D 9C 9S QS KH QH 5C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, TD, 7S, 6D, 9C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QS, QH], non_ranked_cards=[9S, KH, 5C])
    JC 6S 9C QH JH 8D 7S JS KH 2H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JC, JH], non_ranked_cards=[6S, 9C, QH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, 7S, JS, KH, 2H])
    8D 5H TH KC 4D 4S 3S 6S 3D QS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, 5H, TH, KC, 4D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3S, 3D], non_ranked_cards=[4S, 6S, QS])
    2D JD 4C TD 7C 6D TH 7S JC AH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, JD, 4C, TD, 7C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, TH, 7S, JC, AH])
    QS 7S 4C TH 9D TS AD 4D 3H 6H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 7S, 4C, TH, 9D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, AD, 4D, 3H, 6H])
    2D 3H 7D JD 3D AS 2S 9C QC 8S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[3H, 3D], non_ranked_cards=[2D, 7D, JD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, 2S, 9C, QC, 8S])
    4H 9H 9C 2C 7S JH KD 5C 5D 6H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9H, 9C], non_ranked_cards=[4H, 2C, 7S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5C, 5D], non_ranked_cards=[JH, KD, 6H])
    TC 9H 8H JC 3C 9S 8D KS AD KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, 9H, 8H, JC, 3C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KS, KC], non_ranked_cards=[9S, 8D, AD])
    TS 5H JD QS QH QC 8D 5D KH AH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QS, QH], non_ranked_cards=[TS, 5H, JD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 8D, 5D, KH, AH])
    5D AS 8S 6S 4C AH QC QD TH 7H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5D, AS, 8S, 6S, 4C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QC, QD], non_ranked_cards=[AH, TH, 7H])
    3H 4H 7D 6S 4S 9H AS 8H JS 9D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[4H, 4S], non_ranked_cards=[3H, 7D, 6S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9H, 9D], non_ranked_cards=[AS, 8H, JS])
    JD 8C 2C 9D 7D 5H 5S 9S JC KD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, 8C, 2C, 9D, 7D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5H, 5S], non_ranked_cards=[9S, JC, KD])
    KD 9C 4S QD AH 7C AD 9D AC TD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, 9C, 4S, QD, AH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AD, AC], non_ranked_cards=[7C, 9D, TD])
    6S 4H 4S 9C 8D KS TC 9D JH 7C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4H, 4S], non_ranked_cards=[6S, 9C, 8D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, TC, 9D, JH, 7C])
    5S JC 5H 4S QH AC 2C JS 2S 9S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5S, 5H], non_ranked_cards=[JC, 4S, QH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2C, 2S], non_ranked_cards=[AC, JS, 9S])
    8C 5H AS QD AD 5C 7D 8S QC TD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AS, AD], non_ranked_cards=[8C, 5H, QD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5C, 7D, 8S, QC, TD])
    JC 4C 8D 5C KH QS 4D 6H 2H 2C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JC, 4C, 8D, 5C, KH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2H, 2C], non_ranked_cards=[QS, 4D, 6H])
    TH 4S 2D KC 3H QD AC 7H AD 9D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, 4S, 2D, KC, 3H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AC, AD], non_ranked_cards=[QD, 7H, 9D])
    KH QD AS 8H TH KC 8D 7S QH 8C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, QD, AS, 8H, TH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8D, 8C], non_ranked_cards=[KC, 7S, QH])
    JC 6C 7D 8C KH AD QS 2H 6S 2D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JC, 6C, 7D, 8C, KH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2H, 2D], non_ranked_cards=[AD, QS, 6S])
    JC KH 2D 7D JS QC 5H 4C 5D AD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JC, JS], non_ranked_cards=[KH, 2D, 7D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5H, 5D], non_ranked_cards=[QC, 4C, AD])
    TS 3S AD 4S TD 2D TH 6S 9H JH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TS, TD], non_ranked_cards=[3S, AD, 4S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, TH, 6S, 9H, JH])
    9H 2D QS 2C 4S 3D KH AS AC 9D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2D, 2C], non_ranked_cards=[9H, QS, 4S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AS, AC], non_ranked_cards=[3D, KH, 9D])
    KH 6S 8H 4S KD 7D 9D TS QD QC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KH, KD], non_ranked_cards=[6S, 8H, 4S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QD, QC], non_ranked_cards=[7D, 9D, TS])
    JH 5H AH KS AS AD JC QC 5S KH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AH, AS], non_ranked_cards=[JH, 5H, KS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, JC, QC, 5S, KH])
    5D 7D 6D KS KD 3D 7C 4D JD 3S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KS, KD], non_ranked_cards=[5D, 7D, 6D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3D, 3S], non_ranked_cards=[7C, 4D, JD])
    AC JS 8D 5H 9C 3H 4H 4D TS 2C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, JS, 8D, 5H, 9C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4H, 4D], non_ranked_cards=[3H, TS, 2C])
    6H KS KH 9D 7C 2S 6S 8S 2H 3D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KS, KH], non_ranked_cards=[6H, 9D, 7C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2S, 2H], non_ranked_cards=[6S, 8S, 3D])
    6H AC JS 7S 3S TD 8H 3H 4H TH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, AC, JS, 7S, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TD, TH], non_ranked_cards=[8H, 3H, 4H])
    9H TC QC KC 5C KS 6H 4H AC 8S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, TC, QC, KC, 5C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 6H, 4H, AC, 8S])
    TC 7D QH 4S JC TS 6D 6C AC KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, 7D, QH, 4S, JC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6D, 6C], non_ranked_cards=[TS, AC, KH])
    QH 7D 7C JH QS QD TH 3H 5D KS
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[QH, 7D, 7C, QS], non_ranked_cards=[JH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QD, TH, 3H, 5D, KS])
    3D 5S 8D JS 4C 2C KS 7H 9C 4H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, 5S, 8D, JS, 4C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, KS, 7H, 9C, 4H])
    5H 8S 4H TD 2C 3S QD QC 3H KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, 8S, 4H, TD, 2C]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[3S, QD, QC, 3H], non_ranked_cards=[KC])
    QC JS KD 9C AD 5S 9D 7D 7H TS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, JS, KD, 9C, AD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7D, 7H], non_ranked_cards=[5S, 9D, TS])
    8C JC KH 7C 7S 6C TS 2C QD TH
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[7C, 7S], non_ranked_cards=[8C, JC, KH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TS, TH], non_ranked_cards=[6C, 2C, QD])
    5S 9D TH 3C 7S QH 8S 9C 2H 5H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 9D, TH, 3C, 7S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, 8S, 9C, 2H, 5H])
    5D 9H 6H 2S JS KH 3H 7C 2H 5S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5D, 9H, 6H, 2S, JS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, 3H, 7C, 2H, 5S])
    JD 5D 5S 2C TC 2S 6S 6C 3C 8S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[5D, 5S], non_ranked_cards=[JD, 2C, TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6S, 6C], non_ranked_cards=[2S, 3C, 8S])
    4D KH 8H 4H 2D KS 3H 5C 2S 9H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4D, 4H], non_ranked_cards=[KH, 8H, 2D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 3H, 5C, 2S, 9H])
    3S 2D TD 7H 8S 6H JD KC 9C 8D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, 2D, TD, 7H, 8S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, JD, KC, 9C, 8D])
    6S QD JH 7C 9H 5H 8S 8H TH TD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, QD, JH, 7C, 9H]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[8S, 8H, TH, TD], non_ranked_cards=[5H])
    QS 7S TD 7D TS JC KD 7C 3C 2C
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[7S, TD, 7D, TS], non_ranked_cards=[QS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JC, KD, 7C, 3C, 2C])
    3C JD 8S 4H 2D 2S TD AS 4D AC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, JD, 8S, 4H, 2D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AS, AC], non_ranked_cards=[2S, TD, 4D])
    AH KS 6C 4C 4S 7D 8C 9H 6H AS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4C, 4S], non_ranked_cards=[AH, KS, 6C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 8C, 9H, 6H, AS])
    5S 3C 9S 2C QS KD 4D 4S AC 5D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 3C, 9S, 2C, QS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4D, 4S], non_ranked_cards=[KD, AC, 5D])
    2D TS 2C JS KH QH 5D 8C AS KC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2D, 2C], non_ranked_cards=[TS, JS, KH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, 5D, 8C, AS, KC])
    KD 3H 6C TH 8S 7S KH 6H 9S AC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, 3H, 6C, TH, 8S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7S, KH, 6H, 9S, AC])
    6H 7S 6C QS AH 2S 2H 4H 5D 5H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[6H, 6C], non_ranked_cards=[7S, QS, AH]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[2S, 2H, 5D, 5H], non_ranked_cards=[4H])
    5H JC QD 2C 2S JD AS QC 6S 7D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2C, 2S], non_ranked_cards=[5H, JC, QD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, AS, QC, 6S, 7D])
    6C TC AS KD 8H 9D 2C 7D JH 9S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, TC, AS, KD, 8H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9D, 9S], non_ranked_cards=[2C, 7D, JH])
    2H 4C 6C AH 8S TD 3H TH 7C TS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, 4C, 6C, AH, 8S]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[TD, TH, TS], non_ranked_cards=[3H, 7C])
    KD 4S TS 6C QH 8D 9D 9C AH 7D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, 4S, TS, 6C, QH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9D, 9C], non_ranked_cards=[8D, AH, 7D])
    6D JS 5C QD QC 9C 5D 8C 2H KD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QD, QC], non_ranked_cards=[6D, JS, 5C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, 5D, 8C, 2H, KD])
    3C QH JH AD 6S AH KC 8S 6D 6H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, QH, JH, AD, 6S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6D, 6H], non_ranked_cards=[AH, KC, 8S])
    3D 7C 4C 7S 5S 3S 6S 5H JC 3C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7C, 7S], non_ranked_cards=[3D, 4C, 5S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3S, 3C], non_ranked_cards=[6S, 5H, JC])
    QH 7C 5H 3C 3S 8C TS 4C KD 9C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[3C, 3S], non_ranked_cards=[QH, 7C, 5H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, TS, 4C, KD, 9C])
    QD 3S 7S 5H 7H QH JC 7C 8C KD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7S, 7H], non_ranked_cards=[QD, 3S, 5H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, JC, 7C, 8C, KD])
    3C KD KH 2S 4C TS AC 6S 2C 7C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KD, KH], non_ranked_cards=[3C, 2S, 4C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, AC, 6S, 2C, 7C])
    2C KH 3C 4C 6H 4D 5H 5S 7S QD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, KH, 3C, 4C, 6H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5H, 5S], non_ranked_cards=[4D, 7S, QD])
    4D 7C 8S QD TS 9D KS 6H KD 3C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, 7C, 8S, QD, TS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KS, KD], non_ranked_cards=[9D, 6H, 3C])
    QS 4D TS 7S 4C 3H QD 8D 9S TC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4D, 4C], non_ranked_cards=[QS, TS, 7S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, QD, 8D, 9S, TC])
    TS QH AC 6S 3C 9H 9D QS 8S 6H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, QH, AC, 6S, 3C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9H, 9D], non_ranked_cards=[QS, 8S, 6H])
    3S 7S 5D 4S JS 2D 6C QH 6S TH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, 7S, 5D, 4S, JS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6C, 6S], non_ranked_cards=[2D, QH, TH])
    4C 4H AS JS 5D 3D TS 9C AC 8S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4C, 4H], non_ranked_cards=[AS, JS, 5D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, TS, 9C, AC, 8S])
    6S 9C 7C 3S 5C QS AD AS 6H 3C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, 9C, 7C, 3S, 5C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AD, AS], non_ranked_cards=[QS, 6H, 3C])
    9S 8C 7H 3H 6S 7C AS 9H JD KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9S, 8C, 7H, 3H, 6S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, AS, 9H, JD, KH])
    3D 3H 7S 4D 6C 7C AC 2H 9C TH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[3D, 3H], non_ranked_cards=[7S, 4D, 6C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, AC, 2H, 9C, TH])
    4H 5S 3H AC TC TH 9C 9H 9S 8D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, 5S, 3H, AC, TC]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[9C, 9H, 9S], non_ranked_cards=[TH, 8D])
    8D 9H 5H 4D 6C 2H QD 6S 5D 3S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, 9H, 5H, 4D, 6C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, QD, 6S, 5D, 3S])
    4C 5C JD QS 4D 3H TH AC QH 8C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4C, 4D], non_ranked_cards=[5C, JD, QS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, TH, AC, QH, 8C])
    QC 5S 3C 7H AD 4C KS 4H JD 6D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 5S, 3C, 7H, AD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4C, 4H], non_ranked_cards=[KS, JD, 6D])
    QS AH 3H KS 9H 2S JS JH 5H 2H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, AH, 3H, KS, 9H]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[2S, JS, JH, 2H], non_ranked_cards=[5H])
    2H 5S TH 6S TS 3S KS 3C 5H JS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TH, TS], non_ranked_cards=[2H, 5S, 6S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3S, 3C], non_ranked_cards=[KS, 5H, JS])
    2D 9S 7H 3D KC JH 6D 7D JS TD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, 9S, 7H, 3D, KC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JH, JS], non_ranked_cards=[6D, 7D, TD])
    AC JS 8H 2C 8C JH JC 2D TH 7S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[8H, 8C], non_ranked_cards=[AC, JS, 2C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JH, JC], non_ranked_cards=[2D, TH, 7S])
    5D 9S 8H 2H 3D TC AH JC KD 9C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5D, 9S, 8H, 2H, 3D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, AH, JC, KD, 9C])
    9D QD JC 2H 6D KH TS 9S QH TH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9D, QD, JC, 2H, 6D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TS, TH], non_ranked_cards=[KH, 9S, QH])
    2C 8D 4S JD 5H 3H TH TC 9C KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, 8D, 4S, JD, 5H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TH, TC], non_ranked_cards=[3H, 9C, KC])
    AS 3D 9H 7D 4D TH KH 2H 7S 3H
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, 3D, 9H, 7D, 4D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, KH, 2H, 7S, 3H])
    4H 7S KS 2S JS TS 8S 2H QD 8D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, 7S, KS, 2S, JS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8S, 8D], non_ranked_cards=[TS, 2H, QD])
    5S 6H JH KS 8H 2S QC AC 6S 3S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 6H, JH, KS, 8H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, QC, AC, 6S, 3S])
    JC AS AD QS 8H 6C KH 4C 4D QD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AS, AD], non_ranked_cards=[JC, QS, 8H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4C, 4D], non_ranked_cards=[6C, KH, QD])
    2S 3D TS TD 9S KS 6S QS 5C 8D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TS, TD], non_ranked_cards=[2S, 3D, 9S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 6S, QS, 5C, 8D])
    3C 6D 4S QC KC JH QD TH KH AD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 6D, 4S, QC, KC]) ; P2 Hand: Straight(rank=5, ranked_cards=[JH, QD, TH, KH, AD], non_ranked_cards=[])
    9H AH 4D KS 2S 8D JH JC 7C QS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, AH, 4D, KS, 2S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JH, JC], non_ranked_cards=[8D, 7C, QS])
    2D 6C TH 3C 8H QD QH 2S 3S KS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, 6C, TH, 3C, 8H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QD, QH], non_ranked_cards=[2S, 3S, KS])
    6H 5D 9S 4C TS TD JS QD 9D JD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, 5D, 9S, 4C, TS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JS, JD], non_ranked_cards=[TD, QD, 9D])
    5H 8H KH 8S KS 7C TD AD 4S KD
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[8H, KH, 8S, KS], non_ranked_cards=[5H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, TD, AD, 4S, KD])
    2C 7C JC 5S AS 6C 7D 8S 5H 9C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, 7C, JC, 5S, AS]) ; P2 Hand: Straight(rank=5, ranked_cards=[6C, 7D, 8S, 5H, 9C], non_ranked_cards=[])
    6S QD 9S TS KH QS 5S QH 3C KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, QD, 9S, TS, KH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QS, QH], non_ranked_cards=[5S, 3C, KC])
    7D 3H 3C KD 5C AS JH 7H 6H JD
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3H, 3C], non_ranked_cards=[7D, KD, 5C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JH, JD], non_ranked_cards=[AS, 7H, 6H])
    9D 5C 9H KC 8H KS 4S AD 4D 2S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9D, 9H], non_ranked_cards=[5C, KC, 8H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4S, 4D], non_ranked_cards=[KS, AD, 2S])
    3S JD QD 8D 2S 7C 5S 6S 5H TS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, JD, QD, 8D, 2S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5S, 5H], non_ranked_cards=[7C, 6S, TS])
    6D 9S KC TD 3S 6H QD JD 5C 8D
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, 9S, KC, TD, 3S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, QD, JD, 5C, 8D])
    5H 9D TS KD 8D 6H TD QC 4C 7D
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, 9D, TS, KD, 8D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, TD, QC, 4C, 7D])
    6D 4S JD 9D AH 9S AS TD 9H QD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, 4S, JD, 9D, AH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9S, 9H], non_ranked_cards=[AS, TD, QD])
    2D 5S 2H 9C 6H 9S TD QC 7D TC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2D, 2H], non_ranked_cards=[5S, 9C, 6H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TD, TC], non_ranked_cards=[9S, QC, 7D])
    3S 2H KS TS 2C 9C 8S JS 9D 7D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2H, 2C], non_ranked_cards=[3S, KS, TS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9C, 9D], non_ranked_cards=[8S, JS, 7D])
    3C KC 6D 5D 6C 6H 8S AS 7S QS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[6D, 6C], non_ranked_cards=[3C, KC, 5D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, 8S, AS, 7S, QS])
    JH 9S 2H 8D 4C 8H 9H AD TH KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, 9S, 2H, 8D, 4C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8H, 9H, AD, TH, KH])
    QC AS 2S JS 5C 6H KD 3H 7H 2C
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, AS, 2S, JS, 5C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, KD, 3H, 7H, 2C])
    QD 8H 2S 8D 3S 6D AH 2C TC 5C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[8H, 8D], non_ranked_cards=[QD, 2S, 3S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, AH, 2C, TC, 5C])
    JD JS TS 8S 3H 5D TD KC JC 6H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JD, JS], non_ranked_cards=[TS, 8S, 3H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5D, TD, KC, JC, 6H])
    6S QS TC 3H 5D AH JC 7C 7D 4H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, QS, TC, 3H, 5D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7C, 7D], non_ranked_cards=[AH, JC, 4H])
    7C 5D 8H 9C 2H 9H JH KH 5S 2C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 5D, 8H, 9C, 2H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, JH, KH, 5S, 2C])
    9C 7H 6S TH 3S QC QD 4C AC JD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, 7H, 6S, TH, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QC, QD], non_ranked_cards=[4C, AC, JD])
    2H 5D 9S 7D KC 3S QS 2D AS KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, 5D, 9S, 7D, KC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, QS, 2D, AS, KH])
    2S 4S 2H 7D 5C TD TH QH 9S 4D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2S, 2H], non_ranked_cards=[4S, 7D, 5C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TD, TH], non_ranked_cards=[QH, 9S, 4D])
    6D 3S TS 6H 4H KS 9D 8H 5S 2D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[6D, 6H], non_ranked_cards=[3S, TS, 4H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 9D, 8H, 5S, 2D])
    9H KS 4H 3S 5C 5D KH 6H 6S JS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, KS, 4H, 3S, 5C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6H, 6S], non_ranked_cards=[5D, KH, JS])
    KC AS 8C 4C JC KH QC TH QD AH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, AS, 8C, 4C, JC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QC, QD], non_ranked_cards=[KH, TH, AH])
    6S KH 9S 2C 5H TC 3C 7H JC 4D
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, KH, 9S, 2C, 5H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, 3C, 7H, JC, 4D])
    JD 4S 6S 5S 8D 7H 7S 4D 4C 2H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, 4S, 6S, 5S, 8D]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[7H, 7S, 4D, 4C], non_ranked_cards=[2H])
    7H 9H 5D KH 9C 7C TS TC 7S 5H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[9H, 9C], non_ranked_cards=[7H, 5D, KH]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[7C, TS, TC, 7S], non_ranked_cards=[5H])
    4C 8D QC TS 4S 9H 3D AD JS 7C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4C, 4S], non_ranked_cards=[8D, QC, TS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, 3D, AD, JS, 7C])
    8C QS 5C 5D 3H JS AH KC 4S 9D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5C, 5D], non_ranked_cards=[8C, QS, 3H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, AH, KC, 4S, 9D])
    TS JD 8S QS TH JH KH 2D QD JS
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[TS, TH], non_ranked_cards=[JD, 8S, QS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JH, JS], non_ranked_cards=[KH, 2D, QD])
    JD QC 5D 6S 9H 3S 2C 8H 9S TS
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, QC, 5D, 6S, 9H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, 2C, 8H, 9S, TS])
    2S 4C AD 7H JC 5C 2D 6D 4H 3D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, 4C, AD, 7H, JC]) ; P2 Hand: Straight(rank=5, ranked_cards=[5C, 2D, 6D, 4H, 3D], non_ranked_cards=[])
    7S JS 2C 4H 8C AD QD 9C 3S TD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7S, JS, 2C, 4H, 8C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, QD, 9C, 3S, TD])
    JD TS 4C 6H 9H 7D QD 6D 3C AS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, TS, 4C, 6H, 9H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, QD, 6D, 3C, AS])
    AS 7C 4C 6S 5D 5S 5C JS QC 4S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, 7C, 4C, 6S, 5D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5S, 5C], non_ranked_cards=[JS, QC, 4S])
    KD 6S 9S 7C 3C 5S 7D JH QD JS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, 6S, 9S, 7C, 3C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JH, JS], non_ranked_cards=[5S, 7D, QD])
    4S 7S JH 2C 8S 5D 7H 3D QH AD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4S, 7S, JH, 2C, 8S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5D, 7H, 3D, QH, AD])
    TD 6H 2H 8D 4H 2D 7C AD KH 5D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 6H, 2H, 8D, 4H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, 7C, AD, KH, 5D])
    TS 3S 5H 2C QD AH 2S 5C KH TD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, 3S, 5H, 2C, QD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AH, 2S, 5C, KH, TD])
    KC 4D 8C 5D AS 6C 2H 2S 9H 7C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, 4D, 8C, 5D, AS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2H, 2S], non_ranked_cards=[6C, 9H, 7C])
    KD JS QC TS QS KH JH 2C 5D AD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QC, QS], non_ranked_cards=[KD, JS, TS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, JH, 2C, 5D, AD])
    3S 5H KC 6C 9H 3H 2H AD 7D 7S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, 5H, KC, 6C, 9H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7D, 7S], non_ranked_cards=[3H, 2H, AD])
    7S JS JH KD 8S 7D 2S 9H 7C 2H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[JS, JH], non_ranked_cards=[7S, KD, 8S]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[7D, 2S, 7C, 2H], non_ranked_cards=[9H])
    9H 2D 8D QC 6S AD AS 8H 5H 6C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, 2D, 8D, QC, 6S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AD, AS], non_ranked_cards=[8H, 5H, 6C])
    2S 7H 6C 6D 7D 8C 5D 9D JC 3C
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[7H, 6C, 6D, 7D], non_ranked_cards=[2S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, 5D, 9D, JC, 3C])
    7C 9C 7H JD 2H KD 3S KH AD 4S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[7C, 7H], non_ranked_cards=[9C, JD, 2H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KD, KH], non_ranked_cards=[3S, AD, 4S])
    QH AS 9H 4D JD KS KD TS KH 5H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, AS, 9H, 4D, JD]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[KS, KD, KH], non_ranked_cards=[TS, 5H])
    4C 8H 5S 3S 3D 7D TD AD 7S KC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3S, 3D], non_ranked_cards=[4C, 8H, 5S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7D, 7S], non_ranked_cards=[TD, AD, KC])
    JS 8S 5S JC 8H TH 9C 4D 5D KC
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[JS, 8S, JC, 8H], non_ranked_cards=[5S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, 9C, 4D, 5D, KC])
    7C 5S 9C QD 2C QH JS 5H 8D KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 5S, 9C, QD, 2C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, JS, 5H, 8D, KH])
    TD 2S KS 3D AD KC 7S TC 3C 5D
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 2S, KS, 3D, AD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, 7S, TC, 3C, 5D])
    4C 2S AD QS 6C 9S QD TH QH 5C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 2S, AD, QS, 6C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QD, QH], non_ranked_cards=[9S, TH, 5C])
    8C AD QS 2D 2S KC JD KS 6C JC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2D, 2S], non_ranked_cards=[8C, AD, QS]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[KC, JD, KS, JC], non_ranked_cards=[6C])
    8D 4D JS 2H 5D QD 7S 7D QH TS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, 4D, JS, 2H, 5D]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[QD, 7S, 7D, QH], non_ranked_cards=[TS])
    6S 7H 3S 8C 8S 9D QS 8H 6C 9S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[8C, 8S], non_ranked_cards=[6S, 7H, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9D, 9S], non_ranked_cards=[QS, 8H, 6C])
    4S TC 2S 5C QD 4D QS 6D TH 6S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4S, TC, 2S, 5C, QD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6D, 6S], non_ranked_cards=[4D, QS, TH])
    3S 5C 9D 6H 8D 4C 7D TC 7C TD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, 5C, 9D, 6H, 8D]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[7D, TC, 7C, TD], non_ranked_cards=[4C])
    AH 6S AS 7H 5S KD 3H 5H AC 4C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AH, AS], non_ranked_cards=[6S, 7H, 5S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, 3H, 5H, AC, 4C])
    8D 8S AH KS QS 2C AD 6H 7D 5D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[8D, 8S], non_ranked_cards=[AH, KS, QS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, AD, 6H, 7D, 5D])
    6H 9H 9S 2H QS 8S 9C 5D 2D KD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9H, 9S], non_ranked_cards=[6H, 2H, QS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, 9C, 5D, 2D, KD])
    TS QC 5S JH 7D 7S TH 9S 9H AC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, QC, 5S, JH, 7D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9S, 9H], non_ranked_cards=[7S, TH, AC])
    7H 3H 6S KC 4D 6D 5C 4S QD TS
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, 3H, 6S, KC, 4D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, 5C, 4S, QD, TS])
    TD 2S 7C QD 3H JH 9D 4H 7S 7H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 2S, 7C, QD, 3H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7S, 7H], non_ranked_cards=[JH, 9D, 4H])
    KS 3D 4H 5H TC 2S AS 2D 6D 7D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 3D, 4H, 5H, TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2S, 2D], non_ranked_cards=[AS, 6D, 7D])
    8H 3C 7H TD 3H AD KC TH 9C KH
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3C, 3H], non_ranked_cards=[8H, 7H, TD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KC, KH], non_ranked_cards=[AD, TH, 9C])
    TC 4C 2C 9S 9D 9C 5C 2H JD 3C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9S, 9D], non_ranked_cards=[TC, 4C, 2C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, 5C, 2H, JD, 3C])
    3H AC TS 5D AD 8D 6H QC 6S 8C
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[AC, AD], non_ranked_cards=[3H, TS, 5D]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[8D, 6H, 6S, 8C], non_ranked_cards=[QC])
    2S TS 3S JD 7H 8S QH 4C 5S 8D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, TS, 3S, JD, 7H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8S, 8D], non_ranked_cards=[QH, 4C, 5S])
    AC 4S 6C 3C KH 3D 7C 2D 8S 2H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 4S, 6C, 3C, KH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2D, 2H], non_ranked_cards=[3D, 7C, 8S])
    4H 6C 8S TH 2H 4S 8H 9S 3H 7S
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, 6C, 8S, TH, 2H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4S, 8H, 9S, 3H, 7S])
    7C 4C 9C 2C 5C AS 5D KD 4D QH
     - P1 wins - P1 Hand: Flush(rank=6, ranked_cards=[7C, 4C, 9C, 2C, 5C], non_ranked_cards=[]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, 5D, KD, 4D, QH])
    9H 4H TS AS 7D 8D 5D 9S 8C 2H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, 4H, TS, AS, 7D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8D, 8C], non_ranked_cards=[5D, 9S, 2H])
    QC KD AC AD 2H 7S AS 3S 2D 9S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AC, AD], non_ranked_cards=[QC, KD, 2H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7S, AS, 3S, 2D, 9S])
    2H QC 8H TC 6D QD QS 5D KH 3C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, QC, 8H, TC, 6D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QD, QS], non_ranked_cards=[5D, KH, 3C])
    TH JD QS 4C 2S 5S AD 7H 3S AS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, JD, QS, 4C, 2S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AD, AS], non_ranked_cards=[5S, 7H, 3S])
    7H JS 3D 6C 3S 6D AS 9S AC QS
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3D, 3S], non_ranked_cards=[7H, JS, 6C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AS, AC], non_ranked_cards=[6D, 9S, QS])
    9C TS AS 8C TC 8S 6H 9D 8D 6C
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[TS, TC], non_ranked_cards=[9C, AS, 8C]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[8S, 6H, 8D, 6C], non_ranked_cards=[9D])
    4D JD 9C KC 7C 6D KS 3S 8C AS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, JD, 9C, KC, 7C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, KS, 3S, 8C, AS])
    3H 6S TC 8D TS 3S KC 9S 7C AS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TC, TS], non_ranked_cards=[3H, 6S, 8D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, KC, 9S, 7C, AS])
    8C QC 4H 4S 8S 6C 3S TC AH AC
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[8C, 4H, 4S, 8S], non_ranked_cards=[QC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AH, AC], non_ranked_cards=[6C, 3S, TC])
    4D 7D 5C AS 2H 6S TS QC AD TC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, 7D, 5C, AS, 2H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TS, TC], non_ranked_cards=[6S, QC, AD])
    QD QC 8S 4S TH 3D AH TS JH 4H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QD, QC], non_ranked_cards=[8S, 4S, TH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, AH, TS, JH, 4H])
    5C 2D 9S 2C 3H 3C 9D QD QH 7D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2D, 2C], non_ranked_cards=[5C, 9S, 3H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QD, QH], non_ranked_cards=[3C, 9D, 7D])
    KC 9H 6C KD 7S 3C 4D AS TC 2D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KC, KD], non_ranked_cards=[9H, 6C, 7S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 4D, AS, TC, 2D])
    3D JS 4D 9D KS 7D TH QC 3H 3C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, JS, 4D, 9D, KS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3H, 3C], non_ranked_cards=[7D, TH, QC])
    8D 5S 2H 9D 3H 8C 4C 4H 3C TH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, 5S, 2H, 9D, 3H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4C, 4H], non_ranked_cards=[8C, 3C, TH])
    JC TH 4S 6S JD 2D 4D 6C 3D 4C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JC, JD], non_ranked_cards=[TH, 4S, 6S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4D, 4C], non_ranked_cards=[2D, 6C, 3D])
    TS 3S 2D 4H AC 2C 6S 2H JH 6H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, 3S, 2D, 4H, AC]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[2C, 6S, 2H, 6H], non_ranked_cards=[JH])
    TD 8S AD TC AH AC JH 9S 6S 7S
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[TD, AD, TC, AH], non_ranked_cards=[8S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, JH, 9S, 6S, 7S])
    6C KC 4S JD 8D 9H 5S 7H QH AH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, KC, 4S, JD, 8D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, 5S, 7H, QH, AH])
    KD 8D TS JH 5C 5H 3H AD AS JS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, 8D, TS, JH, 5C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AD, AS], non_ranked_cards=[5H, 3H, JS])
    2D 4H 3D 6C 8C 7S AD 5D 5C 8S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, 4H, 3D, 6C, 8C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5D, 5C], non_ranked_cards=[7S, AD, 8S])
    TD 5D 7S 9C 4S 5H 6C 8C 4C 8S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 5D, 7S, 9C, 4S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8C, 8S], non_ranked_cards=[5H, 6C, 4C])
    JS QH 9C AS 5C QS JC 3D QC 7C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, QH, 9C, AS, 5C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QS, QC], non_ranked_cards=[JC, 3D, 7C])
    JC 9C KH JH QS QC 2C TS 3D AD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JC, JH], non_ranked_cards=[9C, KH, QS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 2C, TS, 3D, AD])
    5D JH AC 5C 9S TS 4C JD 8C KS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5D, 5C], non_ranked_cards=[JH, AC, 9S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, 4C, JD, 8C, KS])
    KC AS 2D KH 9H 2C 5S 4D 3D 6H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[KC, KH], non_ranked_cards=[AS, 2D, 9H]) ; P2 Hand: Straight(rank=5, ranked_cards=[2C, 5S, 4D, 3D, 6H], non_ranked_cards=[])
    TH AH 2D 8S JC 3D 8C QH 7S 3S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, AH, 2D, 8S, JC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3D, 3S], non_ranked_cards=[8C, QH, 7S])
    8H QD 4H JC AS KH KS 3C 9S 6D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8H, QD, 4H, JC, AS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KH, KS], non_ranked_cards=[3C, 9S, 6D])
    9S QH 7D 9C 4S AC 7H KH 4D KD
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[9S, 9C], non_ranked_cards=[QH, 7D, 4S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KH, KD], non_ranked_cards=[AC, 7H, 4D])
    AH AD TH 6D 9C 9S KD KS QH 4H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AH, AD], non_ranked_cards=[TH, 6D, 9C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KD, KS], non_ranked_cards=[9S, QH, 4H])
    QD 6H 9C 7C QS 6D 6S 9D 5S JH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QD, QS], non_ranked_cards=[6H, 9C, 7C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6D, 6S], non_ranked_cards=[9D, 5S, JH])
    AH 8D 5H QD 2H JC KS 4H KH 5S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AH, 8D, 5H, QD, 2H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KS, KH], non_ranked_cards=[JC, 4H, 5S])
    5C 2S JS 8D 9C 8C 3D AS KC AH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5C, 2S, JS, 8D, 9C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AS, AH], non_ranked_cards=[8C, 3D, KC])
    JD 9S 2H QS 8H 5S 8C TH 5C 4C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, 9S, 2H, QS, 8H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5S, 5C], non_ranked_cards=[8C, TH, 4C])
    QC QS 8C 2S 2C 3S 9C 4C KS KH
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[QC, QS, 2S, 2C], non_ranked_cards=[8C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KS, KH], non_ranked_cards=[3S, 9C, 4C])
    2D 5D 8S AH AD TD 2C JS KS 8C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AH, AD], non_ranked_cards=[2D, 5D, 8S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 2C, JS, KS, 8C])
    TC 5S 5H 8H QC 9H 6H JD 4H 9S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[5S, 5H], non_ranked_cards=[TC, 8H, QC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9H, 9S], non_ranked_cards=[6H, JD, 4H])
    3C JH 4H 9H AH 4S 2H 4C 8D AC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, JH, 4H, 9H, AH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4S, 4C], non_ranked_cards=[2H, 8D, AC])
    8S TH 4D 7D 6D QD QS 7S TC 7C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, TH, 4D, 7D, 6D]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[QD, QS, 7S, 7C], non_ranked_cards=[TC])
    KH 6D 2D JD 5H JS QD JH 4H 4S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, 6D, 2D, JD, 5H]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[JS, JH, 4H, 4S], non_ranked_cards=[QD])
    9C 7S JH 4S 3S TS QC 8C TC 4H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, 7S, JH, 4S, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TS, TC], non_ranked_cards=[QC, 8C, 4H])
    QH 9D 4D JH QS 3S 2C 7C 6C 2D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QH, QS], non_ranked_cards=[9D, 4D, JH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2C, 2D], non_ranked_cards=[3S, 7C, 6C])
    4H 9S JD 5C 5H AH 9D TS 2D 4C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5C, 5H], non_ranked_cards=[4H, 9S, JD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AH, 9D, TS, 2D, 4C])
    KS JH TS 5D 2D AH JS 7H AS 8D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, JH, TS, 5D, 2D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AH, AS], non_ranked_cards=[JS, 7H, 8D])
    JS AH 8C AD KS 5S 8H 2C 6C TH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AH, AD], non_ranked_cards=[JS, 8C, KS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 8H, 2C, 6C, TH])
    2H 5D AD AC KS 3D 8H TS 6H QC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AD, AC], non_ranked_cards=[2H, 5D, KS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, 8H, TS, 6H, QC])
    6D 4H TS 9C 5H JS JH 6S JD 4C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, 4H, TS, 9C, 5H]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[JS, JH, JD], non_ranked_cards=[6S, 4C])
    JH QH 4H 2C 6D 3C 5D 4C QS KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, QH, 4H, 2C, 6D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 5D, 4C, QS, KC])
    6H 4H 6C 7H 6S 2S 8S KH QC 8C
     - P1 wins - P1 Hand: ThreeOfAKind(rank=4, ranked_cards=[6H, 6C, 6S], non_ranked_cards=[4H, 7H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8S, 8C], non_ranked_cards=[2S, KH, QC])
    3H 3D 5D KS 4H TD AD 3S 4D TS
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3H, 3D], non_ranked_cards=[5D, KS, 4H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TD, TS], non_ranked_cards=[AD, 3S, 4D])
    5S 7C 8S 7D 2C KS 7S 6C 8C JS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7C, 7D], non_ranked_cards=[5S, 8S, 2C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 7S, 6C, 8C, JS])
    5D 2H 3S 7C 5C QD 5H 6D 9C 9H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[5D, 5C], non_ranked_cards=[2H, 3S, 7C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9C, 9H], non_ranked_cards=[QD, 5H, 6D])
    JS 2S KD 9S 8D TD TS AC 8C 9D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, 2S, KD, 9S, 8D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TD, TS], non_ranked_cards=[AC, 8C, 9D])
    5H QD 2S AC 8C 9H KS 7C 4S 3C
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, QD, 2S, AC, 8C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, KS, 7C, 4S, 3C])
    KH AS 3H 8S 9C JS QS 4S AD 4D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, AS, 3H, 8S, 9C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4S, 4D], non_ranked_cards=[JS, QS, AD])
    AS 2S TD AD 4D 9H JC 4C 5H QS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AS, AD], non_ranked_cards=[2S, TD, 4D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, JC, 4C, 5H, QS])
    5D 7C 4H TC 2D 6C JS 4S KC 3S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5D, 7C, 4H, TC, 2D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, JS, 4S, KC, 3S])
    4C 2C 5D AC 9H 3D JD 8S QS QH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 2C, 5D, AC, 9H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QS, QH], non_ranked_cards=[3D, JD, 8S])
    2C 8S 6H 3C QH 6D TC KD AC AH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, 8S, 6H, 3C, QH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AC, AH], non_ranked_cards=[6D, TC, KD])
    QC 6C 3S QS 4S AC 8D 5C AD KH
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[QC, QS], non_ranked_cards=[6C, 3S, 4S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AC, AD], non_ranked_cards=[8D, 5C, KH])
    5S 4C AC KH AS QC 2C 5C 8D 9C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AC, AS], non_ranked_cards=[5S, 4C, KH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 2C, 5C, 8D, 9C])
    8H JD 3C KH 8D 5C 9C QD QH 9D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[8H, 8D], non_ranked_cards=[JD, 3C, KH]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[9C, QD, QH, 9D], non_ranked_cards=[5C])
    7H TS 2C 8C 4S TD JC 9C 5H QH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, TS, 2C, 8C, 4S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, JC, 9C, 5H, QH])
    JS 4S 2C 7C TH 6C AS KS 7S JD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, 4S, 2C, 7C, TH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, AS, KS, 7S, JD])
    JH 7C 9H 7H TC 5H 3D 6D 5D 4D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7C, 7H], non_ranked_cards=[JH, 9H, TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5H, 5D], non_ranked_cards=[3D, 6D, 4D])
    2C QD JH 2H 9D 5S 3D TD AD KS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2C, 2H], non_ranked_cards=[QD, JH, 9D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 3D, TD, AD, KS])
    JD QH 3S 4D TH 7D 6S QS KS 4H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, QH, 3S, 4D, TH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 6S, QS, KS, 4H])
    TC KS 5S 8D 8H AD 2S 2D 4C JH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[8D, 8H], non_ranked_cards=[TC, KS, 5S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2S, 2D], non_ranked_cards=[AD, 4C, JH])
    5S JH TC 3S 2D QS 9D 4C KD 9S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, JH, TC, 3S, 2D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9D, 9S], non_ranked_cards=[QS, 4C, KD])
    AC KH 3H AS 9D KC 9H QD 6C 6S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AC, AS], non_ranked_cards=[KH, 3H, 9D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6C, 6S], non_ranked_cards=[KC, 9H, QD])
    9H 7S 3D 5C 7D KC TD 8H 4H 6S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7S, 7D], non_ranked_cards=[9H, 3D, 5C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, TD, 8H, 4H, 6S])
    3C 7H 8H TC QD 4D 7S 6S QH 6C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 7H, 8H, TC, QD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6S, 6C], non_ranked_cards=[4D, 7S, QH])
    6D AD 4C QD 6C 5D 7D 9D KS TS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[6D, 6C], non_ranked_cards=[AD, 4C, QD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5D, 7D, 9D, KS, TS])
    JH 2H JD 9S 7S TS KH 8D 5D 8H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JH, JD], non_ranked_cards=[2H, 9S, 7S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8D, 8H], non_ranked_cards=[TS, KH, 5D])
    2D 9S 4C 7D 9D 5H QD 6D AC 6S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9S, 9D], non_ranked_cards=[2D, 4C, 7D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6D, 6S], non_ranked_cards=[5H, QD, AC])
    7S 6D JC QD JH 4C 6S QS 2H 7D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JC, JH], non_ranked_cards=[7S, 6D, QD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 6S, QS, 2H, 7D])
    8C TD JH KD 2H 5C QS 2C JS 7S
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, TD, JH, KD, 2H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5C, QS, 2C, JS, 7S])
    TC 5H 4H JH QD 3S 5S 5D 8S KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, 5H, 4H, JH, QD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5S, 5D], non_ranked_cards=[3S, 8S, KH])
    KS KH 7C 2C 5D JH 6S 9C 6D JC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[KS, KH], non_ranked_cards=[7C, 2C, 5D]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[JH, 6S, 6D, JC], non_ranked_cards=[9C])
    5H AH JD 9C JS KC 2H 6H 4D 5S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JD, JS], non_ranked_cards=[5H, AH, 9C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, 2H, 6H, 4D, 5S])
    AS 3C TH QC 6H 9C 8S 8C TD 7C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, 3C, TH, QC, 6H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8S, 8C], non_ranked_cards=[9C, TD, 7C])
    KC 2C QD 9C KH 4D 7S 3C TS 9H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KC, KH], non_ranked_cards=[2C, QD, 9C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, 7S, 3C, TS, 9H])
    9C QC 2S TS 8C TD 9S QD 3S 3C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, QC, 2S, TS, 8C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3S, 3C], non_ranked_cards=[TD, 9S, QD])
    4D 9D TH JH AH 6S 2S JD QH JS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, 9D, TH, JH, AH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JD, JS], non_ranked_cards=[6S, 2S, QH])
    QD 9H 6C KD 7D 7H 5D 6S 8H AH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QD, 9H, 6C, KD, 7D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, 5D, 6S, 8H, AH])
    8H 3C 4S 2H 5H QS QH 7S 4H AC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8H, 3C, 4S, 2H, 5H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QS, QH], non_ranked_cards=[7S, 4H, AC])
    QS 3C 7S 9S 4H 3S AH KS 9D 7C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 3C, 7S, 9S, 4H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, AH, KS, 9D, 7C])
    AD 5S 6S 2H 2D 5H TC 4S 3C 8C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2H, 2D], non_ranked_cards=[AD, 5S, 6S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, TC, 4S, 3C, 8C])
    QH TS 6S 4D JS KS JH AS 8S 6D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, TS, 6S, 4D, JS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, JH, AS, 8S, 6D])
    2C 8S 2S TD 5H AS TC TS 6C KC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2C, 2S], non_ranked_cards=[8S, TD, 5H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TC, TS], non_ranked_cards=[AS, 6C, KC])
    KC TS 8H 2H 3H 7C 4C 5S TH TD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, TS, 8H, 2H, 3H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TH, TD], non_ranked_cards=[7C, 4C, 5S])
    KD AD KH 7H 7S 5D 5H 5S 2D 9C
     - P1 does not win - P1 Hand: TwoPairs(rank=3, ranked_cards=[KD, KH, 7H, 7S], non_ranked_cards=[AD]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[5D, 5H, 5S], non_ranked_cards=[2D, 9C])
    AD 9S 3D 7S 8C QC 7C 9C KD KS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, 9S, 3D, 7S, 8C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KD, KS], non_ranked_cards=[QC, 7C, 9C])
    3C QC 9S 8C 4D 5C AS QD 6C 2C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, QC, 9S, 8C, 4D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5C, AS, QD, 6C, 2C])
    2H KC 8S JD 7S AC 8D 5C 2S 4D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, KC, 8S, JD, 7S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 8D, 5C, 2S, 4D])
    9D QH 3D 2S TC 3S KS 3C 9H TD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9D, QH, 3D, 2S, TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3S, 3C], non_ranked_cards=[KS, 9H, TD])
    KD 6S AC 2C 7H 5H 3S 6C 6H 8C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, 6S, AC, 2C, 7H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6C, 6H], non_ranked_cards=[5H, 3S, 8C])
    QH TC 8S 6S KH TH 4H 5D TS 4D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, TC, 8S, 6S, KH]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[TH, 4H, TS, 4D], non_ranked_cards=[5D])
    8C JS 4H 6H 2C 2H 7D AC QD 3D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, JS, 4H, 6H, 2C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, 7D, AC, QD, 3D])
    QS KC 6S 2D 5S 4H TD 3H JH 4C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, KC, 6S, 2D, 5S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4H, 4C], non_ranked_cards=[TD, 3H, JH])
    7S 5H 7H 8H KH 6H QS TH KD 7D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7S, 7H], non_ranked_cards=[5H, 8H, KH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, QS, TH, KD, 7D])
    5H AD KD 7C KH 5S TD 6D 3C 6C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KD, KH], non_ranked_cards=[5H, AD, 7C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6D, 6C], non_ranked_cards=[5S, TD, 3C])
    8C 9C 5H JD 7C KC KH 7H 2H 3S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, 9C, 5H, JD, 7C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KC, KH], non_ranked_cards=[7H, 2H, 3S])
    7S 4H AD 4D 8S QS TH 3D 7H 5S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4H, 4D], non_ranked_cards=[7S, AD, 8S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, TH, 3D, 7H, 5S])
    8D TC KS KD 9S 6D AD JD 5C 2S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KS, KD], non_ranked_cards=[8D, TC, 9S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, AD, JD, 5C, 2S])
    7H 8H 6C QD 2H 6H 9D TC 9S 7C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, 8H, 6C, QD, 2H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9D, 9S], non_ranked_cards=[6H, TC, 7C])
    8D 6D 4C 7C 6C 3C TH KH JS JH
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[6D, 6C], non_ranked_cards=[8D, 4C, 7C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JS, JH], non_ranked_cards=[3C, TH, KH])
    5S 3S 8S JS 9H AS AD 8H 7S KD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 3S, 8S, JS, 9H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AS, AD], non_ranked_cards=[8H, 7S, KD])
    JH 7C 2C KC 5H AS AD 9C 9S JS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, 7C, 2C, KC, 5H]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[AS, AD, 9C, 9S], non_ranked_cards=[JS])
    AD AC 2C 6S QD 7C 3H TH KS KD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AD, AC], non_ranked_cards=[2C, 6S, QD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KS, KD], non_ranked_cards=[7C, 3H, TH])
    9D JD 4H 8H 4C KH 7S TS 8C KC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[4H, 4C], non_ranked_cards=[9D, JD, 8H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KH, KC], non_ranked_cards=[7S, TS, 8C])
    3S 5S 2H 7S 6H 7D KS 5C 6D AD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, 5S, 2H, 7S, 6H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, KS, 5C, 6D, AD])
    5S 8C 9H QS 7H 7S 2H 6C 7D TD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 8C, 9H, QS, 7H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7S, 7D], non_ranked_cards=[2H, 6C, TD])
    QS 5S TD AC 9D KC 3D TC 2D 4D
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 5S, TD, AC, 9D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, 3D, TC, 2D, 4D])
    TD 2H 7D JD QD 4C 7H 5D KC 3D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 2H, 7D, JD, QD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 7H, 5D, KC, 3D])
    4C 3H 8S KD QH 5S QC 9H TC 5H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 3H, 8S, KD, QH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5S, 5H], non_ranked_cards=[QC, 9H, TC])
    9C QD TH 5H TS 5C 9H AH QH 2C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TH, TS], non_ranked_cards=[9C, QD, 5H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5C, 9H, AH, QH, 2C])
    4D 6S 3C AC 6C 3D 2C 2H TD TH
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[6S, 6C], non_ranked_cards=[4D, 3C, AC]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[2C, 2H, TD, TH], non_ranked_cards=[3D])
    AC 9C 5D QC 4D AD 8D 6D 8C KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 9C, 5D, QC, 4D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8D, 8C], non_ranked_cards=[AD, 6D, KC])
    AD 3C 4H AC 8D 8H 7S 9S TD JC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[AD, AC], non_ranked_cards=[3C, 4H, 8D]) ; P2 Hand: Straight(rank=5, ranked_cards=[8H, 7S, 9S, TD, JC], non_ranked_cards=[])
    4H 9H QH JS 2D TH TD TC KD KS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, 9H, QH, JS, 2D]) ; P2 Hand: FullHouse(rank=7, ranked_cards=[TH, TD, TC, KD, KS], non_ranked_cards=[])
    5S 6S 9S 8D TH AS KH 5H 5C 8S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 6S, 9S, 8D, TH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5H, 5C], non_ranked_cards=[AS, KH, 8S])
    JD 2S 9S 6S 5S 8S 5D 7S 7H 9D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, 2S, 9S, 6S, 5S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7S, 7H], non_ranked_cards=[8S, 5D, 9D])
    5D 8C 4C 9D AD TS 2C 7D KD TC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5D, 8C, 4C, 9D, AD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TS, TC], non_ranked_cards=[2C, 7D, KD])
    8S QS 4D KC 5C 8D 4S KH JD KD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, QS, 4D, KC, 5C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KH, KD], non_ranked_cards=[8D, 4S, JD])
    AS 5C AD QH 7D 2H 9S 7H 7C TC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AS, AD], non_ranked_cards=[5C, QH, 7D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7H, 7C], non_ranked_cards=[2H, 9S, TC])
    2S 8S JD KH 7S 6C 6D AD 5D QC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, 8S, JD, KH, 7S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6C, 6D], non_ranked_cards=[AD, 5D, QC])
    9H 6H 3S 8C 8H AH TC 4H JS TD
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[8C, 8H], non_ranked_cards=[9H, 6H, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TC, TD], non_ranked_cards=[AH, 4H, JS])
    2C TS 4D 7H 2D QC 9C 5D TH 7C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2C, 2D], non_ranked_cards=[TS, 4D, 7H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 9C, 5D, TH, 7C])
    6C 8H QC 5D TS JH 5C 5H 9H 4S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, 8H, QC, 5D, TS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5C, 5H], non_ranked_cards=[JH, 9H, 4S])
    2D QC 7H AS JS 8S 2H 4C 4H 8D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, QC, 7H, AS, JS]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[8S, 4C, 4H, 8D], non_ranked_cards=[2H])
    JS 6S AC KD 3D 3C 4S 7H TH KC
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, 6S, AC, KD, 3D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 4S, 7H, TH, KC])
    QH KH 6S QS 5S 4H 3C QD 3S 3H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[QH, QS], non_ranked_cards=[KH, 6S, 5S]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[3C, 3S, 3H], non_ranked_cards=[4H, QD])
    7H AS KH 8C 4H 9C 5S 3D 6S TS
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, AS, KH, 8C, 4H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, 5S, 3D, 6S, TS])
    9C 7C 3H 5S QD 2C 3D AD AC 5H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, 7C, 3H, 5S, QD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AD, AC], non_ranked_cards=[2C, 3D, 5H])
    JH TD 2D 4C TS 3H KH AD 3S 7S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TD, TS], non_ranked_cards=[JH, 2D, 4C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3H, 3S], non_ranked_cards=[KH, AD, 7S])
    AS 4C 5H 4D 6S KD JC 3C 6H 2D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4C, 4D], non_ranked_cards=[AS, 5H, 6S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, JC, 3C, 6H, 2D])
    3H 6S 8C 2D TH 4S AH QH AD 5H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, 6S, 8C, 2D, TH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AH, AD], non_ranked_cards=[4S, QH, 5H])
    7C 2S 9H 7H KC 5C 6D 5S 3H JC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7C, 7H], non_ranked_cards=[2S, 9H, KC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5C, 5S], non_ranked_cards=[6D, 3H, JC])
    3C TC 9C 4H QD TD JH 6D 9H 5S
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, TC, 9C, 4H, QD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, JH, 6D, 9H, 5S])
    7C 6S 5C 5D 6C 4S 7H 9H 6H AH
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[6S, 5C, 5D, 6C], non_ranked_cards=[7C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4S, 7H, 9H, 6H, AH])
    AD 2H 7D KC 2C 4C 2S 9S 7H 3S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2H, 2C], non_ranked_cards=[AD, 7D, KC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 2S, 9S, 7H, 3S])
    TH 4C 8S 6S 3S AD KS AS JH TD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, 4C, 8S, 6S, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AD, AS], non_ranked_cards=[KS, JH, TD])
    5C TD 4S 4D AD 6S 5D TC 9C 7D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4S, 4D], non_ranked_cards=[5C, TD, AD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, 5D, TC, 9C, 7D])
    8H 3S 4D 4S 5S 6H 5C AC 3H 3D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4D, 4S], non_ranked_cards=[8H, 3S, 5S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3H, 3D], non_ranked_cards=[6H, 5C, AC])
    9H 3C AC 4S QS 8S 9D QH 5H 4D
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, 3C, AC, 4S, QS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, 9D, QH, 5H, 4D])
    JC 6C 5H TS AC 9C JD 8C 7C QD
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JC, 6C, 5H, TS, AC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, JD, 8C, 7C, QD])
    8S 8H 9C JD 2D QC QH 6H 3C 8D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[8S, 8H], non_ranked_cards=[9C, JD, 2D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QC, QH], non_ranked_cards=[6H, 3C, 8D])
    KS JS 2H 6H 5H QH QS 3H 7C 6D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, JS, 2H, 6H, 5H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QH, QS], non_ranked_cards=[3H, 7C, 6D])
    TC 3H 4S 7H QC 2H 3S 8C JS KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, 3H, 4S, 7H, QC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, 3S, 8C, JS, KH])
    AH 8H 5S 4C 9H JD 3H 7S JC AC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AH, 8H, 5S, 4C, 9H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JD, JC], non_ranked_cards=[3H, 7S, AC])
    3C 2D 4C 5S 6C 4S QS 3S JD 3D
     - P1 wins - P1 Hand: Straight(rank=5, ranked_cards=[3C, 2D, 4C, 5S, 6C], non_ranked_cards=[]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3S, 3D], non_ranked_cards=[4S, QS, JD])
    5H 2D TC AH KS 6D 7H AD 8C 6H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, 2D, TC, AH, KS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6D, 6H], non_ranked_cards=[7H, AD, 8C])
    6C 7S 3C JD 7C 8H KS KH AH 6D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[7S, 7C], non_ranked_cards=[6C, 3C, JD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KS, KH], non_ranked_cards=[8H, AH, 6D])
    AH 7D 3H 8H 8S 7H QS 5H 9D 2D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[8H, 8S], non_ranked_cards=[AH, 7D, 3H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, QS, 5H, 9D, 2D])
    JD AC 4H 7S 8S 9S KS AS 9D QH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, AC, 4H, 7S, 8S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9S, 9D], non_ranked_cards=[KS, AS, QH])
    7S 2C 8S 5S JH QS JC AH KD 4C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7S, 2C, 8S, 5S, JH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, JC, AH, KD, 4C])
    AH 2S 9H 4H 8D TS TD 6H QH JD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AH, 2S, 9H, 4H, 8D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TS, TD], non_ranked_cards=[6H, QH, JD])
    4H JC 3H QS 6D 7S 9C 8S 9D 8D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, JC, 3H, QS, 6D]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[9C, 8S, 9D, 8D], non_ranked_cards=[7S])
    5H TD 4S 9S 4C 8C 8D 7H 3H 3D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[4S, 4C], non_ranked_cards=[5H, TD, 9S]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[8C, 8D, 3H, 3D], non_ranked_cards=[7H])
    QS KH 3S 2C 2S 3C 7S TD 4S QD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2C, 2S], non_ranked_cards=[QS, KH, 3S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 7S, TD, 4S, QD])
    7C TD 4D 5S KH AC AS 7H 4C 6C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, TD, 4D, 5S, KH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AC, AS], non_ranked_cards=[7H, 4C, 6C])
    2S 5H 6D JD 9H QS 8S 2C 2H TD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, 5H, 6D, JD, 9H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2C, 2H], non_ranked_cards=[QS, 8S, TD])
    2S TS 6H 9H 7S 4H JC 4C 5D 5S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, TS, 6H, 9H, 7S]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[4H, 4C, 5D, 5S], non_ranked_cards=[JC])
    2C 5H 7D 4H 3S QH JC JS 6D 8H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, 5H, 7D, 4H, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JC, JS], non_ranked_cards=[QH, 6D, 8H])
    4C QH 7C QD 3S AD TH 8S 5S TS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QH, QD], non_ranked_cards=[4C, 7C, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TH, TS], non_ranked_cards=[AD, 8S, 5S])
    9H TC 2S TD JC 7D 3S 3D TH QH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TC, TD], non_ranked_cards=[9H, 2S, JC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3S, 3D], non_ranked_cards=[7D, TH, QH])
    7D 4C 8S 5C JH 8H 6S 3S KC 3H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 4C, 8S, 5C, JH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3S, 3H], non_ranked_cards=[8H, 6S, KC])
    JC 3H KH TC QH TH 6H 2C AC 5H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JC, 3H, KH, TC, QH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, 6H, 2C, AC, 5H])
    QS 2H 9D 2C AS 6S 6C 2S 8C 8S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2H, 2C], non_ranked_cards=[QS, 9D, AS]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[6S, 6C, 8C, 8S], non_ranked_cards=[2S])
    9H 7D QC TH 4H KD QS AC 7S 3C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, 7D, QC, TH, 4H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, QS, AC, 7S, 3C])
    4D JH 6S 5S 8H KS 9S QC 3S AS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, JH, 6S, 5S, 8H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 9S, QC, 3S, AS])
    JD 2D 6S 7S TC 9H KC 3H 7D KD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, 2D, 6S, 7S, TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KC, KD], non_ranked_cards=[9H, 3H, 7D])
    2H KH 7C 4D 4S 3H JS QD 7D KC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4D, 4S], non_ranked_cards=[2H, KH, 7C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, JS, QD, 7D, KC])
    4C JC AS 9D 3C JS 6C 8H QD 4D
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, JC, AS, 9D, 3C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, 6C, 8H, QD, 4D])
    AH JS 3S 6C 4C 3D JH 6D 9C 9H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AH, JS, 3S, 6C, 4C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9C, 9H], non_ranked_cards=[3D, JH, 6D])
    9H 2D 8C 7H 5S KS 6H 9C 2S TC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, 2D, 8C, 7H, 5S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 6H, 9C, 2S, TC])
    6C 8C AD 7H 6H 3D KH AS 5D TH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[6C, 6H], non_ranked_cards=[8C, AD, 7H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, KH, AS, 5D, TH])
    KS 8C 3S TS 8S 4D 5S 9S 6C 4H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[8C, 8S], non_ranked_cards=[KS, 3S, TS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4D, 4H], non_ranked_cards=[5S, 9S, 6C])
    9H 4S 4H 5C 7D KC 2D 2H 9D JH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4S, 4H], non_ranked_cards=[9H, 5C, 7D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2D, 2H], non_ranked_cards=[KC, 9D, JH])
    5C JS TC 9D 9H 5H 7S KH JC 6S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9D, 9H], non_ranked_cards=[5C, JS, TC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, 7S, KH, JC, 6S])
    7C 9H 8H 4D JC KH JD 2H TD TC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 9H, 8H, 4D, JC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TD, TC], non_ranked_cards=[KH, JD, 2H])
    8H 6C 2H 2C KH 6H 9D QS QH 5H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2H, 2C], non_ranked_cards=[8H, 6C, KH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QS, QH], non_ranked_cards=[6H, 9D, 5H])
    AC 7D 2S 3D QD JC 2D 8D JD JH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 7D, 2S, 3D, QD]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[JC, JD, JH], non_ranked_cards=[2D, 8D])
    2H JC 2D 7H 2C 3C 8D KD TD 4H
     - P1 wins - P1 Hand: ThreeOfAKind(rank=4, ranked_cards=[2H, 2D, 2C], non_ranked_cards=[JC, 7H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 8D, KD, TD, 4H])
    3S 4H 6D 8D TS 3H TD 3D 6H TH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, 4H, 6D, 8D, TS]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[3H, TD, 3D, TH], non_ranked_cards=[6H])
    JH JC 3S AC QH 9H 7H 8S QC 2C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JH, JC], non_ranked_cards=[3S, AC, QH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, 7H, 8S, QC, 2C])
    7H TD QS 4S 8S 9C 2S 5D 4D 2H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, TD, QS, 4S, 8S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2S, 2H], non_ranked_cards=[9C, 5D, 4D])
    3D TS 3H 2S QC 8H 6H KC JC KS
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3D, 3H], non_ranked_cards=[TS, 2S, QC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KC, KS], non_ranked_cards=[8H, 6H, JC])
    5D JD 7D TC 8C 6C 9S 3D 8D AC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5D, JD, 7D, TC, 8C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, 9S, 3D, 8D, AC])
    8H 6H JH 6C 5D 8D 8S 4H AD 2C
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[6H, 6C], non_ranked_cards=[8H, JH, 5D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8D, 8S], non_ranked_cards=[4H, AD, 2C])
    9D 4H 2D 2C 3S TS AS TC 3C 5D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2D, 2C], non_ranked_cards=[9D, 4H, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TS, TC], non_ranked_cards=[AS, 3C, 5D])
    4D TH 5H KS QS 6C 4S 2H 3D AD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, TH, 5H, KS, QS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, 4S, 2H, 3D, AD])
    5C KC 6H 2C 5S 3C 4D 2D 9H 9S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[5C, 5S], non_ranked_cards=[KC, 6H, 2C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9H, 9S], non_ranked_cards=[3C, 4D, 2D])
    JD 4C 3H TH QH 9H 5S AH 8S AC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, 4C, 3H, TH, QH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AH, AC], non_ranked_cards=[9H, 5S, 8S])
    7D 9S 6S 2H TD 9C 4H 8H QS 4C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 9S, 6S, 2H, TD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4H, 4C], non_ranked_cards=[9C, 8H, QS])
    3C 6H 5D 4H 8C 9C KC 6S QD QS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 6H, 5D, 4H, 8C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QD, QS], non_ranked_cards=[9C, KC, 6S])
    3S 9H KD TC 2D JS 8C 6S 4H 4S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, 9H, KD, TC, 2D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4H, 4S], non_ranked_cards=[JS, 8C, 6S])
    2S 4C 8S QS 6H KH 3H TH 8C 5D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, 4C, 8S, QS, 6H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, 3H, TH, 8C, 5D])
    2C KH 5S 3S 7S 7H 6C 9D QD 8D
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, KH, 5S, 3S, 7S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, 6C, 9D, QD, 8D])
    8H KS AC 2D KH TS 6C JS KC 7H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KS, KH], non_ranked_cards=[8H, AC, 2D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, 6C, JS, KC, 7H])
    9C KS 5C TD QC AH 6C 5H 9S 7C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, KS, 5C, TD, QC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AH, 6C, 5H, 9S, 7C])
    5D 4D 3H 4H 6S 7C 7S AH QD TD
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[4D, 4H], non_ranked_cards=[5D, 3H, 6S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7C, 7S], non_ranked_cards=[AH, QD, TD])
    2H 7D QC 6S TC TS AH 7S 9D 3H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, 7D, QC, 6S, TC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, AH, 7S, 9D, 3H])
    TH 5H QD 9S KS 7S 7C 6H 8C TD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, 5H, QD, 9S, KS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7S, 7C], non_ranked_cards=[6H, 8C, TD])
    TH 2D 4D QC 5C 7D JD AH 9C 4H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, 2D, 4D, QC, 5C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, JD, AH, 9C, 4H])
    4H 3H AH 8D 6H QC QH 9H 2H 2C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, 3H, AH, 8D, 6H]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[QC, QH, 2H, 2C], non_ranked_cards=[9H])
    2D AD 4C TS 6H 7S TH 4H QS TD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, AD, 4C, TS, 6H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TH, TD], non_ranked_cards=[7S, 4H, QS])
    3C KD 2H 3H QS JD TC QC 5D 8H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[3C, 3H], non_ranked_cards=[KD, 2H, QS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, TC, QC, 5D, 8H])
    KS JC QD TH 9S KD 8D 8C 2D 9C
     - P1 wins - P1 Hand: Straight(rank=5, ranked_cards=[KS, JC, QD, TH, 9S], non_ranked_cards=[]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8D, 8C], non_ranked_cards=[KD, 2D, 9C])
    3C QD KD 6D 4D 8D AH AD QC 8S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, QD, KD, 6D, 4D]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[8D, AH, AD, 8S], non_ranked_cards=[QC])
    8H 3S 9D 2S 3H KS 6H 4C 7C KC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3S, 3H], non_ranked_cards=[8H, 9D, 2S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KS, KC], non_ranked_cards=[6H, 4C, 7C])
    TH 9S 5C 3D 7D 6H AC 7S 4D 2C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, 9S, 5C, 3D, 7D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, AC, 7S, 4D, 2C])
    5C 3D JD 4D 2D 6D 5H 9H 4C KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5C, 3D, JD, 4D, 2D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, 5H, 9H, 4C, KH])
    AS 7H TD 6C 2H 3D QD KS 4C 4S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, 7H, TD, 6C, 2H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4C, 4S], non_ranked_cards=[3D, QD, KS])
    JC 3C AC 7C JD JS 8H 9S QC 5D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JC, JD], non_ranked_cards=[3C, AC, 7C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, 8H, 9S, QC, 5D])
    JD 6S 5S 2H AS 8C 7D 5H JH 3D
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, 6S, 5S, 2H, AS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, 7D, 5H, JH, 3D])
    8D TC 5S 9S 8S 3H JC 5H 7S AS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[8D, 8S], non_ranked_cards=[TC, 5S, 9S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, JC, 5H, 7S, AS])
    5C TD 3D 7D 4H 8D 7H 4D 5D JS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5C, TD, 3D, 7D, 4H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, 7H, 4D, 5D, JS])
    QS 9C KS TD 2S 8S 5C 2H 4H AS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 9C, KS, TD, 2S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, 5C, 2H, 4H, AS])
    TH 7S 4H 7D 3H JD KD 5D 2S KC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[7S, 7D], non_ranked_cards=[TH, 4H, 3H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KD, KC], non_ranked_cards=[JD, 5D, 2S])
    JD 7H 4S 8H 4C JS 6H QH 5S 4H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4S, 4C], non_ranked_cards=[JD, 7H, 8H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, 6H, QH, 5S, 4H])
    2C QS 8C 5S 3H QC 2S 6C QD AD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, QS, 8C, 5S, 3H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QC, QD], non_ranked_cards=[2S, 6C, AD])
    8C 3D JD TC 4H 2H AD 5S AC 2S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, 3D, JD, TC, 4H]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[2H, AD, AC, 2S], non_ranked_cards=[5S])
    5D 2C JS 2D AD 9D 3D 4C 4S JH
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2C, 2D], non_ranked_cards=[5D, JS, AD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4C, 4S], non_ranked_cards=[9D, 3D, JH])
    8D 5H 5D 6H 7S 4D KS 9D TD JD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5H, 5D], non_ranked_cards=[8D, 6H, 7S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, KS, 9D, TD, JD])
    3D 6D 9C 2S AS 7D 5S 5C 8H JD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, 6D, 9C, 2S, AS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5S, 5C], non_ranked_cards=[7D, 8H, JD])
    7C 8S 3S 6S 5H JD TC AD 7H 7S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 8S, 3S, 6S, 5H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7H, 7S], non_ranked_cards=[JD, TC, AD])
    2S 9D TS 4D AC 8D 6C QD JD 3H
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, 9D, TS, 4D, AC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, 6C, QD, JD, 3H])
    9S KH 2C 3C AC 3D 5H 6H 8D 5D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9S, KH, 2C, 3C, AC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5H, 5D], non_ranked_cards=[3D, 6H, 8D])
    KS 3D 2D 6S AS 4C 2S 7C 7H KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 3D, 2D, 6S, AS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7C, 7H], non_ranked_cards=[4C, 2S, KH])
    AC 2H 3S JC 5C QH 4D 2D 5H 7S
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 2H, 3S, JC, 5C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, 4D, 2D, 5H, 7S])
    TS AS JD 8C 6H JC 8S 5S 2C 5D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, AS, JD, 8C, 6H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5S, 5D], non_ranked_cards=[JC, 8S, 2C])
    7S QH 7H 6C QC 8H 2D 7C JD 2S
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[7S, QH, 7H, QC], non_ranked_cards=[6C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2D, 2S], non_ranked_cards=[8H, 7C, JD])
    2C QD 2S 2H JC 9C 5D 2D JD JH
     - P1 wins - P1 Hand: ThreeOfAKind(rank=4, ranked_cards=[2C, 2S, 2H], non_ranked_cards=[QD, JC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JD, JH], non_ranked_cards=[9C, 5D, 2D])
    7C 5C 9C 8S 7D 6D 8D 6C 9S JH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7C, 7D], non_ranked_cards=[5C, 9C, 8S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6D, 6C], non_ranked_cards=[8D, 9S, JH])
    2C AD 6S 5H 3S KS 7S 9D KH 4C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, AD, 6S, 5H, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KS, KH], non_ranked_cards=[7S, 9D, 4C])
    7H 6C 2C 5C TH 9D 8D 3S QC AH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, 6C, 2C, 5C, TH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9D, 8D, 3S, QC, AH])
    5S KC 6H TC 5H 8S TH 6D 3C AH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5S, 5H], non_ranked_cards=[KC, 6H, TC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, TH, 6D, 3C, AH])
    9C KD 4H AD TD 9S 4S 7D 6H 5D
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, KD, 4H, AD, TD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9S, 4S, 7D, 6H, 5D])
    7H 5C 5H 6D AS 4C KD KH 4H 9D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[5C, 5H], non_ranked_cards=[7H, 6D, AS]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[4C, KD, KH, 4H], non_ranked_cards=[9D])
    3C 2S 5C 6C JD QS 2H 9D 7D 3H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 2S, 5C, 6C, JD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 2H, 9D, 7D, 3H])
    AC 2S 6S 7S JS QD 5C QS 6H AD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 2S, 6S, 7S, JS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QD, QS], non_ranked_cards=[5C, 6H, AD])
    5H TH QC 7H TC 3S 7C 6D KC 3D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TH, TC], non_ranked_cards=[5H, QC, 7H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3S, 3D], non_ranked_cards=[7C, 6D, KC])
    4H 3D QC 9S 8H 2C 3S JC KS 5C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, 3D, QC, 9S, 8H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, 3S, JC, KS, 5C])
    4S 6S 2C 6H 8S 3S 3D 9H 3H JS
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[6S, 6H], non_ranked_cards=[4S, 2C, 8S]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[3S, 3D, 3H], non_ranked_cards=[9H, JS])
    4S 8C 4D 2D 8H 9H 7D 9D AH TS
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[4S, 8C, 4D, 8H], non_ranked_cards=[2D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9H, 9D], non_ranked_cards=[7D, AH, TS])
    9S 2C 9H 4C 8D AS 7D 3D 6D 5S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9S, 9H], non_ranked_cards=[2C, 4C, 8D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, 7D, 3D, 6D, 5S])
    6S 4C 7H 8C 3H 5H JC AH 9D 9C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, 4C, 7H, 8C, 3H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9D, 9C], non_ranked_cards=[5H, JC, AH])
    2S 7C 5S JD 8C 3S 3D 4D 7D 6S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, 7C, 5S, JD, 8C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3S, 3D], non_ranked_cards=[4D, 7D, 6S])
    3C KC 4S 5D 7D 3D JD 7H 3H 4H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, KC, 4S, 5D, 7D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3D, 3H], non_ranked_cards=[JD, 7H, 4H])
    9C 9H 4H 4D TH 6D QD 8S 9S 7S
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[9C, 9H, 4H, 4D], non_ranked_cards=[TH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, QD, 8S, 9S, 7S])
    2H AC 8S 4S AD 8C 2C AH 7D TC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AC, AD], non_ranked_cards=[2H, 8S, 4S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, 2C, AH, 7D, TC])
    TS 9H 3C AD KS TC 3D 8C 8H JD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, 9H, 3C, AD, KS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8C, 8H], non_ranked_cards=[TC, 3D, JD])
    QC 8D 2C 3C 7D 7C JD 9H 9C 6C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 8D, 2C, 3C, 7D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9H, 9C], non_ranked_cards=[7C, JD, 6C])
    AH 6S JS JH 5D AS QC 2C JD TD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JS, JH], non_ranked_cards=[AH, 6S, 5D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, QC, 2C, JD, TD])
    9H KD 2H 5D 2D 3S 7D TC AH TS
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2H, 2D], non_ranked_cards=[9H, KD, 5D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TC, TS], non_ranked_cards=[3S, 7D, AH])
    TD 8H AS 5D AH QC AC 6S TC 5H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AS, AH], non_ranked_cards=[TD, 8H, 5D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, AC, 6S, TC, 5H])
    KS 4S 7H 4D 8D 9C TC 2H 6H 3H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4S, 4D], non_ranked_cards=[KS, 7H, 8D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, TC, 2H, 6H, 3H])
    3H KD 4S QD QH 3D 8H 8C TD 7S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QD, QH], non_ranked_cards=[3H, KD, 4S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8H, 8C], non_ranked_cards=[3D, TD, 7S])
    8S JD TC AH JS QS 2D KH KS 4D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[JD, JS], non_ranked_cards=[8S, TC, AH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KH, KS], non_ranked_cards=[QS, 2D, 4D])
    3C AD JC KD JS KH 4S TH 9H 2C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JC, JS], non_ranked_cards=[3C, AD, KD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, 4S, TH, 9H, 2C])
    QC 5S JS 9S KS AS 7C QD 2S JD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 5S, JS, 9S, KS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, 7C, QD, 2S, JD])
    KC 5S QS 3S 2D AC 5D 9H 8H KS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, 5S, QS, 3S, 2D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 5D, 9H, 8H, KS])
    6H 9C TC AD 2C 6D 5S JD 6C 7C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, 9C, TC, AD, 2C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6D, 6C], non_ranked_cards=[5S, JD, 7C])
    QS KH TD QD 2C 3H 8S 2S QC AH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QS, QD], non_ranked_cards=[KH, TD, 2C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, 8S, 2S, QC, AH])
    9D 9H JH TC QH 3C 2S JS 5C 7H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9D, 9H], non_ranked_cards=[JH, TC, QH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 2S, JS, 5C, 7H])
    6C 3S 3D 2S 4S QD 2D TH 5D 2C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[3S, 3D], non_ranked_cards=[6C, 2S, 4S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2D, 2C], non_ranked_cards=[QD, TH, 5D])
    2D 6H 6D 2S JC QH AS 7H 4H KH
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[2D, 6H, 6D, 2S], non_ranked_cards=[JC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, AS, 7H, 4H, KH])
    5H 6S KS AD TC TS 7C AC 4S 4H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, 6S, KS, AD, TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4S, 4H], non_ranked_cards=[TS, 7C, AC])
    AD 3C 4H QS 8C 9D KS 2H 2D 4D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, 3C, 4H, QS, 8C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2H, 2D], non_ranked_cards=[9D, KS, 4D])
    4S 9D 6C 6D 9C AC 8D 3H 7H KD
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[9D, 6C, 6D, 9C], non_ranked_cards=[4S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 8D, 3H, 7H, KD])
    JC AH 6C TS JD 6D AD 3S 5D QD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JC, JD], non_ranked_cards=[AH, 6C, TS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, AD, 3S, 5D, QD])
    JC JH JD 3S 7S 8S JS QC 3H 4S
     - P1 wins - P1 Hand: ThreeOfAKind(rank=4, ranked_cards=[JC, JH, JD], non_ranked_cards=[3S, 7S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, JS, QC, 3H, 4S])
    JD TH 5C 2C AD JS 7H 9S 2H 7S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, TH, 5C, 2C, AD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7H, 7S], non_ranked_cards=[JS, 9S, 2H])
    8D 3S JH 4D QC AS JD 2C KC 6H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, 3S, JH, 4D, QC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, JD, 2C, KC, 6H])
    2C AC 5H KD 5S 7H QD JH AH 2D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5H, 5S], non_ranked_cards=[2C, AC, KD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, QD, JH, AH, 2D])
    JC QH 8D 8S TC 5H 5C AH 8C 6C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[8D, 8S], non_ranked_cards=[JC, QH, TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5H, 5C], non_ranked_cards=[AH, 8C, 6C])
    3H JS 8S QD JH 3C 4H 6D 5C 3S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JS, JH], non_ranked_cards=[3H, 8S, QD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3C, 3S], non_ranked_cards=[4H, 6D, 5C])
    6D 4S 4C AH 5H 5S 3H JD 7C 8D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4S, 4C], non_ranked_cards=[6D, AH, 5H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 3H, JD, 7C, 8D])
    8H AH 2H 3H JS 3C 7D QC 4H KD
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8H, AH, 2H, 3H, JS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 7D, QC, 4H, KD])
    6S 2H KD 5H 8H 2D 3C 8S 7S QD
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, 2H, KD, 5H, 8H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, 3C, 8S, 7S, QD])
    2S 7S KC QC AH TC QS 6D 4C 8D
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, 7S, KC, QC, AH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, QS, 6D, 4C, 8D])
    5S 9H 2C 3S QD 7S 6C 2H 7C 9D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 9H, 2C, 3S, QD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7S, 7C], non_ranked_cards=[6C, 2H, 9D])
    3C 6C 5C 5S JD JC KS 3S 5D TS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5C, 5S], non_ranked_cards=[3C, 6C, JD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JC, KS, 3S, 5D, TS])
    7C KS 6S 5S 2S 2D TC 2H 5H QS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, KS, 6S, 5S, 2S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2D, 2H], non_ranked_cards=[TC, 5H, QS])
    AS 7H 6S TS 5H 9S 9D 3C KD 2H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, 7H, 6S, TS, 5H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9S, 9D], non_ranked_cards=[3C, KD, 2H])
    4S JS QS 3S 4H 7C 2S AC 6S 9D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4S, 4H], non_ranked_cards=[JS, QS, 3S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 2S, AC, 6S, 9D])
    8C JH 2H 5H 7C 5D QH QS KH QC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, JH, 2H, 5H, 7C]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[QH, QS, QC], non_ranked_cards=[5D, KH])
    3S TD 3H 7C KC 8D 5H 8S KH 8C
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3S, 3H], non_ranked_cards=[TD, 7C, KC]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[8D, 8S, 8C], non_ranked_cards=[5H, KH])
    4H KH JD TS 3C 7H AS QC JS 5S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, KH, JD, TS, 3C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, AS, QC, JS, 5S])
    AH 9D 2C 8D 4D 2D 6H 6C KC 6S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AH, 9D, 2C, 8D, 4D]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[6H, 6C, 6S], non_ranked_cards=[2D, KC])
    2S 6H 9D 3S 7H 4D KH 8H KD 3D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, 6H, 9D, 3S, 7H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KH, KD], non_ranked_cards=[4D, 8H, 3D])
    9C TC AC JH KH 4D JD 5H TD 3S
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, TC, AC, JH, KH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, JD, 5H, TD, 3S])
    7S 4H 9D AS 4C 7D QS 9S 2S KH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4H, 4C], non_ranked_cards=[7S, 9D, AS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, QS, 9S, 2S, KH])
    3S 8D 8S KS 8C JC 5C KH 2H 5D
     - P1 wins - P1 Hand: ThreeOfAKind(rank=4, ranked_cards=[8D, 8S, 8C], non_ranked_cards=[3S, KS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5C, 5D], non_ranked_cards=[JC, KH, 2H])
    8S QH 2C 4D KC JS QC 9D AC 6H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, QH, 2C, 4D, KC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, QC, 9D, AC, 6H])
    8S 8C 7C JS JD 6S 4C 9C AC 4S
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[8S, 8C, JS, JD], non_ranked_cards=[7C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4C, 4S], non_ranked_cards=[6S, 9C, AC])
    QH 5D 2C 7D JC 8S 2D JS JH 4C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, 5D, 2C, 7D, JC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JS, JH], non_ranked_cards=[8S, 2D, 4C])
    JS 4C 7S TS JH KC KH 5H QD 4S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[JS, JH], non_ranked_cards=[4C, 7S, TS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KC, KH], non_ranked_cards=[5H, QD, 4S])
    QD 8C 8D 2D 6S TD 9D AC QH 5S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[8C, 8D], non_ranked_cards=[QD, 2D, 6S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 9D, AC, QH, 5S])
    QH QC JS 3D 3C 5C 4H KH 8S 7H
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[QH, QC, 3D, 3C], non_ranked_cards=[JS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5C, 4H, KH, 8S, 7H])
    7C 2C 5S JC 8S 3H QC 5D 2H KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 2C, 5S, JC, 8S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, QC, 5D, 2H, KC])
    5S 8D KD 6H 4H QD QH 6D AH 3D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 8D, KD, 6H, 4H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QD, QH], non_ranked_cards=[6D, AH, 3D])
    7S KS 6C 2S 4D AC QS 5H TS JD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7S, KS, 6C, 2S, 4D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, QS, 5H, TS, JD])
    7C 2D TC 5D QS AC JS QC 6C KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 2D, TC, 5D, QS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, JS, QC, 6C, KC])
    2C KS 4D 3H TS 8S AD 4H 7S 9S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, KS, 4D, 3H, TS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, AD, 4H, 7S, 9S])
    QD 9H QH 5H 4H 4D KH 3S JC AD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QD, QH], non_ranked_cards=[9H, 5H, 4H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, KH, 3S, JC, AD])
    4D AC KC 8D 6D 4C 2D KH 2C JD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, AC, KC, 8D, 6D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2D, 2C], non_ranked_cards=[4C, KH, JD])
    2C 9H 2D AH 3H 6D 9C 7D TC KS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2C, 2D], non_ranked_cards=[9H, AH, 3H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, 9C, 7D, TC, KS])
    8C 3H KD 7C 5C 2S 4S 5H AS AH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, 3H, KD, 7C, 5C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AS, AH], non_ranked_cards=[2S, 4S, 5H])
    TH JD 4H KD 3H TC 5C 3S AC KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, JD, 4H, KD, 3H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, 5C, 3S, AC, KH])
    6D 7H AH 7S QC 6H 2D TD JD AS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7H, 7S], non_ranked_cards=[6D, AH, QC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, 2D, TD, JD, AS])
    JH 5D 7H TC 9S 7D JC AS 5S KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, 5D, 7H, TC, 9S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, JC, AS, 5S, KH])
    2H 8C AD TH 6H QD KD 9H 6S 6C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, 8C, AD, TH, 6H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6S, 6C], non_ranked_cards=[QD, KD, 9H])
    QH KC 9D 4D 3S JS JH 4H 2C 9H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, KC, 9D, 4D, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JS, JH], non_ranked_cards=[4H, 2C, 9H])
    TC 7H KH 4H JC 7D 9S 3H QS 7S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, 7H, KH, 4H, JC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7D, 7S], non_ranked_cards=[9S, 3H, QS])
    AD 7D JH 6C 7H 4H 3S 3H 4D QH
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[7D, 7H], non_ranked_cards=[AD, JH, 6C]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[4H, 3S, 3H, 4D], non_ranked_cards=[QH])
    JD 2H 5C AS 6C QC 4D 3C TC JH
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, 2H, 5C, AS, 6C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 4D, 3C, TC, JH])
    AC JD 3H 6H 4C JC AD 7D 7H 9H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, JD, 3H, 6H, 4C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7D, 7H], non_ranked_cards=[JC, AD, 9H])
    4H TC TS 2C 8C 6S KS 2H JD 9S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TC, TS], non_ranked_cards=[4H, 2C, 8C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, KS, 2H, JD, 9S])
    4C 3H QS QC 9S 9H 6D KC 9D 9C
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[QS, QC], non_ranked_cards=[4C, 3H, 9S]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[9H, 9D, 9C], non_ranked_cards=[6D, KC])
    5C AD 8C 2C QH TH QD JC 8D 8H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5C, AD, 8C, 2C, QH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8D, 8H], non_ranked_cards=[TH, QD, JC])
    QC 2C 2S QD 9C 4D 3S 8D JH QS
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[QC, 2C, 2S, QD], non_ranked_cards=[9C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, 3S, 8D, JH, QS])
    9D 3S 2C 7S 7C JC TD 3C TC 9H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[7S, 7C], non_ranked_cards=[9D, 3S, 2C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TD, TC], non_ranked_cards=[JC, 3C, 9H])
    3C TS 8H 5C 4C 2C 6S 8D 7C 4H
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, TS, 8H, 5C, 4C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, 6S, 8D, 7C, 4H])
    KS 7H 2H TC 4H 2C 3S AS AH QS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 7H, 2H, TC, 4H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AS, AH], non_ranked_cards=[2C, 3S, QS])
    8C 2D 2H 2C 4S 4C 6S 7D 5S 3S
     - P1 does not win - P1 Hand: ThreeOfAKind(rank=4, ranked_cards=[2D, 2H, 2C], non_ranked_cards=[8C, 4S]) ; P2 Hand: Straight(rank=5, ranked_cards=[4C, 6S, 7D, 5S, 3S], non_ranked_cards=[])
    TH QC 5D TD 3C QS KD KC KS AS
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[TH, TD], non_ranked_cards=[QC, 5D, 3C]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[KD, KC, KS], non_ranked_cards=[QS, AS])
    4D AH KD 9H KS 5C 4C 6H JC 7S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KD, KS], non_ranked_cards=[4D, AH, 9H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5C, 4C, 6H, JC, 7S])
    KC 4H 5C QS TC 2H JC 9S AH QH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, 4H, 5C, QS, TC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, JC, 9S, AH, QH])
    4S 9H 3H 5H 3C QD 2H QC JH 8H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3H, 3C], non_ranked_cards=[4S, 9H, 5H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QD, QC], non_ranked_cards=[2H, JH, 8H])
    5D AS 7H 2C 3D JH 6H 4C 6S 7D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5D, AS, 7H, 2C, 3D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6H, 6S], non_ranked_cards=[JH, 4C, 7D])
    9C JD 9H AH JS 8S QH 3H KS 8H
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[9C, JD, 9H, JS], non_ranked_cards=[AH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8S, 8H], non_ranked_cards=[QH, 3H, KS])
    3S AC QC TS 4D AD 3D AH 8S 9H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, AC, QC, TS, 4D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AD, AH], non_ranked_cards=[3D, 8S, 9H])
    7H 3H QS 9C 9S 5H JH JS AH AC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[9C, 9S], non_ranked_cards=[7H, 3H, QS]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[JH, JS, AH, AC], non_ranked_cards=[5H])
    8D 3C JD 2H AC 9C 7H 5S 4D 8H
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, 3C, JD, 2H, AC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, 7H, 5S, 4D, 8H])
    7C JH 9H 6C JS 9S 7H 8C 9D 4H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JH, JS], non_ranked_cards=[7C, 9H, 6C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9S, 9D], non_ranked_cards=[7H, 8C, 4H])
    2D AS 9S 6H 4D JS JH 9H AD QD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, AS, 9S, 6H, 4D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JS, JH], non_ranked_cards=[9H, AD, QD])
    6H 7S JH KH AH 7H TD 5S 6S 2C
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, 7S, JH, KH, AH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, TD, 5S, 6S, 2C])
    8H JH 6S 5H 5S 9D TC 4C QC 9S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[5H, 5S], non_ranked_cards=[8H, JH, 6S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9D, 9S], non_ranked_cards=[TC, 4C, QC])
    7D 2C KD 3H 5H AS QD 7H JS 4D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 2C, KD, 3H, 5H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, QD, 7H, JS, 4D])
    TS QH 6C 8H TH 5H 3C 3H 9C 9D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[TS, TH], non_ranked_cards=[QH, 6C, 8H]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[3C, 3H, 9C, 9D], non_ranked_cards=[5H])
    AD KH JS 5D 3H AS AC 9S 5C KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, KH, JS, 5D, 3H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AS, AC], non_ranked_cards=[9S, 5C, KC])
    2C KH 8C JC QS 6D AH 2D KC TC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, KH, 8C, JC, QS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, AH, 2D, KC, TC])
    9D 3H 2S 7C 4D 6D KH KS 8D 7D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9D, 3H, 2S, 7C, 4D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KH, KS], non_ranked_cards=[6D, 8D, 7D])
    9H 2S TC JH AC QC 3H 5S 3S 8H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, 2S, TC, JH, AC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3H, 3S], non_ranked_cards=[QC, 5S, 8H])
    3S AS KD 8H 4C 3H 7C JH QH TS
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, AS, KD, 8H, 4C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, 7C, JH, QH, TS])
    7S 6D 7H 9D JH 4C 3D 3S 6C AS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7S, 7H], non_ranked_cards=[6D, 9D, JH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3D, 3S], non_ranked_cards=[4C, 6C, AS])
    4S 2H 2C 4C 8S 5H KC 8C QC QD
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[4S, 2H, 2C, 4C], non_ranked_cards=[8S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QC, QD], non_ranked_cards=[5H, KC, 8C])
    3H 3S 6C QS QC 2D 6S 5D 2C 9D
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[3H, 3S, QS, QC], non_ranked_cards=[6C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2D, 2C], non_ranked_cards=[6S, 5D, 9D])
    2H 8D JH 2S 3H 2D 6C 5C 7S AD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2H, 2S], non_ranked_cards=[8D, JH, 3H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, 6C, 5C, 7S, AD])
    9H JS 5D QH 8S TS 2H 7S 6S AD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, JS, 5D, QH, 8S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, 2H, 7S, 6S, AD])
    6D QC 9S 7H 5H 5C 7D KC JD 4H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, QC, 9S, 7H, 5H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5C, 7D, KC, JD, 4H])
    QC 5S 9H 9C 4D 6S KS 2S 4C 7C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9H, 9C], non_ranked_cards=[QC, 5S, 4D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, KS, 2S, 4C, 7C])
    9H 7C 4H 8D 3S 6H 5C 8H JS 7S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9H, 7C, 4H, 8D, 3S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, 5C, 8H, JS, 7S])
    2D 6H JS TD 4H 4D JC TH 5H KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, 6H, JS, TD, 4H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, JC, TH, 5H, KC])
    AC 7C 8D TH 3H 9S 2D 4C KC 4D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 7C, 8D, TH, 3H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4C, 4D], non_ranked_cards=[9S, 2D, KC])
    KD QS 9C 7S 3D KS AD TS 4C 4H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, QS, 9C, 7S, 3D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4C, 4H], non_ranked_cards=[KS, AD, TS])
    QH 9C 8H 2S 7D KS 7H 5D KD 4C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, 9C, 8H, 2S, 7D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KS, KD], non_ranked_cards=[7H, 5D, 4C])
    9C 2S 2H JC 6S 6C TC QC JH 5C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2S, 2H], non_ranked_cards=[9C, JC, 6S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, TC, QC, JH, 5C])
    7S AC 8H KC 8S 6H QS JC 3D 6S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[8H, 8S], non_ranked_cards=[7S, AC, KC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6H, 6S], non_ranked_cards=[QS, JC, 3D])
    JS 2D JH 8C 4S 6H 8H 6D 5D AD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JS, JH], non_ranked_cards=[2D, 8C, 4S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6H, 6D], non_ranked_cards=[8H, 5D, AD])
    6H 7D 2S 4H 9H 7C AS AC 8H 5S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, 7D, 2S, 4H, 9H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AS, AC], non_ranked_cards=[7C, 8H, 5S])
    3C JS 4S 6D 5H 2S QH 6S 9C 2C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, JS, 4S, 6D, 5H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2S, 2C], non_ranked_cards=[QH, 6S, 9C])
    3D 5S 6S 9S 4C QS 8D QD 8S TC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, 5S, 6S, 9S, 4C]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[QS, 8D, QD, 8S], non_ranked_cards=[TC])
    9C 3D AH 9H 5S 2C 7D AD JC 3S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9C, 9H], non_ranked_cards=[3D, AH, 5S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, 7D, AD, JC, 3S])
    7H TC AS 3C 6S 6D 7S KH KC 9H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, TC, AS, 3C, 6S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KH, KC], non_ranked_cards=[6D, 7S, 9H])
    3S TC 8H 6S 5H JH 8C 7D AC 2S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, TC, 8H, 6S, 5H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, 8C, 7D, AC, 2S])
    QD 9D 9C 3S JC 8C KS 8H 5D 4D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9D, 9C], non_ranked_cards=[QD, 3S, JC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8C, 8H], non_ranked_cards=[KS, 5D, 4D])
    JS AH JD 6D 9D 8C 9H 9S 8H 3H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[JS, JD], non_ranked_cards=[AH, 6D, 9D]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[8C, 9H, 9S, 8H], non_ranked_cards=[3H])
    2D 6S 4C 4D 8S AD 4S TC AH 9H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[4C, 4D], non_ranked_cards=[2D, 6S, 8S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AD, AH], non_ranked_cards=[4S, TC, 9H])
    TS AC QC TH KC 6D 4H 7S 8C 2H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TS, TH], non_ranked_cards=[AC, QC, KC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, 4H, 7S, 8C, 2H])
    3C QD JS 9D 5S JC AH 2H TS 9H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, QD, JS, 9D, 5S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JC, AH, 2H, TS, 9H])
    3H 4D QH 5D 9C 5H 7D 4S JC 3S
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, 4D, QH, 5D, 9C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, 7D, 4S, JC, 3S])
    8S TH 3H 7C 2H JD JS TS AC 8D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, TH, 3H, 7C, 2H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JD, JS], non_ranked_cards=[TS, AC, 8D])
    9C 2H TD KC JD 2S 8C 5S AD 2C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, 2H, TD, KC, JD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2S, 2C], non_ranked_cards=[8C, 5S, AD])
    3D KD 7C 5H 4D QH QD TC 6H 7D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, KD, 7C, 5H, 4D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QH, QD], non_ranked_cards=[TC, 6H, 7D])
    7H 2C KC 5S KD 6H AH QC 7S QH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KC, KD], non_ranked_cards=[7H, 2C, 5S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QC, QH], non_ranked_cards=[6H, AH, 7S])
    6H 5C AC 5H 2C 9C 2D 7C TD 2S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5C, 5H], non_ranked_cards=[6H, AC, 2C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2D, 2S], non_ranked_cards=[9C, 7C, TD])
    4D 9D AH 3D 7C JD 4H 8C 4C KS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, 9D, AH, 3D, 7C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4H, 4C], non_ranked_cards=[JD, 8C, KS])
    TH 3C JS QH 8H 4C AS 3D QS QC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, 3C, JS, QH, 8H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QS, QC], non_ranked_cards=[4C, AS, 3D])
    4D 7S 5H JH 6D 7D 6H JS KH 3C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, 7S, 5H, JH, 6D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 6H, JS, KH, 3C])
    QD 8S 7D 2H 2C 7C JC 2S 5H 8C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2H, 2C], non_ranked_cards=[QD, 8S, 7D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, JC, 2S, 5H, 8C])
    QH 8S 9D TC 2H AD 7C 8D QD 6S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, 8S, 9D, TC, 2H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, 7C, 8D, QD, 6S])
    3S 7C AD 9H 2H 9S JD TS 4C 2D
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, 7C, AD, 9H, 2H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9S, JD, TS, 4C, 2D])
    3S AS 4H QC 2C 8H 8S 7S TD TC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, AS, 4H, QC, 2C]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[8H, 8S, TD, TC], non_ranked_cards=[7S])
    JH TH TD 3S 4D 4H 5S 5D QS 2C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TH, TD], non_ranked_cards=[JH, 3S, 4D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5S, 5D], non_ranked_cards=[4H, QS, 2C])
    8C QD QH TC 6D 4S 9S 9D 4H QC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[QD, QH], non_ranked_cards=[8C, TC, 6D]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[4S, 9S, 9D, 4H], non_ranked_cards=[QC])
    8C JS 9D 6H JD 3H AD 6S TD QC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[JS, JD], non_ranked_cards=[8C, 9D, 6H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, AD, 6S, TD, QC])
    KC 8S 3D 7C TD 7D 8D 9H 4S 3S
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, 8S, 3D, 7C, TD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 8D, 9H, 4S, 3S])
    6C 4S 3D 9D KD TC KC KS AC 5S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, 4S, 3D, 9D, KD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KC, KS], non_ranked_cards=[TC, AC, 5S])
    7C 6S QH 3D JS KD 6H 6D 2D 8C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 6S, QH, 3D, JS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6H, 6D], non_ranked_cards=[KD, 2D, 8C])
    JD 2S 5S 4H 8S AC 2D 6S TS 5C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, 2S, 5S, 4H, 8S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 2D, 6S, TS, 5C])
    5H 8C 5S 3C 4S 3D 7C 8D AS 3H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5H, 5S], non_ranked_cards=[8C, 3C, 4S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3D, 3H], non_ranked_cards=[7C, 8D, AS])
    AS TS 7C 3H AD 7D JC QS 6C 6H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AS, AD], non_ranked_cards=[TS, 7C, 3H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6C, 6H], non_ranked_cards=[7D, JC, QS])
    3S 9S 4C AC QH 5H 5D 9H TS 4H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, 9S, 4C, AC, QH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5H, 5D], non_ranked_cards=[9H, TS, 4H])
    6C 5C 7H 7S TD AD JD 5S 2H 2S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7H, 7S], non_ranked_cards=[6C, 5C, TD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2H, 2S], non_ranked_cards=[AD, JD, 5S])
    7D 6C KC 3S JD 8D 8S TS QS KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 6C, KC, 3S, JD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8D, 8S], non_ranked_cards=[TS, QS, KH])
    8S QS 8D 6C TH AC AH 2C 8H 9S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[8S, 8D], non_ranked_cards=[QS, 6C, TH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AC, AH], non_ranked_cards=[2C, 8H, 9S])
    7H TD KH QH 8S 3D 4D AH JD AS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, TD, KH, QH, 8S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AH, AS], non_ranked_cards=[3D, 4D, JD])
    TS 3D 2H JC 2S JH KH 6C QC JS
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2H, 2S], non_ranked_cards=[TS, 3D, JC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JH, JS], non_ranked_cards=[KH, 6C, QC])
    KC TH 2D 6H 7S 2S TC 8C 9D QS
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, TH, 2D, 6H, 7S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, TC, 8C, 9D, QS])
    3C 9D 6S KH 8H 6D 5D TH 2C 2H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 9D, 6S, KH, 8H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2C, 2H], non_ranked_cards=[6D, 5D, TH])
    6H TC 7D AD 4D 8S TS 9H TD 7S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, TC, 7D, AD, 4D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TS, TD], non_ranked_cards=[8S, 9H, 7S])
    JS 6D JD JC 2H AC 6C 3D KH 8D
     - P1 wins - P1 Hand: ThreeOfAKind(rank=4, ranked_cards=[JS, JD, JC], non_ranked_cards=[6D, 2H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 6C, 3D, KH, 8D])
    KH JD 9S 5D 4H 4C 3H 7S QS 5C
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, JD, 9S, 5D, 4H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 3H, 7S, QS, 5C])
    4H JD 5D 3S 3C 4D KH QH QS 7S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3S, 3C], non_ranked_cards=[4H, JD, 5D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QH, QS], non_ranked_cards=[4D, KH, 7S])
    JD TS 8S QD AH 4C 6H 3S 5S 2C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, TS, 8S, QD, AH]) ; P2 Hand: Straight(rank=5, ranked_cards=[4C, 6H, 3S, 5S, 2C], non_ranked_cards=[])
    QS 3D JD AS 8D TH 7C 6S QC KS
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 3D, JD, AS, 8D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, 7C, 6S, QC, KS])
    7S 2H 8C QC 7H AC 6D 2D TH KH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7S, 7H], non_ranked_cards=[2H, 8C, QC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 6D, 2D, TH, KH])
    5S 6C 7H KH 7D AH 8C 5C 7S 3D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7H, 7D], non_ranked_cards=[5S, 6C, KH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AH, 8C, 5C, 7S, 3D])
    3C KD AD 7D 6C 4D KS 2D 8C 4S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, KD, AD, 7D, 6C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4D, 4S], non_ranked_cards=[KS, 2D, 8C])
    7C 8D 5S 2D 2S AH AD 2C 9D TD
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2D, 2S], non_ranked_cards=[7C, 8D, 5S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AH, AD], non_ranked_cards=[2C, 9D, TD])
    3C AD 4S KS JH 7C 5C 8C 9C TH
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, AD, 4S, KS, JH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 5C, 8C, 9C, TH])
    AS TD 4D 7C JD 8C QH 3C 5H 9S
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, TD, 4D, 7C, JD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, QH, 3C, 5H, 9S])
    3H 9C 8S 9S 6S QD KS AH 5H JH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9C, 9S], non_ranked_cards=[3H, 8S, 6S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QD, KS, AH, 5H, JH])
    QC 9C 5S 4H 2H TD 7D AS 8C 9D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 9C, 5S, 4H, 2H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 7D, AS, 8C, 9D])
    8C 2C 9D KD TC 7S 3D KH QC 3C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8C, 2C, 9D, KD, TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3D, 3C], non_ranked_cards=[7S, KH, QC])
    4D AS 4C QS 5S 9D 6S JD QH KS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4D, 4C], non_ranked_cards=[AS, QS, 5S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9D, 6S, JD, QH, KS])
    6D AH 6C 4C 5H TS 9H 7D 3D 5S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[6D, 6C], non_ranked_cards=[AH, 4C, 5H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TS, 9H, 7D, 3D, 5S])
    QS JD 7C 8D 9C AC 3S 6S 6C KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, JD, 7C, 8D, 9C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6S, 6C], non_ranked_cards=[AC, 3S, KH])
    8H JH 5D 9S 6D AS 6S 3S QC 7H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8H, JH, 5D, 9S, 6D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, 6S, 3S, QC, 7H])
    QD AD 5C JH 2H AH 4H AS KC 2C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QD, AD, 5C, JH, 2H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AH, AS], non_ranked_cards=[4H, KC, 2C])
    JH 9C 2C 6H 2D JS 5D 9H KC 6D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2C, 2D], non_ranked_cards=[JH, 9C, 6H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, 5D, 9H, KC, 6D])
    7D 9D KD TH 3H AS 6S QC 6H AD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 9D, KD, TH, 3H]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[AS, 6S, 6H, AD], non_ranked_cards=[QC])
    JD 4H 7D KC 3H JS 3C TH 3D QS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, 4H, 7D, KC, 3H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3C, 3D], non_ranked_cards=[JS, TH, QS])
    4C 3H 8C QD 5H 6H AS 8H AD JD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 3H, 8C, QD, 5H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AS, AD], non_ranked_cards=[6H, 8H, JD])
    TH 8S KD 5D QC 7D JS 5S 5H TS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TH, 8S, KD, 5D, QC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5S, 5H], non_ranked_cards=[7D, JS, TS])
    7D KC 9D QS 3H 3C 6D TS 7S AH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, KC, 9D, QS, 3H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 6D, TS, 7S, AH])
    7C 4H 7H AH QC AC 4D 5D 6D TH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7C, 7H], non_ranked_cards=[4H, AH, QC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 4D, 5D, 6D, TH])
    3C 4H 2S KD 8H 5H JH TC 6C JD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 4H, 2S, KD, 8H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JH, JD], non_ranked_cards=[5H, TC, 6C])
    4S 8C 3D 4H JS TD 7S JH QS KD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4S, 4H], non_ranked_cards=[8C, 3D, JS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 7S, JH, QS, KD])
    7C QC KD 4D 7H 6S AD TD TC KH
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[7C, 7H], non_ranked_cards=[QC, KD, 4D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TD, TC], non_ranked_cards=[6S, AD, KH])
    5H 9H KC 3H 4D 3D AD 6S QD 6H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, 9H, KC, 3H, 4D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6S, 6H], non_ranked_cards=[3D, AD, QD])
    TH 7C 6H TS QH 5S 2C KC TD 6S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TH, TS], non_ranked_cards=[7C, 6H, QH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 2C, KC, TD, 6S])
    7C 4D 5S JD JH 7D AC KD KH 4H
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[JD, JH], non_ranked_cards=[7C, 4D, 5S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KD, KH], non_ranked_cards=[7D, AC, 4H])
    7D 6C 8D 8H 5C JH 8S QD TH JD
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[8D, 8H], non_ranked_cards=[7D, 6C, 5C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JH, JD], non_ranked_cards=[8S, QD, TH])
    8D 7D 6C 7C 9D KD AS 5C QH JH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7D, 7C], non_ranked_cards=[8D, 6C, 9D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, AS, 5C, QH, JH])
    9S 2C 8C 3C 4C KS JH 2D 8D 4H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9S, 2C, 8C, 3C, 4C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, JH, 2D, 8D, 4H])
    7S 6C JH KH 8H 3H 9D 2D AH 6D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7S, 6C, JH, KH, 8H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, 9D, 2D, AH, 6D])
    4D TC 9C 8D 7H TD KS TH KD 3C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, TC, 9C, 8D, 7H]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[TD, KS, TH, KD], non_ranked_cards=[3C])
    JD 9H 8D QD AS KD 9D 2C 2S 9C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, 9H, 8D, QD, AS]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[9D, 2C, 2S, 9C], non_ranked_cards=[KD])
    8D 3H 5C 7H KS 5H QH 2D 8C 9H
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, 3H, 5C, 7H, KS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, QH, 2D, 8C, 9H])
    2D TH 6D QD 6C KC 3H 3S AD 4C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[6D, 6C], non_ranked_cards=[2D, TH, QD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3H, 3S], non_ranked_cards=[KC, AD, 4C])
    4H 3H JS 9D 3C TC 5H QH QC JC
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3H, 3C], non_ranked_cards=[4H, JS, 9D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QH, QC], non_ranked_cards=[TC, 5H, JC])
    3D 5C 6H 3S 3C JC 5S 7S 2S QH
     - P1 wins - P1 Hand: ThreeOfAKind(rank=4, ranked_cards=[3D, 3S, 3C], non_ranked_cards=[5C, 6H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JC, 5S, 7S, 2S, QH])
    AC 5C 8C 4D 5D 4H 2S QD 3C 3H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5C, 5D], non_ranked_cards=[AC, 8C, 4D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3C, 3H], non_ranked_cards=[4H, 2S, QD])
    2C TD AH 9C KD JS 6S QD 4C QC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, TD, AH, 9C, KD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QD, QC], non_ranked_cards=[JS, 6S, 4C])
    QS 8C 3S 4H TC JS 3H 7C JC AD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 8C, 3S, 4H, TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JS, JC], non_ranked_cards=[3H, 7C, AD])
    5H 4D 9C KS JC TD 9S TS 8S 9H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, 4D, 9C, KS, JC]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[TD, 9S, TS, 9H], non_ranked_cards=[8S])
    QD TS 7D AS AC 2C TD 6H 8H AH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AS, AC], non_ranked_cards=[QD, TS, 7D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, TD, 6H, 8H, AH])
    6S AD 8C 4S 9H 8D 9D KH 8S 3C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, AD, 8C, 4S, 9H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8D, 8S], non_ranked_cards=[9D, KH, 3C])
    QS 4D 2D 7S KH JS JC AD 4C 3C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 4D, 2D, 7S, KH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JS, JC], non_ranked_cards=[AD, 4C, 3C])
    QS 9S 7H KC TD TH 5H JS AC JH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 9S, 7H, KC, TD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JS, JH], non_ranked_cards=[TH, 5H, AC])
    6D AC 2S QS 7C AS KS 6S KH 5S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, AC, 2S, QS, 7C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KS, KH], non_ranked_cards=[AS, 6S, 5S])
    6D 8H KH 3C QS 2H 5C 9C 9D 6C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, 8H, KH, 3C, QS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9C, 9D], non_ranked_cards=[2H, 5C, 6C])
    JS 2C 4C 6H 7D JC AC QD TD 3H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, 2C, 4C, 6H, 7D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JC, AC, QD, TD, 3H])
    4H QC 8H JD 4C KD KS 5C KC 7S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[4H, 4C], non_ranked_cards=[QC, 8H, JD]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[KD, KS, KC], non_ranked_cards=[5C, 7S])
    6D 2D 3H 2S QD 5S 7H AS TH 6S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2D, 2S], non_ranked_cards=[6D, 3H, QD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 7H, AS, TH, 6S])
    AS 6D 8D 2C 8S TD 8H QD JC AH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[8D, 8S], non_ranked_cards=[AS, 6D, 2C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 8H, QD, JC, AH])
    9C 9H 2D TD QH 2H 5C TC 3D 8H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9C, 9H], non_ranked_cards=[2D, TD, QH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, 5C, TC, 3D, 8H])
    KC 8S 3D KH 2S TS TC 6S 4D JH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KC, KH], non_ranked_cards=[8S, 3D, 2S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TS, TC], non_ranked_cards=[6S, 4D, JH])
    9H 9D QS AC KC 6H 5D 4D 8D AH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9H, 9D], non_ranked_cards=[QS, AC, KC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, 5D, 4D, 8D, AH])
    9S 5C QS 4H 7C 7D 2H 8S AD JS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9S, 5C, QS, 4H, 7C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 2H, 8S, AD, JS])
    3D AC 9S AS 2C 2D 2H 3H JC KH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AC, AS], non_ranked_cards=[3D, 9S, 2C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2D, 2H], non_ranked_cards=[3H, JC, KH])
    7H QH KH JD TC KS 5S 8H 4C 8D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7H, QH, KH, JD, TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8H, 8D], non_ranked_cards=[KS, 5S, 4C])
    2H 7H 3S 2S 5H QS 3C AS 9H KD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2H, 2S], non_ranked_cards=[7H, 3S, 5H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 3C, AS, 9H, KD])
    AD 3D JD 6H 5S 9C 6D AC 9S 3S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, 3D, JD, 6H, 5S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9C, 9S], non_ranked_cards=[6D, AC, 3S])
    3D 5D 9C 2D AC 4S 2S AD 6C 6S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, 5D, 9C, 2D, AC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6C, 6S], non_ranked_cards=[4S, 2S, AD])
    QC 4C 2D 3H 6S KC QH QD 2H JH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 4C, 2D, 3H, 6S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QH, QD], non_ranked_cards=[KC, 2H, JH])
    QC 3C 8S 4D 9S 2H 5C 8H QS QD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 3C, 8S, 4D, 9S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QS, QD], non_ranked_cards=[2H, 5C, 8H])
    6D KD 6S 7H 3S KH 2H 5C JC 6C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[6D, 6S], non_ranked_cards=[KD, 7H, 3S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, 2H, 5C, JC, 6C])
    3S 9S TC 6S 8H 2D AD 7S 8S TS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, 9S, TC, 6S, 8H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, AD, 7S, 8S, TS])
    3C 6H 9C 3H 5C JC 8H QH TD QD
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[3C, 3H], non_ranked_cards=[6H, 9C, 5C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QH, QD], non_ranked_cards=[JC, 8H, TD])
    3C JS QD 5D TD 2C KH 9H TH AS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, JS, QD, 5D, TD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, KH, 9H, TH, AS])
    9S TC JD 3D 5C 5H AD QH 9H KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9S, TC, JD, 3D, 5C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, AD, QH, 9H, KC])
    TC 7H 4H 8H 3H TD 6S AC 7C 2S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, 7H, 4H, 8H, 3H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 6S, AC, 7C, 2S])
    QS 9D 5D 3C JC KS 4D 6C JH 2S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 9D, 5D, 3C, JC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 4D, 6C, JH, 2S])
    9S 6S 3C 7H TS 4C KD 6D 3D 9C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9S, 6S, 3C, 7H, TS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, KD, 6D, 3D, 9C])
    2D 9H AH AC 7H 2S JH 3S 7C QC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[AH, AC], non_ranked_cards=[2D, 9H, 7H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, JH, 3S, 7C, QC])
    QD 9H 3C 2H AC AS 8S KD 8C KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QD, 9H, 3C, 2H, AC]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[8S, KD, 8C, KH], non_ranked_cards=[AS])
    2D 7S TD TH 6D JD 8D 4D 2H 5S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[TD, TH], non_ranked_cards=[2D, 7S, 6D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JD, 8D, 4D, 2H, 5S])
    8S QH KD JD QS JH 4D KC 5H 3S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QH, QS], non_ranked_cards=[8S, KD, JD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, 4D, KC, 5H, 3S])
    3C KH QC 6D 8H 3S AH 7D TD 2D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, KH, QC, 6D, 8H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, AH, 7D, TD, 2D])
    5S 9H QH 4S 6S 6C 6D TS TH 7S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 9H, QH, 4S, 6S]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[6C, 6D, TS, TH], non_ranked_cards=[7S])
    6C 4C 6D QS JS 9C TS 3H 8D 8S
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[6C, 6D], non_ranked_cards=[4C, QS, JS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8D, 8S], non_ranked_cards=[9C, TS, 3H])
    JS 5C 7S AS 2C AH 2H AD 5S TC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, 5C, 7S, AS, 2C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AH, AD], non_ranked_cards=[2H, 5S, TC])
    KD 6C 9C 9D TS 2S JC 4H 2C QD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[9C, 9D], non_ranked_cards=[KD, 6C, TS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2S, 2C], non_ranked_cards=[JC, 4H, QD])
    QS 9H TC 3H KC KS 4H 3C AD TH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QS, 9H, TC, 3H, KC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 4H, 3C, AD, TH])
    KH 9C 2H KD 9D TC 7S KC JH 2D
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[KH, 9C, KD, 9D], non_ranked_cards=[2H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, 7S, KC, JH, 2D])
    7C 3S KC AS 8C 5D 9C 9S QH 3H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 3S, KC, AS, 8C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9C, 9S], non_ranked_cards=[5D, QH, 3H])
    2D 8C TD 4C 2H QC 5D TC 2C 7D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[2D, 2H], non_ranked_cards=[8C, TD, 4C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 5D, TC, 2C, 7D])
    KS 4D 6C QH TD KH 5D 7C AD 8D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 4D, 6C, QH, TD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, 5D, 7C, AD, 8D])
    2S 9S 8S 4C 8C 3D 6H QD 7C 7H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[8S, 8C], non_ranked_cards=[2S, 9S, 4C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[7C, 7H], non_ranked_cards=[3D, 6H, QD])
    6C 8S QH 5H TS 5C 3C 4S 2S 2H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, 8S, QH, 5H, TS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2S, 2H], non_ranked_cards=[5C, 3C, 4S])
    8S 6S 2H JC 3S 3H 9D 8C 2S 7H
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, 6S, 2H, JC, 3S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, 9D, 8C, 2S, 7H])
    QC 2C 8H 9C AC JD 4C 4H 6S 3S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 2C, 8H, 9C, AC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4C, 4H], non_ranked_cards=[JD, 6S, 3S])
    3H 3S 7D 4C 9S 5H 8H JC 3D TC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[3H, 3S], non_ranked_cards=[7D, 4C, 9S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5H, 8H, JC, 3D, TC])
    QH 2S 2D 9S KD QD 9H AD 6D 9C
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[2S, 2D], non_ranked_cards=[QH, 9S, KD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9H, 9C], non_ranked_cards=[QD, AD, 6D])
    8D 2D KS 9S JC 4C JD KC 4S TH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, 2D, KS, 9S, JC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4C, 4S], non_ranked_cards=[JD, KC, TH])
    KH TS 6D 4D 5C KD 5H AS 9H AD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, TS, 6D, 4D, 5C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AS, AD], non_ranked_cards=[KD, 5H, 9H])
    QD JS 7C 6D 5D 5C TH 5H QH QS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QD, JS, 7C, 6D, 5D]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[5C, 5H, QH, QS], non_ranked_cards=[TH])
    9D QH KH 5H JH 4C 4D TC TH 6C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9D, QH, KH, 5H, JH]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[4C, 4D, TC, TH], non_ranked_cards=[6C])
    KH AS TS 9D KD 9C 7S 4D 8H 5S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KH, KD], non_ranked_cards=[AS, TS, 9D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, 7S, 4D, 8H, 5S])
    KH AS 2S 7D 9D 4C TS TH AH 7C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, AS, 2S, 7D, 9D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TS, TH], non_ranked_cards=[4C, AH, 7C])
    KS 4D AC 8S 9S 8D TH QH 9D 5C
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 4D, AC, 8S, 9S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, TH, QH, 9D, 5C])
    5D 5C 8C QS TC 4C 3D 3S 2C 8D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5D, 5C], non_ranked_cards=[8C, QS, TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3D, 3S], non_ranked_cards=[4C, 2C, 8D])
    9D KS 2D 3C KC 4S 8C KH 6C JC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KS, KC], non_ranked_cards=[9D, 2D, 3C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4S, 8C, KH, 6C, JC])
    8H AH 6H 7D 7S QD 3C 4C 6C KC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7D, 7S], non_ranked_cards=[8H, AH, 6H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QD, 3C, 4C, 6C, KC])
    3H 2C QH 8H AS 7D 4C 8C 4H KC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, 2C, QH, 8H, AS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4C, 4H], non_ranked_cards=[7D, 8C, KC])
    QD 5S 4H 2C TD AH JH QH 4C 8S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QD, 5S, 4H, 2C, TD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AH, JH, QH, 4C, 8S])
    3H QS 5S JS 8H 2S 9H 9C 3S 2C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, QS, 5S, JS, 8H]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[2S, 9H, 9C, 2C], non_ranked_cards=[3S])
    6H TS 7S JC QD AC TD KC 5S 3H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, TS, 7S, JC, QD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, TD, KC, 5S, 3H])
    QH AS QS 7D JC KC 2C 4C 5C 5S
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QH, QS], non_ranked_cards=[AS, 7D, JC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5C, 5S], non_ranked_cards=[KC, 2C, 4C])
    QH 3D AS JS 4H 8D 7H JC 2S 9C
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, 3D, AS, JS, 4H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, 7H, JC, 2S, 9C])
    5D 4D 2S 4S 9D 9C 2D QS 8H 7H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[4D, 4S], non_ranked_cards=[5D, 2S, 9D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, 2D, QS, 8H, 7H])
    6D 7H 3H JS TS AC 2D JH 7C 8S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6D, 7H, 3H, JS, TS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AC, 2D, JH, 7C, 8S])
    JH 5H KC 3C TC 5S 9H 4C 8H 9D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, 5H, KC, 3C, TC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9H, 9D], non_ranked_cards=[5S, 4C, 8H])
    8S KC 5H 9H AD KS 9D KH 8D AH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, KC, 5H, 9H, AD]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KS, KH], non_ranked_cards=[9D, 8D, AH])
    JC 2H 9H KS 6S 3H QC 5H AH 9C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JC, 2H, 9H, KS, 6S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3H, QC, 5H, AH, 9C])
    5C KH 5S AD 6C JC 9H QC 9C TD
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[5C, 5S], non_ranked_cards=[KH, AD, 6C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9H, 9C], non_ranked_cards=[JC, QC, TD])
    5S 5D JC QH 2D KS 8H QS 2H TS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5S, 5D], non_ranked_cards=[JC, QH, 2D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 8H, QS, 2H, TS])
    JH 5H 5S AH 7H 3C 8S AS TD KH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5H, 5S], non_ranked_cards=[JH, AH, 7H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3C, 8S, AS, TD, KH])
    6H 3D JD 2C 4C KC 7S AH 6C JH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, 3D, JD, 2C, 4C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, 7S, AH, 6C, JH])
    4C KS 9D AD 7S KC 7D 8H 3S 9C
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, KS, 9D, AD, 7S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, 7D, 8H, 3S, 9C])
    7H 5C 5H 3C 8H QC 3D KH 6D JC
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5C, 5H], non_ranked_cards=[7H, 3C, 8H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QC, 3D, KH, 6D, JC])
    2D 4H 5D 7D QC AD AH 9H QH 8H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2D, 4H, 5D, 7D, QC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AD, AH], non_ranked_cards=[9H, QH, 8H])
    KD 8C JS 9D 3S 3C 2H 5D 6D 2S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, 8C, JS, 9D, 3S]) ; P2 Hand: OnePair(rank=2, ranked_cards=[2H, 2S], non_ranked_cards=[3C, 5D, 6D])
    8S 6S TS 3C 6H 8D 5S 3H TD 6C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[6S, 6H], non_ranked_cards=[8S, TS, 3C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8D, 5S, 3H, TD, 6C])
    KS 3D JH 9C 7C 9S QS 5S 4H 6H
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KS, 3D, JH, 9C, 7C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9S, QS, 5S, 4H, 6H])
    7S 6S TH 4S KC KD 3S JC JH KS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7S, 6S, TH, 4S, KC]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[KD, JC, JH, KS], non_ranked_cards=[3S])
    7C 3C 2S 6D QH 2C 7S 5H 8H AH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 3C, 2S, 6D, QH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, 7S, 5H, 8H, AH])
    KC 8D QD 6D KH 5C 7H 9D 3D 9C
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KC, KH], non_ranked_cards=[8D, QD, 6D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[9D, 9C], non_ranked_cards=[5C, 7H, 3D])
    6H 2D 8S JS 9S 2S 6D KC 7C TC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6H, 2D, 8S, JS, 9S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, 6D, KC, 7C, TC])
    KD 9C JH 7H KC 8S 2S 7S 3D 6H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KD, KC], non_ranked_cards=[9C, JH, 7H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, 2S, 7S, 3D, 6H])
    4H 9H 2D 4C 8H 7H 5S 8S 2H 8D
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[4H, 4C], non_ranked_cards=[9H, 2D, 8H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8S, 8D], non_ranked_cards=[7H, 5S, 2H])
    AD 7C 3C 7S 5S 4D 9H 3D JC KH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[7C, 7S], non_ranked_cards=[AD, 3C, 5S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, 9H, 3D, JC, KH])
    5D AS 7D 6D 9C JC 4C QH QS KH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5D, AS, 7D, 6D, 9C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QH, QS], non_ranked_cards=[JC, 4C, KH])
    KD JD 7D 3D QS QC 8S 6D JS QD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KD, JD, 7D, 3D, QS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[QC, QD], non_ranked_cards=[8S, 6D, JS])
    6S 8C 5S QH TH 9H AS AC 2C JD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, 8C, 5S, QH, TH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AS, AC], non_ranked_cards=[9H, 2C, JD])
    QC KS QH 7S 3C 4C 5C KC 5D AH
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QC, QH], non_ranked_cards=[KS, 7S, 3C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[5C, 5D], non_ranked_cards=[4C, KC, AH])
    6C 4H 9D AH 2C 3H KD 3D TS 5C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6C, 4H, 9D, AH, 2C]) ; P2 Hand: OnePair(rank=2, ranked_cards=[3H, 3D], non_ranked_cards=[KD, TS, 5C])
    TD 8S QS AS JS 3H KD AC 4H KS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TD, 8S, QS, AS, JS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KD, KS], non_ranked_cards=[3H, AC, 4H])
    7D 5D TS 9H 4H 4C 9C 2H 8C QC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, 5D, TS, 9H, 4H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 9C, 2H, 8C, QC])
    2C 7D 9H 4D KS 4C QH AD KD JS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, 7D, 9H, 4D, KS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, QH, AD, KD, JS])
    QD AD AH KH 9D JS 9H JC KD JD
     - P1 does not win - P1 Hand: OnePair(rank=2, ranked_cards=[AD, AH], non_ranked_cards=[QD, KH, 9D]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[JS, JC, JD], non_ranked_cards=[9H, KD])
    8S 3C 4S TS 7S 4D 5C 2S 6H 7C
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[8S, 3C, 4S, TS, 7S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4D, 5C, 2S, 6H, 7C])
    JS 7S 5C KD 6D QH 8S TD 2H 6S
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JS, 7S, 5C, KD, 6D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, 8S, TD, 2H, 6S])
    QH 6C TC 6H TD 4C 9D 2H QC 8H
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[6C, TC, 6H, TD], non_ranked_cards=[QH]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 9D, 2H, QC, 8H])
    3D TS 4D 2H 6H 6S 2C 7H 8S 6C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, TS, 4D, 2H, 6H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[6S, 6C], non_ranked_cards=[2C, 7H, 8S])
    9H 9D JD JH 3S AH 2C 6S 3H 8S
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[9H, 9D, JD, JH], non_ranked_cards=[3S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AH, 2C, 6S, 3H, 8S])
    2C QS 8C 5S 3H 2S 7D 3C AD 4S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, QS, 8C, 5S, 3H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2S, 7D, 3C, AD, 4S])
    5C QC QH AS TS 4S 6S 4C 5H JS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QC, QH], non_ranked_cards=[5C, AS, TS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4S, 4C], non_ranked_cards=[6S, 5H, JS])
    JH 5C TD 4C 6H JS KD KH QS 4H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, 5C, TD, 4C, 6H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[KD, KH], non_ranked_cards=[JS, QS, 4H])
    TC KH JC 4D 9H 9D 8D KC 3C 8H
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[TC, KH, JC, 4D, 9H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[8D, 8H], non_ranked_cards=[9D, KC, 3C])
    2H TC 8S AD 9S 4H TS 7H 2C 5C
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2H, TC, 8S, AD, 9S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, TS, 7H, 2C, 5C])
    4H 2S 6C 5S KS AH 9C 7C 8H KD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4H, 2S, 6C, 5S, KS]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AH, 9C, 7C, 8H, KD])
    TS QH TD QS 3C JH AH 2C 8D 7D
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[TS, QH, TD, QS], non_ranked_cards=[3C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[JH, AH, 2C, 8D, 7D])
    5D KC 3H 5S AC 4S 7H QS 4C 2H
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[5D, 5S], non_ranked_cards=[KC, 3H, AC]) ; P2 Hand: OnePair(rank=2, ranked_cards=[4S, 4C], non_ranked_cards=[7H, QS, 2H])
    3D 7D QC KH JH 6D 6C TD TH KD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3D, 7D, QC, KH, JH]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[6D, 6C, TD, TH], non_ranked_cards=[KD])
    5S 8D TH 6C 9D 7D KH 8C 9S 6D
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5S, 8D, TH, 6C, 9D]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7D, KH, 8C, 9S, 6D])
    JD QS 7S QC 2S QH JC 4S KS 8D
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[QS, QC], non_ranked_cards=[JD, 7S, 2S]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QH, JC, 4S, KS, 8D])
    7S 5S 9S JD KD 9C JC AD 2D 7C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7S, 5S, 9S, JD, KD]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, JC, AD, 2D, 7C])
    4S 5H AH JH 9C 5D TD 7C 2D 6S
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4S, 5H, AH, JH, 9C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[5D, TD, 7C, 2D, 6S])
    KC 6C 7H 6S 9C QD 5S 4H KS TD
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[6C, 6S], non_ranked_cards=[KC, 7H, 9C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[QD, 5S, 4H, KS, TD])
    6S 8D KS 2D TH TD 9H JD TS 3S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, 8D, KS, 2D, TH]) ; P2 Hand: OnePair(rank=2, ranked_cards=[TD, TS], non_ranked_cards=[9H, JD, 3S])
    KH JS 4H 5D 9D TC TD QC JD TS
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KH, JS, 4H, 5D, 9D]) ; P2 Hand: ThreeOfAKind(rank=4, ranked_cards=[TC, TD, TS], non_ranked_cards=[QC, JD])
    QS QD AC AD 4C 6S 2D AS 3H KC
     - P1 wins - P1 Hand: TwoPairs(rank=3, ranked_cards=[QS, QD, AC, AD], non_ranked_cards=[4C]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, 2D, AS, 3H, KC])
    4C 7C 3C TD QS 9C KC AS 8D AD
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[4C, 7C, 3C, TD, QS]) ; P2 Hand: OnePair(rank=2, ranked_cards=[AS, AD], non_ranked_cards=[9C, KC, 8D])
    KC 7H QC 6D 8H 6S 5S AH 7S 8C
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[KC, 7H, QC, 6D, 8H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[6S, 5S, AH, 7S, 8C])
    3S AD 9H JC 6D JD AS KH 6S JH
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[3S, AD, 9H, JC, 6D]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JD, JH], non_ranked_cards=[AS, KH, 6S])
    AD 3D TS KS 7H JH 2D JS QD AC
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AD, 3D, TS, KS, 7H]) ; P2 Hand: OnePair(rank=2, ranked_cards=[JH, JS], non_ranked_cards=[2D, QD, AC])
    9C JD 7C 6D TC 6H 6C JC 3D 3S
     - P1 does not win - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[9C, JD, 7C, 6D, TC]) ; P2 Hand: TwoPairs(rank=3, ranked_cards=[6H, 6C, 3D, 3S], non_ranked_cards=[JC])
    QC KC 3S JC KD 2C 8D AH QS TS
     - P1 wins - P1 Hand: OnePair(rank=2, ranked_cards=[KC, KD], non_ranked_cards=[QC, 3S, JC]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[2C, 8D, AH, QS, TS])
    AS KD 3D JD 8H 7C 8C 5C QD 6C
     - P1 wins - P1 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[AS, KD, 3D, JD, 8H]) ; P2 Hand: HighCard(rank=1, ranked_cards=[], non_ranked_cards=[7C, 8C, 5C, QD, 6C])






## Solution

How many hands does Player 1 win?: 376





```python

```
