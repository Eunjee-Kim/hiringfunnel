# Information Usage in Multi-Stage Hiring Funnels - oTree Implementation

## Overview

This oTree application implements a hiring funnel study with two experimental conditions:

1. **Condition 1 (Single-stage screening):** Participants see all three interview scores (Resume, Zoom, In-Person) progressively revealed across three stages before making a hiring decision.

2. **Condition 2 (Multi-stage funnel):** Participants make sequential screening decisions at three gates (Gate 1 at Resume, Gate 2 at Zoom, Gate 3 at In-Person), eliminating candidates at each stage.

## Setup & Running

### Prerequisites
- oTree 5.x
- Python 3.6+
- virtualenv (recommended)

### Installation

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install oTree
pip install otree

# Install dependencies for this app
cd hiring_funnel
pip install -r requirements.txt  # if exists
```

### Running the Study

```bash
# From the project root directory
otree runserver

# Access at http://localhost:8000
```

### Configuration

#### Setting the Condition

**Option 1: URL Parameter**
Pass `?cond=1` or `?cond=2` when accessing the study:
- `http://localhost:8000/create_session/hiring_funnel?cond=1` → Condition 1
- `http://localhost:8000/create_session/hiring_funnel?cond=2` → Condition 2

**Option 2: Session Configuration**
Edit the session config in `settings.py`:

```python
SESSION_CONFIGS = [
    dict(
        name='hiring_funnel',
        display_name='Hiring Funnel Study',
        num_demo_participants=1,
        condition=1,  # 1 for single-stage, 2 for funnel
    ),
]
```

**Option 3: Random Assignment**
Leave the condition unspecified in config, and it will be randomly assigned to each participant.

## Study Structure

### Pages Overview

#### 1. Intro & Consent (Round 1 only)
- **Consent:** Standard consent form
- **Instructions:** Study overview with parameter summary
- **Comprehension:** Two questions assessing understanding

#### 2. Practice Round (Round 1)
- **Condition 1 Flow:** Stage 1 Resume → Stage 2 Zoom → Stage 3 Decision
- **Condition 2 Flow:** Gate 1 Select 5 → Gate 1 After → Gate 2 Select 3 → Gate 2 After → Gate 3 Select 1
- **Performance:** Summary table showing practice results

#### 3. Main Rounds (Rounds 2-13, 12 total)
- Same flow as practice
- Performance table updates after each round
- Shows cumulative history

#### 4. Post-Task (Round 12 only)
- **Weights:** Allocate 100 points across Resume/Zoom/In-Person
- **Demographics:** Hiring experience and optional comments
- **Final Payoff:** Display selected round and bonus amount

## Data Storage

### Participant-Level Data (Persisted across rounds)

```python
participant.condition          # 1 or 2
participant.practice_data_json # Practice candidate scores (JSON)
participant.main_data_json     # 12 rounds of candidate data (JSON)
participant.history_json       # Accumulated decisions & rewards (JSON)
```

### Player-Level Data (Per round)

```python
player.Q111_instructions_willing  # Comprehension Q1
player.Q139_condition_choice      # Comprehension Q2
player.gate1_choices              # JSON list of candidates at Gate 1
player.gate2_choices              # JSON list of candidates at Gate 2
player.hired_candidate            # Final hired candidate (A-J)
player.hired_trueq                # True quality of hired candidate
player.reward_str                 # Reward for this round (currency string)
player.resume_weight              # Post-task weight (0-100)
player.zoom_weight                # Post-task weight (0-100)
player.inperson_weight            # Post-task weight (0-100)
player.hiring_experience          # Experience level (0-4)
```

## Data Generation

### Parameters

```python
NUM_ROUNDS = 12           # Main rounds (practice is separate)
NUM_CANDIDATES = 10       # Candidates A-J per round
MU = 50                   # True quality mean
SIGMA = 15                # True quality std dev
SIGMA_RESUME = 15         # Resume score noise
SIGMA_ZOOM = 15           # Zoom score noise
SIGMA_INPERSON = 15       # In-person score noise
```

### Score Generation Algorithm

For each candidate in each round:

```python
true_q = round(MU + randn * SIGMA)
true_q = max(0, true_q)

resume_score = round(true_q + randn * SIGMA_RESUME)
resume_score = max(0, resume_score)

zoom_score = round(true_q + randn * SIGMA_ZOOM)
zoom_score = max(0, zoom_score)

inperson_score = round(true_q + randn * SIGMA_INPERSON)
inperson_score = max(0, inperson_score)
```

The `randn` function generates random draws from a standard normal distribution using `random.gauss(0, 1)`.

## Bonus Calculation

```python
base_reward = 4.00
bonus_rate = 0.05
max_reward = 10.00

reward = min(max_reward, base_reward + bonus_rate * true_quality_of_hired_candidate)
```

Example: If a participant hires a candidate with true quality 70:
- Reward = min(10, 4.00 + 0.05 * 70) = min(10, 7.50) = $7.50

### Final Payment

One main round (1-12) is **randomly selected** from the participant's history. The reward from that round becomes the bonus payment.

## UI/Table Components

### Candidate Score Table

Displays all 10 candidates (A-J) with three score type rows:
- Stage 1: Resume
- Stage 2: Zoom  
- Stage 3: In-Person

**Display logic:**
- Unrevealed scores show as "-"
- Eliminated candidates (funnel condition) are shaded grey (#e6e6e6)
- Responsive: scrollable on mobile, full width on desktop

### Selection Components

**Condition 1 (Single-stage):**
- Radio buttons (one selection) for final hire decision

**Condition 2 (Funnel):**
- Checkboxes with counters for Gate 1 (select 5) and Gate 2 (select 3)
- Radio buttons for Gate 3 (select 1)
- Client-side counter showing "Selected: k / required"
- Server-side validation enforcing exact counts

### Performance History Table

Columns:
- Round (Practice / 1-12)
- Hired Candidate (A-J)
- True Quality (integer)
- Reward if Chosen (currency string like "$7.50")

## Key Files

- `hiring_funnel/__init__.py` - Models, page classes, helper functions
- `hiring_funnel/*.html` - Page templates
- `_templates/candidate_table.html` - Reusable table component
- `_templates/global/Page.html` - Global template with CSS links
- `_static/hiring-funnel.css` - Styling for tables, forms, shading
- `_static/otai-utils.js` - Utility functions (if needed)
- `settings.py` - Session configuration

## Template Reference

| Template | Condition(s) | Purpose |
|----------|-------------|---------|
| Consent.html | Both | Informed consent |
| Instructions.html | Both | Study overview |
| Comprehension.html | Both | Comprehension check |
| PracticeIntro.html | Both | Practice intro |
| PracticeStage1Resume.html | Cond 1 | Resume reveal (practice) |
| PracticeStage2Zoom.html | Cond 1 | Zoom reveal (practice) |
| PracticeStage3Decision.html | Cond 1 | Hiring decision (practice) |
| PracticeGate1.html | Cond 2 | Gate 1 screening (practice) |
| PracticeGate1After.html | Cond 2 | Gate 1 results (practice) |
| PracticeGate2.html | Cond 2 | Gate 2 screening (practice) |
| PracticeGate2After.html | Cond 2 | Gate 2 results (practice) |
| PracticeGate3.html | Cond 2 | Gate 3 decision (practice) |
| PracticePerformance.html | Both | Practice summary |
| MainStage1Resume.html | Cond 1 | Resume reveal (main) |
| MainStage2Zoom.html | Cond 1 | Zoom reveal (main) |
| MainStage3Decision.html | Cond 1 | Hiring decision (main) |
| MainGate1.html | Cond 2 | Gate 1 screening (main) |
| MainGate1After.html | Cond 2 | Gate 1 results (main) |
| MainGate2.html | Cond 2 | Gate 2 screening (main) |
| MainGate2After.html | Cond 2 | Gate 2 results (main) |
| MainGate3.html | Cond 2 | Gate 3 decision (main) |
| MainRoundPerformance.html | Both | Round performance |
| PostTaskWeights.html | Both | Weight allocation |
| Demographics.html | Both | Demographics survey |
| FinalPayoff.html | Both | Final payment display |

## Validation Rules

### Gate/Selection Validation

- **Gate 1:** Must select exactly 5 candidates
- **Gate 2:** Must select exactly 3 from Gate 1 selections
- **Gate 3:** Must select 1 from Gate 2 selections
- **Post-task weights:** Must sum to exactly 100

### Client-Side & Server-Side

- **Client-side:** JavaScript counters provide real-time feedback
- **Server-side:** Python validation in `error_message()` methods enforces requirements

## Customization

### Change Parameters

Edit `C` class in `hiring_funnel/__init__.py`:

```python
class C(BaseConstants):
    NUM_ROUNDS = 12           # Change number of main rounds
    MU = 50                   # Change mean true quality
    SIGMA = 15                # Change variability
    GATE1_SELECT = 5          # Change Gate 1 cutoff
    GATE2_SELECT = 3          # Change Gate 2 cutoff
    DEFAULT_REWARD = 4.0      # Change base reward
    BONUS_RATE = 0.05         # Change per-point bonus
    MAX_REWARD = 10           # Change max reward cap
```

### Modify Styling

Edit `_static/hiring-funnel.css`:

```css
.candidate-scores-table {
    /* Customize table appearance */
}

.score-cell.eliminated {
    background-color: #e6e6e6;  /* Change elimination shade */
    color: #666;
}
```

## Data Export

oTree automatically records:
- All player fields in the database
- Session and participant attributes
- Page visit timestamps

Export data from the admin panel or via oTree commands:
```bash
otree export --create-table
```

## Testing

### Demo Links

- **Condition 1:** http://localhost:8000/demo/hiring_funnel/?cond=1
- **Condition 2:** http://localhost:8000/demo/hiring_funnel/?cond=2
- **Random assignment:** http://localhost:8000/demo/hiring_funnel/

### Test Checklist

- [ ] Consent and instructions display correctly
- [ ] Condition 1: Three stages reveal progressively
- [ ] Condition 2: Gates enforce 5→3→1 selections
- [ ] Performance tables accumulate correctly
- [ ] Eliminated candidates shade properly in Condition 2
- [ ] Final payment is calculated and displayed
- [ ] Data is saved to database correctly

## Troubleshooting

**Issue:** "Cannot find table candidate-scores-table"
- **Solution:** Ensure CSS file is linked in `global/Page.html`

**Issue:** Condition not assigned properly
- **Solution:** Check session config in `settings.py` and URL parameters

**Issue:** Gate selections not validating
- **Solution:** Verify `error_message()` methods are returning correct strings

**Issue:** Payment not calculated
- **Solution:** Ensure `select_final_payment()` is called in FinalPayoff.before_next_page()

## Support

For issues or questions about the implementation, refer to:
- oTree documentation: https://otree.readthedocs.io/
- Study specification document (original brief)
