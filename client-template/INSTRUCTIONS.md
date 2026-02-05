# FastAPI HTML Client Template - Setup Instructions

## For a New Project

### 1. Copy the Template
```bash
cp client-template/template.html your-new-project/client/index.html
```

### 2. Update Configuration (3 lines)
Open `index.html` and find the `CONFIG` object:
```javascript
const CONFIG = {
    API_URL: 'http://localhost:3000',  // ← Change to your API port
    APP_TITLE: '💪 Gym Booking Client',  // ← Change to your app name
    DEFAULT_LOGIN: {
        email: 'test@test.com',  // ← Add test credentials
        password: 'test123'
    }
};
```

### 3. Add Your Custom Sections

Find this comment in the HTML:
```html
<!-- ADD YOUR CUSTOM SECTIONS HERE -->
```

Add sections for your resources:
```html
<!-- WORKOUTS -->
<div class="section">
    <h2>🏋️ Workouts</h2>
    <button onclick="getWorkouts()">Get All Workouts</button>
    
    <div style="margin-top: 15px;">
        <h3>Create Workout</h3>
        <input type="text" id="workoutName" placeholder="Workout Name">
        <input type="number" id="workoutDuration" placeholder="Duration (minutes)">
        <button onclick="createWorkout()">Create Workout</button>
    </div>
    
    <div class="divider">
        <h3>Delete Workout</h3>
        <input type="number" id="deleteWorkoutId" placeholder="Workout ID">
        <button onclick="deleteWorkout()" style="background: #ff6b6b;">Delete</button>
    </div>
    
    <div class="result" id="workoutsResult"></div>
</div>
```

### 4. Add Your Custom Functions

Find this comment in the JavaScript:
```javascript
// ADD YOUR CUSTOM FUNCTIONS HERE
```

Add functions for your resources:
```javascript
// WORKOUTS
async function getWorkouts() {
    const result = await apiCall('/workouts/', 'GET', null, true);
    displayResult('workoutsResult', result);
}

async function createWorkout() {
    const name = document.getElementById('workoutName').value;
    const duration = parseInt(document.getElementById('workoutDuration').value);
    const result = await apiCall('/workouts/', 'POST', { name, duration }, true);
    if (!result.error) await getWorkouts();
    displayResult('workoutsResult', result);
}

async function deleteWorkout() {
    const id = document.getElementById('deleteWorkoutId').value;
    if (!confirm(`Delete workout #${id}?`)) return;
    const result = await apiCall(`/workouts/${id}`, 'DELETE', null, true);
    if (!result.error) {
        await getWorkouts();
        document.getElementById('workoutsResult').innerHTML = '<span class="success">✅ Deleted</span>';
    } else {
        displayResult('workoutsResult', result);
    }
}
```

### 5. Open in Browser
```bash
open client/index.html
# Or just double-click the file
```

## CRUD Patterns

### GET (List all)
```javascript
async function getItems() {
    const result = await apiCall('/items/', 'GET', null, true);
    displayResult('itemsResult', result);
}
```

### POST (Create)
```javascript
async function createItem() {
    const name = document.getElementById('itemName').value;
    const result = await apiCall('/items/', 'POST', { name }, true);
    if (!result.error) await getItems();  // Refresh list
    displayResult('itemsResult', result);
}
```

### PATCH (Update)
```javascript
async function updateItem() {
    const id = document.getElementById('updateItemId').value;
    const name = document.getElementById('updateItemName').value;
    const body = {};
    if (name) body.name = name;
    const result = await apiCall(`/items/${id}`, 'PATCH', body, true);
    if (!result.error) await getItems();
    displayResult('itemsResult', result);
}
```

### DELETE
```javascript
async function deleteItem() {
    const id = document.getElementById('deleteItemId').value;
    if (!confirm(`Delete item #${id}?`)) return;
    const result = await apiCall(`/items/${id}`, 'DELETE', null, true);
    if (!result.error) {
        await getItems();
        document.getElementById('itemsResult').innerHTML = '<span class="success">✅ Deleted</span>';
    } else {
        displayResult('itemsResult', result);
    }
}
```

## Tips

1. **Color scheme for buttons:**
   - Blue (`#4a90e2`): GET/POST (default)
   - Orange (`#ffa94d`): PATCH (update)
   - Red (`#ff6b6b`): DELETE (danger)

2. **Always refresh lists after create/update/delete:**
```javascript
   if (!result.error) await getItems();
```

3. **Use dividers between sections:**
```html
   <div class="divider">
       <h3>Next Section</h3>
   </div>
```

4. **Confirmation for deletes:**
```javascript
   if (!confirm(`Delete #${id}?`)) return;
```

## Time to Build: ~10 minutes per resource

Happy testing! 🚀