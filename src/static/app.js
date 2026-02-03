document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to validate Mergington email
  function validateEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@mergington\.edu$/;
    return emailRegex.test(email);
  }

  // Function to show message
  function showMessage(element, message, type) {
    element.textContent = message;
    element.className = type;
    element.classList.remove("hidden");

    // Hide message after 5 seconds
    setTimeout(() => {
      element.classList.add("hidden");
    }, 5000);
  }

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Clear existing options (except the default one)
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        const spotsLeft = details.max_participants - details.participants.length;
        const isFull = spotsLeft === 0;
        
        activityCard.className = `activity-card ${isFull ? "full" : ""}`;

        // Build participants list HTML
        let participantsHTML = '';
        if (details.participants.length > 0) {
          const participantItems = details.participants
            .map(email => `<li>${email}</li>`)
            .join('');
          participantsHTML = `
            <div class="participants-section">
              <strong>👥 Participants:</strong>
              <ul class="participants-list">
                ${participantItems}
              </ul>
            </div>
          `;
        } else {
          participantsHTML = `
            <div class="participants-section">
              <strong>👥 Participants:</strong>
              <p class="no-participants">Be the first to sign up!</p>
            </div>
          `;
        }

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Capacity:</strong> ${details.participants.length}/${details.max_participants} students enrolled</p>
          <p><strong>Status:</strong> <span class="${isFull ? 'status-full' : 'status-available'}">${isFull ? "FULL" : `${spotsLeft} spots left`}</span></p>
          ${participantsHTML}
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown (only if not full)
        const option = document.createElement("option");
        option.value = name;
        option.textContent = isFull ? `${name} (FULL)` : name;
        option.disabled = isFull;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p class='error-message'>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle signup form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const activity = document.getElementById("activity").value;

    // Validate email format
    if (!validateEmail(email)) {
      showMessage(messageDiv, "Please enter a valid @mergington.edu email address", "error");
      return;
    }

    // Confirm signup
    if (!confirm(`Are you sure you want to sign up for ${activity}?`)) {
      return;
    }

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email: email.toLowerCase() }),
        }
      );

      const result = await response.json();

      if (response.ok) {
        showMessage(messageDiv, result.message, "success");
        signupForm.reset();
        // Refresh activities to show updated counts
        await fetchActivities();
      } else {
        showMessage(messageDiv, result.detail || "An error occurred", "error");
      }
    } catch (error) {
      showMessage(messageDiv, "Failed to sign up. Please try again.", "error");
      console.error("Error signing up:", error);
    }
  });

  // Real-time email validation
  const emailInputs = document.querySelectorAll('input[type="email"]');
  emailInputs.forEach((input) => {
    input.addEventListener("blur", () => {
      const email = input.value.trim();
      if (email && !validateEmail(email)) {
        input.setCustomValidity("Must be a @mergington.edu email address");
        input.reportValidity();
      } else {
        input.setCustomValidity("");
      }
    });

    input.addEventListener("input", () => {
      input.setCustomValidity("");
    });
  });

  // Initialize app
  fetchActivities();
});
