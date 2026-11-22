import subprocess
from collections import defaultdict
import datetime
import io
import os
import sys
import html
import argparse
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    LongTable, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


# =============================================================
# CONFIGURATION
# =============================================================

COLLEGE_NAME = (
    "Swami Keshvanand Institute of Technology, "
    "Management & Gramothan, Jaipur"
)

DEPARTMENT_NAME = (
    "Department of Computer Science & Engineering (Artificial Intelligence)"
)

# =============================================================
# GIT REPOSITORY INFORMATION
# =============================================================

def get_repo_info():

    repo_name = "Project-Repository"
    branch_name = (
        os.environ.get("GITHUB_HEAD_REF")
        or os.environ.get("GITHUB_REF_NAME")
        or "main"
    )

    try:
        root_path = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            encoding="utf-8"
        ).strip()

        repo_name = os.path.basename(root_path)

    except Exception:
        repo_name = os.path.basename(os.getcwd())

    if not os.environ.get("GITHUB_REF_NAME"):
        try:
            current_branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                encoding="utf-8"
            ).strip()

            if current_branch and current_branch != "HEAD":
                branch_name = current_branch

        except Exception:
            pass

    return repo_name, branch_name


# =============================================================
# FETCH LATEST REPOSITORY HISTORY
# =============================================================

def fetch_git_history():

    print("[INFO] Fetching latest repository history...")

    try:
        subprocess.run(
            ["git", "fetch", "--all", "--prune"],
            check=True,
            capture_output=True,
            text=True
        )

        print("[SUCCESS] Repository history fetched.")

    except subprocess.CalledProcessError as e:
        print("[WARNING] Could not fetch remote history.")
        print(e.stderr)


# =============================================================
# GIT METRICS
# =============================================================

def get_git_metrics(interval="weekly", start_date=None, end_date=None):

    if interval not in ["weekly", "monthly", "final"]:
        raise ValueError(
            "Invalid interval. Use weekly, monthly or final."
        )

    fetch_git_history()

    now = datetime.datetime.now().astimezone()

    if start_date and end_date:

        # Custom range: 00:00:00 of start date to 23:59:59 of end date.
        cutoff = start_date
        now = (
            end_date
            + datetime.timedelta(days=1)
            - datetime.timedelta(seconds=1)
        )

        scope_title = (
            f"Custom Range "
            f"({cutoff.strftime('%Y-%m-%d')} "
            f"to {now.strftime('%Y-%m-%d')})"
        )

    elif interval == "weekly":

        cutoff = now - datetime.timedelta(days=7)

        scope_title = (
            f"Last 7 Days "
            f"({cutoff.strftime('%Y-%m-%d %H:%M')} "
            f"to {now.strftime('%Y-%m-%d %H:%M')})"
        )

    elif interval == "monthly":

        cutoff = now - datetime.timedelta(days=30)

        scope_title = (
            f"Last 30 Days "
            f"({cutoff.strftime('%Y-%m-%d %H:%M')} "
            f"to {now.strftime('%Y-%m-%d %H:%M')})"
        )

    else:

        cutoff = None
        scope_title = "Complete Project Lifecycle (All Commits)"

    # Fetch complete history from all locally available references.
    git_args = [
        "git",
        "log",
        "--all",
        "--no-merges",
        "--date=iso-strict",
        "--format=COMMIT|||%H|||%an|||%cI|||%s",
        "--numstat"
    ]

    try:

        raw_output = subprocess.check_output(
            git_args,
            encoding="utf-8",
            errors="replace"
        )

    except subprocess.CalledProcessError as e:

        print("[ERROR] Git command failed:", e)
        return None, None, None, scope_title

    students = defaultdict(
        lambda: {
            "commits": 0,
            "added": 0,
            "deleted": 0,
            "active_days": set()
        }
    )

    timeline_activity = defaultdict(lambda: defaultdict(int))

    student_logs = defaultdict(list)

    current_author = None

    # ---------------------------------------------------------
    # Parse Git history
    # ---------------------------------------------------------

    for line in raw_output.splitlines():

        line = line.strip()

        if not line:
            continue

        # New commit starts here.
        if line.startswith("COMMIT|||"):

            parts = line.split("|||", 4)

            if len(parts) < 5:
                current_author = None
                continue

            sha = parts[1].strip()
            author = parts[2].strip()
            date_str = parts[3].strip()
            message = parts[4].strip()

            # Ignore bot accounts.
            if (
                "bot" in author.lower()
                or "github-actions" in author.lower()
            ):
                current_author = None
                continue

            try:

                # Use the actual Git committer timestamp.
                commit_datetime = datetime.datetime.fromisoformat(
                    date_str
                )

                # Ensure timezone-aware comparison.
                if commit_datetime.tzinfo is None:
                    commit_datetime = commit_datetime.replace(
                        tzinfo=datetime.timezone.utc
                    )

                # Exact date filtering.
                if cutoff and not (cutoff <= commit_datetime <= now):
                    current_author = None
                    continue

            except ValueError:

                current_author = None
                continue

            current_author = author

            commit_date = commit_datetime.date()

            students[author]["commits"] += 1

            students[author]["active_days"].add(commit_date)

            student_logs[author].append(
                (
                    commit_datetime,
                    sha[:8],
                    message
                )
            )

            # Timeline grouping.
            if interval == "weekly":

                period_key = commit_date.strftime("%Y-%m-%d")

            elif interval == "monthly":

                iso = commit_date.isocalendar()

                period_key = (
                    f"{iso.year}-W{iso.week:02d}"
                )

            else:

                period_key = commit_date.strftime("%Y-%m")

            timeline_activity[period_key][author] += 1

        # -----------------------------------------------------
        # Parse lines added and deleted.
        # -----------------------------------------------------

        elif current_author:

            parts = line.split("\t")

            if len(parts) >= 3:

                added = parts[0]
                deleted = parts[1]

                # Binary files have '-' instead of numbers.
                if added.isdigit() and deleted.isdigit():

                    students[current_author]["added"] += int(added)

                    students[current_author]["deleted"] += int(deleted)

    # Sort individual commit logs chronologically.
    for author in student_logs:
        student_logs[author].sort(
            key=lambda x: x[0],
            reverse=True
        )

    print(
        f"[INFO] Found {len(students)} contributors "
        f"for {interval} report."
    )

    return (
        students,
        timeline_activity,
        student_logs,
        scope_title
    )


# =============================================================
# GENERATE CHARTS
# =============================================================

def create_charts(students, timeline_activity, interval):

    fig, (ax1, ax2) = plt.subplots(
        1, 2,
        figsize=(11, 3.8)
    )

    authors = list(students.keys())

    periods = sorted(timeline_activity.keys())

    # ---------------------------------------------------------
    # 1. Commit Timeline
    # ---------------------------------------------------------

    if periods and authors:

        if interval == "weekly":

            labels = [
                datetime.datetime.strptime(
                    p, "%Y-%m-%d"
                ).strftime("%b %d")
                for p in periods
            ]

        else:

            labels = periods

        for author in authors:

            counts = [
                timeline_activity[p].get(author, 0)
                for p in periods
            ]

            ax1.plot(
                labels,
                counts,
                marker="o",
                linewidth=2,
                label=author
            )

        ax1.set_title(
            f"Commit Timeline ({interval.capitalize()})",
            fontsize=10,
            fontweight="bold"
        )

        ax1.set_ylabel("Commits")

        ax1.tick_params(axis="x", rotation=35)

        ax1.grid(
            True,
            linestyle="--",
            alpha=0.5
        )

        ax1.legend(fontsize=7)

    else:

        ax1.text(
            0.5, 0.5,
            "No commits found",
            ha="center",
            va="center"
        )

    # ---------------------------------------------------------
    # 2. Net Lines of Code
    # ---------------------------------------------------------

    if authors:

        net_loc = [
            students[a]["added"] - students[a]["deleted"]
            for a in authors
        ]

        ax2.bar(
            authors,
            net_loc,
            width=0.45
        )

        ax2.set_title(
            "Net Lines of Code Written",
            fontsize=10,
            fontweight="bold"
        )

        ax2.set_ylabel("LOC (Added - Deleted)")

        ax2.tick_params(axis="x", rotation=35)

        ax2.grid(
            axis="y",
            linestyle="--",
            alpha=0.5
        )

    else:

        ax2.text(
            0.5, 0.5,
            "No LOC changes recorded",
            ha="center",
            va="center"
        )

    plt.tight_layout()

    img_buffer = io.BytesIO()

    plt.savefig(
        img_buffer,
        format="png",
        dpi=200,
        bbox_inches="tight"
    )

    plt.close(fig)

    img_buffer.seek(0)

    return Image(
        img_buffer,
        width=500,
        height=170
    )


# =============================================================
# GENERATE PDF REPORT
# =============================================================

def generate_pdf(interval="weekly", start_date=None, end_date=None):

    repo_name, branch_name = get_repo_info()

    (
        students,
        timeline_activity,
        student_logs,
        scope_title
    ) = get_git_metrics(interval, start_date, end_date)

    if students is None:
        return

    date_stamp = datetime.date.today().strftime("%Y-%m-%d")

    # Add the custom range to the filename so reports don't overwrite
    # each other.
    range_stamp = ""
    if start_date and end_date:
        range_stamp = (
            f"_{start_date:%Y-%m-%d}_to_{end_date:%Y-%m-%d}"
        )

    if interval == "weekly":

        report_title = "Weekly Progress Report (Form-3)"

        doc_name = (
            f"{repo_name}_Weekly_Progress_Report_Form-3{range_stamp}_"
            f"{date_stamp}.pdf"
        )

    elif interval == "monthly":

        report_title = "Monthly Progress Report (Form-3)"

        doc_name = (
            f"{repo_name}_Monthly_Progress_Report_Form-3{range_stamp}_"
            f"{date_stamp}.pdf"
        )

    else:

        report_title = "Final Project Evaluation Report"

        doc_name = (
            f"{repo_name}_Final_Report{range_stamp}_{date_stamp}.pdf"
        )

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
        "CollegeStyle",
        parent=styles["Heading1"],
        fontSize=13.5,
        leading=17,
        textColor=colors.HexColor("#0F172A"),
        alignment=1,
        spaceAfter=2
    )

    dept_style = ParagraphStyle(
        "DeptStyle",
        parent=styles["Normal"],
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=6
    )

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading2"],
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1A365D"),
        alignment=1,
        spaceAfter=5
    )

    repo_style = ParagraphStyle(
        "RepoStyle",
        parent=styles["Normal"],
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=3
    )

    meta_style = ParagraphStyle(
        "MetaStyle",
        parent=styles["Normal"],
        fontSize=8.5,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=8
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading2"],
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=7,
        spaceAfter=4
    )

    # Used inside the per-student header row (name + marks box).
    student_head_style = ParagraphStyle(
        "StudentHeadStyle",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#2563EB")
    )

    marks_head_style = ParagraphStyle(
        "MarksHeadStyle",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0F172A"),
        alignment=2
    )

    msg_style = ParagraphStyle(
        "MsgStyle",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1E293B")
    )

    meta_cell_style = ParagraphStyle(
        "MetaCellStyle",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#475569"),
        alignment=1
    )

    story = []

    # =========================================================
    # 1. HEADER
    # =========================================================

    story.append(
        Paragraph(
            f"<b>{html.escape(COLLEGE_NAME)}</b>",
            college_style
        )
    )

    story.append(
        Paragraph(
            f"<b>{html.escape(DEPARTMENT_NAME)}</b>",
            dept_style
        )
    )

    story.append(
        Paragraph(
            f"<u><b>{report_title}</b></u>",
            title_style
        )
    )

    story.append(Spacer(1, 3))

    # =========================================================
    # 2. METADATA
    # =========================================================

    story.append(
        Paragraph(
            f"<b>Project Repository:</b> "
            f"<font color='#2563EB'><b>{html.escape(repo_name)}</b></font>"
            f" &nbsp;|&nbsp; "
            f"<b>Branch:</b> <code>{html.escape(branch_name)}</code>",
            repo_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Evaluation Window:</b> "
            f"{html.escape(scope_title)}"
            f" &nbsp;|&nbsp; "
            f"<b>Generated On:</b> "
            f"{datetime.datetime.now().astimezone().strftime('%B %d, %Y %I:%M %p %Z')}",
            meta_style
        )
    )

    # =========================================================
    # 3. CONTRIBUTION TABLE (with Mentor Marks beside each student)
    # =========================================================

    story.append(
        Paragraph(
            "1. Individual Contribution Breakdown & Mentor Marks",
            section_style
        )
    )

    total_commits = sum(
        data["commits"]
        for data in students.values()
    )

    table_data = [[
        "Student Name",
        "Commits (%)",
        "Lines Added",
        "Lines Deleted",
        "Net LOC",
        "Active Days",
        "Mentor Marks"
    ]]

    if students:

        # Sort contributors by commit count.
        sorted_students = sorted(
            students.items(),
            key=lambda x: x[1]["commits"],
            reverse=True
        )

        for name, data in sorted_students:

            pct = (
                data["commits"] / total_commits * 100
                if total_commits else 0
            )

            net = data["added"] - data["deleted"]

            table_data.append([
                Paragraph(html.escape(name), msg_style),
                f"{data['commits']} ({pct:.1f}%)",
                f"+{data['added']:,}",
                f"-{data['deleted']:,}",
                f"{net:,}",
                f"{len(data['active_days'])} days",
                "_____ / 10"
            ])

    else:

        table_data.append([
            "No commits found in this period.",
            "-", "-", "-", "-", "-", "_____ / 10"
        ])

    summary_table = Table(
        table_data,
        colWidths=[110, 70, 65, 65, 60, 60, 110],
        repeatRows=1
    )

    summary_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#1E293B")),

            ("TEXTCOLOR", (0, 0), (-1, 0),
             colors.whitesmoke),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("ALIGN", (0, 1), (0, -1), "LEFT"),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("FONTSIZE", (0, 0), (-1, -1), 8),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

            ("TOPPADDING", (0, 0), (-1, -1), 8),

            # Highlight the marks column so the mentor can fill it in.
            ("BACKGROUND", (6, 1), (6, -1),
             colors.HexColor("#FFF2C6")),

            ("GRID", (0, 0), (-1, -1),
             0.5, colors.HexColor("#CBD5E1")),

            ("ROWBACKGROUNDS", (0, 1), (5, -1),
             [colors.white, colors.HexColor("#F8FAFC")])
        ])
    )

    story.append(summary_table)

    story.append(Spacer(1, 6))

    # =========================================================
    # 4. CHARTS
    # =========================================================

    story.append(
        Paragraph(
            "2. Visual Trends & Volume",
            section_style
        )
    )

    chart_image = create_charts(
        students,
        timeline_activity,
        interval
    )

    story.append(chart_image)

    story.append(Spacer(1, 6))

    # =========================================================
    # 5. DETAILED COMMIT LOGS (marks box beside each student)
    # =========================================================

    story.append(
        Paragraph(
            f"3. Detailed Commit Logs ({interval.capitalize()})",
            section_style
        )
    )

    if not student_logs:

        story.append(
            Paragraph(
                "<i>No commit logs found for this timeframe.</i>",
                styles["Normal"]
            )
        )

    else:

        for student_name, logs in student_logs.items():

            # One header row per student: name on the left,
            # blank mentor marks field on the right.
            student_header = Table(
                [[
                    Paragraph(
                        f"<b>Student:</b> "
                        f"{html.escape(student_name)}"
                        f" — <i>{len(logs)} commit(s)</i>",
                        student_head_style
                    ),
                    Paragraph(
                        "<b>Mentor Marks:</b> _____ / 10",
                        marks_head_style
                    )
                ]],
                colWidths=[360, 180]
            )

            student_header.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (0, 0),
                     colors.HexColor("#EFF6FF")),

                    ("BACKGROUND", (1, 0), (1, 0),
                     colors.HexColor("#FFF2C6")),

                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

                    ("TOPPADDING", (0, 0), (-1, -1), 5),

                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),

                    ("LEFTPADDING", (0, 0), (-1, -1), 6),

                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),

                    ("BOX", (0, 0), (-1, -1),
                     0.5, colors.HexColor("#CBD5E1")),

                    ("LINEAFTER", (0, 0), (0, 0),
                     0.5, colors.HexColor("#CBD5E1"))
                ])
            )

            story.append(Spacer(1, 4))

            story.append(student_header)

            log_table_data = [[
                "Date",
                "Hash",
                "Commit Message"
            ]]

            for commit_datetime, sha_val, msg_val in logs:

                # Display the actual Git commit date.
                date_val = commit_datetime.strftime(
                    "%d %b %Y"
                )

                safe_msg = (
                    html.escape(msg_val)
                    if msg_val else "(No commit message)"
                )

                log_table_data.append([

                    Paragraph(
                        date_val,
                        meta_cell_style
                    ),

                    Paragraph(
                        f"<code>{html.escape(sha_val)}</code>",
                        meta_cell_style
                    ),

                    Paragraph(
                        safe_msg,
                        msg_style
                    )
                ])

            log_table = LongTable(
                log_table_data,
                colWidths=[70, 60, 410],
                repeatRows=1
            )

            log_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0),
                     colors.HexColor("#475569")),

                    ("TEXTCOLOR", (0, 0), (-1, 0),
                     colors.whitesmoke),

                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),

                    ("FONTNAME", (0, 0), (-1, 0),
                     "Helvetica-Bold"),

                    ("FONTSIZE", (0, 0), (-1, -1), 7.5),

                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),

                    ("TOPPADDING", (0, 0), (-1, -1), 3),

                    ("GRID", (0, 0), (-1, -1),
                     0.5, colors.HexColor("#CBD5E1")),

                    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                     [colors.white, colors.HexColor("#F8FAFC")])
                ])
            )

            story.append(log_table)

            story.append(Spacer(1, 5))

    # =========================================================
    # 6. BUILD PDF
    # =========================================================

    doc.build(story)

    print("\n========================================")
    print("[SUCCESS] PDF REPORT GENERATED")
    print("========================================")

    print(f"File: {doc_name}")
    print(f"Repository: {repo_name}")
    print(f"Branch: {branch_name}")
    print(f"Contributors: {len(students)}")
    print(f"Total commits: {total_commits}")
    print(f"Interval: {interval}")
    print(f"Window: {scope_title}")
    print("========================================")


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Generate a Git-based progress report PDF."
    )

    parser.add_argument(
        "interval",
        nargs="?",
        default="weekly",
        choices=["weekly", "monthly", "final"],
        help="Report type (default: weekly)"
    )

    parser.add_argument(
        "--from",
        dest="start",
        help="Start date, YYYY-MM-DD (use together with --to)"
    )

    parser.add_argument(
        "--to",
        dest="end",
        help="End date, YYYY-MM-DD (use together with --from)"
    )

    args = parser.parse_args()

    start = end = None

    if args.start or args.end:

        if not (args.start and args.end):
            parser.error("--from and --to must be used together")

        try:
            # .astimezone() on a naive datetime treats it as local time.
            start = datetime.datetime.strptime(
                args.start, "%Y-%m-%d"
            ).astimezone()

            end = datetime.datetime.strptime(
                args.end, "%Y-%m-%d"
            ).astimezone()

        except ValueError:
            parser.error("Dates must be in YYYY-MM-DD format")

        if start > end:
            parser.error("--from must not be after --to")

    generate_pdf(args.interval.lower(), start, end)