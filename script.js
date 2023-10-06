document.addEventListener("DOMContentLoaded", function () {
    const sectionDropdown = document.getElementById("sectionDropdown");
    const lightControls = document.getElementById("lightControls");

    // Map of section names to lights (replace with your data)
    const sectionToLights = {
        "section1": ["light1", "light2"],
        "section2": ["light3", "light4"],
        "section3": ["light5", "light6"],
    };

    // Function to create light controls
    function createLightControls(lights) {
        lightControls.innerHTML = ""; // Clear previous controls
        lights.forEach((light) => {
            const lightControl = document.createElement("div");
            lightControl.classList.add("light-control");

            const lightName = document.createElement("h3");
            lightName.textContent = `Light: ${light}`;

            const onOffSwitch = document.createElement("label");
            onOffSwitch.textContent = "On/Off";
            const onOffSlider = document.createElement("input");
            onOffSlider.type = "range";
            onOffSlider.min = "0";
            onOffSlider.max = "1";
            onOffSlider.step = "1";
            onOffSlider.value = "0";
            onOffSwitch.appendChild(onOffSlider);

            const brightnessSlider = document.createElement("label");
            brightnessSlider.textContent = "Brightness";
            const brightnessBar = document.createElement("input");
            brightnessBar.type = "range";
            brightnessBar.min = "0";
            brightnessBar.max = "100";
            brightnessBar.step = "1";
            brightnessBar.value = "50";
            brightnessSlider.appendChild(brightnessBar);

            const setButton = document.createElement("button");
            setButton.textContent = "Set";
            setButton.addEventListener("click", function () {
                // Handle the click event for the "Set" button of this light
                const lightState = {
                    name: light,
                    onOff: onOffSlider.value === "1",
                    brightness: parseInt(brightnessBar.value),
                };
                // Send an API request with lightState to control the light
                sendApiRequest(lightState);
            });

            lightControl.appendChild(lightName);
            lightControl.appendChild(onOffSwitch);
            lightControl.appendChild(brightnessSlider);
            lightControl.appendChild(setButton);

            lightControls.appendChild(lightControl);
        });
    }

    // Event listener for dropdown change
    sectionDropdown.addEventListener("change", function () {
        const selectedOption = sectionDropdown.options[sectionDropdown.selectedIndex];
        const selectedSectionValue = selectedOption.value;

        // Get the lights for the selected section
        const lightsInSelectedSection = sectionToLights[selectedSectionValue];

        // Create light controls for the selected section
        createLightControls(lightsInSelectedSection);
    });

    // Function to send an API request for controlling the light
    
    function sendApiRequest(lightState) {
        // Make an API request to control the light using lightState
        // Implement the API request code here
        const apiRequestPayload = {
            lightName: lightState.name,
            onOff: lightState.onOff,
            brightness: lightState.brightness,
        };
        // Make a POST request to the API endpoint
        fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(apiRequestPayload),
        })
        .then((response) => {
        if (response.ok) {
            console.log(`API request successful for light "${lightState.name}"`);
            // Handle success (e.g., display a success message)
        } else {
            console.error(`API request failed for light "${lightState.name}"`);
            // Handle error (e.g., display an error message)
        }
        })
        .catch((error) => {
        console.error(`API request error for light "${lightState.name}":`, error);
        // Handle network or other errors
        });
        console.log(`Control light "${lightState.name}": On/Off=${lightState.onOff}, Brightness=${lightState.brightness}`);
    }
});
