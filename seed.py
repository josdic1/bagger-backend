# seed.py
from sqlalchemy.orm import Session

from models.platform import Platform
from models.topic import Topic
from models.cheat import Cheat, CheatPlatform, CheatTopic


DEFAULT_PLATFORMS = [
    ("CSS", "css", "language"),
    ("HTML", "html", "language"),
    ("JavaScript", "javascript", "language"),
    ("Python", "python", "language"),
    ("React", "react", "framework"),
    ("SQL", "sql", "language"),
    ("Terminal", "terminal", "tool"),
    ("Regex", "regex", "tool"),
    ("JSON", "json", "format"),
    ("XML", "xml", "format"),
]

DEFAULT_TOPICS = [
    ("Arrays", "arrays"),
    ("Classes", "classes"),
    ("Functions", "functions"),
    ("Loops", "loops"),
    ("Components", "components"),
    ("Setup / Tooling", "setup-tooling"),
    ("HTTP / API", "http-api"),
    ("Debugging", "debugging"),
    ("Strings", "strings"),
    ("Data Transform", "data-transform"),
]

DEFAULT_CHEATS = [
    {
        "title": "CORS: credentials means NO '*'",
        "code": """from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
""",
        "notes": "If allow_credentials=True, you must list exact origins. '*' breaks credentials.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["http-api", "setup-tooling", "debugging"],
    },
    {
        "title": "Do NOT send Bearer token to login/signup",
        "code": """// GOOD
api.post("/api/users/login", data, { skipAuth: true });

// BAD
// sending Authorization header to public auth routes
""",
        "notes": "Login and signup must be public. Do not attach Authorization header.",
        "is_public": True,
        "platform_slugs": ["javascript", "react"],
        "topic_slugs": ["http-api", "debugging"],
    },
    {
        "title": "Trailing Slash Discipline",
        "code": """// GOOD
/api/users

// BAD
/api/users/
/api/users

// FastAPI
@app.get("/api/users")
""",
        "notes": "Pick one style and stick to it. Mixed slashes cause random 404/307.",
        "is_public": True,
        "platform_slugs": ["python", "javascript"],
        "topic_slugs": ["http-api", "debugging"],
    },
    {
        "title": "Vite env must start with VITE_",
        "code": """.env
VITE_API_URL=http://localhost:8080

const API = import.meta.env.VITE_API_URL;
""",
        "notes": "If it doesn’t start with VITE_, it won’t exist in the frontend.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["setup-tooling", "debugging"],
    },
    {
        "title": "Strip trailing slash from API base URL",
        "code": """const base = import.meta.env.VITE_API_URL.replace(/\\/+$/, "");
fetch(`${base}/api/users/me`);
""",
        "notes": "Prevents accidental double slash URLs.",
        "is_public": True,
        "platform_slugs": ["javascript", "react"],
        "topic_slugs": ["http-api", "debugging"],
    },
    {
        "title": "Virtualenv must be active",
        "code": """python3 -m venv venv
source venv/bin/activate
which python
""",
        "notes": "If you install globally, things randomly break later.",
        "is_public": True,
        "platform_slugs": ["python", "terminal"],
        "topic_slugs": ["setup-tooling", "debugging"],
    },
    {
        "title": "Kill Port Conflicts",
        "code": """lsof -i :8080
kill -9 <PID>
""",
        "notes": "Wrong server responding = ghost bugs.",
        "is_public": True,
        "platform_slugs": ["terminal"],
        "topic_slugs": ["setup-tooling", "debugging"],
    },
    {
        "title": "401 Must Immediately Logout",
        "code": """if (response.status === 401) {
  localStorage.removeItem("token");
  window.location.replace("/login");
}
""",
        "notes": "Never spin on VERIFYING SESSION forever.",
        "is_public": True,
        "platform_slugs": ["javascript", "react"],
        "topic_slugs": ["http-api", "debugging"],
    },
    {
        "title": "Production Must Not Point to Localhost",
        "code": """const apiUrl = import.meta.env.VITE_API_URL;

if (import.meta.env.PROD && apiUrl.includes("localhost")) {
  throw new Error("PROD build pointing to localhost API.");
}
""",
        "notes": "Prevents silent production disasters.",
        "is_public": True,
        "platform_slugs": ["javascript", "react"],
        "topic_slugs": ["setup-tooling", "http-api", "debugging"],
    },
    {
        "title": "Derived State: Do NOT use useEffect for Boolean(id)",
        "code": """// GOOD
const inEditMode = Boolean(id);

// BAD
useEffect(() => {
  setInEditMode(Boolean(id));
}, [id]);
""",
        "notes": "If state can be derived from props, derive it directly. Avoid unnecessary useEffect.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["components", "debugging"],
    },
]


def seed_if_empty(db: Session) -> None:
    # -------------------------
    # Seed taxonomy
    # -------------------------
    platform_count = db.query(Platform).count()
    topic_count = db.query(Topic).count()

    if platform_count == 0:
        for name, slug, typ in DEFAULT_PLATFORMS:
            db.add(Platform(name=name, slug=slug, type=typ))

    if topic_count == 0:
        for name, slug in DEFAULT_TOPICS:
            db.add(Topic(name=name, slug=slug))

    if platform_count == 0 or topic_count == 0:
        db.commit()

    # -------------------------
    # Seed cheats (no user required)
    # -------------------------
    if db.query(Cheat).count() != 0:
        return

    platform_map = {p.slug: p.id for p in db.query(Platform).all()}
    topic_map = {t.slug: t.id for t in db.query(Topic).all()}

    for item in DEFAULT_CHEATS:
        cheat = Cheat(
            title=item["title"],
            code=item["code"],
            notes=item.get("notes"),
            is_public=item.get("is_public", True),
            created_by_user_id=None,  # ✅ global/system cheat
        )
        db.add(cheat)
        db.flush()  # get cheat.id

        for slug in set(item.get("platform_slugs", [])):
            pid = platform_map.get(slug)
            if pid is not None:
                db.add(CheatPlatform(cheat_id=cheat.id, platform_id=pid))

        for slug in set(item.get("topic_slugs", [])):
            tid = topic_map.get(slug)
            if tid is not None:
                db.add(CheatTopic(cheat_id=cheat.id, topic_id=tid))

    db.commit()
