function renderDashboard(data) {
    document.getElementById('result-header').textContent = data.profile_summary;
    
    // Update profile summary sidebar
    const p = window.appState.userProfile;
    document.getElementById('profile-summary-details').innerHTML = `
        <p><strong>Name:</strong> ${p.name}</p>
        <p><strong>Age:</strong> ${p.age}</p>
        <p><strong>State:</strong> ${p.state}</p>
        <p><strong>Occupation:</strong> ${p.occupation}</p>
        <p><strong>Income:</strong> ₹${p.annual_income}</p>
    `;

    renderSchemeCards(data.schemes);
}

function renderSchemeCards(schemes) {
    const container = document.getElementById('schemes-container');
    container.innerHTML = '';
    
    if (schemes.length === 0) {
        container.innerHTML = '<p>No matching schemes found based on your profile.</p>';
        return;
    }

    const lang = window.appState.userProfile.preferred_language || 'en';

    schemes.forEach(scheme => {
        const name = lang === 'hi' && scheme.scheme_name_hi ? scheme.scheme_name_hi : scheme.scheme_name;
        const desc = lang === 'hi' && scheme.description_hi ? scheme.description_hi : scheme.description;
        
        let scoreClass = 'score-low';
        if (scheme.match_score >= 80) scoreClass = 'score-high';
        else if (scheme.match_score >= 50) scoreClass = 'score-med';

        const card = document.createElement('div');
        card.className = 'glass-panel scheme-card';
        card.innerHTML = `
            <div class="match-score ${scoreClass}">Match Score: ${Math.round(scheme.match_score)}%</div>
            <h3>${name}</h3>
            <p style="color: var(--text-secondary); font-size: 0.9em; margin-bottom: 0.5rem;">
                ${scheme.ministry} • ${scheme.scheme_type.toUpperCase()}
            </p>
            <p>${scheme.benefits_summary}</p>
            
            <div class="scheme-details" style="display: none; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--glass-border);">
                <h4>About</h4>
                <p>${desc}</p>
                <h4 style="margin-top: 0.5rem;">Why it matches:</h4>
                <ul style="margin-left: 1.5rem; margin-bottom: 0.5rem;">
                    ${scheme.match_reasons.map(r => `<li>${r}</li>`).join('')}
                </ul>
                <h4>Documents Required:</h4>
                <ul style="margin-left: 1.5rem; margin-bottom: 0.5rem;">
                    ${scheme.documents_needed.map(d => `<li>${d}</li>`).join('')}
                </ul>
                <h4>How to Apply:</h4>
                <p style="white-space: pre-line;">${scheme.how_to_apply}</p>
                
                <div style="margin-top: 1rem; display: flex; gap: 1rem;">
                    ${scheme.official_url ? `<a href="${scheme.official_url}" target="_blank" class="btn btn-primary" style="text-decoration:none; padding:0.5rem 1rem;">Official Website</a>` : ''}
                    <button class="btn" style="background:var(--surface);" onclick="askAboutScheme('${scheme.scheme_id}', '${name}')">Ask AI</button>
                </div>
            </div>
            
            <button class="btn expand-btn" style="background: transparent; border: 1px solid var(--primary); color: var(--primary); margin-top: 1rem; width: 100%;">
                View Details ▼
            </button>
        `;

        const expandBtn = card.querySelector('.expand-btn');
        const detailsDiv = card.querySelector('.scheme-details');
        
        expandBtn.addEventListener('click', () => {
            const isHidden = detailsDiv.style.display === 'none';
            detailsDiv.style.display = isHidden ? 'block' : 'none';
            expandBtn.textContent = isHidden ? 'Hide Details ▲' : 'View Details ▼';
        });

        container.appendChild(card);
    });
}

function askAboutScheme(id, name) {
    toggleChat(true);
    const input = document.getElementById('chat-input');
    input.value = `How do I apply for ${name}?`;
    document.getElementById('btn-send').click();
}

document.getElementById('btn-edit-profile').addEventListener('click', () => {
    navigateTo('profile');
});
