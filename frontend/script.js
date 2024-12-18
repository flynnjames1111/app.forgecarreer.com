document.addEventListener('DOMContentLoaded', () => {
    // Theme Toggle Functionality
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;

    // Initialize theme from localStorage
    function initTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        body.classList.toggle('dark-mode', savedTheme === 'dark');
    }

    // Toggle theme function
    function toggleTheme() {
        body.classList.toggle('dark-mode');
        const newTheme = body.classList.contains('dark-mode') ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);
    }

    // Attach theme toggle event
    themeToggle.addEventListener('click', toggleTheme);

    // Initialize theme on page load
    initTheme();

    // AI Configuration Manager
    const AIConfigManager = {
        customInstructions: {},

        configProfiles: {
            'entry-level': {
                customization_level: 'entry',
                custom_tone: 'Emphasize potential and eagerness to learn',
                custom_formatting: 'Clean, modern layout for recent graduates'
            },
            'professional': {
                customization_level: 'professional',
                custom_achievements: 'Highlight quantifiable results',
                custom_branding: 'Strategic career development narrative'
            },
            'executive': {
                customization_level: 'executive',
                custom_leadership: 'Demonstrate strategic leadership impact',
                custom_positioning: 'Position as industry thought leader'
            }
        },

        setCustomConfiguration(profile, additionalInstructions = {}) {
            const baseConfig = this.configProfiles[profile] || this.configProfiles['professional'];
            this.customInstructions = {
                ...baseConfig,
                ...additionalInstructions
            };
        },

        injectCustomPrompt(key, instruction) {
            this.customInstructions[`custom_${key}`] = instruction;
        },

        resetConfiguration() {
            this.customInstructions = {};
        }
    };

    // Resume Generation Function
    async function generateResume(userData) {
        try {
            const payload = {
                ...userData,
                custom_instructions: AIConfigManager.customInstructions
            };

            const response = await fetch('/api/generate-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error('Resume generation failed');
            }

            return await response.json();
        } catch (error) {
            console.error('Resume Generation Error:', error);
            alert('Failed to generate resume. Please try again.');
        }
    }

    // Resume Optimization Function
    async function optimizeResume(existingResume, jobDescription) {
        try {
            const payload = {
                resume: existingResume,
                job_description: jobDescription,
                custom_instructions: AIConfigManager.customInstructions
            };

            const response = await fetch('/api/optimize-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error('Resume optimization failed');
            }

            return await response.json();
        } catch (error) {
            console.error('Resume Optimization Error:', error);
            alert('Failed to optimize resume. Please try again.');
        }
    }

    // Event Listeners and Interactive Components
    const resumeForm = document.getElementById('resumeGenerationForm');
    const optimizationForm = document.getElementById('resumeOptimizationForm');
    const aiConfigSelect = document.getElementById('aiConfigProfile');

    if (resumeForm) {
        resumeForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(resumeForm);
            const userData = Object.fromEntries(formData.entries());

            // Set AI configuration based on user selection
            AIConfigManager.setCustomConfiguration(aiConfigSelect.value);

            const generatedResume = await generateResume(userData);
            // Handle resume display or download
        });
    }

    if (optimizationForm) {
        optimizationForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const existingResume = document.getElementById('existingResume').value;
            const jobDescription = document.getElementById('jobDescription').value;

            const optimizedResume = await optimizeResume(existingResume, jobDescription);
            // Handle optimized resume display
        });
    }
});
