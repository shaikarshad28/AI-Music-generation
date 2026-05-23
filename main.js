document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const btnText = generateBtn.querySelector('.btn-text');
    const spinner = generateBtn.querySelector('.spinner');
    const statusText = document.getElementById('status-text');
    const tracksContainer = document.getElementById('tracks-container');
    const tracksList = document.getElementById('tracks-list');

    generateBtn.addEventListener('click', async () => {
        // Set loading state
        generateBtn.disabled = true;
        btnText.classList.add('hidden');
        spinner.classList.remove('hidden');
        statusText.classList.remove('hidden');
        tracksContainer.classList.add('hidden');
        
        // Clear previous tracks
        tracksList.innerHTML = '';

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (data.status === 'success') {
                const midiUrls = data.midi_urls;
                
                midiUrls.forEach((midiUrl, index) => {
                    const urlWithCacheBuster = midiUrl + '?t=' + new Date().getTime();
                    const trackNumber = index + 1;
                    
                    const trackDiv = document.createElement('div');
                    trackDiv.className = 'track-item';
                    trackDiv.style.marginBottom = '2rem';
                    
                    trackDiv.innerHTML = `
                        <h4>Variation ${trackNumber}</h4>
                        <div class="midi-wrapper">
                            <midi-visualizer type="piano-roll" id="visualizer-${trackNumber}" src="${urlWithCacheBuster}"></midi-visualizer>
                            <midi-player id="player-${trackNumber}" visualizer="#visualizer-${trackNumber}" src="${urlWithCacheBuster}"></midi-player>
                        </div>
                        <div class="actions text-center">
                            <a href="${midiUrl}" class="secondary-button" download>Download Track ${trackNumber}</a>
                        </div>
                    `;
                    
                    tracksList.appendChild(trackDiv);
                });
                
                // Show container
                tracksContainer.classList.remove('hidden');
            } else {
                alert('Failed to generate music: ' + data.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while generating music.');
        } finally {
            // Restore button state
            generateBtn.disabled = false;
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
            statusText.classList.add('hidden');
        }
    });
});
