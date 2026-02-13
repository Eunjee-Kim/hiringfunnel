
# Generate all remaining template files
import os

templates_dir = r"c:\Users\ekim298\OneDrive - UW-Madison\2026 Spring\Information_Usage_in_Hiring_Funnels\hiring_funnel"

# Main condition templates
main_templates = {
    "MainStage1Resume.html": """{{ extends "global/Page.html" }}
{{ block title }}Round {{ round_num }} - Stage 1: Resume{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Round {{ round_num }} - Stage 1: Resume Scores</h2>

<div class="instruction-text">
    <p>Above are the 10 candidates and their Resume scores (Stage 1). Please review the scores and click next to reveal Zoom interview scores (Stage 2).</p>
</div>

<div class="table-scroll">
    <table class="candidate-scores-table">
        <thead>
            <tr>
                <th class="score-type-header">Score Type</th>
                {% for candidate in candidates %}
                    <th class="candidate-header">{{ candidate.label }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="row-label">Stage 1: Resume</td>
                {% for candidate in candidates %}
                    <td class="score-cell">{{ candidate.resume }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 2: Zoom</td>
                {% for candidate in candidates %}
                    <td class="score-cell">{{ candidate.zoom }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 3: In-Person</td>
                {% for candidate in candidates %}
                    <td class="score-cell">{{ candidate.inperson }}</td>
                {% endfor %}
            </tr>
        </tbody>
    </table>
</div>

{{ next_button }}

{{ endblock }}""",

    "MainStage2Zoom.html": """{{ extends "global/Page.html" }}
{{ block title }}Round {{ round_num }} - Stage 2: Zoom{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Round {{ round_num }} - Stage 2: Zoom Scores</h2>

<div class="instruction-text">
    <p>Please review the scores and click next to reveal In-Person interview scores (Stage 3).</p>
</div>

<div class="table-scroll">
    <table class="candidate-scores-table">
        <thead>
            <tr>
                <th class="score-type-header">Score Type</th>
                {% for candidate in candidates %}
                    <th class="candidate-header">{{ candidate.label }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="row-label">Stage 1: Resume</td>
                {% for candidate in candidates %}
                    <td class="score-cell">{{ candidate.resume }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 2: Zoom</td>
                {% for candidate in candidates %}
                    <td class="score-cell">{{ candidate.zoom }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 3: In-Person</td>
                {% for candidate in candidates %}
                    <td class="score-cell">{{ candidate.inperson }}</td>
                {% endfor %}
            </tr>
        </tbody>
    </table>
</div>

{{ next_button }}

{{ endblock }}""",

    "MainStage3Decision.html": """{{ extends "global/Page.html" }}
{{ block title }}Round {{ round_num }} - Final Decision{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Round {{ round_num }} - Final Decision</h2>

<div class="instruction-text">
    <p>Please review all candidate scores and select one candidate to hire.</p>
</div>

<div class="table-scroll">
    <table class="candidate-scores-table">
        <thead>
            <tr>
                <th class="score-type-header">Score Type</th>
                {% for candidate in candidates %}
                    <th class="candidate-header">{{ candidate.label }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="row-label">Stage 1: Resume</td>
                {% for candidate in candidates %}
                    <td class="score-cell">{{ candidate.resume }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 2: Zoom</td>
                {% for candidate in candidates %}
                    <td class="score-cell">{{ candidate.zoom }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 3: In-Person</td>
                {% for candidate in candidates %}
                    <td class="score-cell">{{ candidate.inperson }}</td>
                {% endfor %}
            </tr>
        </tbody>
    </table>
</div>

<div class="candidate-selection">
    <label style="font-weight: 600; width: 100%; margin-bottom: 10px;">Which candidate do you want to hire?</label>
    {% for candidate in candidates %}
        <div class="candidate-radio">
            <input type="radio" id="candidate-{{ candidate.label }}" name="hired_candidate" value="{{ candidate.label }}" required>
            <label for="candidate-{{ candidate.label }}">Candidate {{ candidate.label }}</label>
        </div>
    {% endfor %}
</div>

{{ next_button }}

{{ endblock }}""",

    "MainGate1.html": """{{ extends "global/Page.html" }}
{{ block title }}Round {{ round_num }} - Gate 1: Resume Screening{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Round {{ round_num }} - Gate 1: Resume Screening</h2>

<div class="instruction-text">
    <p>Review the 10 candidates' Resume scores. Select exactly <strong>{{ required_count }} candidates</strong> to advance to Gate 2.</p>
</div>

<div class="table-scroll">
    <table class="candidate-scores-table">
        <thead>
            <tr>
                <th class="score-type-header">Score Type</th>
                {% for candidate in candidates %}
                    <th class="candidate-header">{{ candidate.label }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="row-label">Stage 1: Resume</td>
                {% for candidate in candidates %}
                    <td class="score-cell">{{ candidate.resume }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 2: Zoom</td>
                {% for candidate in candidates %}
                    <td class="score-cell">{{ candidate.zoom }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 3: In-Person</td>
                {% for candidate in candidates %}
                    <td class="score-cell">{{ candidate.inperson }}</td>
                {% endfor %}
            </tr>
        </tbody>
    </table>
</div>

<div class="form-group">
    <label style="font-weight: 600;">Select exactly {{ required_count }} candidates to advance</label>
    <div class="gate-instruction" id="selection-counter">Selected: 0 / {{ required_count }}</div>
    
    {% for candidate in candidates %}
        <div class="candidate-checkbox">
            <input type="checkbox" id="gate1-{{ candidate.label }}" name="gate1_choices" value="{{ candidate.label }}">
            <label for="gate1-{{ candidate.label }}">Candidate {{ candidate.label }} (Resume: {{ candidate.resume }})</label>
        </div>
    {% endfor %}
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('input[name="gate1_choices"]');
    const required = {{ required_count }};
    const counter = document.getElementById('selection-counter');
    
    function updateCounter() {
        const selected = document.querySelectorAll('input[name="gate1_choices"]:checked').length;
        counter.textContent = `Selected: ${selected} / ${required}`;
        counter.className = 'gate-instruction';
        if (selected < required) counter.classList.add('warning');
        else if (selected > required) counter.classList.add('error');
    }
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateCounter);
    });
});
</script>

{{ next_button }}

{{ endblock }}""",

    "MainGate1After.html": """{{ extends "global/Page.html" }}
{{ block title }}Round {{ round_num }} - Gate 1 After{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Round {{ round_num }} - Gate 1 Results</h2>

<div class="instruction-text">
    <p>Now {{ advanced_count }} candidates remain. Eliminated candidates are shaded grey. Click next to see Zoom scores for the remaining candidates.</p>
</div>

<div class="table-scroll">
    <table class="candidate-scores-table">
        <thead>
            <tr>
                <th class="score-type-header">Score Type</th>
                {% for candidate in candidates %}
                    <th class="candidate-header {% if candidate.eliminated %}eliminated{% endif %}">{{ candidate.label }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="row-label">Stage 1: Resume</td>
                {% for candidate in candidates %}
                    <td class="score-cell {% if candidate.eliminated %}eliminated{% endif %}">{{ candidate.resume }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 2: Zoom</td>
                {% for candidate in candidates %}
                    <td class="score-cell {% if candidate.eliminated %}eliminated{% endif %}">{{ candidate.zoom }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 3: In-Person</td>
                {% for candidate in candidates %}
                    <td class="score-cell {% if candidate.eliminated %}eliminated{% endif %}">{{ candidate.inperson }}</td>
                {% endfor %}
            </tr>
        </tbody>
    </table>
</div>

{{ next_button }}

{{ endblock }}""",

    "MainGate2.html": """{{ extends "global/Page.html" }}
{{ block title }}Round {{ round_num }} - Gate 2: Zoom Interviews{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Round {{ round_num }} - Gate 2: Zoom Interviews</h2>

<div class="instruction-text">
    <p>Now you can see Zoom scores. Select exactly <strong>{{ required_count }} candidates</strong> to advance to Gate 3.</p>
</div>

<div class="table-scroll">
    <table class="candidate-scores-table">
        <thead>
            <tr>
                <th class="score-type-header">Score Type</th>
                {% for candidate in candidates %}
                    <th class="candidate-header {% if candidate.eliminated %}eliminated{% endif %}">{{ candidate.label }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="row-label">Stage 1: Resume</td>
                {% for candidate in candidates %}
                    <td class="score-cell {% if candidate.eliminated %}eliminated{% endif %}">{{ candidate.resume }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 2: Zoom</td>
                {% for candidate in candidates %}
                    <td class="score-cell {% if candidate.eliminated %}eliminated{% endif %}">{{ candidate.zoom }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 3: In-Person</td>
                {% for candidate in candidates %}
                    <td class="score-cell {% if candidate.eliminated %}eliminated{% endif %}">{{ candidate.inperson }}</td>
                {% endfor %}
            </tr>
        </tbody>
    </table>
</div>

<div class="form-group">
    <label style="font-weight: 600;">Select exactly {{ required_count }} from remaining candidates</label>
    <div class="gate-instruction" id="selection-counter">Selected: 0 / {{ required_count }}</div>
    
    {% for candidate in available_candidates %}
        <div class="candidate-checkbox">
            <input type="checkbox" id="gate2-{{ candidate }}" name="gate2_choices" value="{{ candidate }}">
            <label for="gate2-{{ candidate }}">Candidate {{ candidate }}</label>
        </div>
    {% endfor %}
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('input[name="gate2_choices"]');
    const required = {{ required_count }};
    const counter = document.getElementById('selection-counter');
    
    function updateCounter() {
        const selected = document.querySelectorAll('input[name="gate2_choices"]:checked').length;
        counter.textContent = `Selected: ${selected} / ${required}`;
        counter.className = 'gate-instruction';
        if (selected < required) counter.classList.add('warning');
        else if (selected > required) counter.classList.add('error');
    }
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateCounter);
    });
});
</script>

{{ next_button }}

{{ endblock }}""",

    "MainGate2After.html": """{{ extends "global/Page.html" }}
{{ block title }}Round {{ round_num }} - Gate 2 After{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Round {{ round_num }} - Gate 2 Results</h2>

<div class="instruction-text">
    <p>Now {{ advanced_count }} candidates remain. Eliminated candidates are shaded grey. Click next to see In-person scores and make your final decision.</p>
</div>

<div class="table-scroll">
    <table class="candidate-scores-table">
        <thead>
            <tr>
                <th class="score-type-header">Score Type</th>
                {% for candidate in candidates %}
                    <th class="candidate-header {% if candidate.eliminated %}eliminated{% endif %}">{{ candidate.label }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="row-label">Stage 1: Resume</td>
                {% for candidate in candidates %}
                    <td class="score-cell {% if candidate.eliminated %}eliminated{% endif %}">{{ candidate.resume }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 2: Zoom</td>
                {% for candidate in candidates %}
                    <td class="score-cell {% if candidate.eliminated %}eliminated{% endif %}">{{ candidate.zoom }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 3: In-Person</td>
                {% for candidate in candidates %}
                    <td class="score-cell {% if candidate.eliminated %}eliminated{% endif %}">{{ candidate.inperson }}</td>
                {% endfor %}
            </tr>
        </tbody>
    </table>
</div>

{{ next_button }}

{{ endblock }}""",

    "MainGate3.html": """{{ extends "global/Page.html" }}
{{ block title }}Round {{ round_num }} - Gate 3: Final Decision{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Round {{ round_num }} - Gate 3: Final Decision</h2>

<div class="instruction-text">
    <p>You now have complete information for the 3 finalists. Select one candidate to hire.</p>
</div>

<div class="table-scroll">
    <table class="candidate-scores-table">
        <thead>
            <tr>
                <th class="score-type-header">Score Type</th>
                {% for candidate in candidates %}
                    <th class="candidate-header">{{ candidate.label }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="row-label">Stage 1: Resume</td>
                {% for candidate in candidates %}
                    <td class="score-cell">{{ candidate.resume }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 2: Zoom</td>
                {% for candidate in candidates %}
                    <td class="score-cell">{{ candidate.zoom }}</td>
                {% endfor %}
            </tr>
            <tr>
                <td class="row-label">Stage 3: In-Person</td>
                {% for candidate in candidates %}
                    <td class="score-cell">{{ candidate.inperson }}</td>
                {% endfor %}
            </tr>
        </tbody>
    </table>
</div>

<div class="candidate-selection">
    <label style="font-weight: 600; width: 100%; margin-bottom: 10px;">Which candidate do you hire?</label>
    {% for candidate in available_candidates %}
        <div class="candidate-radio">
            <input type="radio" id="hired-{{ candidate }}" name="hired_candidate" value="{{ candidate }}" required>
            <label for="hired-{{ candidate }}">Candidate {{ candidate }}</label>
        </div>
    {% endfor %}
</div>

{{ next_button }}

{{ endblock }}""",
}

# Write all templates
for filename, content in main_templates.items():
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created {filename}")

print("All main templates created successfully!")
