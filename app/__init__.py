from flask import Flask, abort, flash, redirect, render_template, request, url_for

from .db import close_db, get_db, init_db


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.update(SECRET_KEY="dev", DATABASE="instance/app.db")

    # --- Security headers (CSP, etc.) + cookie flags ---
    @app.after_request
    def set_security_headers(resp):
        # CSP: blokker inline/eksterne scripts; tillat bare self
        resp.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; object-src 'none'; "
            "base-uri 'self'; frame-ancestors 'none'"
        )
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["X-Frame-Options"] = "DENY"
        resp.headers["Referrer-Policy"] = "no-referrer"
        return resp

    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,  # sett True hvis du bruker HTTPS
    )

    # DB lifecycle
    @app.teardown_appcontext
    def _teardown(exception):
        close_db()

    # CLI: flask --app app:create_app init-db
    @app.cli.command("init-db")
    def init_db_command():
        init_db()
        print("Initialized the database.")

    # --- Routes ---
    @app.get("/")
    def root():
        return redirect(url_for("list_posts"))

    @app.get("/posts")
    def list_posts():
        db = get_db()
        rows = db.execute(
            """
            SELECT p.*,
                   (SELECT COUNT(1) FROM comments c WHERE c.post_id = p.id) AS comment_count
            FROM posts p
            ORDER BY p.created_at DESC
            """
        ).fetchall()
        return render_template("posts/index.html", posts=rows)

    @app.get("/posts/new")
    def new_post():
        return render_template("posts/new.html")

    @app.post("/posts")
    def create_post():
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        if not title or not body:
            flash("Title and body are required.", "error")
            return redirect(url_for("new_post"))
        db = get_db()
        # ✅ fikset: fullstendig streng/SQL
        db.execute(
            "INSERT INTO posts (title, body) VALUES (?, ?)",
            (title, body),
        )
        db.commit()
        return redirect(url_for("list_posts"))

    @app.get("/posts/<int:post_id>")
    def post_detail(post_id: int):
        db = get_db()
        post = db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
        if not post:
            abort(404)
        comments = db.execute(
            "SELECT * FROM comments WHERE post_id = ? ORDER BY created_at ASC",
            (post_id,),
        ).fetchall()
        return render_template("posts/detail.html", post=post, comments=comments)

    @app.post("/posts/<int:post_id>/comments")
    def create_comment(post_id: int):
        # ✅ mitigation: saniter input før lagring
        import bleach

        author = request.form.get("author", "Anonymous").strip() or "Anonymous"
        content = request.form.get("content", "").strip()
        if not content:
            flash("Comment content is required.", "error")
            return redirect(url_for("post_detail", post_id=post_id))

        # Tillat ingen HTML: stripp alt (ren tekst)
        clean = bleach.clean(content, tags=[], attributes={}, strip=True)

        db = get_db()
        exists = db.execute("SELECT 1 FROM posts WHERE id = ?", (post_id,)).fetchone()
        if not exists:
            abort(404)
        db.execute(
            "INSERT INTO comments (post_id, author, content) VALUES (?, ?, ?)",
            (post_id, author, clean),
        )
        db.commit()
        return redirect(url_for("post_detail", post_id=post_id))

    # --- XSS demo endpoint ---
    @app.get("/debug/capture")
    def debug_capture():
        from flask import Response

        captured = request.args.get("c", "<empty>")
        print(f"[XSS-DEMO] captured: {captured}", flush=True)
        return Response("Captured", mimetype="text/plain")

    return app
