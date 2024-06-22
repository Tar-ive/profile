// script.js

document.getElementById('send-btn').addEventListener('click', async () => {
    await sendMessage();
});

document.getElementById('chat-input').addEventListener('keypress', async (event) => {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the default action to avoid form submission
        await sendMessage();
    }
});

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const query = input.value;
    if (!query) return;

    const chatContent = document.getElementById('chat-content');
    
    const userMessage = document.createElement('div');
    userMessage.textContent = `You: ${query}`;
    userMessage.classList.add('message', 'user-message');
    chatContent.appendChild(userMessage);

    input.value = '';

    try {
        const response = await fetch('https://spry-ether-426905-b1.uc.r.appspot.com/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        const botMessage = document.createElement('div');
        botMessage.textContent = `Saksham: ${data.answer}`;
        botMessage.classList.add('message', 'bot-message');
        chatContent.appendChild(botMessage);
    } catch (error) {
        console.error('Error:', error);
        const errorMessage = document.createElement('div');
        errorMessage.textContent = `Error: ${error.message}`;
        errorMessage.classList.add('message', 'bot-message');
        chatContent.appendChild(errorMessage);
    }

    chatContent.scrollTop = chatContent.scrollHeight;
}
