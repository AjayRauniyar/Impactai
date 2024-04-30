

function getStory3() {
    const promptText5 = document.getElementById('storyPrompt5').value;
   
    const fullStory = promptText5;
    fetch('/getstory3', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({story_prompt: fullStory})
    })
    .then(response => response.json())
    .then(data => {
        // Assuming the API response is stored in `data`
        if (data && data.candidates && data.candidates.length > 0) {
            const firstCandidate = data.candidates[0];
            if (firstCandidate.content && firstCandidate.content.parts && firstCandidate.content.parts.length > 0) {
                const text = firstCandidate.content.parts[0].text;
                document.getElementById('storyResult').innerText = text;
                localStorage.setItem('storyText', text);
            } else {
                document.getElementById('storyResult').innerText = 'No text found in the response.';
            }
        } else {
            document.getElementById('storyResult').innerText = 'No candidates found in the response.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('storyResult').innerText = 'Failed to fetch story.';
    });
}
