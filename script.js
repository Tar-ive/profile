

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
        const response = await axios.post('https://profile-429301.uc.r.appspot.com/chat', { query });

        if (response.status !== 200) {
            throw new Error('Network response was not ok');
        }

        const data = response.data;

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
document.addEventListener("DOMContentLoaded", function() {
    axios({
        method: 'get',
        url:  "https://v1.nocodeapi.com/tarivee/medium/fOxBOpbWWxkJPYdG",
        // https://v1.nocodeapi.com/tarive/medium/vIQMTpqhzgUXgjOe',
        params: {},
    }).then(function (response) {
        // Log the response data to inspect the structure
        console.log('API response:', response.data);

        const posts = response.data; // Adjust this if necessary based on console output
        if (Array.isArray(posts) && posts.length > 0) {
            // Render posts without repetition
            renderMediumPosts(posts);
        } else {
            document.getElementById('jsonContent').innerHTML = '<p>No posts available.</p>';
        }
    }).catch(function (error) {
        console.log('Error:', error);
        document.getElementById('jsonContent').innerHTML = `<p>Error loading posts: ${error.message}</p>`;
    });
});

function renderMediumPosts(posts) {
    const jsonContent = document.getElementById('jsonContent');
    jsonContent.innerHTML = ''; // Clear any existing content

    posts.forEach(post => {
        const postCard = document.createElement('div');
        postCard.classList.add('medium-post-card', 'center'); // Updated class names

        // Create and append the post title
        const postTitle = document.createElement('h3');
        postTitle.textContent = post.title;
        const postInfo = document.createElement('div');
        postInfo.classList.add('medium-post-info'); // Updated class names
        postInfo.appendChild(postTitle);

        // Extract and display the first 300 characters of the post content
        let postContent = '';
        if (post.content) {
            postContent = post.content.substring(0, 300) + '...';
        } else if (post.content_encoded) {
            postContent = post.content_encoded.substring(0, 300) + '...';
        }

        const postDescription = document.createElement('p');
        postDescription.innerHTML = postContent;
        postInfo.appendChild(postDescription);

        // Add "Read more" link
        const postLink = document.createElement('a');
        postLink.href = post.link;
        postLink.textContent = 'Read more';
        postLink.target = '_blank';
        postInfo.appendChild(postLink);

        // Append post info to the post card
        postCard.appendChild(postInfo);

        // Append the post card to the container
        jsonContent.appendChild(postCard);
    });
}

function openModal(imageSrc, description) {
    document.getElementById('modalImage').src = imageSrc;
    document.getElementById('modalDescription').innerText = description;
    document.getElementById('imageModal').style.display = 'flex';
  }

  function closeModal() {
    document.getElementById('imageModal').style.display = 'none';
  }