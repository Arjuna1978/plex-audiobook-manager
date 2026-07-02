/**
 * Generic navigator for multi-step workflows
 * @param {string} endpoint - The URL to fetch data from
 * @param {string} currentStepId - The ID of the container to hide
 * @param {string} nextStepId - The ID of the container to show/populate
 * @param {function} onClickHandler - Action when an item tile is clicked
 */
async function navigate(endpoint, currentStepId, nextStepId, onClickHandler) {
    const nextContainer = document.getElementById(nextStepId);

    document.getElementById(currentStepId).style.display = 'none';
    nextContainer.style.display = 'block';

    nextContainer.innerHTML = '<p>Loading...</p>';

    try {
        const response = await fetch(endpoint);
        const data = await response.json();

        nextContainer.innerHTML = '';
        data.forEach(item => {
            const div = document.createElement('div');
            div.className = 'tile';
            div.innerHTML = `<h4>${item.title}</h4>`;
            div.onclick = () => onClickHandler(item);
            nextContainer.appendChild(div);
        });
    } catch (error) {
        nextContainer.innerHTML = '<p>Error loading content.</p>';
        console.error('Navigation error:', error);
    }
}