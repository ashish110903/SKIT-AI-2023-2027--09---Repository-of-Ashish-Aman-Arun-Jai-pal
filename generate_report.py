import subprocess
from collections import defaultdict
import datetime
import io
import os
import sys
import html
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# -------------------------------------------------------------
# CONFIGURATION: Institution & Department Details
# -------------------------------------------------------------
COLLEGE_NAME = "Swami Keshvanand Institute of Technology, Management & Gramothan, Jaipur"
DEPARTMENT_NAME = "Department of Computer Science & Engineering (Artificial Intelligence)"
# -------------------------------------------------------------

# Defined Project Sprint Weeks (Sep 11, 2026 to Nov 20, 2026)
PROJECT_WEEKS = {
    1:  ("2026-09-11", "2026-09-17", "Sprint 1: Requirement & Research"),
    2:  ("2026-09-18", "2026-09-24", "Sprint 1: Architecture & Sensor Specifications"),
    3:  ("2026-09-25", "2026-10-01", "Sprint 2: Backend Structure, Dashboard UI, Data Analysis"),
    4:  ("2026-10-02", "2026-10-08", "Sprint 2-3: Telemetry Ingestion, Live Charts, Feature Extraction"),
    5:  ("2026-10-09", "2026-10-15", "Sprint 3: Database Models, Rainfall Gauge, Data Preprocessing"),
    6:  ("2026-10-16", "2026-10-22", "Sprint 3: Station Registration, Map Visualization, Baseline ML"),
    7:  ("2026-10-23", "2026-10-29", "Sprint 3-4: Historical APIs, Backend Integration, Classifiers"),
    8:  ("2026-10-30", "2026-11-05", "Sprint 4: Alert Dispatcher, Risk Visualizer, Anomaly Detection"),
    9:  ("2026-11-06", "2026-11-12", "Sprint 4-5: Pipeline Coordinator, Alarm UI, Predictor Integration"),
    10: ("2026-11-13", "2026-11-20", "Sprint 5: System Verification, Offline Mode, Production Serving"),
}

def get_repo_info():
    """Extracts the repository name and current branch."""
    repo_name = "CloudBurst-Early-Warning"
    branch_name = os.environ.get("GITHUB_REF_NAME") or os.environ.get("GITHUB_HEAD_REF") or "main"

    try:
        root_path = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], encoding='utf-8').strip()
        repo_name = os.path.basename(root_path)
    except Exception:
        try:
            remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], encoding='utf-8').strip()
            repo_name = remote_url.rstrip('/').split('/')[-1].replace('.git', '')
        except Exception:
            repo_name = os.path.basename(os.getcwd())

    if not os.environ.get("GITHUB_REF_NAME"):
        try:
            current_b = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], encoding='utf-8').strip()
            if current_b and current_b != "HEAD":
                branch_name = current_b
        except Exception:
            pass

    return repo_name, branch_name

def normalize_author(name: str) -> str:
    """
    Normalize git author names to consistent student display names.
    """
    name_lower = name.lower().strip()
    if any(x in name_lower for x in ["ashish", "ashish110903", "ashish sharma"]):
        return "Ashish Sharma"
    if any(x in name_lower for x in ["aman", "aman sharma"]):
        return "Aman Sharma"
    if any(x in name_lower for x in ["arun", "arun sharma"]):
        return "Arun Sharma"
    if any(x in name_lower for x in ["jai", "jaipal", "jai pal", "jaypal"]):
        return "Jai Pal"
    return name

def get_git_metrics(start_date=None, end_date=None, interval_label="weekly", week_num=None):
    """
    Parses Git commit logs across all branches and aggregates metrics for a specific window.
    """
    today = datetime.date.today()
    git_args = ['git', 'log', '--all', '--no-merges', '--pretty=format:COMMIT|||%h|||%an|||%ad|||%s', '--date=short', '--numstat']

    if start_date and end_date:
        if week_num:
            scope_title = f"Week {week_num:02d}: {start_date} to {end_date} ({PROJECT_WEEKS[week_num][2]})"
        else:
            scope_title = f"{start_date} to {end_date}"
    elif interval_label == "monthly":
        since_date = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        scope_title = f"Last 30 Days (Since {since_date})"
    else:
        scope_title = "Complete Project Lifecycle (Sep 11, 2026 to Nov 20, 2026)"

    try:
        raw_output = subprocess.check_output(git_args, encoding='utf-8', errors='replace')
    except subprocess.CalledProcessError:
        print("[ERROR] Git command failed. Please ensure you are inside a Git repository.")
        return None, None, None, scope_title

    if not raw_output.strip():
        return None, None, None, scope_title

    students = defaultdict(lambda: {"commits": 0, "added": 0, "deleted": 0, "active_days": set()})
    timeline_activity = defaultdict(lambda: defaultdict(int))
    student_logs = defaultdict(list)

    current_author = None
    current_date_str = None
    seen_shas = set()

    for line in raw_output.strip().split('\n'):
        line = line.strip()
        if not line:
            continue

        if line.startswith('COMMIT|||'):
            parts = line.split('|||')
            if len(parts) >= 5:
                sha       = parts[1].strip()
                author    = parts[2].strip()
                date_str  = parts[3].strip()
                msg       = parts[4].strip()
            else:
                continue

            # Exclude bot / CI commits
            if "bot" in author.lower() or "github-actions" in author.lower():
                current_author = None
                continue

            # Deduplicate commits that appear on multiple branches
            if sha in seen_shas:
                current_author = None
                continue
            seen_shas.add(sha)

            # Skip commits with future dates beyond project scope (e.g., placeholder 2027 commits)
            if date_str > "2026-11-22":
                current_author = None
                continue

            # Date range filter
            if start_date and end_date:
                if not (start_date <= date_str <= end_date):
                    current_author = None
                    continue

            # Normalize author name
            author = normalize_author(author)

            current_author = author
            current_date_str = date_str

            students[current_author]["commits"] += 1
            students[current_author]["active_days"].add(current_date_str)
            student_logs[current_author].append((date_str, sha, msg))

            try:
                dt = datetime.datetime.strptime(current_date_str, "%Y-%m-%d").date()
                if start_date and end_date:
                    period_key = dt.strftime("%b %d (%a)")
                elif interval_label == "monthly":
                    period_key = f"{dt.isocalendar()[0]}-W{dt.isocalendar()[1]:02d}"
                else:
                    period_key = dt.strftime("%b %d")
                timeline_activity[period_key][current_author] += 1
            except Exception:
                pass

        elif current_author and not line.startswith('COMMIT|||'):
            parts = line.split()
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                students[current_author]["added"] += int(parts[0])
                students[current_author]["deleted"] += int(parts[1])

    return students, timeline_activity, student_logs, scope_title

def create_charts(students, timeline_activity, title_suffix):
    """Generates workload distribution and timeline comparison charts."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.8))
    authors = list(students.keys())

    # Sort periods chronologically
    periods = sorted(list(timeline_activity.keys()))

    # 1. Timeline Chart
    if periods and authors:
        colors_map = {
            'Ashish Sharma': '#1E40AF',
            'Jai Pal': '#0284C7',
            'Aman Sharma': '#059669',
            'Arun Sharma': '#D97706'
        }
        for author in authors:
            counts = [timeline_activity[p].get(author, 0) for p in periods]
            c = colors_map.get(author, None)
            ax1.plot(periods, counts, marker='o', linewidth=2, label=author, color=c)
        ax1.set_title(f"Commit Timeline ({title_suffix})", fontsize=10, fontweight='bold')
        ax1.set_ylabel("Commits")
        ax1.tick_params(axis='x', rotation=30)
        ax1.grid(True, linestyle='--', alpha=0.5)
        ax1.legend(fontsize=8)
    else:
        ax1.text(0.5, 0.5, "No commits found in this period", ha='center', va='center')

    # 2. Net LOC Chart
    if authors:
        net_loc = [students[a]["added"] - students[a]["deleted"] for a in authors]
        colors_list = ['#1E40AF', '#0284C7', '#059669', '#D97706']
        ax2.bar(authors, net_loc, color=colors_list[:len(authors)], width=0.45)
        ax2.set_title("Net Lines of Code Written", fontsize=10, fontweight='bold')
        ax2.set_ylabel("LOC (Added - Deleted)")
        ax2.grid(axis='y', linestyle='--', alpha=0.5)
    else:
        ax2.text(0.5, 0.5, "No LOC recorded", ha='center', va='center')

    plt.tight_layout()
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=200)
    plt.close()
    img_buffer.seek(0)
    return Image(img_buffer, width=500, height=170)

def generate_pdf(interval="weekly", start_date=None, end_date=None, week_num=None, output_filename=None):
    repo_name, branch_name = get_repo_info()
    students, timeline_activity, student_logs, scope_title = get_git_metrics(
        start_date=start_date, end_date=end_date, interval_label=interval, week_num=week_num
    )

    if students is None:
        print("[ERROR] No students or metrics found.")
        return

    if week_num:
        report_title = f"Weekly Progress Report - Week {week_num:02d} (Form-3)"
        default_doc = f"{repo_name}_Weekly_Progress_Report_Form-3_Week_{week_num:02d}_{start_date}_to_{end_date}.pdf"
    elif start_date and end_date:
        report_title = f"Custom Progress Report (Form-3)"
        default_doc = f"{repo_name}_Progress_Report_{start_date}_to_{end_date}.pdf"
    elif interval == "final":
        report_title = "Final Project Evaluation Report"
        default_doc = f"{repo_name}_Final_Report_{datetime.date.today().strftime('%Y-%m-%d')}.pdf"
    else:
        report_title = "Weekly Progress Report (Form-3)"
        default_doc = f"{repo_name}_Weekly_Progress_Report_Form-3_{datetime.date.today().strftime('%Y-%m-%d')}.pdf"

    doc_name = output_filename or default_doc

    doc = SimpleDocTemplate(
        doc_name,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    college_style = ParagraphStyle(
        'CollegeStyle', parent=styles['Heading1'],
        fontSize=13.5, leading=17, textColor=colors.HexColor("#0F172A"), alignment=1, spaceAfter=2
    )
    dept_style = ParagraphStyle(
        'DeptStyle', parent=styles['Normal'],
        fontSize=9.5, leading=13, textColor=colors.HexColor("#475569"), alignment=1, spaceAfter=6
    )
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading2'],
        fontSize=13, leading=17, textColor=colors.HexColor("#1A365D"), alignment=1, spaceAfter=5
    )
    repo_style = ParagraphStyle(
        'RepoStyle', parent=styles['Normal'],
        fontSize=9.5, leading=14, textColor=colors.HexColor("#0F172A"), spaceAfter=3
    )
    meta_style = ParagraphStyle(
        'MetaStyle', parent=styles['Normal'],
        fontSize=8.5, textColor=colors.HexColor("#64748B"), spaceAfter=8
    )
    section_style = ParagraphStyle(
        'SectionStyle', parent=styles['Heading2'],
        fontSize=10.5, leading=14, textColor=colors.HexColor("#0F172A"), spaceBefore=7, spaceAfter=4
    )
    sub_section_style = ParagraphStyle(
        'SubSectionStyle', parent=styles['Heading3'],
        fontSize=9, leading=12, textColor=colors.HexColor("#2563EB"), spaceBefore=5, spaceAfter=2
    )
    msg_style = ParagraphStyle(
        'MsgStyle', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=colors.HexColor("#1E293B")
    )
    meta_cell_style = ParagraphStyle(
        'MetaCellStyle', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=colors.HexColor("#475569"), alignment=1
    )

    story = []

    # 1. Header
    story.append(Paragraph(f"<b>{html.escape(COLLEGE_NAME)}</b>", college_style))
    story.append(Paragraph(f"<b>{html.escape(DEPARTMENT_NAME)}</b>", dept_style))
    story.append(Paragraph(f"<u><b>{report_title}</b></u>", title_style))
    story.append(Spacer(1, 3))

    # 2. Metadata
    story.append(Paragraph(f"<b>Project Repository:</b> <font color='#2563EB'><b>{html.escape(repo_name)}</b></font> &nbsp;|&nbsp; <b>Branch:</b> <code>{html.escape(branch_name)}</code>", repo_style))
    story.append(Paragraph(f"<b>Evaluation Window:</b> {scope_title} &nbsp;|&nbsp; <b>Generated On:</b> {datetime.date.today().strftime('%B %d, %Y')}", meta_style))

    # 3. Individual Summary Table
    story.append(Paragraph("1. Individual Contribution Breakdown", section_style))
    total_commits = sum(data["commits"] for data in students.values())
    table_data = [["Student Name", "Commits (%)", "Lines Added", "Lines Deleted", "Net LOC", "Active Days"]]

    if students:
        for name in sorted(students.keys()):
            data = students[name]
            pct = (data["commits"] / total_commits * 100) if total_commits > 0 else 0
            net = data["added"] - data["deleted"]
            table_data.append([
                html.escape(name),
                f"{data['commits']} ({pct:.1f}%)",
                f"+{data['added']:,}",
                f"-{data['deleted']:,}",
                f"{net:,}",
                f"{len(data['active_days'])} days"
            ])
    else:
        table_data.append(["No commits found in this period.", "-", "-", "-", "-", "-"])

    table = Table(table_data, colWidths=[120, 80, 80, 80, 80, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(table)
    story.append(Spacer(1, 6))

    # 4. Visual Charts
    chart_suffix = f"Week {week_num}" if week_num else interval.capitalize()
    story.append(Paragraph("2. Visual Trends & Volume", section_style))
    chart_image = create_charts(students, timeline_activity, chart_suffix)
    story.append(chart_image)
    story.append(Spacer(1, 6))

    # 5. Detailed Commit Logs per Student
    story.append(Paragraph(f"3. Detailed Commit Logs ({chart_suffix})", section_style))
    if not student_logs:
        story.append(Paragraph("<i>No commit logs found for this timeframe.</i>", styles['Normal']))
    else:
        for student_name in sorted(student_logs.keys()):
            logs = student_logs[student_name]
            student_section = []
            student_section.append(Paragraph(f"<b>Student:</b> {html.escape(student_name)} — <i>{len(logs)} commit(s)</i>", sub_section_style))

            log_table_data = [["Date", "Hash", "Commit Message"]]
            # Sort logs chronologically by date
            sorted_logs = sorted(logs, key=lambda x: x[0])
            for date_val, sha_val, msg_val in sorted_logs:
                safe_msg = html.escape(msg_val) if msg_val else "(No commit message)"
                log_table_data.append([
                    Paragraph(date_val, meta_cell_style),
                    Paragraph(f"<code>{sha_val}</code>", meta_cell_style),
                    Paragraph(safe_msg, msg_style)
                ])

            log_table = Table(log_table_data, colWidths=[70, 60, 410])
            t_style = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#475569")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 7.5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
                ('TOPPADDING', (0, 0), (-1, -1), 2.5),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ]

            log_table.setStyle(TableStyle(t_style))
            student_section.append(log_table)
            student_section.append(Spacer(1, 5))
            story.append(KeepTogether(student_section))

    doc.build(story)
    print(f"[SUCCESS] Generated: {doc_name} -> {len(students)} student(s), {total_commits} commits.")

def generate_all_weeks():
    """Generates PDF reports for all 10 sprint weeks into weekly_reports/ folder."""
    os.makedirs("weekly_reports", exist_ok=True)
    repo_name, _ = get_repo_info()
    print("\n=======================================================")
    print("Generating Form-3 Weekly Progress Reports for All Weeks")
    print("=======================================================\n")
    for w_num in sorted(PROJECT_WEEKS.keys()):
        s_date, e_date, _ = PROJECT_WEEKS[w_num]
        out_file = os.path.join("weekly_reports", f"{repo_name}_Weekly_Report_Week_{w_num:02d}_{s_date}_to_{e_date}.pdf")
        generate_pdf(interval="weekly", start_date=s_date, end_date=e_date, week_num=w_num, output_filename=out_file)
    print("\n[COMPLETE] All 10 weekly reports generated in 'weekly_reports/' directory.")

if __name__ == "__main__":
    arg = sys.argv[1].lower() if len(sys.argv) > 1 else "weekly"

    if arg in ("all", "all_weeks", "--all"):
        generate_all_weeks()
    elif arg.startswith("week") or arg.startswith("w"):
        num_str = arg.replace("week", "").replace("w", "")
        if num_str.isdigit() and int(num_str) in PROJECT_WEEKS:
            w = int(num_str)
            s_date, e_date, _ = PROJECT_WEEKS[w]
            generate_pdf(interval="weekly", start_date=s_date, end_date=e_date, week_num=w)
        else:
            print(f"Unknown week: {arg}. Please use week1 .. week10")
    elif len(sys.argv) >= 3:
        # Custom date range: python generate_report.py 2026-09-11 2026-09-17
        generate_pdf(interval="custom", start_date=sys.argv[1], end_date=sys.argv[2])
    elif arg == "final":
        generate_pdf(interval="final", start_date="2026-09-11", end_date="2026-11-20")
    else:
        # Default: Week 10 (latest project week)
        s_date, e_date, _ = PROJECT_WEEKS[10]
        generate_pdf(interval="weekly", start_date=s_date, end_date=e_date, week_num=10)
