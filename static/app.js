const preText = "percentage of illerate people in ";
const midText = "of ";
const postText ="based on gender remove explaination show data only"

function getStory() {
    const promptText1 = document.getElementById('storyPrompt1').value;
    const promptText2 = document.getElementById('storyPrompt2').value;
    const fullStory = preText + promptText1 + midText + promptText2 + postText;
    fetch('/getstory', {
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
