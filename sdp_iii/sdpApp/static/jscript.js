// DOM Loaded Event
document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded");

    // Example: Toggle Navigation Menu (if added in future)
    const menuToggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");

    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", function () {
            navLinks.classList.toggle("active");
        });
    }

    // Example: Form Validation
    const forms = document.querySelectorAll("form");
    forms.forEach((form) => {
        form.addEventListener("submit", function (event) {
            const inputs = form.querySelectorAll("input[required]");
            let isValid = true;

            inputs.forEach((input) => {
                if (!input.value) {
                    isValid = false;
                    alert(`Please fill out the ${input.name} field.`);
                }
            });

            if (!isValid) {
                event.preventDefault();
            }
        });
    });
});
document.addEventListener("DOMContentLoaded", function () {
    const feed = document.querySelector(".blog-feed");

    // Mock function to fetch more blogs (replace with real API later)
    function fetchMoreBlogs() {
        const newBlog = document.createElement("div");
        newBlog.classList.add("blog-card");
        newBlog.innerHTML = `
            <div class="blog-header">
                <h3>Sample Blog Title</h3>
                <p>by Sample User on 2024-01-01</p>
            </div>
            <div class="blog-content">
                <p>This is a dynamically loaded blog post.</p>
            </div>
            <div class="blog-actions">
                <button>Like</button>
                <button>Comment</button>
                <button>Share</button>
            </div>
        `;
        feed.appendChild(newBlog);
    }

    // Infinite scroll event listener
    window.addEventListener("scroll", function () {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
            fetchMoreBlogs();
        }
    });
});
