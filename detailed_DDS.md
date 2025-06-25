# Detailed Design Specification (DDS) – Detailed Breakdown

## 1. Catalog Parser

**Classes:**
- `CatalogParser`
  - **Methods:**
    - `parse_catalog() -> List[Tea]`
    - `extract_data(html: str) -> List[dict]`
    - `transform_data(raw_data: List[dict]) -> List[Tea]`
    - `update_database(teas: List[Tea])`
    - `log_error(error: Exception)`

**Interface Contracts:**
- `parse_catalog()` triggers the parsing process and returns structured tea data.
- `update_database(data)` updates the database with parsed teas.

---

## 2. Database Layer

**Classes:**
- `Database`
  - **Methods:**
    - `add_tea(tea: Tea)`
    - `get_teas(query: dict) -> List[Tea]`
    - `update_tea(tea_id: int, data: dict)`
    - `delete_tea(tea_id: int)`
    - `add_user(user: User)`
    - `update_user(user_id: int, data: dict)`
    - `get_user(user_id: int) -> User`
    - `add_feedback(feedback: Feedback)`
    - `get_feedback(tea_id: int) -> List[Feedback]`

**Data Models:**
- `Tea`
- `Category`
- `User`
- `Feedback`

**Interface Contracts:**
- CRUD operations for teas, users, feedback.

---

## 3. Recommendation Engine

**Classes:**
- `RecommendationEngine`
  - **Methods:**
    - `suggest_teas(user_id: int) -> List[Tea]`
    - `process_feedback(user_id: int, tea_id: int, feedback: Feedback)`

**Interface Contracts:**
- `suggest_teas(user_id)` returns recommended teas.
- `process_feedback(user_id, tea_id, feedback)` updates the recommendation logic.

---

## 4. Telegram Bot Interface

**Classes:**
- `TelegramBot`
  - **Methods:**
    - `handle_message(message: Message)`
    - `send_message(user_id: int, text: str, options: dict = None)`
    - `register_user(user_id: int)`

**Interface Contracts:**
- `handle_message(message)` processes incoming messages.
- `send_message(user_id, text, options)` sends messages to users.
- `register_user(user_id)` registers new users.

---

## 5. User Profile Manager

**Classes:**
- `UserProfileManager`
  - **Methods:**
    - `create_profile(user_id: int, data: dict)`
    - `update_preferences(user_id: int, preferences: dict)`
    - `get_profile(user_id: int) -> User`
    - `add_history(user_id: int, tea_id: int)`

**Interface Contracts:**
- CRUD for user profiles, update preferences, track history.

---

## 6. Scheduler/Updater

**Classes:**
- `Scheduler`
  - **Methods:**
    - `schedule_task(task: Callable, interval: int)`
    - `run_task_now(task: Callable)`

**Interface Contracts:**
- `schedule_task(task, interval)` schedules periodic tasks.
- `run_task_now(task)` triggers immediate execution.

---

## 7. Admin Dashboard (Future/Optional)

**Classes:**
- `AdminDashboard`
  - **Methods:**
    - `admin_login(credentials: dict) -> bool`
    - `view_stats() -> dict`
    - `manage_catalog()`
    - `manage_users()`

**Interface Contracts:**
- Admin authentication, catalog/user management, analytics.

---

## 8. External Integrations (Future/Optional)

**Classes:**
- `ExternalIntegration`
  - **Methods:**
    - `fetch_external_data() -> List[dict]`
    - `send_order(data: dict)`

**Interface Contracts:**
- Fetch data from external APIs, send orders.

---

## Data Models

```python
class Tea:
    id: int
    name: str
    category: str
    subcategory: str
    description: str
    price: float
    packaging: str
    image_url: str

class Category:
    id: int
    name: str
    parent_id: Optional[int]

class User:
    id: int
    telegram_id: str
    preferences: dict
    history: list

class Feedback:
    id: int
    user_id: int
    tea_id: int
    rating: int
    comment: str
    timestamp: datetime
```

---

## Interface Contracts (Summary Table)

| Module                | Interface/Method                | Description                                 |
|-----------------------|---------------------------------|---------------------------------------------|
| Catalog Parser        | `parse_catalog()`               | Parse and return tea data                   |
|                       | `update_database(data)`         | Update DB with parsed teas                  |
| Database Layer        | `add_tea(tea)`, `get_teas(query)` | CRUD for teas                               |
|                       | `add_user(user)`, `get_user(id)` | CRUD for users                              |
|                       | `add_feedback(feedback)`        | Add user feedback                           |
| Recommendation Engine | `suggest_teas(user_id)`         | Recommend teas                              |
|                       | `process_feedback(...)`         | Update logic with feedback                  |
| Telegram Bot          | `handle_message(message)`       | Process user messages                       |
|                       | `send_message(user_id, text)`   | Send message to user                        |
| User Profile Manager  | `create_profile(...)`           | Create user profile                         |
|                       | `update_preferences(...)`       | Update user preferences                     |
| Scheduler/Updater     | `schedule_task(...)`            | Schedule periodic tasks                     |
| Admin Dashboard       | `admin_login(...)`              | Admin authentication                        |
|                       | `manage_catalog()`              | Catalog management                          |
| External Integrations | `fetch_external_data()`         | Get data from external APIs                 |

---

If you need this in a specific format (e.g., UML, code stubs, or a document), or want a breakdown for a particular module, let me know! 