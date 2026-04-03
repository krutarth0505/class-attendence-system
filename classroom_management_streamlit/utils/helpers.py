import streamlit as st


def inject_base_styles() -> None:
	"""Small visual polish and full sidebar removal for focused dashboards."""
	st.markdown(
		"""
		<style>
			section[data-testid="stSidebar"] {
				display: none;
			}
			[data-testid="stSidebarCollapsedControl"] {
				display: none;
			}
			.block-container {
				padding-top: 2.25rem;
				padding-bottom: 2rem;
			}
			div.stButton > button {
				min-height: 2.5rem;
				line-height: 1.2;
				display: inline-flex;
				align-items: center;
				justify-content: center;
				white-space: nowrap;
			}
			.status-low {
				color: #b91c1c;
				font-weight: 600;
			}
			.status-average {
				color: #92400e;
				font-weight: 600;
			}
			.status-good {
				color: #1d4ed8;
				font-weight: 600;
			}
			.status-excellent {
				color: #166534;
				font-weight: 600;
			}
		</style>
		""",
		unsafe_allow_html=True,
	)


def status_label(percent: float, student_view: bool = False) -> str:
	if percent < 75:
		return "Low Attendance"
	if percent < 90:
		return "Good Attendance" if student_view else "Average"
	return "Excellent"


def status_tag(text: str) -> str:
	if "Low" in text:
		return f"<span class='status-low'>{text}</span>"
	if "Average" in text:
		return f"<span class='status-average'>{text}</span>"
	if "Good" in text:
		return f"<span class='status-good'>{text}</span>"
	return f"<span class='status-excellent'>{text}</span>"


def show_role_sidebar(user: dict) -> None:
	"""Kept for compatibility; sidebar is intentionally hidden."""
	return


def attendance_progress(percent: float) -> None:
	bounded = max(0.0, min(percent, 100.0))
	st.progress(bounded / 100)
	st.caption(f"Attendance Progress: {bounded:.2f}%")
