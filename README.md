# Matt's Guestbook

A simple, real-time guestbook application built and deployed with:

- [FastHTML](https://fastht.ml): A Python framework for building HTML applications
- [HTMX](https://htmx.org): For seamless AJAX requests and updates
- [Replit](https://replit.com): Online IDE and hosting platform
  - [Replit Database](https://docs.replit.com/cloud-services/storage-and-databases/replit-database#what-is-replit-database): Key-value store for message persistence

Say hi: [https://guestbook.mattpalmer.io](https://guestbook.mattpalmer.io)

## Setup

1. Fork the [Replit project](https://replit.com/@matt/FastHTML-guestbook?v=1#main.py)
2. Click "Run."

That's it!

## Configuration

1. Update the `MAX_NAME_CHAR` and `MAX_MESSAGE_CHAR` constants in `main.py` if you want to change input limits
2. Modify the `TIMESTAMP_FMT` constant to change the timestamp format
3. Adjust the styling in `style.css` to customize the appearance
4. The Replit database is used for storing messages (`from replit import db`). 
   1. You can easily swap this with Postgres / SQLite if you'd prefer an alternative.


## Running the Application

1. Open the Replit project
2. Click the "Run" button at the top of the Replit interface
3. The application will start, and you can access it via the provided URL

## Code Structure

- `get_pst_time()`: Retrieves the current time in PST
- `get_all_messages()`: Fetches and sorts all messages from the database
- `add_message()`: Adds a new message to the database
- `create_message_list()`: Generates the HTML for the message list
- `create_guest_counter()`: Creates the guest counter HTML
- Main route handlers:
  - `get()`: Renders the main page
  - `post()`: Handles message submission
  - `get_update_messages()`: Updates the message list

## Contributing

1. Fork the project
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is open-source and available under the MIT License.

## Setup Instructions

1. Create a new Replit project
2. Choose Python as the language
3. Copy the contents of `main.py` into your Replit's `main.py` file
4. Create a new file called `style.css` and copy the CSS content into it
5. Update the `pyproject.toml` file with the following dependencies:

```toml
[tool.poetry.dependencies]
python = ">=3.10.0,<3.12"
python-fasthtml = "^0.2.1"
replit = "^4.0.0"
pytz = "^2024.1"
```

```replit
run = ["uvicorn", "main:app", "--reload"]
[deployment]
run = ["uvicorn", "main:app", "--reload"]
deploymentTarget = "gce"
[[ports]]
localPort = 8000
externalPort = 80
```

7. Run the project using the "Run" button in Replit
8. Access your guestbook application using the provided URL

For more information on Replit and its features, check out the [Replit documentation](https://docs.replit.com).