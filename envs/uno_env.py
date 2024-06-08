from typing import SupportsFloat, Any

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from gymnasium.core import ActType, ObsType

import config
from components.agents import QLearningAgent, MonteCarloAgent
from components.cards import Deck
from components.players import Player
from components.turn import Turn
from components.utils import block_print, bold, check_win


class UNOEnv(gym.Env):
    metadata = {'render.modes': ['AI']}

    def __init__(self):
        super(UNOEnv, self).__init__()
        # 행동 공간 정의: RED, GREEN, BLUE, YELLOW, SKIP, REVERSE, +2, +4, WILD COLOR
        self.action_space = spaces.Discrete(9)

        # 상태 공간 정의
        # 각 카드 유형별 최대 수량은 2로 설정 (일반 카드 RED, GREEN, BLUE, YELLOW)
        # 각 특수 카드 유형별 최대 수량은 1로 설정 (SKIP, REVERSE, +2)
        # WILD 카드의 유형별 최대 수량은 1로 설정 (+4, COLOR CHANGE)
        # 현재 오픈 카드의 색깔 정보는 추가됩니다.

        # 4 일반 카드 + 5 특수 카드 (2 wild cards included)
        card_types = 9
        self.observation_space = spaces.Tuple((
            # color, card counts
            spaces.Discrete(4),
            spaces.Box(low=0, high=2, shape=(card_types,), dtype=np.int32)
        ))

        if config.params['algorithm'] == 'q-learning':
            self.agent = QLearningAgent(config.params['model'])
        else:
            self.agent = MonteCarloAgent(config.params['model'])

        self.starting_name = None
        self.reset()

    def step(
            self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        self.turn_no += 1
        card_open = self.turn.card_open
        bold(f'\n---------- TURN {self.turn_no} ----------')
        print(f'\nCurrent open card: {self.turn.card_open.print_card()}')

        if self.starting_name == self.player_1.name:
            if self.turn_no % 2 == 1:
                player_act, player_pas = self.player_1, self.player_2
            else:
                player_act, player_pas = self.player_2, self.player_1
        else:
            if self.turn_no % 2 == 0:
                player_act, player_pas = self.player_1, self.player_2
            else:
                player_act, player_pas = self.player_2, self.player_1

        player_act.show_hand()
        player_act.show_hand_play(card_open)
        self.turn.action(
            player=player_act,
            opponent=player_pas,
            agent=self.agent,
            algorithm=config.params['algorithm'],
            turn_no=self.turn_no
        )

        terminated = check_win(player_act) or check_win(player_pas)
        truncated = False
        observation = player_act.state

        info = {
            'turn_number': self.turn_no,
            'current_open_card': self.turn.card_open.print_card(),
            'winner': self.winner if terminated else None
        }

        if terminated:
            if not self.winner:
                self.winner = player_act.name if check_win(player_act) else player_pas.name
                print(f'{self.winner} has won!')
            return observation, self.agent.reward, terminated, truncated, info

        if player_act.card_play.value in ["REV", "SKIP"]:
            print(f'{player_act.name} has another turn')
            self.turn_no = self.turn_no - 1

        if (self.turn.count > 0) and (self.turn.count % 2 == 0):
            print(f'Again it is {player_act.name}s turn')
            self.turn_no = self.turn_no - 1

        return observation, self.agent.reward, terminated, truncated, info

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[ObsType, dict[str, Any]]:

        self.player_1 = Player(config.player_name_1, agent=self.agent)
        self.player_2 = Player(config.player_name_2, agent=self.agent)

        self.turn = Turn(
            deck=Deck(),
            player_1=self.player_1,
            player_2=self.player_2,
            agent=self.agent
        )

        if not self.starting_name:
            self.starting_name = self.player_1.name

        if self.starting_name == self.player_1.name:
            self.starting_name = self.player_2.name
        else:
            self.starting_name = self.player_1.name

        self.turn_no = 0
        self.winner = 0

        if self.starting_name == self.player_1.name:
            initial_observation = self.player_1.identify_state(self.turn.card_open)
        else:
            initial_observation = self.player_2.identify_state(self.turn.card_open)

        return initial_observation

    def render(self):
        """Visualize the environment."""
        print(f"Turn number: {self.turn_no}")
        print(f"Current open card: {self.turn.card_open.print_card()}")
        print(f"Player 1 hand: {[card.print_card() for card in self.player_1.hand]}")
        print(f"Player 2 hand: {[card.print_card() for card in self.player_2.hand]}")
        if self.winner:
            print(f"Winner: {self.winner}")


