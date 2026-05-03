let currentStep = 1;

function initProfileForm() {
    updateFormSteps();
    
    document.getElementById('btn-next-1').addEventListener('click', () => {
        if (validateStep(1)) { currentStep = 2; updateFormSteps(); }
    });
    
    document.getElementById('btn-prev-2').addEventListener('click', () => {
        currentStep = 1; updateFormSteps();
    });
    
    document.getElementById('btn-next-2').addEventListener('click', () => {
        if (validateStep(2)) { currentStep = 3; updateFormSteps(); }
    });
    
    document.getElementById('btn-prev-3').addEventListener('click', () => {
        currentStep = 2; updateFormSteps();
    });
    
    document.getElementById('btn-submit').addEventListener('click', async (e) => {
        e.preventDefault();
        if (validateStep(3)) {
            await submitProfile();
        }
    });
}

function updateFormSteps() {
    document.querySelectorAll('.form-step').forEach((el, index) => {
        if (index + 1 === currentStep) {
            el.classList.add('active');
        } else {
            el.classList.remove('active');
        }
    });
    document.getElementById('step-indicator').textContent = `Step ${currentStep} of 3`;
}

function validateStep(step) {
    const stepDiv = document.getElementById(`step-${step}`);
    if (!stepDiv) return true;
    
    const inputs = stepDiv.querySelectorAll('input, select');
    for (let input of inputs) {
        if (!input.checkValidity()) {
            input.reportValidity();
            return false;
        }
    }
    
    return true;
}

async function submitProfile() {
    const btn = document.getElementById('btn-submit');
    btn.textContent = 'Searching...';
    btn.disabled = true;

    // Collect data
    const profile = {
        name: document.getElementById('name').value,
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        state: document.getElementById('state').value,
        occupation: document.getElementById('occupation').value,
        annual_income: parseInt(document.getElementById('income').value) || 0,
        caste_category: document.getElementById('caste').value,
        is_bpl: document.getElementById('bpl').value === 'true',
        marital_status: document.getElementById('marital').value,
        preferred_language: document.getElementById('lang').value,
        // defaults for demo
        has_bank_account: true,
        has_aadhaar: true,
        is_land_owner: document.getElementById('occupation').value === 'farmer',
        has_disability: false
    };

    window.appState.userProfile = profile;

    try {
        const response = await fetch('/api/schemes/find', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(profile)
        });
        
        if (!response.ok) throw new Error('API Error');
        
        const data = await response.json();
        window.appState.schemes = data.schemes;
        
        renderDashboard(data);
        navigateTo('dashboard');
        
    } catch (error) {
        alert('Failed to find schemes. Is the backend running?');
        console.error(error);
    } finally {
        btn.textContent = 'Find Matching Schemes';
        btn.disabled = false;
    }
}
