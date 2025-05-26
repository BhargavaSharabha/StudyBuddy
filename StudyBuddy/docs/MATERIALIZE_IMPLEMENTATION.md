# Materialize CSS Implementation Guide

## Overview

StudyBuddy uses Materialize CSS 1.0.0 as its primary UI framework, providing a modern Material Design interface. This document details how Materialize has been implemented, customized, and extended throughout the application.

## CDN Integration

### Core Dependencies
```html
<!-- Materialize CSS -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">

<!-- Material Icons -->
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

<!-- Google Fonts - Poppins -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<!-- Materialize JavaScript -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
```

### JavaScript Initialization
```html
<script>
document.addEventListener('DOMContentLoaded', function() {
  // Auto-initialize all Materialize components
  M.AutoInit();
  
  // Manual initialization for specific components
  var selectElems = document.querySelectorAll('select');
  M.FormSelect.init(selectElems);
  
  var sidenavElems = document.querySelectorAll('.sidenav');
  M.Sidenav.init(sidenavElems);
  
  var datepickerElems = document.querySelectorAll('.datepicker');
  M.Datepicker.init(datepickerElems, {
    format: 'mm/dd/yyyy',
    autoClose: true
  });
  
  var timepickerElems = document.querySelectorAll('.timepicker');
  M.Timepicker.init(timepickerElems, {
    twelveHour: true,
    autoClose: true
  });
});
</script>
```

---

## Color Scheme and Theming

### Primary Color Palette
```css
:root {
  --primary-color: #009688;      /* Teal */
  --primary-dark: #00796B;       /* Teal Darken-2 */
  --primary-light: #4DB6AC;      /* Teal Lighten-2 */
  --background-color: #f5f5f5;   /* Grey Lighten-4 */
  --text-primary: #212121;       /* Grey Darken-4 */
  --text-secondary: #757575;     /* Grey Darken-1 */
}
```

### Custom Button Styling
```css
.btn, .btn-large {
  background-color: var(--primary-color);
  border-radius: 4px;
  font-weight: 500;
  text-transform: none;
}

.btn:hover, .btn-large:hover {
  background-color: var(--primary-dark);
}

.btn:focus {
  background-color: var(--primary-dark);
  outline: 2px solid white;
  outline-offset: 2px;
}

/* Secondary button variant */
.btn-secondary {
  background-color: #757575;
  color: white;
}

.btn-secondary:hover {
  background-color: #424242;
}
```

### Typography Customization
```css
body {
  font-family: 'Poppins', sans-serif;
  display: flex;
  min-height: 100vh;
  flex-direction: column;
  background-color: var(--background-color);
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
}

.page-title {
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--primary-color);
  font-size: 2.5rem;
}

.card-title {
  font-weight: 600;
  color: var(--primary-color);
  font-size: 1.3rem;
}
```

---

## Navigation Implementation

### Fixed Navigation Bar
```html
<header>
  <div class="navbar-fixed">
    <nav class="teal darken-1" role="navigation" aria-label="Main navigation">
      <div class="nav-wrapper container">
        <a href="{% url 'dashboard' %}" class="brand-logo">Study Buddy</a>
        
        <!-- Desktop Navigation -->
        <ul class="right hide-on-med-and-down">
          <li><a href="{% url 'dashboard' %}">Find Groups</a></li>
          <li><a href="{% url 'create_group' %}">Create Group</a></li>
          <li><a href="{% url 'profile' %}">My Profile</a></li>
          <li><a href="{% url 'logout' %}">Logout</a></li>
        </ul>
        
        <!-- Mobile Navigation Trigger -->
        <a href="#" data-target="mobile-nav" class="sidenav-trigger">
          <i class="material-icons">menu</i>
        </a>
      </div>
    </nav>
  </div>
</header>

<!-- Mobile Side Navigation -->
<ul id="mobile-nav" class="sidenav">
  <li><a href="{% url 'dashboard' %}">Find Groups</a></li>
  <li><a href="{% url 'create_group' %}">Create Group</a></li>
  <li><a href="{% url 'profile' %}">My Profile</a></li>
  <li><a href="{% url 'logout' %}">Logout</a></li>
</ul>
```

### Navigation Styling
```css
nav .brand-logo {
  font-weight: 600;
  font-size: 1.8rem;
}

.sidenav {
  width: 280px;
}

.sidenav li > a {
  font-weight: 500;
  padding: 0 32px;
  height: 64px;
  line-height: 64px;
}

.sidenav li > a:hover {
  background-color: rgba(0, 0, 0, 0.05);
}
```

---

## Grid System Usage

### Container and Row Structure
```html
<div class="container">
  <div class="row">
    <div class="col s12 m6 l4">
      <!-- Content for small (12/12), medium (6/12), large (4/12) -->
    </div>
    <div class="col s12 m6 l8">
      <!-- Content for small (12/12), medium (6/12), large (8/12) -->
    </div>
  </div>
</div>
```

### Responsive Breakpoints
- **Small (s)**: 0-600px (Mobile)
- **Medium (m)**: 601-992px (Tablet)
- **Large (l)**: 993-1200px (Desktop)
- **Extra Large (xl)**: 1201px+ (Large Desktop)

### Grid Examples in StudyBuddy
```html
<!-- Dashboard Filter Section -->
<div class="row">
  <div class="input-field col s12 m5">
    <select name="subject">
      <!-- Subject options -->
    </select>
    <label>Filter by Subject</label>
  </div>
  
  <div class="input-field col s12 m5">
    <input type="text" name="search" placeholder="Search by title...">
    <label>Search</label>
  </div>
  
  <div class="col s12 m2">
    <button type="submit" class="btn waves-effect waves-light">
      <i class="material-icons left">search</i>
      Filter
    </button>
  </div>
</div>
```

---

## Card Components

### Basic Card Structure
```html
<div class="card hoverable">
  <div class="card-content">
    <span class="card-title">Card Title</span>
    <p>Card content goes here with description and details.</p>
  </div>
  <div class="card-action">
    <a href="#" class="btn">Primary Action</a>
    <a href="#" class="btn-flat">Secondary Action</a>
  </div>
</div>
```

### Study Group Card Implementation
```html
<div class="card group-card hoverable">
  <div class="card-content">
    <span class="card-title">{{ group.title }}</span>
    <p class="group-description">{{ group.description|truncatewords:20 }}</p>
    
    <div class="group-details">
      <div class="group-detail">
        <i class="material-icons tiny">subject</i>
        <span>{{ group.subject.name }}</span>
      </div>
      
      <div class="group-detail">
        <i class="material-icons tiny">person</i>
        <span>Host: {{ group.host.username }}</span>
      </div>
      
      <div class="group-detail">
        <i class="material-icons tiny">event</i>
        <span>{{ group.meeting_date|date:"M d, Y" }} at {{ group.meeting_time|time:"g:i A" }}</span>
      </div>
      
      <div class="group-detail">
        <i class="material-icons tiny">location_on</i>
        <span>{{ group.meeting_location|default:"Location TBD" }}</span>
      </div>
      
      <div class="group-detail">
        <i class="material-icons tiny">group</i>
        <span>{{ group.current_member_count }}/{{ group.max_members }} members</span>
      </div>
    </div>
  </div>
  
  <div class="card-action">
    <a href="{% url 'group_details' group.id %}" class="btn">View Details</a>
    
    {% if group.id in user_pending_requests %}
      <span class="btn disabled">Pending Request</span>
    {% elif user in group.members.all %}
      <span class="btn disabled">Already Joined</span>
    {% elif group.is_full %}
      <span class="btn disabled">Group Full</span>
    {% else %}
      <a href="{% url 'join_group' group.id %}" class="btn">Join Group</a>
    {% endif %}
  </div>
</div>
```

### Custom Card Styling
```css
.group-card {
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.group-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

.group-card .card-content {
  padding: 20px;
}

.group-description {
  margin-bottom: 15px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.group-detail {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.group-detail i {
  margin-right: 8px;
  color: var(--text-secondary);
  font-size: 1rem;
}

.group-card .card-action {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-top: 1px solid #eeeeee;
}
```

---

## Form Components

### Input Fields
```html
<div class="input-field">
  <input id="group_title" type="text" name="group_title" required>
  <label for="group_title">Group Title</label>
  <span class="helper-text" data-error="Please enter a group title" data-success="Good">
    Enter a descriptive title for your study group
  </span>
</div>

<div class="input-field">
  <textarea id="description" name="description" class="materialize-textarea" required></textarea>
  <label for="description">Description</label>
  <span class="helper-text">
    Describe the purpose and goals of your study group
  </span>
</div>
```

### Select Dropdowns
```html
<div class="input-field">
  <select name="subject" required>
    <option value="" disabled selected>Choose a subject</option>
    {% for subject in subjects %}
      <option value="{{ subject.id }}">{{ subject.name }}</option>
    {% endfor %}
  </select>
  <label>Subject</label>
</div>
```

### Date and Time Pickers
```html
<div class="input-field">
  <input type="text" name="meeting_date" class="datepicker" required>
  <label for="meeting_date">Meeting Date</label>
</div>

<div class="input-field">
  <input type="text" name="meeting_time" class="timepicker" required>
  <label for="meeting_time">Meeting Time</label>
</div>
```

### Form Validation Styling
```css
.input-field input[type=text]:focus + label,
.input-field input[type=email]:focus + label,
.input-field input[type=password]:focus + label,
.input-field textarea:focus + label {
  color: var(--primary-color);
}

.input-field input[type=text]:focus,
.input-field input[type=email]:focus,
.input-field input[type=password]:focus,
.input-field textarea:focus {
  border-bottom: 1px solid var(--primary-color);
  box-shadow: 0 1px 0 0 var(--primary-color);
}

.input-field .helper-text {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.input-field input.valid {
  border-bottom: 1px solid #4CAF50;
  box-shadow: 0 1px 0 0 #4CAF50;
}

.input-field input.invalid {
  border-bottom: 1px solid #F44336;
  box-shadow: 0 1px 0 0 #F44336;
}
```

---

## Modal Implementation

### Basic Modal Structure
```html
<!-- Modal Trigger -->
<a class="btn modal-trigger" href="#confirm-modal">Delete Group</a>

<!-- Modal Structure -->
<div id="confirm-modal" class="modal">
  <div class="modal-content">
    <h4>Confirm Action</h4>
    <p>Are you sure you want to delete this study group? This action cannot be undone.</p>
  </div>
  <div class="modal-footer">
    <a href="#!" class="modal-close waves-effect waves-green btn-flat">Cancel</a>
    <a href="#!" class="waves-effect waves-red btn red">Delete</a>
  </div>
</div>
```

### Modal Initialization
```javascript
document.addEventListener('DOMContentLoaded', function() {
  var modalElems = document.querySelectorAll('.modal');
  M.Modal.init(modalElems, {
    dismissible: true,
    opacity: 0.5,
    inDuration: 300,
    outDuration: 200
  });
});
```

---

## Collections and Lists

### Basic Collection
```html
<ul class="collection">
  <li class="collection-item">
    <div>
      Group Member Name
      <a href="#!" class="secondary-content">
        <i class="material-icons">send</i>
      </a>
    </div>
  </li>
</ul>
```

### Group Members List
```html
<ul class="collection with-header">
  <li class="collection-header">
    <h5>Group Members ({{ group.current_member_count }})</h5>
  </li>
  
  {% for membership in group.groupmembership_set.all %}
    <li class="collection-item avatar">
      <i class="material-icons circle teal">person</i>
      <span class="title">{{ membership.user.username }}</span>
      <p>
        {% if membership.user == group.host %}
          <span class="badge teal white-text">Host</span>
        {% endif %}
        <br>Joined: {{ membership.date_joined|date:"M d, Y" }}
      </p>
    </li>
  {% endfor %}
</ul>
```

---

## Floating Action Button

### Implementation
```html
<div class="fixed-action-btn">
  <a class="btn-floating btn-large teal pulse" href="{% url 'create_group' %}">
    <i class="large material-icons">add</i>
  </a>
</div>
```

### Styling
```css
.fixed-action-btn {
  bottom: 30px;
  right: 30px;
}

.btn-floating.btn-large {
  width: 56px;
  height: 56px;
  background-color: var(--primary-color);
}

.btn-floating.btn-large:hover {
  background-color: var(--primary-dark);
}

.btn-floating.pulse {
  animation: pulse 2s infinite;
}
```

---

## Toast Notifications

### Django Messages Integration
```html
{% if messages %}
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      {% for message in messages %}
        M.toast({
          html: '{{ message|escapejs }}',
          classes: '{% if message.tags == "error" %}red{% elif message.tags == "success" %}green{% elif message.tags == "warning" %}orange{% else %}blue{% endif %}',
          displayLength: 4000
        });
      {% endfor %}
    });
  </script>
{% endif %}
```

### Custom Toast Styling
```css
.toast {
  border-radius: 4px;
  font-weight: 500;
}

.toast.red {
  background-color: #F44336;
}

.toast.green {
  background-color: #4CAF50;
}

.toast.orange {
  background-color: #FF9800;
}

.toast.blue {
  background-color: #2196F3;
}
```

---

## Responsive Design

### Mobile-First Approach
```css
/* Base styles for mobile */
.hero h1 {
  font-size: 2rem;
  text-align: center;
}

.filter-bar {
  padding: 15px;
  text-align: center;
}

/* Tablet styles */
@media only screen and (min-width: 601px) {
  .hero h1 {
    font-size: 2.5rem;
  }
  
  .filter-bar {
    text-align: left;
  }
}

/* Desktop styles */
@media only screen and (min-width: 993px) {
  .hero h1 {
    font-size: 3rem;
    text-align: left;
  }
  
  .dashboard-hero {
    text-align: left;
  }
}
```

### Hide/Show Classes
```html
<!-- Hide on mobile, show on tablet and up -->
<div class="hide-on-small-only">
  <p>This content is hidden on mobile devices</p>
</div>

<!-- Show only on mobile -->
<div class="hide-on-med-and-up">
  <p>This content only shows on mobile</p>
</div>

<!-- Hide on tablet, show on mobile and desktop -->
<div class="hide-on-med-only">
  <p>This content is hidden on tablets</p>
</div>
```

---

## Accessibility Features

### ARIA Labels and Roles
```html
<nav class="teal darken-1" role="navigation" aria-label="Main navigation">
  <div class="nav-wrapper container">
    <a href="#" class="brand-logo" aria-label="StudyBuddy Home">Study Buddy</a>
    
    <a href="#" data-target="mobile-nav" class="sidenav-trigger" aria-label="Open navigation menu">
      <i class="material-icons">menu</i>
    </a>
  </div>
</nav>
```

### Skip Links
```html
<a href="#main-content" class="skip-link">Skip to main content</a>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--primary-color);
  color: white;
  padding: 8px;
  z-index: 1000;
  text-decoration: none;
}

.skip-link:focus {
  top: 0;
}
</style>
```

### Focus Indicators
```css
a:focus, button:focus, .btn:focus {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

.btn:focus {
  background-color: var(--primary-dark);
}

input:focus, textarea:focus, select:focus {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}
```

---

## Custom Components

### Status Badges
```html
<span class="badge-status {% if group.is_full %}full{% elif user in group.members.all %}joined{% elif group.id in user_pending_requests %}pending{% else %}available{% endif %}">
  {% if group.is_full %}
    Full
  {% elif user in group.members.all %}
    Joined
  {% elif group.id in user_pending_requests %}
    Pending
  {% else %}
    Available
  {% endif %}
</span>
```

```css
.badge-status {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-status.available {
  background-color: #4CAF50;
  color: white;
}

.badge-status.pending {
  background-color: #FF9800;
  color: white;
}

.badge-status.joined {
  background-color: #2196F3;
  color: white;
}

.badge-status.full {
  background-color: #F44336;
  color: white;
}
```

### Loading Spinners
```html
<div class="loading-spinner">
  <div class="preloader-wrapper small active">
    <div class="spinner-layer spinner-teal-only">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="gap-patch">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>
  </div>
</div>
```

---

## Performance Optimizations

### CSS Optimization
```css
/* Use transform for animations instead of changing layout properties */
.group-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  will-change: transform;
}

.group-card:hover {
  transform: translateY(-5px);
}

/* Optimize repaints */
.btn {
  backface-visibility: hidden;
  transform: translateZ(0);
}
```

### JavaScript Optimization
```javascript
// Debounce search input
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Apply debouncing to search
const searchInput = document.querySelector('#search');
if (searchInput) {
  searchInput.addEventListener('input', debounce(function(e) {
    // Perform search
  }, 300));
}
```

---

## Browser Compatibility

### Supported Features
- **CSS Grid**: Used for complex layouts
- **Flexbox**: Used extensively for component layouts
- **CSS Custom Properties**: Used for theming
- **ES6+ JavaScript**: Used for modern syntax

### Fallbacks
```css
/* Flexbox fallback for older browsers */
.row {
  display: -webkit-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display: flex;
}

/* Grid fallback */
.grid-container {
  display: grid;
  display: -ms-grid; /* IE 10-11 */
}
```

### Polyfills
```html
<!-- For older browsers -->
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6,Array.prototype.includes,CustomEvent,Element.prototype.closest"></script>
```

---

## Testing and Debugging

### CSS Testing
```css
/* Debug mode - shows element boundaries */
.debug * {
  outline: 1px solid red;
}

.debug .container {
  outline-color: blue;
}

.debug .row {
  outline-color: green;
}

.debug [class*="col"] {
  outline-color: orange;
}
```

### JavaScript Console Debugging
```javascript
// Check if Materialize is loaded
if (typeof M !== 'undefined') {
  console.log('Materialize loaded successfully');
  console.log('Version:', M.version);
} else {
  console.error('Materialize not loaded');
}

// Debug component initialization
document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM loaded, initializing components...');
  
  var selectElems = document.querySelectorAll('select');
  console.log('Found', selectElems.length, 'select elements');
  
  M.FormSelect.init(selectElems);
  console.log('FormSelect initialized');
});
```

---

## Best Practices

### Component Organization
1. **Consistent Naming**: Use descriptive class names
2. **Modular CSS**: Organize styles by component
3. **Responsive Design**: Mobile-first approach
4. **Accessibility**: Include ARIA labels and focus indicators
5. **Performance**: Optimize animations and transitions

### Code Maintenance
1. **Documentation**: Comment complex CSS rules
2. **Version Control**: Track Materialize version updates
3. **Testing**: Test across different devices and browsers
4. **Optimization**: Minimize CSS and JavaScript in production

### Future Considerations
1. **Component Library**: Consider creating reusable components
2. **Design System**: Establish consistent design tokens
3. **Performance Monitoring**: Track Core Web Vitals
4. **Accessibility Audits**: Regular accessibility testing

---

*Last updated: [Current Date]*
*Version: 1.0* 