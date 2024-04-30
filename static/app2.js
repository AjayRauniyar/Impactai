const preText1 = "percentage of technical knowledge in  ";
const midText1 = "of ";
const postText1 =" district based on gender remove explaination show data only"

function getStory2() {
    const promptText3 = document.getElementById('storyPrompt3').value;
    const promptText4 = document.getElementById('storyPrompt4').value;
    const fullStory = preText1 + promptText3 + midText1 + promptText4 + postText1;
    fetch('/getstory2', {
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
