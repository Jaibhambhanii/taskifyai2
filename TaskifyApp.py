import sys
import threading
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template_string
import webbrowser
import webview
import tkinter as tk
from tkinterweb import HtmlFrame
API_KEY = "AIzaSyDKJ_SeturlrytQPA65Rfn2zSyzywgqvbg"  # Replace with your actual Gemini API key
genai.configure(api_key=API_KEY)

app = Flask(__name__)
tasks = []  # Global task list to store generated tasks

HTML_PAGE="""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taskify AI </title>
    <link href="https://fonts.googleapis.com/css2?family=Abril+Fatface&display=swap" rel="stylesheet">
    <style>
        :root {
            --pixel-size: 2;
        }
        
        body {
    font-family: 'Abril Fatface', cursive;
    background-color: #000000;
    color: #D5B8FF;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    height: 100vh;
    background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), /* Adding a tint */
                url('https://i.seadn.io/gae/SFh6PsQCIvZgo4__NLybHsV_AHYSJ1LvS8ZK1wyeSgr1C65Ts4q9pM04Xv2dv3a0rWgNiRQlni9DJoqVyku1EloFEsM_0-RpF-n4zQ?auto=format&dpr=1&w=1000') no-repeat center center fixed;
    background-size: cover;
}


        h1 {
            font-size: 28px;
            text-align: center;
            margin: 20px;
            font-weight: bold;
            color: #D5B8FF;
        }

        .main-container {
            display: flex;
            gap: 20px;
            justify-content: center;
            align-items: flex-start;
            flex: 1;
            width: 90%;
        }

        .task-section {
            flex: 3;
            display: flex;
            flex-direction: column;
        }

        .chat-section {
            flex: 2;
            display: flex;
            flex-direction: column;
            background: #1E1E1E;
            border: 2px solid #6A5ACD;
            border-radius: 6px;
            padding: 10px;
        }

        .task-input-container {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            margin-left: 120px;
            margin-top: 65px;
        }

        .task-input-container select, 
        .task-input-container input {
            font-family: 'Abril Fatface', cursive;
            width: 300px; /* Increase width slightly */
            height: 40px; /* Increase height slightly */
            padding: 10px; /* Add more padding for better spacing */
            border: 2px solid #D5B8FF;
            border-radius: 6px;
            background-color: #1E1E1E;
            color: #D5B8FF;
            font-size: 11px; /* Increase font size slightly */
        }
        #taskListContainer { /* Container for task list if applicable */
    margin: 0;
    padding: 0;
    border: none; /* Ensure no extra border */
}


        .task-input-container button {
            width: 50px;
            height: 30px;
            background-color: #6A5ACD;
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            font-size: 11px;
            font-weight: bold;
            cursor: pointer;
        }

        .task-input-container button:hover {
            background-color: #483D8B;
        }
        .task-list {
    display: none; /* Hidden until tasks are added */
    max-height: 350px; /* Optional: Limit height for scrolling */
    overflow-y: auto; /* Add scrolling when necessary */
    background: #1E1E1E; /* Unified background for the task list */
    border-radius: 6px; /* Slight rounding for the edges */
    border: 1px solid #6A5ACD; /* Ensure the border only appears with content */
    padding: 0; /* Remove padding for a seamless look */
    margin: 0; /* Remove margin to avoid extra spacing */
}

.task-item {
    padding: 10px; /* Inner padding for spacing */
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: #D5B8FF; /* Text color */
    transition: background-color 0.3s ease; /* Smooth hover effect */
}

.task-item:hover {
    background: #6A5ACD; /* Highlight color when hovered */
    color: #FFFFFF; /* Change text color on hover */
}

.task-item span {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    flex-grow: 1;
    margin-right: 10px; /* Space between text and delete button */
}

.delete-btn {
    background: none;
    border: none;
    color: #FF5C5C; 
    font-size: 14px;
    cursor: pointer;
    transition: color 0.3s ease; /* Smooth hover effect */
}

.delete-btn:hover {
    color: #FF1C1C; /* Change color on hover */
}

        
/* Style for the scrollbar */
.task-list::-webkit-scrollbar {
    width: 8px; /* Make the scrollbar narrower */
}

.chatbox::-webkit-scrollbar {
    width: 10px; /* Slightly wider scrollbar for chatbot */
}

.chatbox::-webkit-scrollbar-thumb {
    background: #6A5ACD; /* Chatbot thumb color */
}

.chatbox::-webkit-scrollbar-thumb:hover {
    background: #483D8B; /* Chatbot thumb hover color */
}

.chatbox::-webkit-scrollbar-track {
    background: #1E1E1E; /* Chatbot track color */
}


.task-list::-webkit-scrollbar-thumb {
    background: #6A5ACD; /* Scrollbar thumb color */
    border-radius: 10px; /* Rounded scrollbar thumb */
}

.task-list::-webkit-scrollbar-thumb:hover {
    background: #483D8B; /* Darker color on hover */
}

.task-list::-webkit-scrollbar-track {
    background: #1E1E1E; /* Scrollbar track color */
}

.task-item {
    background: #1E1E1E; /* Consistent background color */
    padding: 8px 12px; /* Add padding inside each task item */
    margin-bottom: 6px; /* Add spacing between task items */
    border-radius: 4px; /* Rounded corners */
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 14px; /* Slightly larger font size for readability */
    color: #D5B8FF; /* Matching text color */
}

.task-item:hover {
    background-color: #292929; /* Add hover effect for better interactivity */
    cursor: pointer; /* Indicate interactivity */
}

.task-item input[type="checkbox"] {
    margin-right: 10px; /* Add spacing between the checkbox and text */
}
.main-container {
    margin: 0;
    padding: 0;
}

.task-list,
.task-section,
.chat-section {
    margin: 0;
    padding: 0;
}

div {
    border: none; /* Temporarily disable borders for debugging */
    background-color: transparent; /* Remove unintended background colors */
}

.delete-btn {
    background: none;
    border: none;
    color: #FF5C5C;
    font-size: 16px; /* Slightly larger for better visibility */
    cursor: pointer;
    transition: color 0.3s ease; /* Smooth color transition */
}

.delete-btn:hover {
    color: #FF1C1C; /* Slightly darker on hover */
}

.progress-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px; /* Space between circle and label */
    margin-left: 50px; /* Shift the progress circle to the right */
}


        .progress-circle {
            font-family: 'Abril Fatface', cursive;
            width: 120px;
            height: 120px;
            background: conic-gradient(#6A5ACD 0% 0%, #1E1E1E 0%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            color: #D5B8FF;
            border: 2px solid #D5B8FF;
            margin-bottom: 5px; /* Move the circle slightly up */
            transform: translateY(-10px); /* Fine-tune upward position */
        }
        #progressLabel {
    font-size: 16px;
    color: #D5B8FF;
    text-align: center;
    margin-bottom: 10px;
}
        
       
        .chatbot-container {
            position: relative;
            top: 20px; /* Move the container 20px down */
            width: 70%; /* Adjusted width for better usability */
            max-width: 800px; /* Ensure the chatbot doesn't stretch too far */
            margin-top: 50px auto; /* Center it horizontally */
            background: #1E1E1E; /* Background color */
            padding: 20px; /* Padding for inner spacing */
            border: 2px solid #6A5ACD; /* Theme-matching border */
            border-radius: 10px; /* Smooth corners */
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.5); /* Depth with shadow */
            display: flex;
            flex-direction: column;
            height: 550px; /* Increased height for usability */
            justify-content: space-between; /* Maintain spacing between elements */
        }



        .chat-header {
            font-weight: bold;
            text-align: center;
            margin-bottom: 15px;
            color: #D5B8FF;
            font-size: 24px; /* Slightly larger font size */
        }

        .chatbox {
            flex-grow: 1; /* Allow chatbox to expand dynamically */
            overflow-y: auto;
            padding: 15px;
            background: #2A2A2A; /* Background color for chat messages */
            border-radius: 8px;
            font-size: 14px; /* Larger font size for readability */
            color: #D5B8FF; /* Text color matching the theme */
            border: 1px solid #6A5ACD; /* Border for the chatbox */
            max-height: 350px; /* Allows for a larger chat area */
            min-height: 350px; /* Gives enough space for displaying messages */
        }

        .chatbox p {
            margin: 8px 0; /* Add spacing between messages */
        }

        .user-message {
            color: #FFFFFF;
            text-align: left;
        }

        .bot-message {
            color: #6A5ACD;
            text-align: left;
        }

        .chat-input-container {
            display: flex;
            gap: 15px; /* Increased spacing between the input and button */
            margin-top: 20px; /* Space above the input container */
        }

        .chat-input-container input {
            flex: 1;
            font-family: 'Abril Fatface', cursive;
            padding: 15px; /* Larger padding for a bigger input box */
            border: 1px solid #D5B8FF;
            border-radius: 8px; /* Rounded corners */
            background: #1E1E1E; /* Input background color */
            color: #D5B8FF; /* Input text color */
            font-size: 14px; /* Increased font size */
            box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.3); /* Slightly stronger shadow for depth */
        }

        .chat-input-container input::placeholder {
            color: #A5A5A5; /* Placeholder text color */
        }

        .chat-input-container button {
            background: #6A5ACD; /* Button background color */
            border: none;
            font-family: 'Abril Fatface', cursive;
            padding: 15px 25px; /* Adjusted padding for size */
            color: white; /* Button text color */
            cursor: pointer; /* Pointer cursor for interaction */
            border-radius: 8px; /* Rounded corners */
            font-size: 11x; /* Increased font size */
            box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.3); /* Slightly stronger shadow */
            transition: background-color 0.3s ease; /* Smooth hover transition */
        }

        .chat-input-container button:hover {
            background: #483D8B; /* Darker shade for hover effect */
        }
        /* Positioning and Styling the Productivity Timer Button */
        

    </style>
</head>
<body>
    <h1>Taskify AI : Bring your ideas to life</h1>

    <div class="main-container">
        <div class="task-section">
            <div class="task-input-container" id="inputContainer">
                <input type="text" id="taskInput" placeholder="Describe your idea or task" />
                <button onclick="addTask()">+</button>
                <button onclick="generateTasks()">GEN</button>
            </div>
    
            <ul class="task-list" id="taskList"></ul>
        </div>
        
        <div class="chat-section">
            <div class="chat-header">Taskify AI Chatbot</div>
            <div class="chatbox" id="chatbox">
                <p class="bot-message">Hi! I can help you with tasks</p>
            </div>
            <div class="chat-input-container">
                <input type="text" id="chatInput" placeholder="Ask Taskify..." />
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>
    
    <!-- Progress Circle Container -->
<div class="progress-container" id="progressContainer">
    <div class="progress-circle" id="progressCircle">
        <span id="progressPercent">0%</span>
    </div>
    <!-- Label for the circle -->
    <div id="progressLabel">Progress Bar</div>
</div>




    <script>
        let tasks = [];
        
        // Add a new task
        function addTask() {
            const taskInput = document.getElementById("taskInput");

            if (!taskInput || !taskInput.value.trim()) return;

            const newTask = {
                text: taskInput.value.trim(),
                completed: false
            };

            tasks.push(newTask);
            taskInput.value = ""; // Clear the input box
            renderTasks(); // Update task list UI
            updateProgress(); // Update progress bar
        }

        // Generate tasks via API (Flask)
        function generateTasks() {
            const taskInput = document.getElementById("taskInput");
            const description = taskInput ? taskInput.value.trim() : "";

            if (!description) {
                alert("Please enter a task or idea description.");
                return;
            }

            fetch("http://127.0.0.1:5000/generate-tasks", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ description: description })
            })
                .then(response => response.json())
                .then(data => {
                    // Directly handle tasks without checking for an error key
                    if (Array.isArray(data.tasks)) {
                        tasks = data.tasks.map(task => ({
                            text: task.text || task, // Handle both string or object tasks
                            completed: task.completed || false
                        }));
                        renderTasks();
                        updateProgress();

                        // Clear input field after generating tasks
                        document.getElementById("taskInput").value = "";
                    } else {
                        console.warn("Unexpected tasks format received:", data.tasks);
                        alert("Unexpected data format received from server.");
                    }
                })

        }

        // Render tasks dynamically
        function renderTasks() {
            const taskList = document.getElementById("taskList");
            taskList.innerHTML = ""; // Clear the existing task list

            tasks.forEach((task, index) => {
                const li = document.createElement("li");
                li.className = "task-item";
                li.innerHTML = `
                    <input type="checkbox" ${task.completed ? "checked" : ""} onclick="toggleTask(${index})">
                    <span>${task.text}</span>
                    <button class="delete-btn" onclick="deleteTask(${index})">🗑</button>
                `;
                taskList.appendChild(li);
            });

            taskList.style.display = tasks.length > 0 ? "block" : "none"; // Show task list only if there are tasks
        }

        // Toggle completion status of a task
        function toggleTask(index) {
            tasks[index].completed = !tasks[index].completed;
            renderTasks();
            updateProgress();
        }

        // Delete a task
        function deleteTask(index) {
            tasks.splice(index, 1);
            renderTasks();
            updateProgress();
        }

        // Update progress bar based on task completion
        function updateProgress() {
            const completedTasks = tasks.filter(task => task.completed).length;
            const totalTasks = tasks.length;
            const percent = totalTasks === 0 ? 0 : Math.round((completedTasks / totalTasks) * 100);

            document.getElementById("progressPercent").textContent = `${percent}%`;
            document.getElementById("progressCircle").style.background = `conic-gradient(#6A5ACD ${percent}%, #1E1E1E ${percent}%)`;

            document.getElementById("congratsMessage").style.display = percent === 100 ? "block" : "none";
        }

        function sendMessage() {
    const input = document.getElementById("chatInput").value.trim();
    const chatbox = document.getElementById("chatbox");

    if (!input) return;

    chatbox.innerHTML += `<p class="user-message">👤 ${input}</p>`;
    document.getElementById("chatInput").value = "";

    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                chatbox.innerHTML += `<p class="bot-message">❌ ${data.error}</p>`;
            } else {
                chatbox.innerHTML += `<p class="bot-message">🤖 ${data.response}</p>`;

                // Ensure that the manually added tasks are preserved
                if (Array.isArray(data.tasks)) {
                    // Merge existing tasks with new tasks (preserve old ones)
                    data.tasks.forEach(task => {
                        if (!tasks.some(existingTask => existingTask.text === task.text)) {
                            tasks.push(task); // Add only new tasks
                        }
                    });
                    renderTasks();
                    updateProgress();
                }
            }
        })

    chatbox.scrollTop = chatbox.scrollHeight;
}




    </script>

        
</body>
</html>
"""
@app.route("/")
def index():
    """Serve the main HTML page."""
    return render_template_string(HTML_PAGE)

@app.route("/generate-tasks", methods=["POST"])
def generate_tasks():
    """Generate tasks based on user input."""
    try:
        data = request.json
        project_description = data.get("description", "").strip()

        # Ensure that description is provided
        if not project_description:
            return jsonify({"error": "Missing description"}), 400

        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"Generate up to 10 concise tasks for the request that the person gave which is '{project_description}'. "
            "Keep tasks simple, clear, and free of special formatting like **bold text** or symbols."
        )

        response = model.generate_content(prompt)

        # Split and filter out empty tasks from the response
        global tasks
        tasks = [{"text": task.strip(), "completed": False} for task in response.text.split("\n") if task.strip()]

        # Ensure tasks are generated before returning
        if not tasks:
            return jsonify({"error": "No tasks were generated. Try again."}), 500

        return jsonify({"tasks": tasks})

    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chatbot interactions."""
    try:
        data = request.json
        user_input = data.get("message", "").strip()

        if not user_input:
            return jsonify({"error": "Message is required"}), 400

        global tasks
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = (
            f"Respond to the user's query concisely and clearly. "
            f"Here is the current list of tasks:\n{[task['text'] for task in tasks]}. "
            "Provide guidance regardless of whether it is relevant to the tasks or not. "
            "If there are multiple ideas, present them as a numbered list without using any special formatting like **bold text** or * symbols."
        )

        response = model.generate_content(f"{prompt}\n\nUser Input: {user_input}")
        clean_response = response.text.replace("**", "").strip()

        clean_response = clean_response[:500] + "..." if len(clean_response) > 500 else clean_response

        return jsonify({"response": clean_response, "tasks": tasks})

    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": f"Internal error: {str(e)}"}), 500

def run_flask():
    """Run the Flask app."""
    app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
    # Run the app on localhost (default: http://127.0.0.1:5000)
    app.run(debug=True, host="127.0.0.1", port=5000)