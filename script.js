document.getElementById('send-btn').addEventListener('click', async () => {
    const input = document.getElementById('chat-input');
    const query = input.value;
    if (!query) return;

    const chatContent = document.getElementById('chat-content');
    const userMessage = document.createElement('div');
    userMessage.textContent = `You: ${query}`;
    userMessage.style.color = '#fff'; // Ensure text color is white
    chatContent.appendChild(userMessage);

    input.value = '';

    try {
        const response = await fetch('http://127.0.0.1:8080/chat', {
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
        botMessage.textContent = `Bot: ${data.answer}`;
        botMessage.style.color = '#fff'; // Ensure text color is white
        chatContent.appendChild(botMessage);
    } catch (error) {
        console.error('Error:', error);
        const errorMessage = document.createElement('div');
        errorMessage.textContent = `Error: ${error.message}`;
        errorMessage.style.color = '#fff'; // Ensure text color is white
        chatContent.appendChild(errorMessage);
    }

    chatContent.scrollTop = chatContent.scrollHeight;
});
