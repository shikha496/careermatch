
import plotly.graph_objects as go
import plotly.express as px


def base_layout(dark=False):
    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": "Inter",
            "color": "#EDF3FA" if dark else "#19263A"
        },
        "margin": dict(l=20, r=20, t=40, b=20)
    }


def match_gauge(score, dark=False):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={
                "suffix": "%",
                "font": {
                    "size": 38,
                    "color": "#EDF3FA" if dark else "#19263A"
                }
            },
            title={"text": "ATS MATCH RATE"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#17A673", "thickness": 0.23},
                "bgcolor": "#1A2940" if dark else "#F1F5F9",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "#FDE2E2"},
                    {"range": [40, 70], "color": "#FFF0C9"},
                    {"range": [70, 100], "color": "#D8F5E7"}
                ]
            }
        )
    )

    fig.update_layout(
        **base_layout(dark),
        height=260
    )

    return fig


def skill_comparison(matched, missing, dark=False):

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=["Skills"],
        y=[matched],
        name="Matched",
        marker_color="#17A673"
    ))

    fig.add_trace(go.Bar(
        x=["Skills"],
        y=[missing],
        name="Missing",
        marker_color="#E34D59"
    ))

    fig.update_layout(
        **base_layout(dark),
        barmode="stack",
        height=280,
        yaxis_title="Number of skills",
        legend=dict(orientation="h", y=1.12)
    )

    return fig


def score_breakdown(scores, dark=False):

    labels = [
        "Skills",
        "Experience",
        "Education",
        "Keywords",
        "Structure"
    ]

    values = [
        scores.get("skills") or 0,
        scores.get("experience", 0),
        scores.get("education", 0),
        scores.get("keywords", 0),
        scores.get("structure", 0)
    ]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker_color=[
            "#438CF5",
            "#17A673",
            "#E9A23B",
            "#8B72DC",
            "#2CA6B7"
        ]
    ))

    fig.update_layout(
        **base_layout(dark),
        height=320,
        xaxis=dict(range=[0, 100], title="Score (%)"),
        yaxis=dict(autorange="reversed")
    )

    return fig


def performance_radar(scores, dark=False):

    labels = list(scores.keys())
    values = list(scores.values())

    if not labels:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill="toself",
        line=dict(color="#438CF5", width=3),
        fillcolor="rgba(67,140,245,.2)"
    ))

    fig.update_layout(
        **base_layout(dark),
        height=350,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False
    )

    return fig


def category_donut(values, labels, dark=False):

    fig = px.pie(
        values=values,
        names=labels,
        hole=.68,
        color_discrete_sequence=[
            "#438CF5",
            "#17A673",
            "#E9A23B",
            "#8B72DC"
        ]
    )

    fig.update_layout(
        **base_layout(dark),
        height=320
    )

    return fig
