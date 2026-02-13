
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
import json
import random

doc = ''
class C(BaseConstants):
    # built-in constants
    NAME_IN_URL = 'hiring_funnel'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 13  # 1 practice + 12 main
    # user-defined constants
    NUM_MAIN_ROUNDS = 12
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
    # Demo choice
    demo_choice = models.IntegerField(
        label='Which condition would you like to explore?',
        choices=[
            (1, 'Condition 1: One-Time Selection'),
            (2, 'Condition 2: Multi-Stage Funnel'),
        ],
        widget=widgets.RadioSelect
    )
    
    # Comprehension check questions
    Q111_instructions_willing = models.IntegerField(
        label='Sometimes survey takers rush through the questions without reading any instructions. Doing that ruins our results. Are you willing to read the instructions on the next pages?',
        choices=[
            (1, 'No'),
            (2, 'Yes'),
        ],
        widget=widgets.RadioSelect
    )
    
    Q_ultimate_mission = models.IntegerField(
        label='What is your ultimate mission in every single hiring case?',
        choices=[
            (1, 'To pick the candidate with the best Resume score.'),
            (2, 'To pick the candidate with the highest True Quality.'),
            (3, 'To pick the candidate I would want to have a beer with.'),
            (4, 'To pick randomly and finish quickly.'),
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    
    Q_decision_process = models.IntegerField(
        label='How will you make hiring decisions in this study?',
        choices=[
            (1, 'I will only see the Resume scores and must choose a hire.'),
            (2, 'I will see only the In-Person Interview scores and must choose a hire.'),
            (3, 'I will see scores across all three stages (Resume, Zoom, In-Person) and then choose one hire.'),
            (4, 'I must eliminate candidates based on their Resume before seeing any other scores.'),
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    
    Q_score_interpretation = models.IntegerField(
        label='How should you interpret the scores (Resume, Zoom, In-Person) you see?',
        choices=[
            (1, 'They are noisy clues that are usually helpful, but sometimes wrong.'),
            (2, 'They are perfect facts. I can always trust them 100%.'),
            (3, 'They are useless. I should just guess the true quality by rules of thumb.'),
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    
    Q_bonus_calculation = models.IntegerField(
        label='How is your final cash bonus calculated?',
        choices=[
            (1, 'It is the AVERAGE true quality of all 12 people I hired.'),
            (2, 'It depends on the true quality of the ONE random hire I made during the study.'),
            (3, 'It depends only on the true quality of the very LAST candidate I hire in the final round.'),
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    
    Q_advance_candidate = models.IntegerField(
        label='What happens when you advance a candidate to the next round?',
        choices=[
            (1, 'I immediately hire them.'),
            (2, 'I get more information (a new score) about them.'),
            (3, 'Their previous scores are deleted.'),
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    
    # Comprehension error attempt counters
    Q111_instructions_willing_errors = models.IntegerField(default=0, help_text="Count of incorrect attempts for Q111_instructions_willing")
    Q_ultimate_mission_errors = models.IntegerField(default=0, help_text="Count of incorrect attempts for Q_ultimate_mission")
    Q_score_interpretation_errors = models.IntegerField(default=0, help_text="Count of incorrect attempts for Q_score_interpretation")
    Q_decision_process_errors = models.IntegerField(default=0, help_text="Count of incorrect attempts for Q_decision_process")
    Q_advance_candidate_errors = models.IntegerField(default=0, help_text="Count of incorrect attempts for Q_advance_candidate")
    Q_bonus_calculation_errors = models.IntegerField(default=0, help_text="Count of incorrect attempts for Q_bonus_calculation")
    
    # Practice round data (per round stored at participant level, but accessible here)
    practice_hired_candidate = models.StringField(blank=True)
    practice_hired_trueq = models.IntegerField(blank=True)
    practice_reward = models.StringField(blank=True)
    
    # Main round decision data (per round)
    gate1_choices = models.LongStringField(blank=True, help_text="JSON list of candidates selected at Gate 1")
    gate2_choices = models.LongStringField(blank=True, help_text="JSON list of candidates selected at Gate 2")
    hired_candidate = models.StringField(blank=True, help_text="Final hired candidate label (A-J)")
    hired_trueq = models.IntegerField(blank=True)
    reward_str = models.StringField(blank=True, help_text="Currency string for this round")
    
    # Post-task survey
    resume_weight = models.IntegerField(blank=True, min=0, max=100)
    zoom_weight = models.IntegerField(blank=True, min=0, max=100)
    inperson_weight = models.IntegerField(blank=True, min=0, max=100)
    open_ended_explanation = models.LongStringField(blank=True)
    
    # Demographics
    has_hiring_experience = models.IntegerField(
        label='Do you have any experience with a real-world hiring task?',
        choices=[
            (1, 'Yes, I have.'),
            (2, 'No, I don\'t.'),
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    
    hiring_experience_type = models.StringField(
        label='Which of these describe your hiring experience the best?',
        choices=[
            ('it', 'Hiring in an IT company'),
            ('academic', 'Faculty hiring in an academic school'),
            ('other', 'None of these: Please describe it.'),
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    
    hiring_experience_other = models.LongStringField(
        label='Please describe your hiring experience:',
        blank=True
    )
    
    age_range = models.StringField(
        label='What is your age range?',
        choices=[
            ('18-25', '18-25'),
            ('26-35', '26-35'),
            ('36-45', '36-45'),
            ('45+', '45+'),
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    
    gender = models.StringField(
        label='What is your gender?',
        choices=[
            ('female', 'Female'),
            ('male', 'Male'),
            ('unwilling', 'Unwilling to respond'),
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    
    device_type = models.StringField(
        label='On what type of device are you completing this survey?',
        choices=[
            ('computer', 'Computer'),
            ('smartphone', 'Smart Phone'),
            ('tablet', 'Tablet'),
            ('other', 'Other'),
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    
    survey_comments = models.LongStringField(
        label='Do you have comments for us about this survey?',
        blank=True
    )

# built-in hook function(s) (called automatically by oTree)
# <hook-functions>
def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        participant = player.participant
        if subsession.round_number == 1:
            # Initialize condition if not already set
            # DemoChoice page will set this after user selects their condition
            if 'condition' not in participant.vars:
                participant.condition = 1  # Default to condition 1, will be overwritten by DemoChoice if needed
            
            # Generate practice data (will be done after condition is set, defaulting to 10 candidates)
            practice_data = generate_candidate_data()
            participant.practice_data_json = json.dumps(practice_data)
            
            # Store practice candidate labels for condition 1 (random 3 out of 10)
            practice_labels = random.sample(list(C.CANDIDATE_LABELS), 3)
            participant.vars['practice_c1_labels'] = practice_labels
            
            # Generate main round data (12 rounds)
            main_data = []
            main_c1_labels = []
            for _ in range(C.NUM_MAIN_ROUNDS):
                main_data.append(generate_candidate_data())
                # Generate random 3 candidates for each main round in condition 1
                main_c1_labels.append(random.sample(list(C.CANDIDATE_LABELS), 3))
            participant.main_data_json = json.dumps(main_data)
            participant.vars['main_c1_labels'] = main_c1_labels
            
            # Initialize history tracking
            participant.history_json = json.dumps([])
            
            # Initialize selected round/payment fields
            participant.selected_round = 0
            participant.selected_candidate = ''
            participant.selected_true_quality = 0
            participant.selected_reward_string = '$0.00'
    
# </hook-functions>

# the below function(s) are user-defined, not called by oTree
# <helper-functions>

def generate_candidate_data():
    """Generate data for 10 candidates with true quality and noisy scores."""
    result = {}
    for i in range(C.NUM_CANDIDATES):
        true_q = round(C.MU + random.gauss(0, 1) * C.SIGMA)
        true_q = max(0, true_q)
        
        # Generate noisy scores
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
    """Calculate reward based on true quality of hired candidate."""
    reward = C.DEFAULT_REWARD + C.BONUS_RATE * true_quality
    reward = min(C.MAX_REWARD, reward)  # Cap at MAX_REWARD
    reward = max(C.DEFAULT_REWARD, reward)  # Floor at DEFAULT_REWARD
    return f"${reward:.2f}"

def get_history(participant):
    """Get accumulated history of decisions."""
    if participant.history_json:
        return json.loads(participant.history_json)
    return []

def add_to_history(participant, round_num, hired_candidate, true_q, reward_str):
    """Add a decision to the history."""
    history = get_history(participant)
    history.append({
        'round': round_num,
        'hired_candidate': hired_candidate,
        'true_q': true_q,
        'reward': reward_str
    })
    participant.history_json = json.dumps(history)

def select_final_payment(participant):
    """Select one main round for final payment."""
    history = get_history(participant)
    main_rounds = [h for h in history if h['round'] > 0]
    if main_rounds:
        selected = random.choice(main_rounds)
        participant.selected_round = selected['round']
        participant.selected_reward_string = selected['reward']
        reward_float = float(selected['reward'].replace('$', ''))
        # Ensure reward doesn't exceed MAX_REWARD
        reward_float = min(C.MAX_REWARD, reward_float)
        participant.payoff = cu(reward_float)
        participant.selected_candidate = selected['hired_candidate']
        participant.selected_true_quality = selected['true_q']

def get_round_data(participant, round_num=None):
    """Get candidate data for a specific round (practice=0, main=1-12)."""
    if round_num is None or round_num == 0:
        return json.loads(participant.practice_data_json)
    else:
        main_data = json.loads(participant.main_data_json)
        index = round_num - 1
        if index >= len(main_data):
            # Extend main data if rounds were increased after session creation
            while len(main_data) <= index:
                main_data.append(generate_candidate_data())
            participant.main_data_json = json.dumps(main_data)
        return main_data[index]

def get_c1_candidate_labels(participant, round_num=None):
    """Get the 3 random candidate labels for condition 1 for a specific round (practice=0, main=1-12)."""
    if round_num is None or round_num == 0:
        # Handle missing practice_c1_labels (for backward compatibility with existing participants)
        if 'practice_c1_labels' not in participant.vars:
            practice_labels = random.sample(list(C.CANDIDATE_LABELS), 3)
            participant.vars['practice_c1_labels'] = practice_labels
        return participant.vars['practice_c1_labels']
    else:
        # Handle missing main_c1_labels (for backward compatibility with existing participants)
        if 'main_c1_labels' not in participant.vars:
            # Generate labels for all main rounds
            main_c1_labels = [random.sample(list(C.CANDIDATE_LABELS), 3) for _ in range(C.NUM_MAIN_ROUNDS)]
            participant.vars['main_c1_labels'] = main_c1_labels
        
        main_c1_labels = participant.vars['main_c1_labels']
        index = round_num - 1
        if index >= len(main_c1_labels):
            # Extend labels if rounds were increased after session creation
            while len(main_c1_labels) <= index:
                main_c1_labels.append(random.sample(list(C.CANDIDATE_LABELS), 3))
            participant.vars['main_c1_labels'] = main_c1_labels
        return main_c1_labels[index]

def get_round_data_for_condition(participant, round_num, condition):
    """Get candidate data filtered for the specified condition.
    For condition 1: Returns only 3 randomly selected candidates.
    For condition 2: Returns all 10 candidates."""
    all_data = get_round_data(participant, round_num)
    
    if condition == 1:
        # Get the 3 selected labels for this round
        selected_labels = get_c1_candidate_labels(participant, round_num)
        # Filter to only include selected candidates
        filtered_data = {label: all_data[label] for label in selected_labels}
        return filtered_data, selected_labels
    else:
        # Return all 10 candidates in their original order
        return all_data, list(C.CANDIDATE_LABELS)

def calculate_progress_percentage(player: 'BasePlayer', page_name: str = '') -> int:
    """Calculate condition-aware progress through the study as a percentage.
    Tracks progress page-by-page for accurate progress display."""
    condition = get_condition(player)
    round_num = player.round_number
    
    # Define page order for each condition in Round 1
    round1_pages_both = ['Consent', 'PreInstructionsDisclaimer', 'InstructionsPart1', 'Instructions', 'Comprehension', 'PracticeIntro']
    round1_pages_c1 = ['PracticeStage1Resume', 'PracticeStage2Zoom', 'PracticeStage3Decision', 'PracticePerformance']
    round1_pages_c2 = ['PracticeGate1', 'PracticeGate1After', 'PracticeGate2', 'PracticeGate2After', 'PracticeGate3', 'PracticePerformance']
    
    # Main round pages (rounds 2-13)
    main_pages_c1 = ['MainStage1Resume', 'MainStage2Zoom', 'MainStage3Decision', 'MainRoundPerformance']
    main_pages_c2 = ['MainGate1', 'MainGate1After', 'MainGate2', 'MainGate2After', 'MainGate3', 'MainRoundPerformance']
    
    # Final pages (round 13 only)
    final_pages = ['PostTaskWeights', 'Demographics', 'FinalPayoff']
    
    pages_completed = 0
    
    if condition == 1:
        total_pages = 62  # 6+5 (round1) + 4*12 (main) + 3 (final)
        
        if round_num == 1:
            # Count pages in round 1
            all_round1_pages = round1_pages_both + round1_pages_c1
            if page_name in all_round1_pages:
                pages_completed = all_round1_pages.index(page_name) + 1
            else:
                pages_completed = len(all_round1_pages)
        elif round_num <= 13:
            # Completed round 1, now in main rounds
            pages_completed = 11  # All of round 1
            main_round = round_num - 1  # rounds 2-13 map to main 1-12
            
            # Add completed main rounds
            pages_completed += (main_round - 1) * 4
            
            # Add current page within this round
            if page_name in main_pages_c1:
                pages_completed += main_pages_c1.index(page_name) + 1
            elif page_name in final_pages and round_num == 13:
                pages_completed += 4  # All main round pages
                pages_completed += final_pages.index(page_name) + 1
            else:
                pages_completed += 4  # Assume at end of round
        else:
            pages_completed = total_pages
    else:
        total_pages = 88  # 6+7 (round1) + 6*12 (main) + 3 (final)
        
        if round_num == 1:
            all_round1_pages = round1_pages_both + round1_pages_c2
            if page_name in all_round1_pages:
                pages_completed = all_round1_pages.index(page_name) + 1
            else:
                pages_completed = len(all_round1_pages)
        elif round_num <= 13:
            pages_completed = 13  # All of round 1
            main_round = round_num - 1
            
            pages_completed += (main_round - 1) * 6
            
            if page_name in main_pages_c2:
                pages_completed += main_pages_c2.index(page_name) + 1
            elif page_name in final_pages and round_num == 13:
                pages_completed += 6
                pages_completed += final_pages.index(page_name) + 1
            else:
                pages_completed += 6
        else:
            pages_completed = total_pages
    
    progress = int((pages_completed / total_pages) * 100)
    return max(0, min(progress, 100))

def get_condition(player: 'BasePlayer'):
    """Safely get participant's condition choice across rounds."""
    stored = player.participant.vars.get('condition')
    if stored is not None:
        return stored
    return player.field_maybe_none('demo_choice')

# </helper-functions>

class BasePage(Page):
    """Base page class that automatically includes progress percentage."""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_name = self.__class__.__name__
        context['progress_percentage'] = calculate_progress_percentage(self.player, page_name)
        return context

class DemoChoice(BasePage):
    """Demo selection page - allows user to choose which condition to preview"""
    form_model = 'player'
    form_fields = ['demo_choice']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    def vars_for_template(self):
        return {
            'condition_1_description': 'Single-Stage Screening: You will see all 10 candidates with just their Resume scores. You select 1 candidate to hire based on this information.',
            'condition_2_description': 'Multi-Stage Funnel: You will screen candidates through 3 gates. Gate 1: Review 10 Resume scores, select 5 to advance. Gate 2: Review selected candidates\' Zoom scores, select 3 to advance. Gate 3: Review all scores for final 3, select 1 to hire.',
        }
    
    def form_valid(self):
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        choice = player.field_maybe_none('demo_choice')
        if choice is not None:
            player.participant.vars['condition'] = choice
            player.participant.condition = choice

class Consent(BasePage):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class PreInstructionsDisclaimer(BasePage):
    form_model = 'player'
    form_fields = ['Q111_instructions_willing']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    @staticmethod
    def error_message(player: Player, values):
        if values.get('Q111_instructions_willing') != 2:
            player.Q111_instructions_willing_errors += 1
            return 'Please confirm that you are willing to read the instructions.'

class InstructionsPart1(BasePage):
    form_model = 'player'
    form_fields = ['Q_ultimate_mission']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        condition = get_condition(player)
        return dict(
            is_condition_1=condition == 1,
            is_condition_2=condition == 2,
            mu=C.MU,
            sigma=C.SIGMA,
            sigma_resume=C.SIGMA_RESUME
        )
    
    @staticmethod
    def error_message(player: Player, values):
        if values.get('Q_ultimate_mission') and values['Q_ultimate_mission'] != 2:
            player.Q_ultimate_mission_errors += 1
            return 'Please review your ultimate goal. You should aim to hire the candidate with the highest True Quality.'

class Instructions(BasePage):
    form_model = 'player'
    form_fields = ['Q_score_interpretation']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        condition = get_condition(player)
        return dict(
            is_condition_1=condition == 1,
            is_condition_2=condition == 2,
            mu=C.MU,
            sigma=C.SIGMA,
            sigma_resume=C.SIGMA_RESUME
        )
    
    @staticmethod
    def error_message(player: Player, values):
        if values.get('Q_score_interpretation') and values['Q_score_interpretation'] != 1:
            player.Q_score_interpretation_errors += 1
            return 'Please review the instructions about how to interpret scores. Scores are noisy signals, not perfect information.'

class Comprehension(BasePage):
    form_model = 'player'
    
    @staticmethod
    def get_form_fields(player: Player):
        condition = get_condition(player)
        if condition == 1:
            return ['Q_decision_process', 'Q_bonus_calculation']
        else:  # condition == 2
            return ['Q_advance_candidate', 'Q_bonus_calculation']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            is_condition_1=get_condition(player) == 1,
            is_condition_2=get_condition(player) == 2
        )
    
    @staticmethod
    def error_message(player: Player, values):
        condition = get_condition(player)
        
        # Check Q_bonus_calculation (must be "ONE random hire")
        if values.get('Q_bonus_calculation') and values['Q_bonus_calculation'] != 2:
            player.Q_bonus_calculation_errors += 1
            return 'Please review how your bonus is calculated. It depends on ONE randomly selected round, not an average or the last round.'
        
        # Condition 1 specific validation
        if condition == 1:
            if values.get('Q_decision_process') and values['Q_decision_process'] != 3:
                player.Q_decision_process_errors += 1
                return 'Please review the decision process. You will see scores across all three stages and then choose one hire.'
        
        # Condition 2 specific validation
        if condition == 2:
            if values.get('Q_advance_candidate') and values['Q_advance_candidate'] != 2:
                player.Q_advance_candidate_errors += 1
                return 'Please review what happens when you advance a candidate. You get more information (a new score) about them.'

class PracticeIntro(BasePage):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            is_condition_1=get_condition(player) == 1
        )

# Practice Round Pages - Condition 1 (Single-stage)
class PracticeStage1Resume(BasePage):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and get_condition(player) == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        condition = get_condition(player)
        data, labels = get_round_data_for_condition(player.participant, 0, condition)
        candidates = []
        for label in labels:
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': '-',
                'inperson': '-'
            })
        return dict(
            candidates=candidates,
            is_practice=True,
            round_num=0
        )

class PracticeStage2Zoom(BasePage):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and get_condition(player) == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        condition = get_condition(player)
        data, labels = get_round_data_for_condition(player.participant, 0, condition)
        candidates = []
        for label in labels:
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': data[label]['zoom'],
                'inperson': '-'
            })
        return dict(
            candidates=candidates,
            is_practice=True,
            round_num=0
        )

class PracticeStage3Decision(BasePage):
    form_model = 'player'
    form_fields = ['hired_candidate']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and get_condition(player) == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        condition = get_condition(player)
        data, labels = get_round_data_for_condition(player.participant, 0, condition)
        candidates = []
        for label in labels:
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': data[label]['zoom'],
                'inperson': data[label]['inperson'],
                'true_q': data[label]['true_q']
            })
        return dict(
            candidates=candidates,
            is_practice=True,
            round_num=0
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        condition = get_condition(player)
        data, _ = get_round_data_for_condition(player.participant, 0, condition)
        hired_label = player.hired_candidate
        hired_data = data[hired_label]
        true_q = hired_data['true_q']
        reward_str = calculate_reward(true_q)
        
        # Store practice results
        player.practice_hired_candidate = hired_label
        player.practice_hired_trueq = true_q
        player.practice_reward = reward_str
        
        # Add to history (round 0 = practice)
        add_to_history(player.participant, 0, hired_label, true_q, reward_str)

class PracticePerformance(BasePage):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            hired_candidate=player.field_maybe_none('practice_hired_candidate') or '',
            last_round_true_q=player.field_maybe_none('practice_hired_trueq') or 0,
            reward=player.field_maybe_none('practice_reward') or ''
        )


# Main Round Pages - Condition 1 (Single-stage)
class MainStage1Resume(BasePage):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return get_condition(player) == 1 and player.round_number > 1
    
    @staticmethod
    def vars_for_template(player: Player):
        condition = get_condition(player)
        data, labels = get_round_data_for_condition(player.participant, player.round_number, condition)
        candidates = []
        for label in labels:
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': '-',
                'inperson': '-'
            })
        return dict(
            candidates=candidates,
            round_num=player.round_number - 1
        )

class MainStage2Zoom(BasePage):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return get_condition(player) == 1 and player.round_number > 1
    
    @staticmethod
    def vars_for_template(player: Player):
        condition = get_condition(player)
        data, labels = get_round_data_for_condition(player.participant, player.round_number, condition)
        candidates = []
        for label in labels:
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': data[label]['zoom'],
                'inperson': '-'
            })
        return dict(
            candidates=candidates,
            round_num=player.round_number - 1
        )

class MainStage3Decision(BasePage):
    form_model = 'player'
    form_fields = ['hired_candidate']
    
    @staticmethod
    def is_displayed(player: Player):
        return get_condition(player) == 1 and player.round_number > 1
    
    @staticmethod
    def vars_for_template(player: Player):
        condition = get_condition(player)
        data, labels = get_round_data_for_condition(player.participant, player.round_number, condition)
        candidates = []
        for label in labels:
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': data[label]['zoom'],
                'inperson': data[label]['inperson'],
                'true_q': data[label]['true_q']
            })
        return dict(
            candidates=candidates,
            round_num=player.round_number - 1
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        condition = get_condition(player)
        data, _ = get_round_data_for_condition(player.participant, player.round_number, condition)
        hired_label = player.hired_candidate
        hired_data = data[hired_label]
        true_q = hired_data['true_q']
        reward_str = calculate_reward(true_q)
        
        player.hired_trueq = true_q
        player.reward_str = reward_str
        add_to_history(player.participant, player.round_number, hired_label, true_q, reward_str)

class MainRoundPerformance(BasePage):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number > 1
    
    @staticmethod
    def vars_for_template(player: Player):
        history = get_history(player.participant)
        # Filter to only show main rounds (exclude practice which has round == 0)
        main_history = [h for h in history if h['round'] > 0]
        
        # Adjust round numbers for display (convert from internal numbering to user-facing)
        for entry in main_history:
            entry['display_round'] = entry['round'] - 1
        
        last_item = main_history[-1] if main_history else None
        return dict(
            history=main_history,
            last_round_true_q=last_item['true_q'] if last_item else 0,
            round_num=player.round_number - 1
        )

# Funnel Condition Pages (Gate-based)
class PracticeGate1(BasePage):
    form_model = 'player'
    form_fields = ['gate1_choices']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and get_condition(player) == 2
    
    @staticmethod
    def vars_for_template(player: Player):
        data = get_round_data(player.participant, 0)
        candidates = []
        for label in C.CANDIDATE_LABELS:
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': '-',
                'inperson': '-'
            })
        form_error = player.session.vars.get('form_error_gate1', '')
        form_post_gate1_choices = player.session.vars.get('form_post_gate1_choices', [])
        return dict(
            candidates=candidates,
            is_practice=True,
            round_num=0,
            gate_num=1,
            required_count=C.GATE1_SELECT,
            form_error=form_error,
            form_post_gate1_choices=form_post_gate1_choices
        )

    @staticmethod
    def error_message(player: Player, values):
        gate1_raw = values.get('gate1_choices')
        try:
            gate1_choices = json.loads(gate1_raw) if gate1_raw else []
        except (json.JSONDecodeError, TypeError):
            gate1_choices = []

        if len(gate1_choices) != C.GATE1_SELECT:
            msg = f'Please select exactly {C.GATE1_SELECT} candidates.'
            player.session.vars['form_error_gate1'] = msg
            player.session.vars['form_post_gate1_choices'] = gate1_choices
            return msg

        player.session.vars['form_error_gate1'] = ''
        player.session.vars['form_post_gate1_choices'] = []
        player.gate1_choices = json.dumps(gate1_choices)
    


class PracticeGate1After(BasePage):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and get_condition(player) == 2
    
    @staticmethod
    def vars_for_template(player: Player):
        data = get_round_data(player.participant, 0)
        gate1_choices_json = player.field_maybe_none('gate1_choices')
        # Handle both JSON array format and plain string format
        if gate1_choices_json:
            try:
                gate1_choices = json.loads(gate1_choices_json)
            except (json.JSONDecodeError, TypeError):
                # If not JSON, treat as single string or empty
                gate1_choices = [gate1_choices_json] if isinstance(gate1_choices_json, str) and gate1_choices_json else []
        else:
            gate1_choices = []
        eliminated = [c for c in C.CANDIDATE_LABELS if c not in gate1_choices]
        candidates = []
        for label in C.CANDIDATE_LABELS:
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': '-',
                'inperson': '-',
                'eliminated': label in eliminated
            })
        return dict(
            candidates=candidates,
            gate1_choices=gate1_choices,
            is_practice=True,
            round_num=0,
            gate_num=1,
            advanced_count=len(gate1_choices)
        )

class PracticeGate2(BasePage):
    form_model = 'player'
    form_fields = ['gate2_choices']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and get_condition(player) == 2
    
    @staticmethod
    def vars_for_template(player: Player):
        data = get_round_data(player.participant, 0)
        gate1_choices_json = player.field_maybe_none('gate1_choices')
        gate1_choices = json.loads(gate1_choices_json) if gate1_choices_json else []
        eliminated = [c for c in C.CANDIDATE_LABELS if c not in gate1_choices]
        candidates = []
        for label in C.CANDIDATE_LABELS:
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': data[label]['zoom'],
                'inperson': '-',
                'eliminated': label in eliminated
            })
        available_candidates = gate1_choices
        form_error = player.session.vars.get('form_error_gate2', '')
        form_post_gate2_choices = player.session.vars.get('form_post_gate2_choices', [])
        return dict(
            candidates=candidates,
            available_candidates=available_candidates,
            is_practice=True,
            round_num=0,
            gate_num=2,
            required_count=C.GATE2_SELECT,
            form_error=form_error,
            form_post_gate2_choices=form_post_gate2_choices
        )

    @staticmethod
    def error_message(player: Player, values):
        gate2_raw = values.get('gate2_choices')
        try:
            gate2_choices = json.loads(gate2_raw) if gate2_raw else []
        except (json.JSONDecodeError, TypeError):
            gate2_choices = []

        if len(gate2_choices) != C.GATE2_SELECT:
            msg = f'Please select exactly {C.GATE2_SELECT} candidates.'
            player.session.vars['form_error_gate2'] = msg
            player.session.vars['form_post_gate2_choices'] = gate2_choices
            return msg

        gate1_choices_json = player.field_maybe_none('gate1_choices')
        if gate1_choices_json:
            try:
                gate1_choices = json.loads(gate1_choices_json)
            except (json.JSONDecodeError, TypeError):
                gate1_choices = [gate1_choices_json] if isinstance(gate1_choices_json, str) and gate1_choices_json else []
        else:
            gate1_choices = []

        if not all(c in gate1_choices for c in gate2_choices):
            msg = 'All selected candidates must be from Gate 1 selections.'
            player.session.vars['form_error_gate2'] = msg
            player.session.vars['form_post_gate2_choices'] = gate2_choices
            return msg

        player.session.vars['form_error_gate2'] = ''
        player.session.vars['form_post_gate2_choices'] = []
        player.gate2_choices = json.dumps(gate2_choices)


class PracticeGate2After(BasePage):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and get_condition(player) == 2 and player.field_maybe_none('gate2_choices') is not None
    
    @staticmethod
    def vars_for_template(player: Player):
        data = get_round_data(player.participant, 0)
        gate1_choices_json = player.field_maybe_none('gate1_choices')
        # Handle both JSON array format and plain string format
        if gate1_choices_json:
            try:
                gate1_choices = json.loads(gate1_choices_json)
            except (json.JSONDecodeError, TypeError):
                gate1_choices = [gate1_choices_json] if isinstance(gate1_choices_json, str) and gate1_choices_json else []
        else:
            gate1_choices = []
        
        gate2_choices_json = player.field_maybe_none('gate2_choices')
        # Handle both JSON array format and plain string format
        if gate2_choices_json:
            try:
                gate2_choices = json.loads(gate2_choices_json)
            except (json.JSONDecodeError, TypeError):
                gate2_choices = [gate2_choices_json] if isinstance(gate2_choices_json, str) and gate2_choices_json else []
        else:
            gate2_choices = []
        
        candidates = []
        for label in C.CANDIDATE_LABELS:
            eliminated = label not in gate2_choices
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': data[label]['zoom'],
                'inperson': '-',
                'eliminated': eliminated
            })
        return dict(
            candidates=candidates,
            gate2_choices=gate2_choices,
            is_practice=True,
            round_num=0,
            gate_num=2,
            advanced_count=len(gate2_choices)
        )

class PracticeGate3(BasePage):
    form_model = 'player'
    form_fields = ['hired_candidate']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and get_condition(player) == 2
    
    @staticmethod
    def vars_for_template(player: Player):
        data = get_round_data(player.participant, 0)
        gate2_choices = json.loads(player.gate2_choices) if player.gate2_choices else []
        candidates = []
        for label in C.CANDIDATE_LABELS:
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': data[label]['zoom'],
                'inperson': data[label]['inperson'],
                'true_q': data[label]['true_q'],
                'available': label in gate2_choices
            })
        return dict(
            candidates=candidates,
            available_candidates=gate2_choices,
            is_practice=True,
            round_num=0,
            gate_num=3
        )
    
    @staticmethod
    def error_message(player: Player, values):
        hired = values.get('hired_candidate')
        gate2_choices = json.loads(player.gate2_choices) if player.gate2_choices else []
        if hired and hired not in gate2_choices:
            return 'Selected candidate must be from Gate 2 selections.'
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        data = get_round_data(player.participant, 0)
        hired_label = player.hired_candidate
        hired_data = data[hired_label]
        true_q = hired_data['true_q']
        reward_str = calculate_reward(true_q)
        
        player.practice_hired_candidate = hired_label
        player.practice_hired_trueq = true_q
        player.practice_reward = reward_str
        add_to_history(player.participant, 0, hired_label, true_q, reward_str)

# Main Rounds - Condition 2 (Funnel)
class MainGate1(BasePage):
    form_model = 'player'
    form_fields = ['gate1_choices']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number > 1 and get_condition(player) == 2
    
    @staticmethod
    def vars_for_template(player: Player):
        data = get_round_data(player.participant, player.round_number)
        candidates = []
        for label in C.CANDIDATE_LABELS:
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': '-',
                'inperson': '-'
            })
        return dict(
            candidates=candidates,
            round_num=player.round_number - 1,
            gate_num=1,
            required_count=C.GATE1_SELECT,
            form_error=player.session.vars.get('form_error_gate1', ''),
            form_post_gate1_choices=player.session.vars.get('form_post_gate1_choices', [])
        )

    @staticmethod
    def error_message(player: Player, values):
        gate1_raw = values.get('gate1_choices')
        try:
            gate1_choices = json.loads(gate1_raw) if gate1_raw else []
        except (json.JSONDecodeError, TypeError):
            gate1_choices = []

        if len(gate1_choices) != C.GATE1_SELECT:
            msg = f'Please select exactly {C.GATE1_SELECT} candidates.'
            player.session.vars['form_error_gate1'] = msg
            player.session.vars['form_post_gate1_choices'] = gate1_choices
            return msg

        player.session.vars['form_error_gate1'] = ''
        player.session.vars['form_post_gate1_choices'] = []
        player.gate1_choices = json.dumps(gate1_choices)

class MainGate1After(BasePage):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number > 1 and get_condition(player) == 2 and player.field_maybe_none('gate1_choices') is not None
    
    @staticmethod
    def vars_for_template(player: Player):
        data = get_round_data(player.participant, player.round_number)
        gate1_choices_json = player.field_maybe_none('gate1_choices')
        # Handle both JSON array format and plain string format
        if gate1_choices_json:
            try:
                gate1_choices = json.loads(gate1_choices_json)
            except (json.JSONDecodeError, TypeError):
                gate1_choices = [gate1_choices_json] if isinstance(gate1_choices_json, str) and gate1_choices_json else []
        else:
            gate1_choices = []
        eliminated = [c for c in C.CANDIDATE_LABELS if c not in gate1_choices]
        candidates = []
        for label in C.CANDIDATE_LABELS:
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': '-',
                'inperson': '-',
                'eliminated': label in eliminated
            })
        return dict(
            candidates=candidates,
            gate1_choices=gate1_choices,
            round_num=player.round_number - 1,
            gate_num=1,
            advanced_count=len(gate1_choices)
        )

class MainGate2(BasePage):
    form_model = 'player'
    form_fields = ['gate2_choices']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number > 1 and get_condition(player) == 2 and player.field_maybe_none('gate1_choices') is not None
    
    @staticmethod
    def vars_for_template(player: Player):
        data = get_round_data(player.participant, player.round_number)
        gate1_choices_json = player.field_maybe_none('gate1_choices')
        gate1_choices = json.loads(gate1_choices_json) if gate1_choices_json else []
        eliminated = [c for c in C.CANDIDATE_LABELS if c not in gate1_choices]
        candidates = []
        for label in C.CANDIDATE_LABELS:
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': data[label]['zoom'],
                'inperson': '-',
                'eliminated': label in eliminated
            })
        return dict(
            candidates=candidates,
            available_candidates=gate1_choices,
            round_num=player.round_number - 1,
            gate_num=2,
            required_count=C.GATE2_SELECT,
            form_error=player.session.vars.get('form_error_gate2', ''),
            form_post_gate2_choices=player.session.vars.get('form_post_gate2_choices', [])
        )

    @staticmethod
    def error_message(player: Player, values):
        gate2_raw = values.get('gate2_choices')
        try:
            gate2_choices = json.loads(gate2_raw) if gate2_raw else []
        except (json.JSONDecodeError, TypeError):
            gate2_choices = []

        if len(gate2_choices) != C.GATE2_SELECT:
            msg = f'Please select exactly {C.GATE2_SELECT} candidates.'
            player.session.vars['form_error_gate2'] = msg
            player.session.vars['form_post_gate2_choices'] = gate2_choices
            return msg

        gate1_choices_json = player.field_maybe_none('gate1_choices')
        if gate1_choices_json:
            try:
                gate1_choices = json.loads(gate1_choices_json)
            except (json.JSONDecodeError, TypeError):
                gate1_choices = [gate1_choices_json] if isinstance(gate1_choices_json, str) and gate1_choices_json else []
        else:
            gate1_choices = []

        if not all(c in gate1_choices for c in gate2_choices):
            msg = 'All selected candidates must be from Gate 1 selections.'
            player.session.vars['form_error_gate2'] = msg
            player.session.vars['form_post_gate2_choices'] = gate2_choices
            return msg

        player.session.vars['form_error_gate2'] = ''
        player.session.vars['form_post_gate2_choices'] = []
        player.gate2_choices = json.dumps(gate2_choices)

class MainGate2After(BasePage):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number > 1 and get_condition(player) == 2 and player.field_maybe_none('gate2_choices') is not None
    
    @staticmethod
    def vars_for_template(player: Player):
        data = get_round_data(player.participant, player.round_number)
        gate1_choices_json = player.field_maybe_none('gate1_choices')
        # Handle both JSON array format and plain string format
        if gate1_choices_json:
            try:
                gate1_choices = json.loads(gate1_choices_json)
            except (json.JSONDecodeError, TypeError):
                gate1_choices = [gate1_choices_json] if isinstance(gate1_choices_json, str) and gate1_choices_json else []
        else:
            gate1_choices = []
        
        gate2_choices_json = player.field_maybe_none('gate2_choices')
        # Handle both JSON array format and plain string format
        if gate2_choices_json:
            try:
                gate2_choices = json.loads(gate2_choices_json)
            except (json.JSONDecodeError, TypeError):
                gate2_choices = [gate2_choices_json] if isinstance(gate2_choices_json, str) and gate2_choices_json else []
        else:
            gate2_choices = []
        
        candidates = []
        for label in C.CANDIDATE_LABELS:
            is_eliminated = label not in gate2_choices
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': data[label]['zoom'],
                'inperson': '-',
                'eliminated': is_eliminated
            })
        return dict(
            candidates=candidates,
            gate2_choices=gate2_choices,
            round_num=player.round_number - 1,
            gate_num=2,
            advanced_count=len(gate2_choices)
        )

class MainGate3(BasePage):
    form_model = 'player'
    form_fields = ['hired_candidate']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number > 1 and get_condition(player) == 2
    
    @staticmethod
    def vars_for_template(player: Player):
        data = get_round_data(player.participant, player.round_number)
        gate2_choices = json.loads(player.gate2_choices) if player.gate2_choices else []
        candidates = []
        for label in C.CANDIDATE_LABELS:
            candidates.append({
                'label': label,
                'resume': data[label]['resume'],
                'zoom': data[label]['zoom'],
                'inperson': data[label]['inperson'],
                'true_q': data[label]['true_q'],
                'available': label in gate2_choices
            })
        return dict(
            candidates=candidates,
            available_candidates=gate2_choices,
            round_num=player.round_number - 1,
            gate_num=3
        )
    
    @staticmethod
    def error_message(player: Player, values):
        hired = values.get('hired_candidate')
        gate2_choices = json.loads(player.gate2_choices) if player.gate2_choices else []
        if hired and hired not in gate2_choices:
            return 'Selected candidate must be from Gate 2 selections.'
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        data = get_round_data(player.participant, player.round_number)
        hired_label = player.hired_candidate
        hired_data = data[hired_label]
        true_q = hired_data['true_q']
        reward_str = calculate_reward(true_q)
        
        player.hired_trueq = true_q
        player.reward_str = reward_str
        add_to_history(player.participant, player.round_number, hired_label, true_q, reward_str)

# Post-task pages
class PostTaskWeights(BasePage):
    form_model = 'player'
    form_fields = ['resume_weight', 'zoom_weight', 'inperson_weight']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
    @staticmethod
    def error_message(player: Player, values):
        resume = values.get('resume_weight', 0) or 0
        zoom = values.get('zoom_weight', 0) or 0
        inperson = values.get('inperson_weight', 0) or 0
        total = resume + zoom + inperson
        if total != 100:
            return f'Weights must sum to 100. Current total: {total}'

class Demographics(BasePage):
    form_model = 'player'
    form_fields = ['has_hiring_experience', 'hiring_experience_type', 'hiring_experience_other', 'age_range', 'gender', 'device_type', 'survey_comments']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
    @staticmethod
    def error_message(player: Player, values):
        # All fields are required except survey_comments
        if not values.get('has_hiring_experience'):
            return 'Please indicate whether you have hiring experience.'
        
        # If they have experience, require experience type
        if values.get('has_hiring_experience') == 1:
            if not values.get('hiring_experience_type'):
                return 'Please select which type of hiring experience you have.'
            # If they selected "other", require description
            if values.get('hiring_experience_type') == 'other' and not values.get('hiring_experience_other'):
                return 'Please describe your hiring experience.'
        
        if not values.get('age_range'):
            return 'Please select your age range.'
        
        if not values.get('gender'):
            return 'Please select your gender.'
        
        if not values.get('device_type'):
            return 'Please select the device type you are using.'

class FinalPayoff(BasePage):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        select_final_payment(player.participant)
    
    @staticmethod
    def vars_for_template(player: Player):
        if not player.participant.selected_round:
            select_final_payment(player.participant)
        # Set player payoff for display
        if player.participant.payoff and not player.payoff:
            player.payoff = player.participant.payoff
        return dict(
            selected_round=player.participant.selected_round,
            selected_candidate=player.participant.selected_candidate,
            selected_true_q=player.participant.selected_true_quality,
            selected_reward=player.participant.selected_reward_string,
            payoff=player.participant.payoff
        )

page_sequence = [
    DemoChoice,
    Consent,
    PreInstructionsDisclaimer,
    InstructionsPart1,
    Instructions,
    Comprehension,
    PracticeIntro,
    # Condition 1 Practice
    PracticeStage1Resume,
    PracticeStage2Zoom,
    PracticeStage3Decision,
    # Condition 2 Practice
    PracticeGate1,
    PracticeGate1After,
    PracticeGate2,
    PracticeGate2After,
    PracticeGate3,
    # Both conditions practice performance
    PracticePerformance,
    # Condition 1 Main
    MainStage1Resume,
    MainStage2Zoom,
    MainStage3Decision,
    # Condition 2 Main
    MainGate1,
    MainGate1After,
    MainGate2,
    MainGate2After,
    MainGate3,
    # Both conditions main performance
    MainRoundPerformance,
    # Post-task
    PostTaskWeights,
    Demographics,
    FinalPayoff,
]
