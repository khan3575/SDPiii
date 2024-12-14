// DOM Loaded Event
document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded");

    // Attach all functionality
    attachMenuToggle();
    attachFormValidation();
    attachLikeButtonHandler();
    attachCommentButtonHandler();
    attachInfiniteScroll();
    attachForgotPasswordHandler();
});

// Function to handle menu toggle
function attachMenuToggle() {
    const menuToggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");

    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", function () {
            navLinks.classList.toggle("active");
        });
    }
}

// Function to validate forms
function attachFormValidation() {
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
}

// Function to handle Like Button Click
function attachLikeButtonHandler() {
    document.querySelectorAll(".like-button").forEach((button) => {
        button.addEventListener("click", async () => {
            const blogId = button.getAttribute("data-blog-id");
            const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            if (!blogId) {
                console.error("Blog ID is missing on like button.");
                return;
            }

            try {
                const response = await fetch(`/like_blog/${blogId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    button.textContent = `Like (${data.like_count})`;

                    // Toggle the liked class
                    if (data.liked) {
                        button.classList.add("liked");
                    } else {
                        button.classList.remove("liked");
                    }
                } else {
                    alert("An error occurred while liking the blog.");
                }
            } catch (error) {
                console.error("Error liking the blog:", error);
            }
        });
    });
}

// Function to handle Comment Button Click
function attachCommentButtonHandler() {
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
}

// Function to handle infinite scroll
function attachInfiniteScroll() {
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

            // Rebind event listeners for dynamically added buttons
            attachLikeButtonHandler();
        } else {
            console.error("Failed to load more blogs.");
        }
    }

    window.addEventListener("scroll", function () {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
            fetchMoreBlogs();
        }
    });
}

// Function to handle forgot password
function attachForgotPasswordHandler() {
    const forgotPasswordForm = document.getElementById("forgot-password-form");
    const forgotPasswordMessage = document.getElementById("response-message");

    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const formData = new FormData(forgotPasswordForm);

            try {
                const response = await fetch(forgotPasswordForm.action, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                    },
                    body: formData,
                });

                const data = await response.json();

                // Display response message
                forgotPasswordMessage.classList.remove("hidden");
                if (data.status === "success") {
                    forgotPasswordMessage.textContent = data.message;
                    forgotPasswordMessage.style.color = "green";
                } else {
                    forgotPasswordMessage.textContent = data.message;
                    forgotPasswordMessage.style.color = "red";
                }
            } catch (error) {
                console.error("Error submitting forgot password form:", error);
                forgotPasswordMessage.classList.remove("hidden");
                forgotPasswordMessage.textContent = "An error occurred. Please try again.";
                forgotPasswordMessage.style.color = "red";
            }
        });
    }
}
