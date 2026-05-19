"""StaffHub Portal FastAPI app for CyberForge learning scenario."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from database import get_connection, init_database
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from seed import seed_if_needed

APP_ROOT = Path(__file__).parent
templates = Jinja2Templates(directory=str(APP_ROOT / "templates"))
app = FastAPI(title="StaffHub Portal")


def _configure_logger() -> logging.Logger:
    log_path = Path(os.getenv("STAFFHUB_LOG_FILE", "/app/logs/staffhub.log"))
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("staffhub")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger


logger = _configure_logger()


@app.on_event("startup")
def startup_event() -> None:
    init_database()
    seed_if_needed()
    logger.info("staffhub_startup_complete")


def get_user_by_id(user_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


def get_current_user(request: Request) -> dict | None:
    raw_user_id = request.cookies.get("staffhub_session")
    if not raw_user_id:
        return None
    try:
        return get_user_by_id(int(raw_user_id))
    except ValueError:
        return None


@app.get("/", response_class=HTMLResponse)
def root() -> RedirectResponse:
    return RedirectResponse(url="/login", status_code=302)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, error: str | None = None) -> HTMLResponse:
    return templates.TemplateResponse("login.html", {"request": request, "error": error})


@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...)) -> RedirectResponse:
    with get_connection() as conn:
        # Intentional educational weakness: plaintext password comparison.
        row = conn.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password),
        ).fetchone()

    source_ip = request.client.host if request.client else "unknown"
    if not row:
        logger.warning("auth_failure email=%s source_ip=%s", email, source_ip)
        return RedirectResponse(url="/login?error=Invalid+credentials", status_code=303)

    user = dict(row)
    logger.info(
        "auth_success user=%s role=%s source_ip=%s",
        user["email"],
        user["role"],
        source_ip,
    )

    response = RedirectResponse(url="/dashboard", status_code=303)
    # Intentional educational weakness: predictable, non-signed session value.
    response.set_cookie("staffhub_session", str(user["id"]), httponly=False)
    return response


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request) -> Response:
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    with get_connection() as conn:
        users = [dict(row) for row in conn.execute("SELECT * FROM users ORDER BY id").fetchall()]

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user, "users": users},
    )


@app.get("/profile/{user_id}", response_class=HTMLResponse)
def profile(request: Request, user_id: int) -> Response:
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    # Intentional educational weakness: no authorization check for profile access.
    profile_user = get_user_by_id(user_id)
    if not profile_user:
        return RedirectResponse(url="/dashboard", status_code=302)

    logger.info(
        "profile_view actor=%s target=%s actor_role=%s",
        user["email"],
        profile_user["email"],
        user["role"],
    )
    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "user": user, "profile": profile_user},
    )


@app.get("/logout")
def logout() -> RedirectResponse:
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("staffhub_session")
    return response
