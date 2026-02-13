# Condition 1 Data Changes

## Summary
Implemented separate data generation for Condition 1 that reduces the number of candidates from 10 to 3 per round. The 3 candidates are randomly selected from the 10-candidate pool (A-J) for each round.

## Changes Made

### 1. Data Generation (hiring_funnel/__init__.py)

#### Creating Session Function
- Added random sampling of 3 candidates from the pool of 10 (A-J) for **each round**
- For **practice round**: `practice_c1_labels` - 3 random candidates
- For **main rounds (1-12)**: `main_c1_labels` - 3 random candidates per round
- Each round gets a **different random selection** of 3 candidates

#### New Helper Functions

**`get_c1_candidate_labels(participant, round_num)`**
- Returns the 3 randomly selected candidate labels for condition 1 for a specific round
- Handles both practice (round_num=0) and main rounds (1-12)

**`get_round_data_for_condition(participant, round_num, condition)`**
- Returns candidate data filtered for the specified condition
- For **condition 1**: Returns only the 3 selected candidates
- For **condition 2**: Returns all 10 candidates (existing behavior)

### 2. Condition 1 Pages Updated

#### Practice Round Pages
- `PracticeStage1Resume` - Updated to use `get_round_data_for_condition()`
- `PracticeStage2Zoom` - Updated to use `get_round_data_for_condition()`
- `PracticeStage3Decision` - Updated to use `get_round_data_for_condition()`

#### Main Round Pages
- `MainStage1Resume` - Updated to use `get_round_data_for_condition()`
- `MainStage2Zoom` - Updated to use `get_round_data_for_condition()`
- `MainStage3Decision` - Updated to use `get_round_data_for_condition()`

### 3. HTML Templates Updated

All templates now display candidates dynamically based on the filtered list:

**Practice Templates:**
- `PracticeStage1Resume.html`
- `PracticeStage2Zoom.html`
- `PracticeStage3Decision.html`

**Main Round Templates:**
- `MainStage1Resume.html`
- `MainStage2Zoom.html`
- `MainStage3Decision.html`

#### Template Changes
- Changed `colspan="10"` to `colspan="{{ candidates|length }}"`
- Changed hardcoded "10 candidates" text to `{{ candidates|length }} candidates`
- All loops iterate over the filtered candidate list

## Data Structure

### For Condition 1
```
Practice Round:
  - 3 randomly selected candidates from A-J
  - Labels stored in: participant.practice_c1_labels

Main Rounds (1-12):
  - Each round has 3 randomly selected candidates from A-J
  - Different random selection for each round
  - Labels stored in: participant.main_c1_labels (array of 12 lists)
```

### For Condition 2 (Unchanged)
```
All rounds:
  - All 10 candidates (A-J) displayed
  - Existing multi-stage funnel process (Gate 1: 5→3, Gate 2: 3→1)
```

## Backward Compatibility

- Condition 2 (multi-stage funnel) is **unaffected**
- All existing functionality for condition 2 remains the same
- The system automatically handles both conditions based on player.participant.condition

## Future Modifications

The framework is ready for the following future changes:
1. **Different candidate selection per round** - Already supports (each round has independent selection)
2. **Different number of candidates** - Change the `3` in `random.sample(list(C.CANDIDATE_LABELS), 3)` to any number
3. **Stratified sampling** - Can implement selection logic based on true quality percentiles or other criteria
4. **Consistent candidates per round** - Simple modification to reuse the same 3 candidates across all rounds
