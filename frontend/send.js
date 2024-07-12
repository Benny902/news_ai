document.addEventListener('DOMContentLoaded', () => {
    // function to send an email based on user token
    const sendEmail = async () => {
        const token = localStorage.getItem('token');
        const url = 'http://localhost:5000/email';

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token ? token : '',
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                const errorMessage = errorData.error || `HTTP error! Status: ${response.status}`; 
                throw new Error(errorMessage);
            }

            const data = await response.json();
            console.log('email sent with the summarized news:', data);
            displayMessage('email sent with the summarized news');

        } catch (error) {
            console.error('Error sending email:', error.message);
            displayMessage('Error sending email: ' + error.message);
        }
    };

    // function to send a telegram message based on user token -- didnt made backend route yet, im missing telegram credentials / need to create telegram bot
    const sendTelegram = async () => {
        const token = localStorage.getItem('token');
        displayMessage('telegram function not made yet.');
    };

    // function to display messages
    const displayMessage = (message) => {
        const contentDiv = document.getElementById('message-content');
        contentDiv.textContent = message;
    };

    // event listeners for the send buttons
    const sendEmailButton = document.getElementById('sendEmail');
    if (sendEmailButton) {
        sendEmailButton.addEventListener('click', sendEmail);
    }

    const sendTelegramButton = document.getElementById('sendTelegram');
    if (sendTelegramButton) {
        sendTelegramButton.addEventListener('click', sendTelegram);
    }
    
});
