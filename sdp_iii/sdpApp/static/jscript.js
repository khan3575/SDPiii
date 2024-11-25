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

    // Form Validation
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

    // Handle Like Button Click
    document.querySelectorAll(".like-button").forEach((button) => {
        button.addEventListener("click", async () => {
            const blogId = button.getAttribute("data-blog-id");
            const response = await fetch(`/like_blog/${blogId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                },
            });

            if (response.ok) {
                const data = await response.json();
                button.textContent = `Like (${data.like_count})`;
            } else {
                alert("Error liking the blog.");
            }
        });
    });

    // Handle Comment Button Click
    document.querySelectorAll(".comment-button").forEach((button) => {
        button.addEventListener("click", async () => {
            const blogId = button.getAttribute("data-blog-id");
            const response = await fetch(`/get_comments/${blogId}/`);
            const popup = document.getElementById("comment-popup");
            const popupComments = document.getElementById("popup-comments");

            if (response.ok) {
                const comments = await response.json();
                popupComments.innerHTML = comments
                    .map((comment) => `<p><strong>${comment.user_id__first_name}:</strong> ${comment.comments}</p>`)
                    .join("");
                popup.classList.remove("hidden");
            } else {
                alert("Error loading comments.");
            }
        });
    });

    // Close Comment Popup
    const closePopup = document.getElementById("close-popup");
    closePopup.addEventListener("click", () => {
        document.getElementById("comment-popup").classList.add("hidden");
    });

    // Infinite Scroll for Blog Feed
    const feed = document.querySelector(".blog-feed");

    async function fetchMoreBlogs() {
        const response = await fetch("/load_more_blogs/");
        if (response.ok) {
            const newBlogs = await response.json();
            newBlogs.forEach((blog) => {
                const newBlog = document.createElement("div");
                newBlog.classList.add("blog-card");
                newBlog.innerHTML = `
                    <div class="blog-header">
                        <h3>${blog.blog_title}</h3>
                        <p>by ${blog.user.first_name} ${blog.user.last_name} on ${blog.date}</p>
                    </div>
                    <div class="blog-content">
                        <p>${blog.text}</p>
                    </div>
                    <div class="blog-actions">
                        <button class="like-button" data-blog-id="${blog.blog_id}">Like (${blog.like_count})</button>
                        <button class="comment-button" data-blog-id="${blog.blog_id}">Comments (${blog.comment_count})</button>
                    </div>
                `;
                feed.appendChild(newBlog);
            });
        } else {
            console.error("Failed to load more blogs.");
        }
    }

    window.addEventListener("scroll", function () {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
            fetchMoreBlogs();
        }
    });
});
