
from otree.api import (
    Currency,
    cu,
    currency_range,
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    ExtraModel,
    WaitPage,
    Page,
    read_csv,
)

import units
import shared_out

doc = ''
class C(BaseConstants):
    # built-in constants
    NAME_IN_URL = 'hiring_funnel'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 12
    # user-defined constants
    NUM_CANDIDATES = 10
    MU = 50
    SIGMA = 15
    SIGMA_RESUME = 15
    SIGMA_ZOOM = 15
    SIGMA_INPERSON = 15
    DEFAULT_REWARD = 4.0
    BONUS_RATE = 0.05
    MAX_REWARD = 10
    GATE1_SELECT = 5
    GATE2_SELECT = 3
    CANDIDATE_LABELS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    Q111_instructions_willing = models.IntegerField(
        label='Sometimes survey takers rush through the questions without reading any instructions. Doing that ruins our results. Are you willing to read the instructions on the next pages?',
        choices=[
            (1, 'No'),
            (2, 'Yes'),
        ],
        widget=widgets.RadioSelect
    )
    Q139_condition_choice = models.IntegerField(
        label='Which condition you do want to test?',
        choices=[
            (1, 'Condition 1 (Single-stage screening)'),
            (2, 'Condition 2 (Multi-stage screening)'),
        ],
        widget=widgets.RadioSelect
    )
    gate1_selected = models.LongStringField()
    gate2_selected = models.LongStringField()
    final_hire = models.StringField()
    hired_true_quality = models.IntegerField()
    reward_string = models.StringField()
# built-in hook function(s) (called automatically by oTree)
# <hook-functions>
def creating_session(subsession: Subsession):
    
    import json
    import random
    for player in subsession.get_players():
        participant = player.participant
        if subsession.round_number == 1:
            if 'condition' in subsession.session.config:
                participant.condition = subsession.session.config['condition']
            else:
                participant.condition = random.choice([1, 2])
            practice_data = generate_candidate_data()
            participant.practice_data_json = json.dumps(practice_data)
            main_data = []
            for _ in range(C.NUM_ROUNDS):
                main_data.append(generate_candidate_data())
            participant.main_data_json = json.dumps(main_data)
            participant.history_json = json.dumps([])
    
# </hook-functions>
# the below function(s) are user-defined, not called by oTree
# <helper-functions>
def generate_candidate_data():
    
    import random
    result = {}
    for i in range(C.NUM_CANDIDATES):
        true_q = round(C.MU + random.gauss(0, 1) * C.SIGMA)
        true_q = max(0, true_q)
        resume = round(true_q + random.gauss(0, 1) * C.SIGMA_RESUME)
        resume = max(0, resume)
        zoom = round(true_q + random.gauss(0, 1) * C.SIGMA_ZOOM)
        zoom = max(0, zoom)
        inperson = round(true_q + random.gauss(0, 1) * C.SIGMA_INPERSON)
        inperson = max(0, inperson)
        result[C.CANDIDATE_LABELS[i]] = {
            'true_q': true_q,
            'resume': resume,
            'zoom': zoom,
            'inperson': inperson
        }
    return result
    
def calculate_reward(true_quality):
    
    reward = min(C.MAX_REWARD, C.DEFAULT_REWARD + C.BONUS_RATE * true_quality)
    return f"${reward:.2f}"
    
def get_history(participant):
    
    import json
    if participant.history_json:
        return json.loads(participant.history_json)
    return []
    
def add_to_history(participant, round_num, true_q, reward_str):
    
    import json
    history = get_history(participant)
    history.append({
        'round': round_num,
        'true_q': true_q,
        'reward': reward_str
    })
    participant.history_json = json.dumps(history)
    
def select_final_payment(participant):
    
    import random
    import json
    history = get_history(participant)
    main_rounds = [h for h in history if h['round'] > 0]
    if main_rounds:
        selected = random.choice(main_rounds)
        participant.selected_round = selected['round']
        participant.selected_reward_string = selected['reward']
        reward_float = float(selected['reward'].replace('$', ''))
        participant.payoff = cu(reward_float)
        main_data = json.loads(participant.main_data_json)
        round_data = main_data[selected['round'] - 1]
        for label, data in round_data.items():
            if data['true_q'] == selected['true_q']:
                participant.selected_candidate = label
                participant.selected_true_quality = selected['true_q']
                break
    
# </helper-functions>
class Consent(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        
        return player.round_number == 1
        
class Instructions(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        
        return player.round_number == 1
        
    @staticmethod
    def vars_for_template(player: Player):
        
        return dict(
            condition=player.participant.condition,
            is_funnel=player.participant.condition == 2
        )
        
class Comprehension(Page):
    form_model = 'player'
    form_fields = ['Q111_instructions_willing', 'Q139_condition_choice']
    @staticmethod
    def is_displayed(player: Player):
        
        return player.round_number == 1
        
class PracticeIntro(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        
        return player.round_number == 1
        
class PracticeGate1(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        pass
    @staticmethod
    def vars_for_template(player: Player):
        pass
class PracticeGate1After(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        pass
    @staticmethod
    def vars_for_template(player: Player):
        pass
class PracticeGate2(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        pass
    @staticmethod
    def vars_for_template(player: Player):
        pass
class PracticeGate2After(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        pass
    @staticmethod
    def vars_for_template(player: Player):
        pass
class PracticeGate3(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        pass
    @staticmethod
    def vars_for_template(player: Player):
        pass
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass
class PracticePerformance(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        pass
    @staticmethod
    def vars_for_template(player: Player):
        pass
class MainRoundGate1(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        pass
    @staticmethod
    def vars_for_template(player: Player):
        pass
class MainRoundGate1After(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        pass
    @staticmethod
    def vars_for_template(player: Player):
        pass
class MainRoundGate2(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        pass
    @staticmethod
    def vars_for_template(player: Player):
        pass
class MainRoundGate2After(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        pass
    @staticmethod
    def vars_for_template(player: Player):
        pass
class MainRoundGate3(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        pass
    @staticmethod
    def vars_for_template(player: Player):
        pass
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass
class MainRoundPerformance(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        pass
    @staticmethod
    def vars_for_template(player: Player):
        pass
class PostTaskWeights(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        pass
    @staticmethod
    def error_message(player: Player, values):
        pass
class Demographics(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        pass
class FinalPayoff(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        pass
    @staticmethod
    def vars_for_template(player: Player):
        pass
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass
page_sequence = [Consent, Instructions, Comprehension, PracticeIntro, PracticeGate1, PracticeGate1After, PracticeGate2, PracticeGate2After, PracticeGate3, PracticePerformance, MainRoundGate1, MainRoundGate1After, MainRoundGate2, MainRoundGate2After, MainRoundGate3, MainRoundPerformance, PostTaskWeights, Demographics, FinalPayoff]