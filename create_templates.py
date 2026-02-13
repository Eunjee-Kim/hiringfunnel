
# Script to create all remaining template files
import os

templates_dir = r"c:\Users\ekim298\OneDrive - UW-Madison\2026 Spring\Information_Usage_in_Hiring_Funnels\hiring_funnel"

templates = {
    "PracticeGate1After.html": """{{ extends "global/Page.html" }}
{{ block title }}Practice Round - Gate 1 After Screening{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Practice Round - Gate 1 Results</h2>

<div class="instruction-text">
    <p>Now that you have selected the candidates to advance, only {{ advanced_count }} candidates remain. Candidates eliminated in the previous round are shaded grey. Click next to reveal the Zoom interview scores (Stage 2) for these {{ advanced_count }} candidates.</p>
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

    "PracticeGate2.html": """{{ extends "global/Page.html" }}
{{ block title }}Practice Round - Gate 2: Zoom Interviews{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Practice Round - Gate 2: Zoom Interviews</h2>

<div class="instruction-text">
    <p>Now you can see Zoom interview scores for the {{ required_count }} finalists. Select exactly <strong>3 candidates</strong> to advance to Gate 3.</p>
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
    <label style="font-weight: 600;">Gate 2: Select exactly {{ required_count }} candidates to advance</label>
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
        if (selected < required) {
            counter.classList.add('warning');
        } else if (selected > required) {
            counter.classList.add('error');
        }
    }
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateCounter);
    });
});
</script>

{{ next_button }}

{{ endblock }}""",

    "PracticeGate2After.html": """{{ extends "global/Page.html" }}
{{ block title }}Practice Round - Gate 2 After Screening{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Practice Round - Gate 2 Results</h2>

<div class="instruction-text">
    <p>Now that you have selected the candidates to advance, only {{ advanced_count }} candidates remain. Candidates eliminated are shaded grey. Click next to reveal In-person interview scores (Stage 3) and make your final decision.</p>
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

    "PracticeGate3.html": """{{ extends "global/Page.html" }}
{{ block title }}Practice Round - Gate 3: Final Decision{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Practice Round - Gate 3: Final Decision</h2>

<div class="instruction-text">
    <p>You now have all information for the 3 finalists. Select one candidate to hire. Remember: your bonus depends on this candidate's true quality!</p>
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
    <label style="font-weight: 600; width: 100%; margin-bottom: 10px;">Gate 3: Which candidate do you hire?</label>
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

for filename, content in templates.items():
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created {filename}")

print("All templates created successfully!")
