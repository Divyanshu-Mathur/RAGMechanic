from pathlib import Path
from datetime import datetime
from html import escape
import json


class HTMLReport:

    def __init__(self, output_path="rag_report.html"):

        self.output_path = Path(output_path)

        # All queries in this RAG session
        self.history = []

    # =========================================================
    # PUBLIC API
    # =========================================================

    def add_result(self, result):

        self.history.append(result)

    def generate(self):

        html = self._build_html()

        self.output_path.write_text(
            html,
            encoding="utf-8"
        )

        return self.output_path

    # =========================================================
    # MAIN HTML
    # =========================================================

    def _build_html(self):

        generated_at = datetime.now().strftime(
            "%d %b %Y, %I:%M %p"
        )

        return f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>RAG Mechanic Report</title>


<style>

/* =========================================================
   GLOBAL
   ========================================================= */

* {{
    box-sizing: border-box;
}}

body {{

    margin: 0;

    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    background: #f5f7fb;

    color: #172033;
}}

.container {{

    max-width: 1200px;

    margin: auto;

    padding: 40px 24px 80px;
}}


/* =========================================================
   HEADER
   ========================================================= */

.header {{

    display: flex;

    justify-content: space-between;

    align-items: center;

    margin-bottom: 32px;
}}

.logo {{

    font-size: 28px;

    font-weight: 800;
}}

.logo span {{
    color: #6366f1;
}}

.generated {{

    color: #64748b;

    font-size: 13px;
}}


/* =========================================================
   STATS
   ========================================================= */

.stats {{

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 16px;

    margin-bottom: 36px;
}}

.stat-card {{

    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 14px;

    padding: 22px;

    box-shadow:
        0 3px 12px
        rgba(0,0,0,0.04);
}}

.stat-label {{

    display: block;

    color: #64748b;

    font-size: 13px;

    margin-bottom: 10px;
}}

.stat-value {{

    font-size: 28px;

    font-weight: 750;
}}


/* =========================================================
   SECTION
   ========================================================= */

.section {{

    margin-bottom: 38px;
}}

.section-title {{

    font-size: 20px;

    font-weight: 750;

    margin-bottom: 16px;
}}


/* =========================================================
   QUERY
   ========================================================= */

.query-card,
.panel,
.history-card {{

    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 14px;

    box-shadow:
        0 3px 12px
        rgba(0,0,0,0.04);
}}

.query-card {{

    padding: 26px;
}}

.label {{

    color: #6366f1;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1px;

    margin-bottom: 8px;
}}

.question {{

    font-size: 20px;

    font-weight: 650;

    line-height: 1.5;

    margin-bottom: 25px;
}}

.answer-label {{

    margin-top: 10px;
}}

.answer {{

    white-space: pre-wrap;

    line-height: 1.7;

    color: #475569;
}}


/* =========================================================
   PANELS
   ========================================================= */

.panel {{

    margin-top: 18px;

    padding: 24px;
}}

.panel h3 {{

    margin-top: 0;

    margin-bottom: 20px;

    font-size: 16px;
}}


/* =========================================================
   TABLE
   ========================================================= */

.table-wrapper {{

    overflow-x: auto;
}}

table {{

    width: 100%;

    border-collapse: collapse;

    font-size: 14px;
}}

th {{

    text-align: left;

    color: #64748b;

    font-size: 12px;

    text-transform: uppercase;

    padding: 12px;

    border-bottom:
        1px solid #e5e7eb;
}}

td {{

    padding: 14px 12px;

    border-bottom:
        1px solid #f1f5f9;
}}

.score {{

    font-weight: 700;

    color: #4f46e5;
}}


/* =========================================================
   COMPRESSION
   ========================================================= */

.compression {{

    display: flex;

    align-items: center;

    gap: 22px;

    flex-wrap: wrap;
}}

.compression-box {{

    min-width: 130px;

    text-align: center;

    padding: 18px;

    background: #f8fafc;

    border-radius: 12px;
}}

.compression-box span,
.compression-box small {{

    display: block;

    color: #64748b;

    font-size: 12px;
}}

.compression-box strong {{

    display: block;

    font-size: 30px;

    margin: 5px;
}}

.arrow {{

    font-size: 28px;

    color: #94a3b8;
}}

.compression-ratio {{

    margin-left: auto;

    text-align: center;

    padding: 15px 25px;

    background: #eef2ff;

    border-radius: 12px;
}}

.compression-ratio span {{

    display: block;

    font-size: 12px;

    color: #64748b;
}}

.compression-ratio strong {{

    font-size: 25px;

    color: #4f46e5;
}}


/* =========================================================
   LATENCY
   ========================================================= */

.latency-grid {{

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 12px;
}}

.latency-grid div {{

    background: #f8fafc;

    padding: 18px;

    border-radius: 10px;
}}

.latency-grid span {{

    display: block;

    color: #64748b;

    font-size: 12px;

    margin-bottom: 7px;
}}

.latency-grid strong {{

    font-size: 18px;
}}

.latency-grid .total {{

    background: #eef2ff;
}}


/* =========================================================
   EVALUATION
   ========================================================= */

.evaluation-grid {{

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 14px;
}}

.metric {{

    padding: 20px;

    border-radius: 12px;

    background: #f8fafc;
}}

.metric span {{

    display: block;

    color: #64748b;

    margin-bottom: 8px;
}}

.metric strong {{

    font-size: 27px;
}}


/* =========================================================
   SOURCES
   ========================================================= */

.sources {{

    display: flex;

    gap: 10px;

    flex-wrap: wrap;
}}

.source {{

    padding: 8px 12px;

    border-radius: 20px;

    background: #eef2ff;

    color: #4f46e5;

    font-size: 13px;

    font-weight: 600;
}}


/* =========================================================
   HISTORY
   ========================================================= */

.history {{

    display: flex;

    flex-direction: column;

    gap: 10px;
}}

.history-card {{

    padding: 18px 20px;

    cursor: pointer;

    transition:
        transform 0.15s,
        box-shadow 0.15s,
        border 0.15s;
}}

.history-card:hover {{

    transform: translateY(-2px);

    box-shadow:
        0 6px 18px
        rgba(0,0,0,0.08);
}}

.history-card.active {{

    border-left:
        4px solid #6366f1;

    background: #fafaff;
}}

.history-number {{

    color: #6366f1;

    font-size: 11px;

    font-weight: 800;

    text-transform: uppercase;

    margin-bottom: 6px;
}}

.history-question {{

    font-weight: 600;

    margin-bottom: 10px;
}}

.history-meta {{

    display: flex;

    gap: 18px;

    color: #64748b;

    font-size: 12px;
}}


/* =========================================================
   EMPTY
   ========================================================= */

.empty {{

    padding: 40px;

    text-align: center;

    color: #64748b;
}}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media(max-width: 800px) {{

    .stats,
    .latency-grid {{

        grid-template-columns:
            repeat(2, 1fr);
    }}

    .evaluation-grid {{

        grid-template-columns: 1fr;
    }}
}}

@media(max-width: 500px) {{

    .stats,
    .latency-grid {{

        grid-template-columns: 1fr;
    }}

    .header {{

        display: block;
    }}

    .generated {{

        margin-top: 8px;
    }}
}}

</style>

</head>


<body>


<div class="container">


<header class="header">

    <div class="logo">
        RAG<span>Lab</span>
    </div>

    <div class="generated">
        Generated {generated_at}
    </div>

</header>


{self._overview()}


<!-- =====================================================
     CURRENT QUERY
     ===================================================== -->

<section class="section">

    <div class="section-title">
        Query Details
    </div>

    <div id="query-details">

        {self._query_details(0)}

    </div>

</section>


<!-- =====================================================
     QUERY HISTORY
     ===================================================== -->

<section class="section">

    <div class="section-title">
        Query History
    </div>

    <div class="history">

        {self._history_cards()}

    </div>

</section>


</div>


<!-- =====================================================
     JAVASCRIPT
     ===================================================== -->

<script>

const queryData = {self._javascript_data()};


function showQuery(index) {{

    const container =
        document.getElementById(
            "query-details"
        );

    container.innerHTML =
        queryData[index].html;


    // Remove active state
    document
        .querySelectorAll(".history-card")
        .forEach(card => {{
            card.classList.remove("active");
        }});


    // Add active state
    const selected =
        document.querySelector(
            `[data-query-index="${{index}}"]`
        );

    if (selected) {{
        selected.classList.add("active");
    }}


    // Scroll to query details
    document
        .getElementById("query-details")
        .scrollIntoView({{
            behavior: "smooth",
            block: "start"
        }});
}}


// Select latest query initially
showQuery({len(self.history) - 1});

</script>


</body>

</html>
"""

    # =========================================================
    # OVERVIEW
    # =========================================================

    def _overview(self):

        total = len(self.history)

        faithfulness_values = []

        relevancy_values = []

        latency_values = []

        for result in self.history:

            if result.evaluation:

                value = getattr(
                    result.evaluation,
                    "faithfulness",
                    None
                )

                if value is not None:
                    faithfulness_values.append(
                        float(value)
                    )

                value = getattr(
                    result.evaluation,
                    "answer_relevancy",
                    None
                )

                if value is not None:
                    relevancy_values.append(
                        float(value)
                    )

            latency_values.append(
                result.total_latency
            )

        avg_faithfulness = (
            sum(faithfulness_values)
            / len(faithfulness_values)
            if faithfulness_values
            else 0
        )

        avg_relevancy = (
            sum(relevancy_values)
            / len(relevancy_values)
            if relevancy_values
            else 0
        )

        avg_latency = (
            sum(latency_values)
            / len(latency_values)
            if latency_values
            else 0
        )

        return f"""
<div class="stats">

    <div class="stat-card">

        <span class="stat-label">
            Total Queries
        </span>

        <span class="stat-value">
            {total}
        </span>

    </div>


    <div class="stat-card">

        <span class="stat-label">
            Avg. Faithfulness
        </span>

        <span class="stat-value">
            {avg_faithfulness:.2f}
        </span>

    </div>


    <div class="stat-card">

        <span class="stat-label">
            Avg. Relevancy
        </span>

        <span class="stat-value">
            {avg_relevancy:.2f}
        </span>

    </div>


    <div class="stat-card">

        <span class="stat-label">
            Avg. Latency
        </span>

        <span class="stat-value">
            {avg_latency:.2f}s
        </span>

    </div>

</div>
"""

    # =========================================================
    # QUERY DETAILS
    # =========================================================

    def _query_details(self, index):

        if not self.history:

            return """
            <div class="empty">
                No queries have been executed yet.
            </div>
            """

        return self._query_html(
            self.history[index]
        )

    # =========================================================
    # QUERY HTML
    # =========================================================

    def _query_html(self, result):

        return f"""

<div class="query-card">


    <div class="label">
        QUESTION
    </div>


    <div class="question">

        {escape(result.question)}

    </div>


    <div class="label answer-label">
        ANSWER
    </div>


    <div class="answer">

        {escape(result.answer)}

    </div>


</div>


{self._retrieval(result)}


{self._compression(result)}


{self._latency(result)}


{self._evaluation(result)}


{self._sources(result)}

"""

    # =========================================================
    # RETRIEVAL
    # =========================================================

    def _retrieval(self, result):

        rows = ""

        for i, doc in enumerate(
            result.retrieved_documents,
            start=1
        ):

            score = doc.metadata.get(
                "similarity_score"
            )

            source = doc.metadata.get(
                "source",
                "Unknown"
            )

            page = doc.metadata.get(
                "page",
                "-"
            )

            score_text = (
                f"{float(score):.3f}"
                if score is not None
                else "-"
            )

            rows += f"""
<tr>

    <td>{i}</td>

    <td>
        {escape(str(source))}
    </td>

    <td>
        {page}
    </td>

    <td>

        <span class="score">
            {score_text}
        </span>

    </td>

</tr>
"""

        return f"""
<div class="panel">

    <h3>
        Retrieved Chunks
    </h3>

    <div class="table-wrapper">

        <table>

            <thead>

                <tr>

                    <th>#</th>

                    <th>Source</th>

                    <th>Page</th>

                    <th>Similarity</th>

                </tr>

            </thead>

            <tbody>

                {rows}

            </tbody>

        </table>

    </div>

</div>
"""

    # =========================================================
    # COMPRESSION
    # =========================================================

    def _compression(self, result):

        before = result.retrieved_count

        after = result.compressed_count

        ratio = result.compression_ratio

        return f"""
<div class="panel">

    <h3>
        Context Compression
    </h3>

    <div class="compression">


        <div class="compression-box">

            <span>
                Before
            </span>

            <strong>
                {before}
            </strong>

            <small>
                chunks
            </small>

        </div>


        <div class="arrow">
            →
        </div>


        <div class="compression-box">

            <span>
                After
            </span>

            <strong>
                {after}
            </strong>

            <small>
                chunks
            </small>

        </div>


        <div class="compression-ratio">

            <span>
                Compression
            </span>

            <strong>
                {ratio:.1f}%
            </strong>

        </div>


    </div>

</div>
"""

    # =========================================================
    # LATENCY
    # =========================================================

    def _latency(self, result):

        return f"""
<div class="panel">

    <h3>
        Latency
    </h3>

    <div class="latency-grid">


        <div>

            <span>
                Retrieval
            </span>

            <strong>
                {result.retrieval_latency:.3f}s
            </strong>

        </div>


        <div>

            <span>
                Compression
            </span>

            <strong>
                {result.compression_latency:.3f}s
            </strong>

        </div>


        <div>

            <span>
                Generation
            </span>

            <strong>
                {result.generation_latency:.3f}s
            </strong>

        </div>


        <div class="total">

            <span>
                Total
            </span>

            <strong>
                {result.total_latency:.3f}s
            </strong>

        </div>


    </div>

</div>
"""

    # =========================================================
    # EVALUATION
    # =========================================================

    def _evaluation(self, result):

        if result.evaluation is None:

            return ""

        evaluation = result.evaluation

        faithfulness = getattr(
            evaluation,
            "faithfulness",
            None
        )

        relevancy = getattr(
            evaluation,
            "answer_relevancy",
            None
        )

        hallucination = getattr(
            evaluation,
            "hallucination",
            None
        )

        return f"""
<div class="panel">

    <h3>
        Evaluation
    </h3>

    <div class="evaluation-grid">


        {self._metric(
            "Faithfulness",
            faithfulness
        )}


        {self._metric(
            "Answer Relevancy",
            relevancy
        )}


        {self._metric(
            "Hallucination",
            hallucination
        )}


    </div>

</div>
"""

    # =========================================================
    # METRIC
    # =========================================================

    def _metric(self, name, value):

        if value is None:

            formatted = "-"

        else:

            formatted = f"{float(value):.2f}"

        return f"""
<div class="metric">

    <span>
        {name}
    </span>

    <strong>
        {formatted}
    </strong>

</div>
"""

    # =========================================================
    # SOURCES
    # =========================================================

    def _sources(self, result):

        sources = ""

        for source in result.sources:

            sources += f"""
<span class="source">

    {escape(str(source))}

</span>
"""

        return f"""
<div class="panel">

    <h3>
        Sources Used
    </h3>

    <div class="sources">

        {sources}

    </div>

</div>
"""

    # =========================================================
    # HISTORY CARDS
    # =========================================================

    def _history_cards(self):

        cards = ""

        for index, result in enumerate(
            self.history
        ):

            evaluation = result.evaluation

            faithfulness = "-"

            if evaluation:

                value = getattr(
                    evaluation,
                    "faithfulness",
                    None
                )

                if value is not None:

                    faithfulness = (
                        f"{float(value):.2f}"
                    )


            cards += f"""
<div
    class="history-card"
    data-query-index="{index}"
    onclick="showQuery({index})"
>


    <div class="history-number">

        Query {index + 1}

    </div>


    <div class="history-question">

        {escape(result.question)}

    </div>


    <div class="history-meta">

        <span>
            {result.total_latency:.2f}s
        </span>

        <span>
            {result.retrieved_count}
            chunks
        </span>

        <span>
            Faithfulness:
            {faithfulness}
        </span>

    </div>


</div>
"""

        return cards

    # =========================================================
    # JAVASCRIPT DATA
    # =========================================================

    def _javascript_data(self):

        data = []

        for result in self.history:

            data.append({

                "html":
                    self._query_html(
                        result
                    )

            })

        return json.dumps(
            data,
            ensure_ascii=False
        )
