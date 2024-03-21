document.addEventListener('DOMContentLoaded', () => {
    // Selectors for the buttons and content sections
    const gamesButton = document.querySelector('.games-button');
    const appsButton = document.querySelector('.apps-button');
    const papersButton = document.querySelector('.papers-button');
    const gamesContent = document.querySelector('.games');
    const appsContent = document.querySelector('.apps');
    const papersContent = document.querySelector('.papers');

    // Toggle display function
    function toggleDisplay(element) {
        if (element.style.display === 'flex') {
            element.style.display = 'none';
        } else {
            element.style.display = 'block';
        }
    }

    // Event listeners for buttons
    gamesButton.addEventListener('click', (e) => {
        e.preventDefault(); // Prevents navigating to the anchor link
        toggleDisplay(gamesContent);
        // hide other sections
        appsContent.style.display = 'none';
        papersContent.style.display = 'none';
    });

    appsButton.addEventListener('click', (e) => {
        e.preventDefault(); // Prevents navigating to the anchor link
        toggleDisplay(appsContent);
        // hide other sections
        gamesContent.style.display = 'none';
        papersContent.style.display = 'none';
    });

    papersButton.addEventListener('click', (e) => {
        e.preventDefault(); // Prevents navigating to the anchor link
        toggleDisplay(papersContent);
        // hide other sections
        gamesContent.style.display = 'none';
        appsContent.style.display = 'none';
    });
});
