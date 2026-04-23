# app/utils/status_bar.py
def handle_error_success(
    status_bar,
    color_theme,
    reset_timer,
    is_success: bool = None,
    msg: str = None
):
    if is_success == False:
        status_bar.setStyleSheet(
            f"""
                QStatusBar {{
                    border: 2px solid green;
                    background-color: {color_theme['success']};
                    color: black;
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                    font-style: italic;
                    font-size: 12px;
                }}
            """
        )
    elif is_success:
        status_bar.setStyleSheet(
            f"""
                QStatusBar {{
                    border: 2px solid red;
                    background-color: {color_theme['error']};
                    color: black;
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                    font-style: italic;
                    font-size: 12px;
                }}
            """
        )
    elif is_success is None:
        status_bar.setStyleSheet(
            f"""
                QStatusBar {{
                    border: 2px solid orange;
                    background-color: {color_theme['warning']};
                    color: black;
                    letter-spacing: 0.1em;
                    word-spacing: 0.1em;
                    font-style: italic;
                    font-size: 12px;
                }}
            """
        )
    status_bar.showMessage(msg)
    reset_timer.start()