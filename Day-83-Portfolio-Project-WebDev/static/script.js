// Function to display projects based on the selected topic
async function displayProjects(topic) {
    const projectContainer = document.getElementById("projects-display");
    projectContainer.innerHTML = ""; // Clear previous projects

        try {
            const response = await fetch(`/api/projects/${topic}`)
            if (!response.ok) {
                throw new Error("Failed to fetch projects");
            }

            const projects = await response.json()

            // Loop through the projects and add them to the page
            projects.forEach(project => {
            const projectCard = document.createElement("div");
            projectCard.classList.add("project-card");
            projectCard.innerHTML = `
                <img src="${project.image}" alt="${project.title}">
                <div class = "project-card-description-bg">
                <div class = "project-card-description">
                <h3>${project.title}</h3>
                <p>${project.description}</p>
                <a href="${project.github}" target="_blank">View on GitHub</a>
                </div>
                </div>
            `;
            projectContainer.appendChild(projectCard);
        });
    } catch (error) {
        console.error(error);
        projectContainer.innerHTML = `<p>Failed to load projects. Please try again later.</p>`;
    }
}

// Add event listeners to the topic buttons
document.querySelectorAll(".topic-button").forEach(button => {
    button.addEventListener("click", () => {
        const topic = button.getAttribute("data-topic");
        displayProjects(topic);
    });
});
// Display the first topic's projects by default
displayProjects("web");


let previousScrollPosition = window.scrollY; 
const navbar = document.getElementById("navbar");

window.addEventListener("scroll", () => {
    const currentScrollPosition = window.scrollY; 

    if (currentScrollPosition > previousScrollPosition) {
        navbar.style.top = "-60px"; 
    } else {
        navbar.style.top = "0"; 
    }

    previousScrollPosition = currentScrollPosition;
});