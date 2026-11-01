
def metric_card(title, value, icon="📊", color="#4F46E5"):
    return f"""
    <div style="
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        border-left: 5px solid {color};
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    ">
        <div style="
            font-size: 15px;
            color: #64748b;
            font-weight: 600;
        ">
            {icon} {title}
        </div>

        <div style="
            font-size: 30px;
            font-weight: 700;
            color: #1e293b;
            margin-top: 10px;
        ">
            {value}
        </div>
    </div>
    """


def section_title(title):
    return f"""
    <div style="
        padding: 10px 0;
        margin: 20px 0 15px 0;
        border-bottom: 2px solid #4F46E5;
    ">
        <h3 style="
            color: #1e293b;
            font-size: 22px;
            font-weight: 700;
            margin: 0;
        ">
            {title}
        </h3>
    </div>
    """


def custom_css():
    return """
    <style>
        .stApp {
            background-color: #f8fafc;
        }

        div[data-testid="stMetric"] {
            background-color: white;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
        }

        h1, h2, h3 {
            color: #1e293b;
        }
    </style>
    """
import html


def apply_theme(theme):
    background = "#101827" if theme == "Dark" else "#f8fafc"
    foreground = "#edf3fa" if theme == "Dark" else "#19263a"
    border = "#26364d" if theme == "Dark" else "#e2e8f0"
    return f"""
    <style>
        .stApp {{ background-color: {background}; color: {foreground}; }}
        h1, h2, h3, p, label {{ color: {foreground}; }}
        div[data-testid="stMetric"] {{
            background: {background}; border: 1px solid {border};
            padding: 14px; border-radius: 12px;
        }}
        .brand {{ font-size: 24px; font-weight: 700; }}
        .brand span {{ color: #438cf5; }}
        .status {{ padding: 8px 0; color: #17a673; }}
    </style>
    """


def page_header(title, subtitle):
    return f"""
    <div style="padding: 0 0 12px 0">
        <h1>{html.escape(title)}</h1>
        <p>{html.escape(subtitle)}</p>
    </div>
    """


def section_title(title):
    return f"""
    <div style="padding: 10px 0; margin: 20px 0 15px 0;
                border-bottom: 2px solid #4f46e5">
        <h3 style="margin: 0">{html.escape(title)}</h3>
    </div>
    """


def skill_chips(skills, variant="neutral"):
    palette = {
        "matched": ("#dcfce7", "#166534"),
        "missing": ("#fee2e2", "#991b1b"),
        "neutral": ("#e0e7ff", "#3730a3"),
    }
    background, foreground = palette.get(variant, palette["neutral"])
    chips = [
        (
            '<span style="display:inline-block;background:'
            + background
            + ";color:"
            + foreground
            + ';padding:5px 10px;border-radius:20px;margin:3px">'
            + html.escape(str(skill))
            + "</span>"
        )
        for skill in skills
    ]
    return " ".join(chips) if chips else '<span style="color:#64748b">None identified</span>'


def custom_css():
    return apply_theme("Light")
