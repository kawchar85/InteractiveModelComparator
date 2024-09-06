async function fetchData() {
    try {
        const response = await fetch('/api/getData');
        const data = await response.json();
        const content = document.getElementById("content");
        content.innerHTML = "";  // Clear previous content
        if (data.imageBoxes) {
            new ImageBox(content, data.imageBoxes);
        } else {
            content.innerHTML = "<p>No image data available.</p>";
        }
    } catch (error) {
        console.error("Error fetching data:", error);
        document.getElementById("content").innerHTML = "<p>Failed to load data. Please try again later.</p>";
    }
}

async function changeImage(direction) {
    try {
        await fetch(`/api/changeIndex?direction=${direction}`);
        await fetchData();  // Refresh the data after changing index
    } catch (error) {
        console.error("Error changing current image:", error);
        document.getElementById("content").innerHTML = "<p>Error changing images. Please try again.</p>";
    }
}

window.onload = fetchData;