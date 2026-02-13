
# Generate remaining templates
import os

templates_dir = r"c:\Users\ekim298\OneDrive - UW-Madison\2026 Spring\Information_Usage_in_Hiring_Funnels\hiring_funnel"

templates = {
    "PracticeIntro.html": """{{ extends "global/Page.html" }}
{{ block title }}Practice Round{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Practice Round</h2>

<div class="instruction-text">
    <p>Now you will complete a practice round. This round works the same way as the main rounds but will not count towards your final payment.</p>
    <p><strong>Your task:</strong> Review candidate information as it is revealed and make hiring decisions to maximize the true quality of hired candidates.</p>
    <p>After the practice round, you will complete 12 main rounds. Your final payment bonus will be based on one randomly selected main round.</p>
</div>

{{ next_button }}

{{ endblock }}""",

    "PracticePerformance.html": """{{ extends "global/Page.html" }}
{{ block title }}Practice Performance{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Practice Round - Performance Summary</h2>

<div class="performance-box">
    <h3>Last Round Results</h3>
    <p><strong>Hired Candidate True Quality:</strong> {{ last_round_true_q }}</p>
</div>

<h3>Performance History</h3>
<div class="table-scroll">
    <table class="history-table">
        <thead>
            <tr>
                <th>Round</th>
                <th>Hired Candidate</th>
                <th>True Quality</th>
                <th>Reward if Chosen</th>
            </tr>
        </thead>
        <tbody>
            {% for entry in history %}
                <tr>
                    <td>{% if entry.round == 0 %}Practice{% else %}{{ entry.round }}{% endif %}</td>
                    <td>{{ entry.hired_candidate }}</td>
                    <td>{{ entry.true_q }}</td>
                    <td>{{ entry.reward }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<div class="instruction-text">
    <p><strong>Next:</strong> You have now finished the practice round. Next you begin the main cases, lasting 12 rounds. The same reward formula applies: $4.00 + 0.05 × true quality of hired candidate, capped at $10.00.</p>
</div>

{{ next_button }}

{{ endblock }}""",

    "MainRoundPerformance.html": """{{ extends "global/Page.html" }}
{{ block title }}Performance So Far - Round {{ round_num }}{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Performance So Far</h2>

<div class="performance-box">
    <h3>Last Round ({{ round_num }})</h3>
    <p><strong>Hired Candidate True Quality:</strong> {{ last_round_true_q }}</p>
</div>

<h3>Cumulative History</h3>
<div class="table-scroll">
    <table class="history-table">
        <thead>
            <tr>
                <th>Round</th>
                <th>Hired Candidate</th>
                <th>True Quality</th>
                <th>Reward if Chosen</th>
            </tr>
        </thead>
        <tbody>
            {% for entry in history %}
                <tr>
                    <td>{% if entry.round == 0 %}Practice{% else %}{{ entry.round }}{% endif %}</td>
                    <td>{{ entry.hired_candidate }}</td>
                    <td>{{ entry.true_q }}</td>
                    <td>{{ entry.reward }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

{{ next_button }}

{{ endblock }}""",

    "PracticeIntro.html": """{{ extends "global/Page.html" }}
{{ block title }}Practice Introduction{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Practice Round Introduction</h2>

<p>You will now complete a practice round using the hiring scenario described in the instructions.</p>

<p><strong>Condition:</strong> {% if is_single_stage %}Single-stage screening{% else %}Multi-stage funnel screening{% endif %}</p>

<div class="instruction-text">
    <p><strong>Remember:</strong> Your bonus payment depends on the true quality of the candidates you hire. The better your hiring decisions, the higher your payment.</p>
</div>

{{ next_button }}

{{ endblock }}""",

    "PostTaskWeights.html": """{{ extends "global/Page.html" }}
{{ block title }}Post-Task Survey - Weights{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Post-Task Survey: Weights</h2>

<p>In making your hiring decisions, how much weight did you give to each interview stage? Please allocate 100 points total.</p>

<div class="form-group">
    <label for="resume_weight">Stage 1: Resume Weight</label>
    <input type="number" id="resume_weight" name="resume_weight" min="0" max="100" value="0" required>
    <small>Points allocated to Resume scores</small>
</div>

<div class="form-group">
    <label for="zoom_weight">Stage 2: Zoom Weight</label>
    <input type="number" id="zoom_weight" name="zoom_weight" min="0" max="100" value="0" required>
    <small>Points allocated to Zoom scores</small>
</div>

<div class="form-group">
    <label for="inperson_weight">Stage 3: In-Person Weight</label>
    <input type="number" id="inperson_weight" name="inperson_weight" min="0" max="100" value="0" required>
    <small>Points allocated to In-Person scores</small>
</div>

<div id="total-display" style="font-weight: 600; margin-top: 15px; padding: 10px; background-color: #f0f0f0; border-radius: 4px;">
    Total: 0 / 100
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input[type="number"]');
    const totalDisplay = document.getElementById('total-display');
    
    function updateTotal() {
        const resume = parseInt(document.getElementById('resume_weight').value) || 0;
        const zoom = parseInt(document.getElementById('zoom_weight').value) || 0;
        const inperson = parseInt(document.getElementById('inperson_weight').value) || 0;
        const total = resume + zoom + inperson;
        
        totalDisplay.textContent = `Total: ${total} / 100`;
        totalDisplay.style.backgroundColor = total === 100 ? '#e8f5e9' : '#fff3e0';
        totalDisplay.style.color = total === 100 ? '#2e7d32' : '#e65100';
    }
    
    inputs.forEach(input => {
        input.addEventListener('change', updateTotal);
        input.addEventListener('input', updateTotal);
    });
});
</script>

{{ next_button }}

{{ endblock }}""",

    "Demographics.html": """{{ extends "global/Page.html" }}
{{ block title }}Demographics{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Demographics & Experience</h2>

<div class="form-group">
    <label for="hiring_experience">Do you have hiring experience?</label>
    <select id="hiring_experience" name="hiring_experience" required>
        <option value="">-- Please Select --</option>
        <option value="0">None</option>
        <option value="1">Less than 1 year</option>
        <option value="2">1-3 years</option>
        <option value="3">3-5 years</option>
        <option value="4">More than 5 years</option>
    </select>
</div>

<div class="form-group">
    <label for="demographics_comment">Additional comments about the study:</label>
    <textarea id="demographics_comment" name="demographics_comment" placeholder="Optional: Share any feedback or observations..."></textarea>
</div>

{{ next_button }}

{{ endblock }}""",

    "FinalPayoff.html": """{{ extends "global/Page.html" }}
{{ block title }}Study Complete - Final Payoff{{ endblock }}

{{ block content }}

<link rel="stylesheet" href="{{ static 'hiring-funnel.css' }}">

<h2>Study Complete!</h2>

<div class="performance-box">
    <h3>Your Final Payoff</h3>
    <p><strong>Selected Round:</strong> {{ selected_round }}</p>
    <p><strong>Hired Candidate:</strong> {{ selected_candidate }}</p>
    <p><strong>True Quality:</strong> {{ selected_true_q }}</p>
    <p><strong>Bonus Amount:</strong> {{ selected_reward }}</p>
    <p style="font-size: 1.2em; font-weight: 700; color: #2e7d32; margin-top: 15px;">
        Total Payment: {{ payoff }}
    </p>
</div>

<p style="margin-top: 30px;">Thank you for your participation! Your payment will be processed according to the study procedures.</p>

{{ endblock }}
""",
}

for filename, content in templates.items():
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created {filename}")

print("All remaining templates created!")
