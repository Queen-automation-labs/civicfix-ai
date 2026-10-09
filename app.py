from flask import Flask, request, render_template_string
from research_engine import CivicResearchEngine
from authority_matcher import AuthorityMatcher
from action_generator import ActionGenerator
from official_channel_finder import OfficialChannelFinder
from official_source_filter import OfficialSourceFilter

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CivicFix AI</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            background: #070b14;
            color: #f4f7fb;
            min-height: 100vh;
        }

        .container {
            width: min(1100px, 92%);
            margin: auto;
            padding: 35px 0 60px;
        }

        .badge {
            display: inline-block;
            padding: 7px 13px;
            border: 1px solid #29405f;
            border-radius: 30px;
            color: #7dd3fc;
            background: #0d1728;
            font-size: 13px;
            margin-bottom: 18px;
        }

        h1 {
            font-size: clamp(42px, 8vw, 78px);
            line-height: 0.95;
            margin-bottom: 18px;
            letter-spacing: -3px;
        }

        .accent {
            color: #38bdf8;
        }

        .subtitle {
            max-width: 700px;
            color: #aab7c9;
            font-size: 18px;
            line-height: 1.6;
            margin-bottom: 35px;
        }

        .card {
            background: #0d1422;
            border: 1px solid #1e2b3f;
            border-radius: 20px;
            padding: 25px;
            margin-top: 20px;
            box-shadow: 0 15px 45px rgba(0,0,0,.25);
        }

        label {
            display: block;
            color: #cbd5e1;
            margin-bottom: 9px;
            font-size: 14px;
            font-weight: bold;
        }

        textarea, input {
            width: 100%;
            background: #080e19;
            color: white;
            border: 1px solid #26364d;
            border-radius: 12px;
            padding: 15px;
            font-size: 16px;
            outline: none;
            margin-bottom: 18px;
        }

        textarea {
            min-height: 130px;
            resize: vertical;
        }

        textarea:focus, input:focus {
            border-color: #38bdf8;
        }

        button {
            width: 100%;
            border: 0;
            border-radius: 12px;
            padding: 16px;
            background: #38bdf8;
            color: #06101c;
            font-size: 16px;
            font-weight: 800;
            cursor: pointer;
        }

        button:hover {
            background: #67d5ff;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 25px;
        }

        .mini {
            background: #0b111d;
            border: 1px solid #1d2b3e;
            border-radius: 15px;
            padding: 18px;
        }

        .mini .icon {
            font-size: 25px;
            margin-bottom: 10px;
        }

        .mini h3 {
            font-size: 15px;
            margin-bottom: 7px;
        }

        .mini p {
            color: #8291a5;
            font-size: 13px;
            line-height: 1.5;
        }

        .footer {
            text-align: center;
            color: #617086;
            margin-top: 40px;
            font-size: 13px;
        }

        @media(max-width: 700px) {
            .grid {
                grid-template-columns: 1fr;
            }

            .container {
                padding-top: 25px;
            }
        }
    </style>
</head>

<body>

<div class="container">

    <div class="badge">● LIVE CIVIC INTELLIGENCE</div>

    <h1>
        From Problem<br>
        to <span class="accent">Action.</span>
    </h1>

    <p class="subtitle">
        CivicFix AI researches the web, identifies the most likely
        responsible authority, gathers evidence, and turns a civic
        problem into a clear action plan.
    </p>

    <div class="card">

        <form method="POST">

            <label>WHAT IS THE PROBLEM?</label>

            <textarea
                name="problem"
                placeholder="Example: There are dangerous potholes on the main road in my area..."
                required
            ></textarea>

            <label>LOCATION</label>

            <input
                name="location"
                placeholder="Example: Patna, Bihar"
                required
            >

            <button type="submit">
                FIND THE RIGHT ACTION →
            </button>

        </form>

    </div>

    <div class="grid">

        <div class="mini">
            <div class="icon">🔎</div>
            <h3>Live Research</h3>
            <p>
                Search current web information instead of relying
                only on static knowledge.
            </p>
        </div>

        <div class="mini">
            <div class="icon">🎯</div>
            <h3>Authority Matching</h3>
            <p>
                Identify the authority most likely responsible
                for the reported issue.
            </p>
        </div>

        <div class="mini">
            <div class="icon">📋</div>
            <h3>Action Ready</h3>
            <p>
                Turn research into a practical complaint and
                next-step action plan.
            </p>
        </div>

    </div>

    <div class="footer">
        CivicFix AI • Evidence-driven civic action
    </div>

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template_string(HTML)

    problem = request.form.get("problem", "").strip()
    location = request.form.get("location", "").strip()

    if not problem or not location:
        return render_template_string(
            HTML + """
            <p style="color:#ffb86b;padding:20px">
            Please enter both the problem and location, then try again.
            </p>
            """
        ), 400

    try:
        engine = CivicResearchEngine()
        research = engine.research(problem, location)

        google_data = research.get("google", {})
        maps_data = research.get("maps", {})
        news_data = research.get("news", {})

        google_results = google_data.get("organic_results", [])
        maps_results = maps_data.get("local_results", [])
        news_results = news_data.get("news_results", [])

        if isinstance(maps_results, dict):
            maps_results = [maps_results]

        official_filter = OfficialSourceFilter()
        official_google = official_filter.filter_results(google_results)

        matcher = AuthorityMatcher()
        authority_result = matcher.match(
            problem, google_results, maps_results, news_results
        )

        generator = ActionGenerator()
        action = generator.generate(
            problem, location, authority_result,
            official_google, maps_results, news_results
        )

        channels = OfficialChannelFinder().find(problem, location)

        page = """
        <!doctype html>
        <html lang="en">
        <head>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>CivicFix AI — Research Results</title>
          <style>
            body { background:#070b14; color:#f4f7fb; font-family:Arial,sans-serif;
                   max-width:900px; margin:auto; padding:24px; line-height:1.6; }
            .card { background:#111827; border:1px solid #263449; border-radius:14px;
                    padding:20px; margin:16px 0; overflow-wrap:anywhere; }
            h1,h2 { color:#38bdf8; }
            a { color:#7dd3fc; }
            pre { white-space:pre-wrap; overflow-wrap:anywhere; }
            .note { color:#fbbf24; }
            button { background:#38bdf8; color:#07111d; padding:10px 16px;
                     border:0; border-radius:8px; font-weight:bold; }
          </style>
        </head>
        <body>
          <h1>CivicFix AI — Research Report</h1>
          <div class="card">
            <h2>Reported issue</h2>
            <p><b>Problem:</b> {{ problem }}</p>
            <p><b>Location:</b> {{ location }}</p>
          </div>
          <div class="card">
            <h2>Suggested authority</h2>
            <p><b>{{ authority }}</b></p>
            <p>{{ reason }}</p>
            <p class="note">This is a preliminary keyword-based suggestion,
            not a verified determination of the responsible authority. Please confirm which department manages this issue.</p>
          </div>
          <div class="card">
            <h2>Official complaint channels found</h2>
            {% if channels %}
              {% for channel in channels %}
                <p><a href="{{ channel.link }}" target="_blank" rel="noopener">
                {{ channel.title or channel.link }}</a></p>
                <p>{{ channel.snippet }}</p>
              {% endfor %}
              <p class="note">Check that the channel accepts this issue before
              submitting. An official domain alone does not prove relevance.</p>
            {% else %}
              <p>No matching official channel was found in this search.
              Do not assume a general government portal accepts this complaint.</p>
            {% endif %}
          </div>
          <div class="card">
            <h2>Official search evidence</h2>
            {% if evidence %}
              {% for item in evidence %}
                <p><a href="{{ item.link }}" target="_blank" rel="noopener">
                {{ item.title or item.link }}</a></p>
                <p>{{ item.snippet }}</p>
              {% endfor %}
            {% else %}
              <p>No matching official Google results were found.</p>
            {% endif %}
          </div>
          <div class="card">
            <h2>Other live research</h2>
            <p>Google results: {{ google_count }} |
               Maps results: {{ maps_count }} |
               News results: {{ news_count }}</p>
            <p>These counts indicate returned search items, not proof that
            each item is relevant or independently verified.</p>
          </div>
          <div class="card">
            <h2>Complaint draft</h2>
            <pre id="draft">{{ complaint }}</pre>
            <button onclick="navigator.clipboard.writeText(
              document.getElementById('draft').innerText
            ).then(()=>this.innerText='Copied').catch(()=>this.innerText='Copy unavailable')">
              Copy complaint
            </button>
          </div>
          <div class="card">
            <h2>Next action</h2>
            <p>{{ next_action }}</p>
            <a href="/">← Back to CivicFix AI</a>
          </div>
        </body>
        </html>
        """

        return render_template_string(
            page,
            problem=problem,
            location=location,
            authority=action.get("authority", "Relevant local authority"),
            reason=action.get("reason", ""),
            channels=channels,
            evidence=action.get("evidence", []),
            google_count=len(google_results),
            maps_count=len(maps_results),
            news_count=len(news_results),
            complaint=action.get("complaint_draft", ""),
            next_action=action.get("next_action", "")
        )

    except Exception as e:
        app.logger.exception("CivicFix research failed: %s", e)
        return render_template_string(
            """
            <body style="background:#070b14;color:white;font-family:Arial;padding:24px">
              <h1>Research could not be completed</h1>
              <p>Please check the terminal logs, API quota and network connection.</p>
              <a style="color:#38bdf8" href="/">Back to CivicFix AI</a>
            </body>
            """
        ), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501, debug=True)
