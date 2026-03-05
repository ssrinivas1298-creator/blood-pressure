document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        age: document.getElementById('age').value,
        gender: document.getElementById('gender').value,
        hemoglobin: document.getElementById('hemoglobin').value,
        rbc_count: document.getElementById('rbc_count').value,
        mcv: document.getElementById('mcv').value
    };

    const submitBtn = e.target.querySelector('button');
    submitBtn.innerText = 'Analyzing...';
    submitBtn.disabled = true;

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        
        if (result.error) {
            alert('Error: ' + result.error);
            return;
        }

        displayResult(result);
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during analysis.');
    } finally {
        submitBtn.innerText = 'Analyze Health Status';
        submitBtn.disabled = false;
    }
});

function displayResult(result) {
    const resultCard = document.getElementById('resultCard');
    const statusIndicator = document.getElementById('statusIndicator');
    const confidenceBar = document.getElementById('confidenceBar');
    const confidenceText = document.getElementById('confidenceText');
    const interpretationTitle = document.getElementById('interpretationTitle');
    const interpretationDesc = document.getElementById('interpretationDesc');
    const recList = document.getElementById('recList');

    resultCard.style.display = 'block';
    
    // Status
    statusIndicator.innerText = result.interpretation;
    statusIndicator.className = 'status-badge ' + (result.is_anemic ? 'status-anemic' : 'status-normal');
    
    // Confidence
    confidenceBar.style.width = result.confidence + '%';
    confidenceText.innerText = result.confidence + '%';
    
    // Interpretation
    interpretationTitle.innerText = "Clinical Interpretation";
    interpretationDesc.innerText = result.description;
    
    // Recommendations
    recList.innerHTML = '';
    result.recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.innerText = rec;
        recList.appendChild(li);
    });

    // Smooth scroll to result
    resultCard.scrollIntoView({ behavior: 'smooth' });
}
