# Do_yoUNO2
UNO 강화학습 프로젝트입니다.

## UNO 카드 구성

- **기본 카드**: 4가지 색깔(빨강, 노랑, 초록, 파랑)로 구성되며, 각 색깔별로 0번 카드 1장, 1~9번 카드 각 2장씩 포함합니다.
- **특수 카드**: 스킵(Skip), 리버스(Reverse), 2장 뽑기(Draw 2) 각각 2장씩 존재합니다.
- **와일드카드**: 일반 색깔 바꾸기(Wild) 4장, 4장 뽑기(Wild Draw 4) 4장, 카드 재분배(Wild Shuffle Hands) 1장, 커스텀 효과(Wild Customizable) 3장이 포함됩니다.

## 기본 규칙

**게임 시작**

2~10명이 참여할 수 있으며, 각 플레이어는 카드 5장씩 받습니다. 남은 카드는 덮어 두고, 가장 위에 있는 카드를 뒤집어 제출 더미(Discard Pile)로 사용하여 게임을 시작합니다.

**플레이 진행**

- **카드 제출**: 플레이어는 제출 더미의 최상단 카드와 동일한 색, 숫자, 심볼 혹은 와일드카드를 낼 수 있습니다.
- **와일드카드 사용**: 와일드카드를 사용하여 색을 변경할 수 있습니다.
- **카드 부족 시**: 낼 카드가 없으면 덱에서 한 장을 뽑습니다. 뽑은 카드가 낼 수 있는 카드면 즉시 낼 수 있습니다.
- **카드 모두 사용**: 모든 카드를 사용해 첫 번째로 카드를 다 낸 사람이 그 라운드의 승자가 됩니다.

**특수 카드 효과**

- **스킵**: 다음 플레이어는 턴을 건너뜁니다.
- **리버스**: 게임의 진행 방향을 바꿉니다.
- **2장 뽑기**: 다음 플레이어는 두 장을 뽑고 턴을 넘깁니다.
- **4장 뽑기**: 특정 조건(제출 더미의 최상단 카드와 색이 다를 때)에만 사용 가능하며, 다음 플레이어는 네 장을 뽑고 턴을 넘깁니다.

**우노(UNO)**

- **카드 2장 상태**: 카드를 2장 가지고 있을 때 다음 카드를 내면, '우노'를 외쳐야 합니다.
- **페널티**: '우노'를 외치지 않고 적발되면, 2장의 페널티를 받습니다.

**점수 계산**

게임이 끝나면, 카드에 적힌 숫자대로 점수가 계산됩니다. 특수 카드는 각각 20점, 와일드카드는 50점으로 계산됩니다. 남은 카드가 없는 플레이어가 1위가 되며, 점수가 가장 낮은 플레이어가 높은 순위를 얻습니다.

## Reference

아래 코드를 그대로 실행해본 결과, episode 10000번 기준으로 reward가 업데이트 되지 않았습니다. 

변경 사항은 다음과 같습니다.

1. reward 재정의하였습니다.
2. openai gym (gymnaisum) env에 맞게 코드 수정했습니다.
3. 시각화 코드를 추가하였습니다. (win rate, coverage)

[[github](https://github.com/bernhard-pfann/uno-card-game-rl/tree/main)][[blog](https://towardsdatascience.com/tackling-uno-card-game-with-reinforcement-learning-fad2fc19355c)]

## State 정의

상태 공간은 게임의 현재 상태를 나타냅니다. 상태 공간은 다음과 같이 정의됩니다:

- **일반 카드 (RED, GREEN, BLUE, YELLOW)**: 각 색깔별로 최대 2장까지 가능
- **특수 카드 (SKIP, REVERSE, +2)**: 각 특수 카드 유형별로 최대 1장까지 가능
- **WILD 카드 (+4, COLOR CHANGE)**: 각 와일드 카드 유형별로 최대 1장까지 가능

또한, 상태 공간에는 현재 오픈 카드의 색깔 정보가 추가되어 있습니다. 이 정보는 플레이어가 카드를 낼 때 참고할 수 있는 중요한 요소입니다.

normal cards in hand ≥ normal cards playable

현실 게임에서는 손에 있는 카드만 플레이 할 수 있습니다. q table은 위 조건을 만족하는 27000가지 state로 구성됩니다. 

**UNO를 외치는 것은 고려하지 않습니다.**

![Untitled (28)](https://github.com/cshooon/Do_yoUNO2/assets/113033780/50cd409b-05cd-4e24-90a4-ef27b89c9ae4)

## Action 정의

- **행동 공간 (Action Space)**: 이는 플레이어가 선택할 수 있는 모든 가능한 행동을 정의합니다. 게임에서는 다음 9가지 행동이 가능합니다:
    - Open Card: 덱에 올려져 있는 카드
    - RED: 빨간색 카드 내기
    - GREEN: 초록색 카드 내기
    - BLUE: 파란색 카드 내기
    - YELLOW: 노란색 카드 내기
    - SKIP: 순서 건너뛰기 카드 내기
    - REVERSE: 순서 뒤집기 카드 내기
    - +2: 상대방이 2장을 뽑는 카드 내기
    - +4: 상대방이 4장을 뽑는 와일드 카드 내기 (색깔도 변경 가능)
    - WILD COLOR: 색깔 변경 와일드 카드 내기

![Untitled (29)](https://github.com/cshooon/Do_yoUNO2/assets/113033780/ba0dbe12-f778-495b-877a-4e577f1214e9)

## Monte Carlo

몬테 카를로 방법은 각 에피소드가 완전히 끝날 때까지 기다린 후에, 방문한 각 상태에 대한 보상을 업데이트하는 방식으로 강화학습을 수행합니다. 이 접근법은 결과가 확실하게 나타나는 전체 게임 또는 에피소드의 결과를 통해 학습합니다. 각 에피소드의 모든 선택과 그 결과를 저장하고, 에피소드가 종료되면 저장된 정보를 사용하여 학습을 진행합니다.

![Untitled (30)](https://github.com/cshooon/Do_yoUNO2/assets/113033780/cafacf49-9ebe-4bc4-ac31-df91d4402911)

### Reward

- 상태별 보상 계산: 각 상태에서 에이전트가 가지고 있는 카드의 총 수(`states_t`)를 계산하고, 카드 수에 따라 다음과 같이 보상을 할당합니다:
    - **모든 카드 사용 (게임 종료)**: 보상 = 1.0
    - **카드 2장 이하**: 보상 = 0.5
    - **카드 5장 이하**: 보상 = 0.25
    - **카드 8장 이하**: 보상 = 0.12
    - **그 외 경우 (많은 카드 남음)**: 보상 = 0.06
- 이렇게 설정된 보상은 게임을 빠르게 마칠수록 높은 보상을 받게 하여 에이전트가 게임을 빠르게 종료하도록 동기를 부여합니다.

## Q learning

Q learning은 각 상태에서 취할 수 있는 모든 가능한 행동의 가치( Q table value)를 추정하고, 이러한 추정치를 바탕으로 최적의 행동을 선택하는 강화학습 방법입니다. 각 행동 후에, 에이전트는 받은 보상과 다음 상태에서의 최대 Q 값을 사용하여 현재의 Q 값을 업데이트합니다. 이 과정을 통해 에이전트는 시간이 지남에 따라 최적의 정책을 학습하게 됩니다.

![Untitled (31)](https://github.com/cshooon/Do_yoUNO2/assets/113033780/2eb64424-53af-4452-b473-ca08acffe285)

장기적 보상보다 현재에 카드를 줄이는 것이 더 중요하기 때문에 discount factor를 1로 설정합니다. 위 식에서 생략되었습니다.

### Reward

- **initial_rewards**: 모든 상태와 행동에 대해 일정한 초기 보상(0.5)을 설정합니다. 이는 학습 초기에 아직 탐색되지 않은 행동들에 대해 공평한 기회를 제공하기 위함입니다.
- **update_rewards**: 각 턴이 지날 때마다 보상을 지수적으로 감소시키는 함수입니다. `decay_rate` (0.005)는 감소율을 결정하며, 이는 에이전트가 초기에 더 많은 탐색을 하고 시간이 지남에 따라 탐색보다는 활용을 더 많이 하도록 유도합니다. 최소 보상은 0.00001로 설정되어 있어 완전히 보상이 사라지지 않도록 합니다.

위 두 함수를 통해 reward를 매 Turn마다 업데이트 합니다.

## 코드 설명

step 함수를 통해 게임을 진행하고 q table을 업데이트합니다. 크게 **init,** step, reset으로 구성됩니다.

```bash
pip install -r requirements.txt
```

위 명령어를 통해 환경을 구축할 수 있습니다. main 함수를 실행해 결과를 확인할 수 있습니다.

```python
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
```

```python
def step(
        self, action: ActType
) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
    # turn 횟수를 count합니다.
    self.turn_no += 1
    # 덱 맨 위에 있는 card입니다.
    card_open = self.turn.card_open
    bold(f'\n---------- TURN {self.turn_no} ----------')
    print(f'\nCurrent open card: {self.turn.card_open.print_card()}')

		# 순서 로직
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
    
    # action을 수행합니다.
    self.turn.action(
        player=player_act,
        opponent=player_pas,
        agent=self.agent,
        algorithm=config.params['algorithm'],
        turn_no=self.turn_no
    )
```

```python
def reset(
    self,
    *,
    seed: int | None = None,
    options: dict[str, Any] | None = None,
) -> tuple[ObsType, dict[str, Any]]:

    self.player_1 = Player(config.player_name_1, agent=self.agent)
    self.player_2 = Player(config.player_name_2, agent=self.agent)
		
		# Deck을 초기화합니다.
    self.turn = Turn(
        deck=Deck(),
        player_1=self.player_1,
        player_2=self.player_2,
        agent=self.agent
    )
		
		# 순서 로직
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
```

## 최종 결과

10000번의 에피소드를 실행하였습니다. Human player는 랜덤으로 action을 선택한 경우를 말합니다. 에피소드마다 AI (agent)는 Human (random)과 대결합니다.

### Monte-Carlo

![coverageq](https://github.com/cshooon/Do_yoUNO2/assets/113033780/68d4728d-30b6-4f01-8cfe-50abb2fd9333)

이 그래프는 몬테 카를로 방법을 사용하여 학습하는 동안 Q-table에 존재하는 비-제로(non-zero) 항목의 수가 에피소드를 거치면서 어떻게 변하는지 보여줍니다. 초기에는 급격한 상승을 보이며, 점차 학습이 진행됨에 따라 증가 속도가 둔화됩니다. 이는 에이전트가 새로운 상태와 행동 조합을 탐색하면서 학습을 확장하고 있음을 나타냅니다.

![win_rate2](https://github.com/cshooon/Do_yoUNO2/assets/113033780/a4cc9466-1e86-4aa9-9cd1-26bce699d199)

이 그래프는 몬테 카를로 방법을 사용할 때 인공지능(AI) 에이전트와 인간 플레이어의 승률이 에피소드에 따라 어떻게 변하는지 보여줍니다. AI의 승률이 초기에 급격히 상승한 후 안정되며, 인간 플레이어의 승률은 점차 감소하여 안정됩니다. 승률이 0.5를 넘지만 차이가 크지 않습니다.

### Q-learning

![coverage](https://github.com/cshooon/Do_yoUNO2/assets/113033780/d7d8a28a-b844-45be-9675-100b4d4c6f59)

이 그래프는 Q-learning 방법을 사용하는 동안 Q-table의 커버리지가 어떻게 변하는지 보여줍니다. 몬테 카를로 방법과 유사한 추세를 보이며, 에피소드가 진행됨에 따라 느리지만 꾸준히 증가합니다. 이는 Q-learning이 계속해서 새로운 상태를 탐색하고 학습을 확장하고 있음을 의미합니다.

![win_rate](https://github.com/cshooon/Do_yoUNO2/assets/113033780/e3f36b96-94ce-4d21-a69b-ec470d5e60bf)

이 그래프는 Q-러닝을 사용할 때 AI와 인간 플레이어의 승률이 어떻게 변하는지 보여줍니다. AI의 승률이 초기에 급격하게 상승하고 이후 안정적으로 유지되는 반면, 인간 플레이어의 승률은 감소하며 일정한 수준으로 안정화됩니다. 마찬가지로, 승률이 0.5를 넘지만 Human(랜덤) 차이가 크지 않습니다.

## 보완점

random으로 가능한 action을 골랐을 때보다 승률이 높지만 크게 차이가 나이 않는 것은 UNO 게임이 랜덤으로 덱을 섞고 카드를 받기 때문입니다. 승률 60%를 목표로 다음과 같이 보완할 예정입니다.

**UNO 규칙 통합**

현재 모델은 플레이어가 한 장의 카드만 남았을 때 'UNO'를 호출해야 하는 중요한 규칙을 고려하지 않고 있습니다. 이를 개선하기 위해 상태 공간을 확장하여 플레이어가 카드를 한 장만 남겼을 때 이를 인지할 수 있도록 하며, 이 상태에서 'UNO'를 성공적으로 호출하면 추가 보상을 제공하고 실패 시 패널티를 부과합니다. 이는 에이전트가 게임의 규칙을 더 정확히 이해하고 준수하도록 유도할 것입니다.

**에피소드 수 확장**

현재 10,000개의 에피소드로는 모델이 충분히 학습하기에 제한적입니다. 학습 데이터의 양을 늘려 알고리즘의 성능을 개선할 수 있도록 컴퓨팅 리소스를 확대하고, 에피소드 수를 증가시킬 필요가 있습니다. 또한, 여러 에이전트가 동시에 학습할 수 있도록 병렬 처리 시스템을 도입함으로써 에피소드 처리 속도와 효율성을 크게 향상시킬 수 있습니다.

**A3C 알고리즘 적용**

A3C (Asynchronous Advantage Actor-Critic) 알고리즘의 적용은 복수의 에이전트가 독립적으로 학습하면서 전체적인 학습 프로세스를 가속화합니다. 이 방법은 각 에이전트가 비동기적으로 경험을 수집하고, 중앙 집중식 서버에 업데이트를 제공함으로써 보다 효과적으로 최적의 정책을 학습합니다. 게임 상황이 다양한 UNO에 적합할 것이라고 예상됩니다.
