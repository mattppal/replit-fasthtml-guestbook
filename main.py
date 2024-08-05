from fasthtml.common import (
    Div,
    P,
    Span,
    Small,
    fast_app,
    Link,
    Script,
    Meta,
    serve,
    Label,
    Input,
    Form,
    Button,
    Title,
    H1,
    H2,
    Main,
)
from datetime import datetime
from replit import db
import json
import pytz
from typing import List, Dict, Any

# Constants for input character limits and timestamp format
MAX_NAME_CHAR: int = 15
MAX_MESSAGE_CHAR: int = 50
TIMESTAMP_FMT: str = "%Y-%m-%d %I:%M:%S %p PST"


def get_pst_time() -> datetime:
    """
    Get the current time in Pacific Standard Time (PST).

    Returns:
        datetime: Current time in PST.
    """
    utc_now = datetime.now(pytz.utc)
    pst_tz = pytz.timezone("US/Pacific")
    return utc_now.astimezone(pst_tz)


def get_all_messages() -> List[Dict[str, Any]]:
    """
    Retrieve all messages from the database and sort them by timestamp.

    Returns:
        List[Dict[str, Any]]: A list of message dictionaries sorted by
        timestamp in descending order.
    """
    messages = []
    for key in db.keys():
        if key.startswith("message_"):
            messages.append(json.loads(db[key]))
    return sorted(
        messages,
        key=lambda x: datetime.strptime(x["timestamp"], TIMESTAMP_FMT),
        reverse=True,
    )


def add_message(name: str, message: str) -> None:
    """
    Add a new message to the database.

    Args:
        name (str): The name of the message author.
        message (str): The content of the message.
    """
    timestamp = get_pst_time().strftime(TIMESTAMP_FMT)
    new_id = str(len(db.keys()) + 1)
    new_message = {
        "id": new_id,
        "name": name,
        "message": message,
        "timestamp": timestamp,
    }
    db[f"message_{new_id}"] = json.dumps(new_message)


def create_message_list(messages: List[Dict[str, Any]]) -> Div:
    """
    Create an HTML representation of the message list.

    Args:
        messages (List[Dict[str, Any]]): A list of message dictionaries.

    Returns:
        Div: An HTML Div element containing the formatted message list.
    """
    if not messages:
        return Div(
            P("No messages yet. Be the first to say hi!"),
            id="message-list",
            cls="empty-state",
        )
    return Div(
        *[
            Div(
                Div(
                    Div(
                        Span(f"{msg['name']}: ", cls="message-name"),
                        Span(msg["message"], cls="message-text"),
                    ),
                    Small(msg["timestamp"], cls="message-timestamp"),
                    cls="message-content",
                ),
                cls="message",
            )
            for msg in messages
        ],
        id="message-list",
        cls="message-list",
    )


def create_guest_counter(count: int) -> Div:
    """
    Create an HTML representation of the guest counter.

    Args:
        count (int): The number of guests who have left messages.

    Returns:
        Div: An HTML Div element containing the formatted guest counter.
    """
    return Div(
        f"{count} guests have said hi so far ",
        Span("👋", cls="emoji"),
        id="guest-counter",
        cls="guest-counter",
    )


app, rt = fast_app(
    default_hdrs=False,
    hdrs=(
        Link(
            rel="stylesheet",
            href="https://unpkg.com/sakura.css/css/sakura-vader.css",
            type="text/css",
        ),
        Link(rel="stylesheet", href="/style.css", type="text/css"),
        Link(rel="icon", type="assets/x-icon", href="/assets/favicon.png"),
        Script(src="https://unpkg.com/htmx.org@1.9.10"),
        Script(
            """
            function updateCharCount(inputId, countId, maxLength) {
                const input = document.getElementById(inputId);
                const count = document.getElementById(countId);
                const remainingChars = maxLength - input.value.length;
                count.textContent = remainingChars + '/' + maxLength;
            }
        """
        ),
        Meta(name="viewport", content="width=device-width, initial-scale=1"),
        Meta(name="og:image", content="/assets/matts-guestbook.jpg"),
    ),
)


@rt("/", methods=["GET"])
def get() -> tuple:
    """
    Handle GET requests for the main page.

    Returns:
        tuple: A tuple containing the HTML elements for the main page.
    """
    all_messages = get_all_messages()
    guest_counter = create_guest_counter(len(all_messages))
    message_list = create_message_list(all_messages)
    form = Form(
        Div(
            Div(
                Label("Name:", fr="name"),
                Div(
                    Input(
                        type="text",
                        id="name",
                        name="name",
                        required=True,
                        placeholder="Enter your name",
                        maxlength=str(MAX_NAME_CHAR),
                        oninput=(
                            f"updateCharCount('message', 'messageCount', "
                            f"{MAX_NAME_CHAR})"
                        ),
                    ),
                    Span(id="nameCount", cls="char-count"),
                    cls="input-with-counter",
                ),
                cls="input-wrapper",
            ),
            Div(
                Label("Message:", fr="message"),
                Div(
                    Input(
                        type="text",
                        id="message",
                        name="message",
                        required=True,
                        placeholder="Enter your message",
                        maxlength=str(MAX_MESSAGE_CHAR),
                        oninput=(
                            f"updateCharCount('message', 'messageCount', "
                            f"{MAX_MESSAGE_CHAR})"
                        ),
                    ),
                    Span(id="messageCount", cls="char-count"),
                    cls="input-with-counter",
                ),
                cls="input-wrapper",
            ),
            cls="input-group",
        ),
        Button("Submit", type="submit"),
        id="message-form",
        hx_post="/submit-message",
        hx_target="#update-area",
        hx_swap="innerHTML",
    )
    footer = Div(
        "made with ❤️ by ",
        A("matt", href="https://x.com/mattppal", target="_blank"),
        cls="footer",
    )
    return (
        Title("matt's guestbook"),
        Main(
            H1("✍️ matt's guestbook"),
            form,
            H2("🪵 log"),
            Div(
                guest_counter,
                message_list,
                id="update-area",
                hx_get="/update-messages",
                hx_trigger="every 10s",
            ),
            footer,
        ),
    )


@rt("/submit-message", methods=["POST"])
def post(name: str, message: str) -> Div:
    """
    Handle POST requests for submitting a new message.

    Args:
        name (str): The name of the message author.
        message (str): The content of the message.
    Returns:
        Div: An HTML Div element containing the updated guest counter and
             message list.
    """
    add_message(name, message)
    all_messages = get_all_messages()
    guest_counter = create_guest_counter(len(all_messages))
    message_list = create_message_list(all_messages)
    return Div(
        guest_counter,
        message_list,
        id="update-area",
        hx_get="/update-messages",
        hx_trigger="every 10s",
    )


@rt("/update-messages", methods=["GET"])
def get_update_messages() -> Div:
    """
    Handle GET requests for updating the message list.
    Returns:
        Div: An HTML Div element containing the updated guest counter and
             message list.
    """
    all_messages = get_all_messages()
    guest_counter = create_guest_counter(len(all_messages))
    message_list = create_message_list(all_messages)
    return Div(
        guest_counter,
        message_list,
        id="update-area",
        hx_get="/update-messages",
        hx_trigger="every 10s",
    )


serve()
