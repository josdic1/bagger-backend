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
    ("Styling", "styling"),
    ("DOM / Events", "dom-events"),
    ("File I/O", "file-io"),
    ("Database", "database"),
]

DEFAULT_CHEATS = [
    # ========================================
    # CORS & HTTP/API
    # ========================================
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
        "title": "Axios: set default header once at app start",
        "code": """import axios from "axios";

if (localStorage.getItem("authToken")) {
  axios.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem("authToken")}`;
}
""",
        "notes": "Sets Authorization header globally for all future axios requests.",
        "is_public": True,
        "platform_slugs": ["javascript", "react"],
        "topic_slugs": ["http-api", "setup-tooling"],
    },
    {
        "title": "Axios: remove authorization header",
        "code": """delete axios.defaults.headers.common["Authorization"];
""",
        "notes": "Clears the Authorization header from all future axios requests (e.g., on logout).",
        "is_public": True,
        "platform_slugs": ["javascript", "react"],
        "topic_slugs": ["http-api"],
    },
    {
        "title": "Return 201 for POST/creation",
        "code": """from fastapi import Response

@app.post("/api/items")
def create_item(item: ItemCreate):
    new_item = Item(**item.dict())
    db.add(new_item)
    db.commit()
    return Response(status_code=201, content=new_item.json())
""",
        "notes": "201 Created is the correct HTTP status for successful resource creation.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["http-api"],
    },
    {
        "title": "Return 204 for DELETE/no content",
        "code": """from fastapi import Response

@app.delete("/api/items/{id}")
def delete_item(id: int):
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise HTTPException(404)
    db.delete(item)
    db.commit()
    return Response(status_code=204)
""",
        "notes": "204 No Content is standard for successful deletions with no response body.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["http-api"],
    },
    {
        "title": "CORS, env, port, GET/POST, static hosting",
        "code": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hello")
def hello():
    return {"message": "Hello"}

# Serve React frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
""",
        "notes": "Full FastAPI setup with CORS, environment port, endpoints, and static file serving.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["http-api", "setup-tooling"],
    },
    {
        "title": "Fetch w/ GET, POST, PUT, DELETE + auth",
        "code": """const token = localStorage.getItem("token");

// GET
fetch("/api/items", {
  headers: { "Authorization": `Bearer ${token}` }
});

// POST
fetch("/api/items", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify({ name: "New Item" })
});

// PUT
fetch("/api/items/123", {
  method: "PUT",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify({ name: "Updated" })
});

// DELETE
fetch("/api/items/123", {
  method: "DELETE",
  headers: { "Authorization": `Bearer ${token}` }
});
""",
        "notes": "Standard fetch patterns for all CRUD operations with authentication.",
        "is_public": True,
        "platform_slugs": ["javascript", "react"],
        "topic_slugs": ["http-api"],
    },

    # ========================================
    # SETUP / TOOLING
    # ========================================
    {
        "title": "Vite env must start with VITE_",
        "code": """.env
VITE_API_URL=http://localhost:8080

const API = import.meta.env.VITE_API_URL;
""",
        "notes": "If it doesn't start with VITE_, it won't exist in the frontend.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["setup-tooling", "debugging"],
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
        "title": ".env for Backend",
        "code": """# .env
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-secret-key-here
""",
        "notes": "Store sensitive config in .env, load with python-dotenv.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["setup-tooling"],
    },
    {
        "title": ".env for Frontend",
        "code": """# .env
VITE_API_URL=http://localhost:8080
""",
        "notes": "Vite requires VITE_ prefix for env vars to be exposed to client.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["setup-tooling"],
    },
    {
        "title": "Railway: Add env variables",
        "code": """# Railway dashboard:
# Settings → Variables
# Add key-value pairs
# Deploy automatically picks them up
""",
        "notes": "Set environment variables in Railway dashboard, not in code.",
        "is_public": True,
        "platform_slugs": ["terminal"],
        "topic_slugs": ["setup-tooling"],
    },
    {
        "title": "Export all code from project",
        "code": """import os

IGNORE_DIRS = {
    'node_modules', '.git', '__pycache__',
    'venv', '.venv', 'env',
    '.vscode', 'dist', 'build', 'coverage'
}

IGNORE_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg',
    '.pyc', '.zip', '.tar', '.gz', '.map', '.lock',
    '.woff', '.woff2', '.ttf', '.eot', '.mp3', '.mp4'
}

IGNORE_FILES = {
    'package-lock.json', 'yarn.lock',
    '.DS_Store', 'pack_project.py',
    'project_context.txt'
}

def pack_files(start_path='.'):
    with open('project_context.txt', 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(start_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for file in files:
                if file in IGNORE_FILES:
                    continue

                _, ext = os.path.splitext(file)
                if ext.lower() in IGNORE_EXTENSIONS:
                    continue

                filepath = os.path.join(root, file)

                try:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                except Exception:
                    continue

                outfile.write("\\n" + "=" * 60 + "\\n")
                outfile.write(f"FILE: {filepath}\\n")
                outfile.write("=" * 60 + "\\n\\n")
                outfile.write(content + "\\n")

if __name__ == "__main__":
    pack_files()
    print("Done! Saved to project_context.txt")
""",
        "notes": "In root, create 'pack_project.py' and run python pack_project.py for backend, and python3 pack_project.py for Frontend",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["setup-tooling", "file-io"],
    },
    {
        "title": "Search code for text",
        "code": """grep -rn "useCatering" src/ → include line numbers
grep -r "useCatering(" src/ → find function calls specifically
grep -rl "useCatering" src/ → list only filenames containing it
""",
        "notes": "Find where a hook, function, or identifier is used, trace imports or references across a codebase",
        "is_public": True,
        "platform_slugs": ["terminal"],
        "topic_slugs": ["setup-tooling", "debugging"],
    },

    # ========================================
    # REACT COMPONENTS & HOOKS
    # ========================================
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
    {
        "title": "useEffect Syntax",
        "code": """import { useEffect } from "react";

useEffect(() => {
  // code to run on mount or when dependencies change

  return () => {
    // cleanup (optional)
  };
}, [dependency1, dependency2]);
""",
        "notes": "Runs after render. Empty array [] = run once. No array = run every render.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["components"],
    },
    {
        "title": "useState Syntax",
        "code": """import { useState } from "react";

const [count, setCount] = useState(0);
""",
        "notes": "Manages local component state. Call setter to trigger re-render.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["components"],
    },
    {
        "title": "useContext Syntax",
        "code": """import { createContext, useContext } from "react";

const ThemeContext = createContext();

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Child />
    </ThemeContext.Provider>
  );
}

function Child() {
  const theme = useContext(ThemeContext);
  return <div>{theme}</div>;
}
""",
        "notes": "Shares data across component tree without prop drilling.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["components"],
    },
    {
        "title": "Map over array in JSX",
        "code": """const items = ["apple", "banana", "cherry"];

return (
  <ul>
    {items.map((item, index) => (
      <li key={index}>{item}</li>
    ))}
  </ul>
);
""",
        "notes": "Use .map() to render lists. Always provide a key prop.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["components", "arrays"],
    },
    {
        "title": "Conditional rendering with &&",
        "code": """return (
  <div>
    {isLoggedIn && <p>Welcome back!</p>}
  </div>
);
""",
        "notes": "Render element only if condition is true.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["components"],
    },
    {
        "title": "Conditional rendering with ternary",
        "code": """return (
  <div>
    {isLoggedIn ? <p>Welcome!</p> : <p>Please log in.</p>}
  </div>
);
""",
        "notes": "Render one thing or another based on condition.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["components"],
    },
    {
        "title": "Pass function as prop",
        "code": """function Parent() {
  const handleClick = () => alert("Clicked!");
  return <Child onClick={handleClick} />;
}

function Child({ onClick }) {
  return <button onClick={onClick}>Click me</button>;
}
""",
        "notes": "Pass callbacks down to child components.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["components", "functions"],
    },
    {
        "title": "React Router: Setup",
        "code": """import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}
""",
        "notes": "Basic routing setup for multi-page React apps.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["components", "setup-tooling"],
    },
    {
        "title": "React Router: Link & useNavigate",
        "code": """import { Link, useNavigate } from "react-router-dom";

function Nav() {
  const navigate = useNavigate();

  return (
    <nav>
      <Link to="/">Home</Link>
      <button onClick={() => navigate("/about")}>Go to About</button>
    </nav>
  );
}
""",
        "notes": "Link for declarative navigation, useNavigate for programmatic.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["components"],
    },
    {
        "title": "React Router: useParams",
        "code": """import { useParams } from "react-router-dom";

function UserProfile() {
  const { userId } = useParams();
  return <div>User ID: {userId}</div>;
}

// Route definition:
// <Route path="/users/:userId" element={<UserProfile />} />
""",
        "notes": "Extract dynamic route parameters.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["components"],
    },
    {
        "title": "Controlled Input",
        "code": """const [value, setValue] = useState("");

<input
  value={value}
  onChange={(e) => setValue(e.target.value)}
/>
""",
        "notes": "React controls the input value via state.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["components", "dom-events"],
    },
    {
        "title": "Handle form submit",
        "code": """const handleSubmit = (e) => {
  e.preventDefault();
  // process form data
};

<form onSubmit={handleSubmit}>
  <input />
  <button type="submit">Submit</button>
</form>
""",
        "notes": "Prevent default form submission and handle manually.",
        "is_public": True,
        "platform_slugs": ["react", "javascript"],
        "topic_slugs": ["components", "dom-events"],
    },

    # ========================================
    # JAVASCRIPT CORE
    # ========================================
    {
        "title": "Array: .map()",
        "code": """const numbers = [1, 2, 3];
const doubled = numbers.map(n => n * 2);
// [2, 4, 6]
""",
        "notes": "Transform each element, return new array.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["arrays", "data-transform"],
    },
    {
        "title": "Array: .filter()",
        "code": """const numbers = [1, 2, 3, 4];
const evens = numbers.filter(n => n % 2 === 0);
// [2, 4]
""",
        "notes": "Keep only elements that pass the test.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["arrays", "data-transform"],
    },
    {
        "title": "Array: .reduce()",
        "code": """const numbers = [1, 2, 3, 4];
const sum = numbers.reduce((acc, n) => acc + n, 0);
// 10
""",
        "notes": "Reduce array to single value.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["arrays", "data-transform"],
    },
    {
        "title": "Array: .find()",
        "code": """const users = [{id: 1, name: "Alice"}, {id: 2, name: "Bob"}];
const user = users.find(u => u.id === 2);
// {id: 2, name: "Bob"}
""",
        "notes": "Returns first element that matches, or undefined.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["arrays"],
    },
    {
        "title": "Array: .some()",
        "code": """const numbers = [1, 2, 3, 4];
const hasEven = numbers.some(n => n % 2 === 0);
// true
""",
        "notes": "Returns true if ANY element passes test.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["arrays"],
    },
    {
        "title": "Array: .every()",
        "code": """const numbers = [2, 4, 6];
const allEven = numbers.every(n => n % 2 === 0);
// true
""",
        "notes": "Returns true if ALL elements pass test.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["arrays"],
    },
    {
        "title": "Spread operator for arrays",
        "code": """const arr1 = [1, 2];
const arr2 = [3, 4];
const combined = [...arr1, ...arr2];
// [1, 2, 3, 4]
""",
        "notes": "Merge or copy arrays without mutation.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["arrays"],
    },
    {
        "title": "Spread operator for objects",
        "code": """const obj1 = { a: 1, b: 2 };
const obj2 = { ...obj1, c: 3 };
// { a: 1, b: 2, c: 3 }
""",
        "notes": "Copy or merge objects. Later values override earlier ones.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["data-transform"],
    },
    {
        "title": "Destructuring assignment",
        "code": """const { name, age } = { name: "Alice", age: 30 };
// name = "Alice", age = 30

const [first, second] = [10, 20];
// first = 10, second = 20
""",
        "notes": "Extract values from objects or arrays.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["data-transform"],
    },
    {
        "title": "Arrow function",
        "code": """const add = (a, b) => a + b;

// Multi-line
const greet = (name) => {
  return `Hello, ${name}`;
};
""",
        "notes": "Concise function syntax. No 'this' binding.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["functions"],
    },
    {
        "title": "Template literals",
        "code": """const name = "Alice";
const message = `Hello, ${name}!`;
// "Hello, Alice!"
""",
        "notes": "Interpolate variables into strings.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["strings"],
    },
    {
        "title": "Ternary operator",
        "code": """const isAdult = age >= 18 ? "Yes" : "No";
""",
        "notes": "Inline conditional expression.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["functions"],
    },
    {
        "title": "Optional chaining",
        "code": """const user = { profile: { name: "Alice" } };
const name = user?.profile?.name;
// "Alice"

const missingName = user?.settings?.theme;
// undefined (no error)
""",
        "notes": "Safely access nested properties without errors.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["debugging"],
    },
    {
        "title": "Nullish coalescing",
        "code": """const value = null ?? "default";
// "default"

const count = 0 ?? 10;
// 0 (because 0 is not null/undefined)
""",
        "notes": "Provide fallback only for null/undefined, not for falsy values.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["debugging"],
    },
    {
        "title": "Promise: basic syntax",
        "code": """const promise = new Promise((resolve, reject) => {
  if (success) {
    resolve(data);
  } else {
    reject(error);
  }
});

promise
  .then(data => console.log(data))
  .catch(err => console.error(err));
""",
        "notes": "Handle async operations.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["functions"],
    },
    {
        "title": "Async/await",
        "code": """async function fetchData() {
  try {
    const response = await fetch("/api/data");
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
  }
}
""",
        "notes": "Cleaner async syntax than .then() chains.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["functions"],
    },
    {
        "title": "for loop",
        "code": """for (let i = 0; i < 5; i++) {
  console.log(i);
}
""",
        "notes": "Classic loop with counter.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["loops"],
    },
    {
        "title": "for...of loop",
        "code": """const items = ["a", "b", "c"];
for (const item of items) {
  console.log(item);
}
""",
        "notes": "Loop over iterable values.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["loops"],
    },
    {
        "title": "for...in loop",
        "code": """const obj = { a: 1, b: 2 };
for (const key in obj) {
  console.log(key, obj[key]);
}
""",
        "notes": "Loop over object keys.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["loops"],
    },
    {
        "title": ".forEach() loop",
        "code": """const items = ["a", "b", "c"];
items.forEach((item, index) => {
  console.log(index, item);
});
""",
        "notes": "Functional loop over array. Cannot break early.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["loops", "arrays"],
    },
    {
        "title": "setTimeout",
        "code": """setTimeout(() => {
  console.log("Runs after 2 seconds");
}, 2000);
""",
        "notes": "Execute code after delay (in milliseconds).",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["functions"],
    },
    {
        "title": "setInterval",
        "code": """const intervalId = setInterval(() => {
  console.log("Runs every 1 second");
}, 1000);

// Stop it later:
clearInterval(intervalId);
""",
        "notes": "Execute code repeatedly at interval.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["functions"],
    },
    {
        "title": "try/catch",
        "code": """try {
  const data = JSON.parse(input);
} catch (error) {
  console.error("Parse error:", error);
}
""",
        "notes": "Handle errors gracefully.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["debugging"],
    },
    {
        "title": "typeof operator",
        "code": """typeof "hello";  // "string"
typeof 42;       // "number"
typeof true;     // "boolean"
typeof undefined; // "undefined"
typeof null;     // "object" (quirk)
typeof [];       // "object"
typeof {};       // "object"
typeof function(){}; // "function"
""",
        "notes": "Check data type. Be aware null returns 'object'.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["debugging"],
    },
    {
        "title": "Check if array",
        "code": """Array.isArray([1, 2, 3]);  // true
Array.isArray("hello");     // false
""",
        "notes": "Only reliable way to check for arrays (typeof returns 'object').",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["arrays", "debugging"],
    },

    # ========================================
    # PYTHON CORE
    # ========================================
    {
        "title": "List comprehension",
        "code": """numbers = [1, 2, 3, 4]
doubled = [n * 2 for n in numbers]
# [2, 4, 6, 8]
""",
        "notes": "Pythonic way to transform lists.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["arrays", "data-transform"],
    },
    {
        "title": "Filter with list comprehension",
        "code": """numbers = [1, 2, 3, 4]
evens = [n for n in numbers if n % 2 == 0]
# [2, 4]
""",
        "notes": "Filter list inline.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["arrays", "data-transform"],
    },
    {
        "title": "Dictionary comprehension",
        "code": """words = ["apple", "banana"]
lengths = {word: len(word) for word in words}
# {"apple": 5, "banana": 6}
""",
        "notes": "Build dictionaries from iterables.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["data-transform"],
    },
    {
        "title": "f-string",
        "code": """name = "Alice"
message = f"Hello, {name}!"
# "Hello, Alice!"
""",
        "notes": "String interpolation in Python 3.6+.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["strings"],
    },
    {
        "title": "Lambda function",
        "code": """add = lambda a, b: a + b
result = add(2, 3)
# 5
""",
        "notes": "Anonymous function. Use sparingly.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["functions"],
    },
    {
        "title": "map()",
        "code": """numbers = [1, 2, 3]
doubled = list(map(lambda x: x * 2, numbers))
# [2, 4, 6]
""",
        "notes": "Apply function to all items. Returns iterator.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["arrays", "data-transform"],
    },
    {
        "title": "filter()",
        "code": """numbers = [1, 2, 3, 4]
evens = list(filter(lambda x: x % 2 == 0, numbers))
# [2, 4]
""",
        "notes": "Filter items by condition. Returns iterator.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["arrays", "data-transform"],
    },
    {
        "title": "Unpacking",
        "code": """a, b = [1, 2]
# a = 1, b = 2

first, *rest = [1, 2, 3, 4]
# first = 1, rest = [2, 3, 4]
""",
        "notes": "Extract values from sequences.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["data-transform"],
    },
    {
        "title": "Enumerate",
        "code": """items = ["a", "b", "c"]
for index, item in enumerate(items):
    print(index, item)
# 0 a
# 1 b
# 2 c
""",
        "notes": "Loop with index and value.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["loops"],
    },
    {
        "title": "Zip",
        "code": """names = ["Alice", "Bob"]
ages = [25, 30]
for name, age in zip(names, ages):
    print(name, age)
# Alice 25
# Bob 30
""",
        "notes": "Combine multiple iterables.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["loops", "data-transform"],
    },
    {
        "title": "Try/except",
        "code": """try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
""",
        "notes": "Handle exceptions.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["debugging"],
    },
    {
        "title": "Class definition",
        "code": """class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, I'm {self.name}"

p = Person("Alice", 30)
print(p.greet())
""",
        "notes": "Define classes with __init__ constructor and methods.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["classes"],
    },
    {
        "title": "Class inheritance",
        "code": """class Animal:
    def speak(self):
        return "Sound"

class Dog(Animal):
    def speak(self):
        return "Woof"

d = Dog()
print(d.speak())  # "Woof"
""",
        "notes": "Inherit from parent class and override methods.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["classes"],
    },
    {
        "title": "Read file",
        "code": """with open("file.txt", "r") as f:
    content = f.read()
""",
        "notes": "Read entire file into string. Auto-closes file.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["file-io"],
    },
    {
        "title": "Write file",
        "code": """with open("file.txt", "w") as f:
    f.write("Hello, world!")
""",
        "notes": "Write string to file. Creates/overwrites file.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["file-io"],
    },
    {
        "title": "Append to file",
        "code": """with open("file.txt", "a") as f:
    f.write("New line\\n")
""",
        "notes": "Append to end of file without overwriting.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["file-io"],
    },
    {
        "title": "JSON: load from file",
        "code": """import json

with open("data.json", "r") as f:
    data = json.load(f)
""",
        "notes": "Parse JSON file into Python dict/list.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["file-io", "data-transform"],
    },
    {
        "title": "JSON: save to file",
        "code": """import json

data = {"name": "Alice", "age": 30}
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)
""",
        "notes": "Write Python dict/list to JSON file.",
        "is_public": True,
        "platform_slugs": ["python"],
        "topic_slugs": ["file-io", "data-transform"],
    },

    # ========================================
    # SQL / DATABASE
    # ========================================
    {
        "title": "SELECT: basic query",
        "code": """SELECT * FROM users;
SELECT name, email FROM users;
""",
        "notes": "Fetch all columns or specific columns.",
        "is_public": True,
        "platform_slugs": ["sql"],
        "topic_slugs": ["database"],
    },
    {
        "title": "WHERE: filter rows",
        "code": """SELECT * FROM users WHERE age > 25;
SELECT * FROM users WHERE name = 'Alice';
""",
        "notes": "Filter results by condition.",
        "is_public": True,
        "platform_slugs": ["sql"],
        "topic_slugs": ["database"],
    },
    {
        "title": "INSERT: add row",
        "code": """INSERT INTO users (name, email, age)
VALUES ('Alice', 'alice@example.com', 30);
""",
        "notes": "Add new record to table.",
        "is_public": True,
        "platform_slugs": ["sql"],
        "topic_slugs": ["database"],
    },
    {
        "title": "UPDATE: modify rows",
        "code": """UPDATE users
SET age = 31
WHERE name = 'Alice';
""",
        "notes": "Update existing records.",
        "is_public": True,
        "platform_slugs": ["sql"],
        "topic_slugs": ["database"],
    },
    {
        "title": "DELETE: remove rows",
        "code": """DELETE FROM users WHERE id = 5;
""",
        "notes": "Remove records from table.",
        "is_public": True,
        "platform_slugs": ["sql"],
        "topic_slugs": ["database"],
    },
    {
        "title": "JOIN: combine tables",
        "code": """SELECT users.name, orders.total
FROM users
JOIN orders ON users.id = orders.user_id;
""",
        "notes": "Combine rows from two tables based on related column.",
        "is_public": True,
        "platform_slugs": ["sql"],
        "topic_slugs": ["database"],
    },
    {
        "title": "ORDER BY: sort results",
        "code": """SELECT * FROM users ORDER BY age DESC;
""",
        "notes": "Sort by column. DESC = descending, ASC = ascending (default).",
        "is_public": True,
        "platform_slugs": ["sql"],
        "topic_slugs": ["database"],
    },
    {
        "title": "LIMIT: restrict rows",
        "code": """SELECT * FROM users LIMIT 10;
""",
        "notes": "Return only first N rows.",
        "is_public": True,
        "platform_slugs": ["sql"],
        "topic_slugs": ["database"],
    },
    {
        "title": "COUNT: aggregate",
        "code": """SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM users WHERE age > 25;
""",
        "notes": "Count rows matching condition.",
        "is_public": True,
        "platform_slugs": ["sql"],
        "topic_slugs": ["database"],
    },
    {
        "title": "GROUP BY: aggregate by category",
        "code": """SELECT age, COUNT(*) FROM users GROUP BY age;
""",
        "notes": "Group rows by column and aggregate.",
        "is_public": True,
        "platform_slugs": ["sql"],
        "topic_slugs": ["database"],
    },

    # ========================================
    # CSS / STYLING
    # ========================================
    {
        "title": "Flexbox: center content",
        "code": """.container {
  display: flex;
  justify-content: center;
  align-items: center;
}
""",
        "notes": "Center children horizontally and vertically.",
        "is_public": True,
        "platform_slugs": ["css"],
        "topic_slugs": ["styling"],
    },
    {
        "title": "Flexbox: space between",
        "code": """.container {
  display: flex;
  justify-content: space-between;
}
""",
        "notes": "Distribute children with space between them.",
        "is_public": True,
        "platform_slugs": ["css"],
        "topic_slugs": ["styling"],
    },
    {
        "title": "Grid: basic layout",
        "code": """.container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1rem;
}
""",
        "notes": "Create 3-column grid with equal widths.",
        "is_public": True,
        "platform_slugs": ["css"],
        "topic_slugs": ["styling"],
    },
    {
        "title": "Media query: responsive",
        "code": """@media (max-width: 768px) {
  .container {
    flex-direction: column;
  }
}
""",
        "notes": "Apply styles for specific screen sizes.",
        "is_public": True,
        "platform_slugs": ["css"],
        "topic_slugs": ["styling"],
    },
    {
        "title": "Box model: padding vs margin",
        "code": """.box {
  padding: 1rem;  /* inside spacing */
  margin: 1rem;   /* outside spacing */
}
""",
        "notes": "Padding = inside, Margin = outside.",
        "is_public": True,
        "platform_slugs": ["css"],
        "topic_slugs": ["styling"],
    },
    {
        "title": "Position: absolute",
        "code": """.parent {
  position: relative;
}

.child {
  position: absolute;
  top: 10px;
  right: 10px;
}
""",
        "notes": "Position element relative to nearest positioned ancestor.",
        "is_public": True,
        "platform_slugs": ["css"],
        "topic_slugs": ["styling"],
    },
    {
        "title": "Position: fixed",
        "code": """.header {
  position: fixed;
  top: 0;
  width: 100%;
}
""",
        "notes": "Fix element to viewport (stays on scroll).",
        "is_public": True,
        "platform_slugs": ["css"],
        "topic_slugs": ["styling"],
    },
    {
        "title": "z-index: layer order",
        "code": """.overlay {
  position: absolute;
  z-index: 10;
}
""",
        "notes": "Control stacking order. Higher = on top. Only works on positioned elements.",
        "is_public": True,
        "platform_slugs": ["css"],
        "topic_slugs": ["styling"],
    },
    {
        "title": "Pseudo-classes: :hover, :focus",
        "code": """button:hover {
  background-color: blue;
}

input:focus {
  border-color: green;
}
""",
        "notes": "Style elements based on state.",
        "is_public": True,
        "platform_slugs": ["css"],
        "topic_slugs": ["styling"],
    },
    {
        "title": "CSS variables",
        "code": """:root {
  --primary-color: #3490dc;
}

.button {
  background-color: var(--primary-color);
}
""",
        "notes": "Define reusable values.",
        "is_public": True,
        "platform_slugs": ["css"],
        "topic_slugs": ["styling"],
    },
    {
        "title": "Tailwind-style utility classes",
        "code": """/* Define utilities in your CSS */
.bg-orange { background-color: #eb5638; }
.text-white { color: #ebe5c0; }
.p-4 { padding: 1rem; }
.m-2 { margin: 0.5rem; }
.flex { display: flex; }
.justify-center { justify-content: center; }
.items-center { align-items: center; }
""",
        "notes": "Inspired by Tailwind",
        "is_public": True,
        "platform_slugs": ["css"],
        "topic_slugs": ["styling"],
    },
    {
        "title": "Color Palette",
        "code": """Orange: #eb5638
Black: #2b2b2b 
White: #ebe5c0
""",
        "notes": "Color list with css hex codes",
        "is_public": True,
        "platform_slugs": ["css"],
        "topic_slugs": ["styling"],
    },

    # ========================================
    # HTML / DOM
    # ========================================
    {
        "title": "Basic HTML structure",
        "code": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <h1>Hello World</h1>
</body>
</html>
""",
        "notes": "Minimal HTML5 boilerplate.",
        "is_public": True,
        "platform_slugs": ["html"],
        "topic_slugs": ["setup-tooling"],
    },
    {
        "title": "Semantic HTML",
        "code": """<header>...</header>
<nav>...</nav>
<main>
  <article>...</article>
  <section>...</section>
</main>
<footer>...</footer>
""",
        "notes": "Use semantic tags for accessibility and SEO.",
        "is_public": True,
        "platform_slugs": ["html"],
        "topic_slugs": ["styling"],
    },
    {
        "title": "Form elements",
        "code": """<form>
  <label for="name">Name:</label>
  <input type="text" id="name" name="name" />

  <label for="email">Email:</label>
  <input type="email" id="email" name="email" />

  <button type="submit">Submit</button>
</form>
""",
        "notes": "Basic form with labels and inputs.",
        "is_public": True,
        "platform_slugs": ["html"],
        "topic_slugs": ["dom-events"],
    },
    {
        "title": "querySelector",
        "code": """const element = document.querySelector(".my-class");
const allElements = document.querySelectorAll(".my-class");
""",
        "notes": "Select DOM elements by CSS selector.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["dom-events"],
    },
    {
        "title": "addEventListener",
        "code": """const button = document.querySelector("button");
button.addEventListener("click", () => {
  alert("Clicked!");
});
""",
        "notes": "Attach event handler to element.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["dom-events"],
    },
    {
        "title": "Modify DOM content",
        "code": """const div = document.querySelector(".my-div");
div.textContent = "New text";
div.innerHTML = "<p>New HTML</p>";
""",
        "notes": "Change element content.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["dom-events"],
    },
    {
        "title": "Add/remove CSS class",
        "code": """const element = document.querySelector(".box");
element.classList.add("active");
element.classList.remove("inactive");
element.classList.toggle("visible");
""",
        "notes": "Manipulate element classes.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["dom-events", "styling"],
    },
    {
        "title": "Create and append element",
        "code": """const newDiv = document.createElement("div");
newDiv.textContent = "Hello";
document.body.appendChild(newDiv);
""",
        "notes": "Create new DOM elements programmatically.",
        "is_public": True,
        "platform_slugs": ["javascript"],
        "topic_slugs": ["dom-events"],
    },

    # ========================================
    # REGEX
    # ========================================
    {
        "title": "Regex: test for match",
        "code": """const pattern = /hello/i;
pattern.test("Hello world");  // true
""",
        "notes": "Check if string matches pattern. i = case-insensitive.",
        "is_public": True,
        "platform_slugs": ["regex", "javascript"],
        "topic_slugs": ["strings"],
    },
    {
        "title": "Regex: extract matches",
        "code": """const text = "Phone: 555-1234";
const match = text.match(/\\d{3}-\\d{4}/);
// ["555-1234"]
""",
        "notes": "Extract matched substring.",
        "is_public": True,
        "platform_slugs": ["regex", "javascript"],
        "topic_slugs": ["strings"],
    },
    {
        "title": "Regex: replace",
        "code": """const text = "Hello world";
const result = text.replace(/world/, "there");
// "Hello there"
""",
        "notes": "Replace matched text.",
        "is_public": True,
        "platform_slugs": ["regex", "javascript"],
        "topic_slugs": ["strings"],
    },
    {
        "title": "Regex: common patterns",
        "code": """\\d   - digit
\\w   - word character
\\s   - whitespace
.    - any character
*    - 0 or more
+    - 1 or more
?    - 0 or 1
{n}  - exactly n
{n,} - n or more
^    - start of string
$    - end of string
""",
        "notes": "Common regex building blocks.",
        "is_public": True,
        "platform_slugs": ["regex"],
        "topic_slugs": ["strings"],
    },

    # ========================================
    # TERMINAL
    # ========================================
    {
        "title": "Navigate directories",
        "code": """pwd     # print working directory
ls      # list files
cd dir  # change to directory
cd ..   # go up one level
cd ~    # go to home
""",
        "notes": "Basic navigation commands.",
        "is_public": True,
        "platform_slugs": ["terminal"],
        "topic_slugs": ["setup-tooling"],
    },
    {
        "title": "File operations",
        "code": """touch file.txt      # create file
mkdir mydir         # create directory
rm file.txt         # delete file
rm -rf mydir        # delete directory
cp src dest         # copy
mv src dest         # move/rename
""",
        "notes": "Create, delete, copy, move files/directories.",
        "is_public": True,
        "platform_slugs": ["terminal"],
        "topic_slugs": ["file-io"],
    },
    {
        "title": "View file contents",
        "code": """cat file.txt        # print entire file
head file.txt       # first 10 lines
tail file.txt       # last 10 lines
less file.txt       # paginated view
""",
        "notes": "Display file contents in terminal.",
        "is_public": True,
        "platform_slugs": ["terminal"],
        "topic_slugs": ["file-io"],
    },
    {
        "title": "Git: basic workflow",
        "code": """git status
git add .
git commit -m "message"
git push
""",
        "notes": "Stage, commit, and push changes.",
        "is_public": True,
        "platform_slugs": ["terminal"],
        "topic_slugs": ["setup-tooling"],
    },
    {
        "title": "Git: branches",
        "code": """git branch             # list branches
git branch feature     # create branch
git checkout feature   # switch to branch
git merge feature      # merge into current
""",
        "notes": "Work with branches.",
        "is_public": True,
        "platform_slugs": ["terminal"],
        "topic_slugs": ["setup-tooling"],
    },
    {
        "title": "Find files",
        "code": """find . -name "*.js"
""",
        "notes": "Search for files by name pattern.",
        "is_public": True,
        "platform_slugs": ["terminal"],
        "topic_slugs": ["file-io"],
    },
    {
        "title": "Pipe commands",
        "code": """ls | grep "test"      # filter ls output
cat file.txt | wc -l  # count lines
""",
        "notes": "Chain commands together.",
        "is_public": True,
        "platform_slugs": ["terminal"],
        "topic_slugs": ["setup-tooling"],
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