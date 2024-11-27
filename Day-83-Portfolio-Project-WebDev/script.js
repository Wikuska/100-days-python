const projects = {
    web: [ 
        {
            title: "Blog Website",
            description: "Simple and functional blog website. Users can register, log in and leave comments. Admin can also add and delete posts.",
            image: "images/blog.JPG",
            github: "https://github.com/Wikuska/100-days-python/tree/main/Day-69-Blog-Project-Part-4",
        },
        {
            title: "Coffee&Wifi",
            description: "Website that collects information about cafes and amenities available there for working on electronic devices.",
            image: "images/coffeewifi.JPG",
            github: "https://github.com/Wikuska/100-days-python/tree/main/Day-62-Coffe%26Wifi-Page",
        },
        {
            title: "My Top Movies Website",
            description: "Website collecting my Top 10 movies with ratings. It is possible to add new movies using the API and manage existing ones.",
            image: "images/topmovies.JPG",
            github: "https://github.com/Wikuska/100-days-python/tree/main/Day-64-My-Top-Movies-Website",
        }
    ],
    data: [
        {
            title: "Stock Alert",
            description: "A program that monitors a designated share on the market. In the event of a significant drop or increase in its price, it sends an email notification.",
            image: "images/stockalert.JPG",
            github: "https://github.com/Wikuska",
        },
        {
            title: "Flight Deals Finder",
            description: "A program that look through flight connection between oririn city and locations typed in google sheets file in next 6 months. If any connection price is lower than goal price in file, an email notification is sent.",
            image: "images/flightdeals.jpg",
            github: "https://github.com/Wikuska",
        }
    ],
    game: [
        {
            title: "Snake Game",
            description: "Simple snake game made with Turtle module in python. Monitors game score, saves high score value for future games.",
            image: "images/snake.JPG",
            github: "https://github.com/Wikuska",
        },
        {
            title: "Turtle Races",
            description: "Game where colorful turtles race to finish line. User can try to guess which colour will be the first before game starts.",
            image: "images/races.JPG",
            github: "https://github.com/Wikuska",
        },
        {
            title: "Road Crossing",
            description: "Game where users job is to move turtle to other side of road without being hit by a car. Every level cars speed goeas up, when turtle is hit game is over.",
            image: "images/roadcrossing.jpg",
            github: "https://github.com/Wikuska",
        },
        {
            title: "Quizz Game",
            description: "Quizz game with simple UI, questions are collected from Open Trivia Database, their number and category can be changed.",
            image: "images/quizz.jpg",
            github: "https://github.com/Wikuska",
        }
    ]
}

// Function to display projects based on the selected topic
function displayProjects(topic) {
    const projectContainer = document.getElementById("projects-display");
    projectContainer.innerHTML = ""; // Clear previous projects

    // Get the relevant projects based on the topic
    const topicProjects = projects[topic];

    // Loop through the projects and add them to the page
    topicProjects.forEach(project => {
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