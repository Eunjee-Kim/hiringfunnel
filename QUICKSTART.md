# Quick Start Guide - Hiring Funnel Study

## What Was Implemented

A complete oTree application for "Information Usage in Multi-Stage Hiring Funnels" with:

✅ **Two experimental conditions:**
- Condition 1: Single-stage screening (progressive reveal of Resume → Zoom → In-Person)
- Condition 2: Multi-stage funnel (gating with 5 → 3 → 1 selections)

✅ **Full study flow:**
1. Consent + Instructions + Comprehension check
2. Practice round (full scenario)
3. 12 main rounds
4. Post-task survey (weights, demographics)
5. Final payment display

✅ **Key features:**
- Accurate data generation matching specification (mean 50, std 15 for all distributions)
- Bonus calculation: $4.00 + 0.05 × true quality, capped at $10
- One random main round selected for payment
- Performance tracking with cumulative history tables
- Eliminated candidates shaded in funnel condition
- Client-side selection counters with server-side validation
- Responsive table design (scrollable on mobile)

✅ **Data storage:**
- All decisions tracked per round
- Full candidate score arrays retained
- Payment parameters recorded
- Survey responses captured

## File Structure

```
hiring_funnel/
├── __init__.py                 # Models, pages, logic (850+ lines)
├── Consent.html               # Consent form
├── Instructions.html          # Study overview
├── Comprehension.html         # Comprehension check (Q111, Q139)
├── PracticeIntro.html         # Practice intro
├── PracticeStage1Resume.html  # Practice Cond1: Resume reveal
├── PracticeStage2Zoom.html    # Practice Cond1: Zoom reveal
├── PracticeStage3Decision.html# Practice Cond1: Hiring decision
├── PracticeGate1.html         # Practice Cond2: Gate 1 (select 5)
├── PracticeGate1After.html    # Practice Cond2: Gate 1 results
├── PracticeGate2.html         # Practice Cond2: Gate 2 (select 3)
├── PracticeGate2After.html    # Practice Cond2: Gate 2 results
├── PracticeGate3.html         # Practice Cond2: Gate 3 (select 1)
├── PracticePerformance.html   # Practice summary
├── MainStage1Resume.html      # Main Cond1: Resume reveal
├── MainStage2Zoom.html        # Main Cond1: Zoom reveal
├── MainStage3Decision.html    # Main Cond1: Hiring decision
├── MainGate1.html             # Main Cond2: Gate 1
├── MainGate1After.html        # Main Cond2: Gate 1 results
├── MainGate2.html             # Main Cond2: Gate 2
├── MainGate2After.html        # Main Cond2: Gate 2 results
├── MainGate3.html             # Main Cond2: Gate 3
├── MainRoundPerformance.html  # Main round summary
├── PostTaskWeights.html       # Weight allocation (must sum to 100)
├── Demographics.html          # Hiring experience + comments
└── FinalPayoff.html           # Final payment display

_static/
├── hiring-funnel.css          # Tables, shading, styling
├── styles.css                 # (existing)
└── otai-utils.js              # (existing)

_templates/
└── global/
    └── Page.html              # Updated to include hiring-funnel.css
```

## How to Run

### 1. Start oTree Server
```bash
otree runserver
```

### 2. Create Session
Access the admin panel at `http://localhost:8000/admin/`

**Option A: With Condition Choice**
```
http://localhost:8000/create_session/hiring_funnel?cond=1
http://localhost:8000/create_session/hiring_funnel?cond=2
```

**Option B: Random Assignment**
```
http://localhost:8000/create_session/hiring_funnel
```

### 3. Join as Participant
```
http://localhost:8000/participant/XXXXX/
```

## Key Technical Details

### Data Generation
- **Pre-generated:** All 13 rounds of candidate data (practice + 12 main) created at session start
- **Storage:** JSON arrays stored in participant attributes
- **Distribution:** Normal(50, 15) for true quality; independent normal noise for each score

### Selection Validation

**Condition 1:**
- Gate 3 (final decision): Choose 1 of 10 (radio buttons)

**Condition 2:**
- Gate 1: Choose exactly 5 of 10 (checkboxes)
- Gate 2: Choose exactly 3 of 5 (checkboxes, only advanced candidates shown)
- Gate 3: Choose exactly 1 of 3 (radio buttons)

### Bonus Calculation

```
For each round (practice and main 1-12):
  reward = min(10.00, 4.00 + 0.05 * true_quality_of_hired_candidate)

Final payment:
  - Random main round (1-12) selected
  - Payoff = reward from that round
```

### Performance History

**Tracks per round:**
- Round number
- Hired candidate (A-J label)
- True quality (integer)
- Reward if chosen ("$X.XX")

**Cumulative table** shown after each main round showing all previous results

## Important Parameters

Located in `hiring_funnel/__init__.py`, class `C`:

```python
NUM_ROUNDS = 12          # Main rounds (12) - change here if needed
NUM_CANDIDATES = 10      # Always 10, candidates A-J
MU = 50                  # Mean true quality
SIGMA = 15               # True quality std dev
SIGMA_RESUME = 15        # Resume score noise
SIGMA_ZOOM = 15          # Zoom score noise
SIGMA_INPERSON = 15      # In-person score noise
DEFAULT_REWARD = 4.0     # Base bonus
BONUS_RATE = 0.05        # Per-point bonus
MAX_REWARD = 10          # Reward cap
GATE1_SELECT = 5         # Gate 1 cutoff
GATE2_SELECT = 3         # Gate 2 cutoff
```

## Customization Examples

### Change number of main rounds to 8:
```python
NUM_ROUNDS = 8
```

### Change base bonus to $5.00 with higher rate:
```python
DEFAULT_REWARD = 5.0
BONUS_RATE = 0.08
```

### Increase reward cap:
```python
MAX_REWARD = 15.0
```

## Testing Checklist

- [ ] **Condition 1 (Cond 1):** Three pages reveal progressively (Resume → Zoom → In-Person)
- [ ] **Condition 2 (Cond 2):** Five pages per round (Gate1 → After → Gate2 → After → Gate3)
- [ ] **Gate validation:** Can't proceed without 5, 3, 1 selections (respectively)
- [ ] **Tables:** All scores display correctly, eliminated candidates shade grey (Cond2)
- [ ] **Practice round:** Shows performance table after completion
- [ ] **History:** Cumulative table grows with each main round
- [ ] **Payment:** Final bonus calculated and displayed correctly
- [ ] **Weights:** Must sum to 100 before proceeding
- [ ] **Data:** All player fields saved to database

## Troubleshooting

### Issue: "Page not found"
→ Check page class exists in __init__.py and is in page_sequence

### Issue: Condition not being assigned
→ Verify URL parameter (?cond=1 or ?cond=2) or check settings.py

### Issue: Table not styled
→ Ensure hiring-funnel.css is linked in global/Page.html

### Issue: Selection validation not working
→ Check error_message() method returns correct string

### Issue: Payment not calculated
→ Verify select_final_payment() called in FinalPayoff.before_next_page()

## File Sizes (Reference)

- __init__.py: ~1100 lines
- hiring-funnel.css: ~400 lines
- 24 HTML templates: ~50-100 lines each
- Total implementation: ~3500 lines

## Database Fields

**Per round (Player model):**
- Q111_instructions_willing (comprehension Q1)
- Q139_condition_choice (comprehension Q2)
- gate1_choices (JSON: ["A", "B", ...])
- gate2_choices (JSON: ["A", "C", ...])
- hired_candidate ("A" through "J")
- hired_trueq (integer 0-100+)
- reward_str ("$7.50" format)
- resume_weight (0-100)
- zoom_weight (0-100)
- inperson_weight (0-100)
- hiring_experience ("0"-"4")

**Per session (Participant attrs):**
- condition (1 or 2)
- practice_data_json (all candidate data)
- main_data_json (all rounds data)
- history_json (accumulated decisions)
- selected_round (final payment round)
- selected_candidate (hired candidate in payment round)
- selected_true_quality (true quality of selected)
- payoff (oTree currency object)

## Next Steps

1. **Test**: Run through study with both conditions
2. **Adjust**: Modify parameters in __init__.py as needed
3. **Deploy**: Follow oTree deployment guide for production server
4. **Collect**: Run with actual participants
5. **Analyze**: Export data and conduct analysis

## Support Resources

- Full implementation details: See README.md
- oTree documentation: https://otree.readthedocs.io/
- Study specification: Original requirements document
