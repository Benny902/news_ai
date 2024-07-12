document.addEventListener('DOMContentLoaded', () => {
    // function to fetch news headers and links based on user token
    const fetchNews = async () => {
        const token = localStorage.getItem('token');
        const url = 'http://localhost:5000/news';

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token ? token : '',
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            if (!data.articles || !Array.isArray(data.articles)) {
                throw new Error('Expected an array of articles');
            }

            displayNewsHeaders(data.articles);

        } catch (error) {
            console.error('Error fetching news:', error.message);
        }
    };

    // function to display article headers as clickable links
    const displayNewsHeaders = (articles) => {
        const container = document.createElement('div');
        container.classList.add('article-container');

        articles.forEach(article => {
            const header = document.createElement('h3');
            const link = document.createElement('a');
            link.href = article.link;
            link.textContent = article.header;
            link.target = '_blank'; // Open link in new tab
            link.classList.add('article-link');
            header.appendChild(link);
            container.appendChild(header);
        });

        // clear previous content
        const contentDiv = document.getElementById('news-content');
        contentDiv.innerHTML = ''; 
        contentDiv.appendChild(container); // append the container to the contentDiv
    };

    // function to fetch news headers, links, and content based on user token
    const fetchSummaries = async () => {
        const token = localStorage.getItem('token');
        const url = 'http://localhost:5000/summary';

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token ? token : '',
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            if (!data.articles || !Array.isArray(data.articles)) {
                throw new Error('Expected an array of articles');
            }

            displayArticles(data.articles);

        } catch (error) {
            console.error('Error fetching content:', error.message);
        }
    };

    // function to display article headers and content
    const displayArticles = (articles) => {
        const container = document.createElement('div');
        container.classList.add('article-container');

        articles.forEach(article => {
            const articleDiv = document.createElement('div');
            articleDiv.classList.add('article');

            const header = document.createElement('h3');
            const link = document.createElement('a');
            const summary = document.createElement('p');
            link.href = article.link;
            link.textContent = article.header;
            summary.textContent = article.summary;
            link.target = '_blank'; // to open link in new tab
            link.classList.add('article-link');
            header.appendChild(link);

            const content = document.createElement('p');
            content.textContent = article.content;
            content.classList.add('article-content');

            articleDiv.appendChild(header);
            articleDiv.appendChild(content);
            articleDiv.appendChild(summary);
            container.appendChild(articleDiv);
        });

        // clear previous content
        const contentDiv = document.getElementById('news-content');
        contentDiv.innerHTML = '';   
        contentDiv.appendChild(container); // append the container to the contentDiv
    };

    // event listeners for the fetch buttons
    const fetchNewsButton = document.getElementById('fetchNews');
    if (fetchNewsButton) {
        fetchNewsButton.addEventListener('click', fetchNews);
    }

    const fetchSummariesButton = document.getElementById('fetchSummaries');
    if (fetchSummariesButton) {
        fetchSummariesButton.addEventListener('click', fetchSummaries);
    }
});
