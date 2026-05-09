import streamlit as st
import json, csv, os, uuid
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Rachel's Tea – Digestive Health Survey",
    page_icon="🍵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

CONFIG_FILE = "survey_config.json"
RESPONSES_FILE = "responses.csv"

# ── Config ─────────────────────────────────────────────────────────────────────
def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

# ── Responses ──────────────────────────────────────────────────────────────────
def save_response(answers, cfg):
    questions = cfg["questions"]
    fieldnames = ["timestamp", "session_id"] + [q["id"] for q in questions]
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "session_id": st.session_state.get("session_id", ""),
    }
    for q in questions:
        row[q["id"]] = answers.get(q["id"], "")
    exists = os.path.exists(RESPONSES_FILE) and os.path.getsize(RESPONSES_FILE) > 0
    with open(RESPONSES_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            w.writeheader()
        w.writerow(row)

def load_responses():
    if not os.path.exists(RESPONSES_FILE):
        return pd.DataFrame()
    try:
        return pd.read_csv(RESPONSES_FILE)
    except Exception:
        return pd.DataFrame()

# ── CSS ────────────────────────────────────────────────────────────────────────
def inject_css(p="#2D6A4F"):
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, .stApp {{ background: #FAFAFA !important; min-height: 100vh; font-family: 'Inter', sans-serif !important; }}
[data-testid="stToolbar"], [data-testid="stHeaderActionElements"], [data-testid="stAppDeployButton"], #MainMenu, footer {{ display: none !important; }}
.block-container {{ padding: 3.5rem 0 0 0 !important; max-width: 760px !important; }}

/* ── Force Light Theme Text Colors (Fix for Streamlit Dark Mode) ── */
.stApp .block-container h1, .stApp .block-container h2, .stApp .block-container h3, 
.stApp .block-container p, .stApp .block-container span, .stApp .block-container label, 
.stApp .block-container div[data-testid="stMarkdownContainer"] {{
    color: #1F2937 !important;
}}
/* Keep specific custom colored elements readable */
.stApp .block-container div[data-testid="stButton"] > button[kind="primary"] p,
.stApp .block-container div[data-testid="stButton"] > button[kind="primary"] span {{
    color: #FFFFFF !important;
}}
.stApp .block-container .ans-head span, .stApp .block-container .cta-title, .stApp .block-container .cta-body {{ color: #FFFFFF !important; }}
.stApp .block-container .offer-top-badge, .stApp .block-container .offer-top-price {{ color: #7C4700 !important; }}
.stApp .block-container .offer-top-title, .stApp .block-container .offer-top-price b {{ color: #1a1a1a !important; }}
.stApp .block-container .cta-btn {{ color: #1a1a1a !important; }}

/* Fix Admin Panel Inputs in Dark Mode */
.stApp .block-container textarea, .stApp .block-container input, 
.stApp .block-container div[data-baseweb="select"] > div {{
    background-color: #FFFFFF !important;
    color: #1F2937 !important;
    border-color: #D1D5DB !important;
}}

/* ── Banner ── */
.rt-banner-container {{
    background: #FFFFFF;
    width: 100%;
    padding: 1.5rem 1rem;
    text-align: center;
    border-bottom: 1px solid #E5E7EB;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    margin-bottom: 1rem;
}}
.rt-logo-text {{
    font-family: 'Inter', sans-serif !important;
    font-size: 2.6rem;
    font-weight: 800;
    color: #3A7D44;
    letter-spacing: -1.2px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    line-height: 1;
}}
.rt-logo-tagline {{
    font-size: 0.85rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #5C7A5C;
    font-weight: 500;
    margin-top: 0.5rem;
}}

/* ── Progress bar area ── */
.prog-area {{ display:flex; align-items:center; gap:1rem; padding:1.2rem 1.6rem 0.6rem; }}
.prog-bar-bg {{ flex:1; height:8px; background:#E5E7EB; border-radius:999px; overflow:hidden; }}
.prog-bar-fill {{ height:100%; border-radius:999px; background:#6366F1; transition:width .5s ease; }}
.prog-count {{ font-size:.85rem; color:#6B7280; font-weight:600; white-space:nowrap; }}

/* ── Brand ── */
.brand-center {{ text-align:center; padding:.6rem 1.6rem .2rem; }}
.brand-name {{ font-size:1.05rem; font-weight:800; color:{p}; }}

/* ── Question text ── */
.q-title {{ font-size:1.55rem; font-weight:800; color:#111827; line-height:1.35; padding:.8rem 1.6rem 1.2rem; }}

/* ── Option buttons ── */
div.element-container:has(.options-marker) ~ div.element-container div[data-testid="stButton"] > button[kind="secondary"] {{
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    width: 100% !important;
    background: #FFFFFF !important;
    color: #1F2937 !important;
    border: 2px solid #F3F4F6 !important;
    border-radius: 16px !important;
    padding: 1.2rem 1.25rem !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    cursor: pointer !important;
    transition: all .2s ease !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
    margin-bottom: .6rem !important;
}}
div.element-container:has(.options-marker) ~ div.element-container div[data-testid="stButton"] > button[kind="secondary"] div[data-testid="stMarkdownContainer"] {{
    width: 100% !important;
}}
div.element-container:has(.options-marker) ~ div.element-container div[data-testid="stButton"] > button[kind="secondary"] p {{
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 100% !important;
    margin: 0 !important;
    white-space: normal !important;
    text-align: left !important;
}}
div.element-container:has(.options-marker) ~ div.element-container div[data-testid="stButton"] > button[kind="secondary"] p::after {{
    content: '';
    display: inline-block;
    width: 24px;
    min-width: 24px;
    height: 24px;
    min-height: 24px;
    flex-shrink: 0;
    border: 2px solid #D1D5DB;
    border-radius: 6px;
    background-color: #FFFFFF;
    margin-left: 1rem;
    transition: all 0.2s;
}}

div.element-container:has(.options-marker) ~ div.element-container div[data-testid="stButton"] > button[kind="secondary"]:hover {{
    border-color: #C7D2FE !important;
    background: #FAFAFF !important;
    transform: translateY(-1px) !important;
}}

/* Sidebar Button Reset */
section[data-testid="stSidebar"] div[data-testid="stButton"] > button {{
    background-color: transparent !important;
    color: #F1F5F9 !important;
    border: 1px solid rgba(241, 245, 249, 0.2) !important;
    border-radius: 0.5rem !important;
    padding: 0.5rem 1rem !important;
    justify-content: center !important;
    box-shadow: none !important;
}}
section[data-testid="stSidebar"] div[data-testid="stButton"] > button p::after {{
    display: none !important;
}}
section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {{
    border-color: #6366F1 !important;
    color: #6366F1 !important;
    background-color: rgba(99, 102, 241, 0.1) !important;
}}

/* Primary (action) buttons */
div[data-testid="stButton"] > button[kind="primary"],
div[data-testid="stButton"] > button.stBaseButton-primary {{
    background: #6366F1 !important; 
    color: #fff !important; 
    border: none !important;
    border-radius: 16px !important; 
    font-size: 1.15rem !important; 
    font-weight: 700 !important;
    text-align: center !important; 
    padding: 1rem 1.5rem !important; 
    width: 100% !important;
    box-shadow: 0 4px 16px rgba(99,102,241,0.3) !important;
    justify-content: center !important; 
    margin-bottom: 0 !important;
    margin-top: 1rem !important;
}}
div[data-testid="stButton"] > button[kind="primary"] p::after,
div[data-testid="stButton"] > button.stBaseButton-primary p::after {{
    display: none !important;
}}
div[data-testid="stButton"] > button[kind="primary"]:hover,
div[data-testid="stButton"] > button.stBaseButton-primary:hover {{
    background: #4F46E5 !important; 
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.4) !important;
}}
div[data-testid="stButton"] > button[kind="primary"]:disabled,
div[data-testid="stButton"] > button.stBaseButton-primary:disabled {{
    background: #E5E7EB !important; 
    color: #9CA3AF !important;
    box-shadow: none !important; 
    transform: none !important; 
    cursor: not-allowed !important;
}}

/* Back button — subtle */
.back-btn div[data-testid="stButton"] > button {{
    background: #FFFFFF !important;
    color: #374151 !important;
    border: 2px solid #E5E7EB !important;
    border-radius: 50% !important;
    width: 42px !important;
    height: 42px !important;
    padding: 0 !important;
    font-size: 1.2rem !important;
    justify-content: center !important;
    margin-bottom: 0 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,.04) !important;
}}
.back-btn div[data-testid="stButton"] > button p::after {{
    display: none !important;
}}
.back-btn div[data-testid="stButton"] > button:hover {{
    background: #F9FAFB !important;
    border-color: #D1D5DB !important;
    transform: translateY(-1px) !important;
}}

/* ── Email input ── */
div[data-testid="stTextInput"] > div > input {{
    border-radius: 14px !important;
    border: 2px solid #E5E7EB !important;
    padding: .85rem 1rem !important;
    font-size: 1rem !important;
    background: #fff !important;
    transition: border-color .2s !important;
}}
div[data-testid="stTextInput"] > div > input:focus {{
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.15) !important;
}}

/* ── Completion screen ── */
.offer-top {{
    background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%);
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
    margin: 1rem 1.6rem .5rem;
    text-align: center;
    box-shadow: 0 4px 24px rgba(245,158,11,.35);
}}
.offer-top-badge {{ font-size:.68rem; font-weight:800; text-transform:uppercase; letter-spacing:1.5px; color:#7C4700; margin-bottom:.4rem; }}
.offer-top-title {{ font-size:1.35rem; font-weight:800; color:#1a1a1a; margin:.2rem 0; }}
.offer-top-price {{ font-size:.95rem; color:#7C4700; font-weight:600; margin-top:.3rem; }}
.offer-top-price b {{ font-size:1.6rem; color:#333; }}

.done-section {{ padding:.8rem 1.6rem 1.2rem; }}
.done-headline {{ font-size:1.45rem; font-weight:800; color:#111827; margin-bottom:.4rem; }}
.done-sub {{ font-size:.93rem; color:#6B7280; line-height:1.65; margin-bottom:1.2rem; }}

/* Answer table */
.ans-wrap {{ background:#fff; border-radius:16px; border:1px solid #E5E7EB; overflow:hidden; margin-bottom:1.2rem; }}
.ans-head {{ display:flex; background:{p}; padding:.6rem 1rem; }}
.ans-head span {{ font-size:.72rem; font-weight:700; color:#fff; text-transform:uppercase; letter-spacing:.8px; }}
.ans-row {{ display:flex; align-items:flex-start; padding:.7rem 1rem; border-bottom:1px solid #F3F4F6; }}
.ans-row:last-child {{ border-bottom:none; }}
.ans-q {{ font-size:.85rem; color:#374151; flex:1; padding-right:.75rem; line-height:1.45; }}
.ans-a {{ font-size:.85rem; font-weight:700; color:{p}; text-align:right; max-width:46%; flex-shrink:0; }}

/* CTA bottom box */
.cta-bottom {{
    background: linear-gradient(135deg, #1B4332 0%, {p} 100%);
    border-radius: 20px;
    padding: 1.8rem;
    text-align: center;
    margin-bottom: 1.2rem;
}}
.cta-title {{ font-size:1.1rem; font-weight:800; color:#fff; margin-bottom:.45rem; }}
.cta-body {{ font-size:.88rem; color:rgba(255,255,255,.88); line-height:1.65; margin-bottom:1.1rem; }}
.cta-btn {{
    display:block; background:#FBBF24; color:#1a1a1a !important;
    text-decoration:none; padding:.95rem 1.5rem; border-radius:13px;
    font-size:1rem; font-weight:800; transition:all .2s;
}}
.cta-btn:hover {{ background:#F59E0B; transform:translateY(-2px); text-decoration:none; }}
.disc {{ font-size:.7rem; color:rgba(255,255,255,.4); margin-top:.65rem; }}

/* Sidebar admin */
section[data-testid="stSidebar"] {{ background: #0F172A !important; }}
section[data-testid="stSidebar"] * {{ color: #F1F5F9 !important; }}
section[data-testid="stSidebar"] input {{ background: #1E293B !important; border-color: #334155 !important; }}
/* Remove extra margin streamlit adds to button containers */
div[data-testid="stButton"] {{ margin: 0 !important; }}
</style>
""", unsafe_allow_html=True)

EMOJIS = ["🌿","💊","🔥","🤔","❤️","🍬","🥗","🍔","📅","💩","📧","✨","😊","⚡","🌱"]

def render_banner():
    st.markdown("""
<div class="rt-banner-container">
    <div class="rt-logo-text">
        <span style="color: #3A7D44; font-size: 2.8rem;">🌿</span>
        <span>Rachelstea.com</span>
    </div>
    <div class="rt-logo-tagline">
        Natural Digestive Relief Solutions
    </div>
</div>
""", unsafe_allow_html=True)

# ── Survey ─────────────────────────────────────────────────────────────────────
def show_survey(cfg):
    questions = cfg["questions"]
    total = len(questions)
    ss = st.session_state
    ss.setdefault("current_q", 0)
    ss.setdefault("answers", {})
    ss.setdefault("session_id", str(uuid.uuid4()))
    ss.setdefault("survey_complete", False)
    ss.setdefault("response_saved", False)

    if ss.survey_complete:
        show_completion(cfg)
        return

    # Banner only shown for question screens (completion page renders its own)
    render_banner()

    idx = ss.current_q
    if idx >= total:
        if not ss.response_saved:
            save_response(ss.answers, cfg)
            ss.response_saved = True
        ss.survey_complete = True
        st.rerun()
        return

    q = questions[idx]
    pct = int((idx / total) * 100)

    # ── Progress row ──
    c_back, c_prog, c_cnt = st.columns([0.09, 0.76, 0.15])
    with c_back:
        if idx > 0:
            st.markdown('<div class="back-btn">', unsafe_allow_html=True)
            if st.button("←", key="back_btn"):
                ss.current_q -= 1
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    with c_prog:
        st.markdown(
            f'<div style="padding-top:.65rem"><div class="prog-bar-bg">'
            f'<div class="prog-bar-fill" style="width:{pct}%"></div></div></div>',
            unsafe_allow_html=True,
        )
    with c_cnt:
        st.markdown(
            f'<div class="prog-count" style="padding-top:.6rem">{idx+1}/{total}</div>',
            unsafe_allow_html=True,
        )


    # ── Question ──
    st.markdown(f'<div class="q-title">{q["text"]}</div>', unsafe_allow_html=True)

    # ── Options ──
    current_ans = ss.answers.get(q["id"])

    with st.container():
        st.markdown('<div style="padding:0 1.6rem;">', unsafe_allow_html=True)

        if q["type"] == "single_choice":
            opts = q.get("options", [])
            emojis_list = q.get("emojis", [])
            selected_index = opts.index(current_ans) if current_ans in opts else -1
            
            style_html = ""
            if selected_index >= 0:
                style_html = f"""<style>
                div.element-container:has(.options-marker) ~ div.element-container:nth-of-type({selected_index + 2}) div[data-testid="stButton"] > button[kind="secondary"] {{
                    border-color: #6366F1 !important;
                    background: #EEEDFE !important;
                    color: #3730A3 !important;
                    font-weight: 600 !important;
                    box-shadow: 0 4px 12px rgba(99,102,241,0.1) !important;
                }}
                div.element-container:has(.options-marker) ~ div.element-container:nth-of-type({selected_index + 2}) div[data-testid="stButton"] > button[kind="secondary"] p::after {{
                    background-color: #FFFFFF !important;
                    border-color: #6366F1 !important;
                    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='%236366F1'%3E%3Cpath fill-rule='evenodd' d='M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z' clip-rule='evenodd'/%3E%3C/svg%3E") !important;
                    background-size: 80% !important;
                    background-position: center !important;
                    background-repeat: no-repeat !important;
                }}
                </style>""".replace('\n', ' ')

            with st.container():
                st.markdown(f'<div style="display:none; margin:0; padding:0;"><span class="options-marker"></span>{style_html}</div>', unsafe_allow_html=True)
                for i, opt in enumerate(opts):
                    em = emojis_list[i] if i < len(emojis_list) else EMOJIS[i % len(EMOJIS)]
                    label = f"{em}  {opt}"
                    if st.button(label, key=f"opt_{q['id']}_{i}"):
                        ss.answers[q["id"]] = opt
                        st.rerun()

            # ── Next button for single choice ──
            msg_style = "visibility: hidden;" if current_ans else ""
            st.markdown(f'<div style="color: #6B7280; font-size: 0.95rem; text-align: center; margin-top: 1rem; margin-bottom: 0.5rem; font-weight: 500; {msg_style}">Please choose your option to continue</div>', unsafe_allow_html=True)
            
            st.markdown('<div id="action-btn-single">', unsafe_allow_html=True)
            if st.button("Next →", key=f"next_{q['id']}", disabled=not current_ans, type="primary"):
                if idx < total - 1:
                    ss.current_q += 1
                else:
                    if not ss.response_saved:
                        save_response(ss.answers, cfg)
                        ss.response_saved = True
                    ss.survey_complete = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        elif q["type"] == "email":
            val = st.text_input(
                "email",
                value=current_ans or "",
                placeholder="your@email.com",
                key=f"email_{q['id']}",
                label_visibility="collapsed",
            )
            ss.answers[q["id"]] = val
            st.markdown("<br>", unsafe_allow_html=True)
            can = "@" in (val or "") and "." in (val or "")
            st.markdown('<div id="action-btn-email">', unsafe_allow_html=True)
            if st.button(
                "Submit & Claim My Gift →" if idx == total - 1 else "Next →",
                key="email_next",
                disabled=not can,
                type="primary",
            ):
                if idx < total - 1:
                    ss.current_q += 1
                else:
                    if not ss.response_saved:
                        save_response(ss.answers, cfg)
                        ss.response_saved = True
                    ss.survey_complete = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        elif q["type"] == "text":
            val = st.text_area(
                "answer",
                value=current_ans or "",
                key=f"txt_{q['id']}",
                height=110,
                label_visibility="collapsed",
                placeholder="Type your answer here…",
            )
            ss.answers[q["id"]] = val
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div id="action-btn-txt">', unsafe_allow_html=True)
            if st.button("Next →", key="txt_next", disabled=not (val or "").strip(), type="primary"):
                if idx < total - 1:
                    ss.current_q += 1
                else:
                    if not ss.response_saved:
                        save_response(ss.answers, cfg)
                        ss.response_saved = True
                    ss.survey_complete = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

# ── Completion ─────────────────────────────────────────────────────────────────
def show_completion(cfg):
    ss = st.session_state
    c = cfg["completion"]
    questions = cfg["questions"]

    render_banner()

    # 🎁 Gummies offer — TOP
    st.markdown(f"""
<div class="offer-top">
  <div class="offer-top-badge">🎁 {c['offer_badge']}</div>
  <div class="offer-top-title">{c['offer_headline']}</div>
  <div class="offer-top-price">Only <b>{c['offer_price']}</b> {c['offer_price_label']}</div>
</div>""", unsafe_allow_html=True)

    # Done section
    st.markdown(f"""
<div class="done-section">
  <div class="done-headline">{c['headline']}</div>
  <div class="done-sub">{c['subheadline']}</div>

  <div class="ans-wrap">
    <div class="ans-head">
      <span style="flex:1">Question</span>
      <span>Your Answer</span>
    </div>""", unsafe_allow_html=True)

    for q in questions:
        ans = ss.answers.get(q["id"], "—")
        short_q = q["text"][:60] + ("…" if len(q["text"]) > 60 else "")
        st.markdown(
            f'<div class="ans-row">'
            f'<span class="ans-q">{short_q}</span>'
            f'<span class="ans-a">{ans}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown(f"""
  </div>

  <div class="cta-bottom">
    <div class="cta-title">{c['offer_headline']}</div>
    <div class="cta-body">{c['offer_body']}</div>
    <a href="{c['cta_url']}" target="_blank" class="cta-btn">{c['cta_label']}</a>
    <div class="disc">{c['disclaimer']}</div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div style="padding:0 1.6rem 2rem">', unsafe_allow_html=True)
    st.markdown('<div id="action-btn-restart">', unsafe_allow_html=True)
    if st.button("↩ Take Survey Again", key="restart_btn", type="primary"):
        for k in ["current_q", "answers", "survey_complete", "response_saved", "session_id"]:
            ss.pop(k, None)
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

# ── Admin Panel ────────────────────────────────────────────────────────────────
def show_admin(cfg):
    import plotly.express as px
    st.title("⚙️ Admin Panel")
    st.caption("All changes save instantly to `survey_config.json` — no code needed.")
    t1, t2, t3, t4 = st.tabs(["📋 Questions", "🎨 Branding", "🎁 Completion", "📊 Responses"])

    with t1:
        st.subheader("Survey Questions")
        for i, q in enumerate(cfg["questions"]):
            label = f"Q{i+1}: {q['text'][:52]}{'…' if len(q['text'])>52 else ''}"
            with st.expander(label):
                cfg["questions"][i]["text"] = st.text_area("Question text", value=q["text"], key=f"qt_{i}")
                types = ["single_choice", "email", "text"]
                cfg["questions"][i]["type"] = st.selectbox(
                    "Type", types,
                    index=types.index(q["type"]) if q["type"] in types else 0,
                    key=f"qtp_{i}",
                )
                if cfg["questions"][i]["type"] == "single_choice":
                    opts_str = "\n".join(q.get("options", []))
                    new_opts = st.text_area("Options (one per line)", value=opts_str, key=f"qo_{i}", height=120)
                    cfg["questions"][i]["options"] = [o.strip() for o in new_opts.splitlines() if o.strip()]
                c1, c2, c3 = st.columns(3)
                with c1:
                    if i > 0 and st.button("⬆ Up", key=f"up_{i}"):
                        cfg["questions"][i], cfg["questions"][i-1] = cfg["questions"][i-1], cfg["questions"][i]
                        save_config(cfg); st.rerun()
                with c2:
                    if i < len(cfg["questions"])-1 and st.button("⬇ Down", key=f"dn_{i}"):
                        cfg["questions"][i], cfg["questions"][i+1] = cfg["questions"][i+1], cfg["questions"][i]
                        save_config(cfg); st.rerun()
                with c3:
                    if st.button("🗑 Delete", key=f"dl_{i}"):
                        cfg["questions"].pop(i); save_config(cfg); st.rerun()

        st.divider()
        st.subheader("➕ Add New Question")
        with st.form("add_q_form"):
            nq_text = st.text_area("Question text", placeholder="Enter your question…")
            nq_type = st.selectbox("Type", ["single_choice", "email", "text"])
            nq_opts = st.text_area("Options (single_choice, one per line)", height=90)
            if st.form_submit_button("Add Question ✓"):
                if nq_text.strip():
                    nq = {
                        "id": f"q{len(cfg['questions'])+1}_{uuid.uuid4().hex[:4]}",
                        "text": nq_text.strip(),
                        "type": nq_type,
                        "required": True,
                    }
                    if nq_type == "single_choice":
                        nq["options"] = [o.strip() for o in nq_opts.splitlines() if o.strip()]
                    cfg["questions"].append(nq)
                    save_config(cfg); st.success("✅ Question added!"); st.rerun()

        if st.button("💾 Save All Question Edits", type="primary"):
            save_config(cfg); st.success("✅ Saved!")

    with t2:
        b = cfg["brand"]
        b["name"]          = st.text_input("Brand Name",        value=b["name"])
        b["tagline"]       = st.text_input("Tagline",            value=b["tagline"])
        b["logo_emoji"]    = st.text_input("Logo Emoji",         value=b.get("logo_emoji","🍵"))
        b["primary_color"] = st.color_picker("Primary Color",   value=b["primary_color"])
        b["accent_color"]  = st.color_picker("Accent Color",    value=b["accent_color"])
        cfg["admin_password"] = st.text_input(
            "Admin Password", value=cfg.get("admin_password", "Zee2025"), type="password"
        )
        cfg["brand"] = b
        if st.button("💾 Save Branding", type="primary"):
            save_config(cfg); st.success("✅ Saved!")

    with t3:
        c = cfg["completion"]
        textarea_fields = {"subheadline", "result_intro", "offer_body"}
        for field, label in [
            ("headline","Headline"), ("subheadline","Subheadline"), ("result_intro","Result Intro"),
            ("offer_badge","Offer Badge"), ("offer_headline","Offer Headline"), ("offer_body","Offer Body"),
            ("offer_price","Price"), ("offer_price_label","Price Label"),
            ("cta_label","CTA Button Text"), ("cta_url","CTA URL"), ("disclaimer","Disclaimer"),
        ]:
            if field in textarea_fields:
                c[field] = st.text_area(label, value=c[field], height=70)
            else:
                c[field] = st.text_input(label, value=c[field])
        cfg["completion"] = c
        if st.button("💾 Save Completion Settings", type="primary"):
            save_config(cfg); st.success("✅ Saved!")

    with t4:
        df = load_responses()
        if df.empty:
            st.info("No responses yet. Share the survey link to start collecting!")
        else:
            st.metric("Total Responses", len(df))
            st.dataframe(df, use_container_width=True)
            for q in cfg["questions"]:
                if q["id"] in df.columns and q["type"] == "single_choice":
                    counts = df[q["id"]].value_counts().reset_index()
                    counts.columns = ["Answer", "Count"]
                    fig = px.bar(
                        counts, x="Answer", y="Count", title=q["text"][:65],
                        color_discrete_sequence=[cfg["brand"]["primary_color"]],
                    )
                    fig.update_layout(
                        plot_bgcolor="white", paper_bgcolor="white",
                        font_family="Inter", showlegend=False,
                        margin=dict(t=48, b=20, l=20, r=20),
                    )
                    st.plotly_chart(fig, use_container_width=True)
            st.download_button(
                "⬇ Download CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="responses.csv",
                mime="text/csv",
            )

# ── Admin sidebar auth ─────────────────────────────────────────────────────────
def admin_sidebar(cfg):
    with st.sidebar:
        st.markdown("### 🔐 Admin Access")
        pwd = st.text_input("Password", type="password", key="admin_pwd")
        if st.button("Enter Admin", key="admin_enter"):
            if pwd == cfg.get("admin_password", "rachel2024"):
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("Incorrect password.")
        if st.session_state.get("admin_auth"):
            if st.button("🚪 Exit Admin", key="admin_exit"):
                st.session_state.admin_auth = False
                st.rerun()

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    cfg = load_config()
    inject_css(cfg["brand"]["primary_color"])
    admin_sidebar(cfg)
    if st.session_state.get("admin_auth"):
        show_admin(cfg)
    else:
        show_survey(cfg)

if __name__ == "__main__":
    main()
