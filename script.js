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

    // User Onboarding Functionality
    const onboardingSteps = document.querySelectorAll('.onboarding-step');
    const onboardingProgress = document.getElementById('onboardingProgress');
    const startOnboardingBtn = document.getElementById('startOnboarding');

    let currentStep = 0;

    function updateOnboardingProgress() {
        const progressPercentage = (currentStep / (onboardingSteps.length - 1)) * 100;
        onboardingProgress.style.width = `${progressPercentage}%`;

        onboardingSteps.forEach((step, index) => {
            step.classList.toggle('active', index <= currentStep);
        });
    }

    // Simulate onboarding progression
    startOnboardingBtn.addEventListener('click', () => {
        if (currentStep < onboardingSteps.length - 1) {
            currentStep++;
            updateOnboardingProgress();
        } else {
            alert('Onboarding complete! Ready to create your resume.');
        }
    });

    // Testimonial Carousel
    const testimonialCarousel = document.querySelector('.testimonial-carousel');
    let currentTestimonial = 0;

    function rotateTestimonials() {
        const testimonials = document.querySelectorAll('.testimonial-item');
        currentTestimonial = (currentTestimonial + 1) % testimonials.length;
        
        testimonials.forEach((testimonial, index) => {
            testimonial.style.transform = `translateX(${-currentTestimonial * 100}%)`;
        });
    }

    // Rotate testimonials every 5 seconds
    setInterval(rotateTestimonials, 5000);

    // Pricing Plan Interaction
    const pricingCards = document.querySelectorAll('.pricing-card');
    
    pricingCards.forEach(card => {
        card.addEventListener('click', () => {
            pricingCards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
        });
    });

    // Template Selection Functionality
    const templateCards = document.querySelectorAll('.template-card');
    const aiRecommendationBtn = document.getElementById('aiTemplateRecommendation');

    // Template Selection Logic
    templateCards.forEach(card => {
        card.addEventListener('click', () => {
            // Remove selected state from all cards
            templateCards.forEach(c => c.classList.remove('selected'));
            
            // Add selected state to clicked card
            card.classList.add('selected');

            // Get template name
            const templateName = card.querySelector('.template-select').getAttribute('data-template');
            
            // Optional: You could trigger a modal or next step here
            console.log(`Selected Template: ${templateName}`);
        });
    });

    // AI Template Recommendation
    aiRecommendationBtn.addEventListener('click', () => {
        // Simulated AI recommendation logic
        const templates = [
            'corporate-classic',
            'creative-modern', 
            'tech-minimalist', 
            'academic-research', 
            'startup-founder', 
            'international-global', 
            'non-profit-impact', 
            'remote-work', 
            'executive-leadership'
        ];

        // Randomly recommend a template
        const recommendedTemplate = templates[Math.floor(Math.random() * templates.length)];
        const recommendedCard = document.querySelector(`[data-template="${recommendedTemplate}"]`).closest('.template-card');

        // Scroll to and highlight recommended template
        recommendedCard.scrollIntoView({ behavior: 'smooth' });
        
        // Temporary highlight effect
        recommendedCard.classList.add('recommended');
        setTimeout(() => {
            recommendedCard.classList.remove('recommended');
        }, 3000);

        // Optional: Show a modal with recommendation explanation
        alert(`Based on your profile, we recommend the ${recommendedTemplate.replace('-', ' ')} template!`);
    });

    // Download and Signup Routing
    const downloadButtons = document.querySelectorAll('.download-btn');
    
    downloadButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Check if user is logged in (you'd replace this with actual authentication logic)
            const isLoggedIn = false; // Placeholder
            
            if (!isLoggedIn) {
                // Redirect to signup page
                window.location.href = 'signup.html';
            } else {
                // Proceed with download logic
                // You can add download functionality here
                alert('Downloading resume...');
            }
        });
    });

    // Advanced AI Configuration and Prompt Injection
    const AIConfigManager = {
        customInstructions: {},

        // Preset AI Configuration Profiles
        configProfiles: {
            'entry-level': {
                customization_level: 'entry',
                custom_tone: 'Emphasize potential and eagerness to learn',
                custom_formatting: 'Use a clean, modern layout suitable for recent graduates'
            },
            'professional': {
                customization_level: 'professional',
                custom_achievements: 'Highlight quantifiable results and career progression',
                custom_branding: 'Create a narrative that shows strategic career development'
            },
            'executive': {
                customization_level: 'executive',
                custom_leadership: 'Demonstrate strategic leadership and organizational impact',
                custom_positioning: 'Position as a thought leader in the industry'
            }
        },

        // Method to set custom AI configuration
        setCustomConfiguration(profile, additionalInstructions = {}) {
            const baseConfig = this.configProfiles[profile] || this.configProfiles['professional'];
            this.customInstructions = {
                ...baseConfig,
                ...additionalInstructions
            };
        },

        // Advanced prompt injection method
        injectCustomPrompt(key, instruction) {
            this.customInstructions[`custom_${key}`] = instruction;
        },

        // Reset custom configuration
        resetConfiguration() {
            this.customInstructions = {};
        }
    };

    // Enhanced Resume Generation with Custom AI Configuration
    async function generateResume(userData) {
        try {
            const payload = {
                ...userData,
                custom_instructions: AIConfigManager.customInstructions
            };

            const response = await fetch('http://localhost:5000/generate-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            
            if (data.status === 'success') {
                const resumePreview = document.getElementById('resumePreview');
                resumePreview.textContent = data.resume_content;
                
                const downloadBtn = document.getElementById('downloadResume');
                downloadBtn.disabled = false;
            } else {
                throw new Error(data.error || 'Resume generation failed');
            }
        } catch (error) {
            console.error('Error generating resume:', error);
            alert('Failed to generate resume. Please try again.');
        }
    }

    // Enhanced Resume Optimization with Custom AI Configuration
    async function optimizeResume(existingResume, jobDescription) {
        try {
            const payload = {
                resume_content: existingResume,
                job_description: jobDescription,
                custom_instructions: AIConfigManager.customInstructions
            };

            const response = await fetch('http://localhost:5000/optimize-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            
            if (data.status === 'success') {
                const optimizedResumePreview = document.getElementById('optimizedResumePreview');
                optimizedResumePreview.textContent = data.optimized_resume;
            } else {
                throw new Error(data.error || 'Resume optimization failed');
            }
        } catch (error) {
            console.error('Error optimizing resume:', error);
            alert('Failed to optimize resume. Please try again.');
        }
    }

    // Event Listeners for Resume Generation and Optimization
    const resumeForm = document.getElementById('resumeGenerationForm');
    const optimizationForm = document.getElementById('resumeOptimizationForm');
    const aiConfigSelect = document.getElementById('aiConfigProfile');
    const customPromptInput = document.getElementById('customPromptInput');

    // AI Configuration Profile Selection
    if (aiConfigSelect) {
        aiConfigSelect.addEventListener('change', (e) => {
            const selectedProfile = e.target.value;
            AIConfigManager.setCustomConfiguration(selectedProfile);
        });
    }

    // Custom Prompt Injection
    if (customPromptInput) {
        customPromptInput.addEventListener('input', (e) => {
            const customKey = document.getElementById('customPromptKey').value;
            AIConfigManager.injectCustomPrompt(customKey, e.target.value);
        });
    }

    // Resume Generation Form
    if (resumeForm) {
        resumeForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(resumeForm);
            const userData = {
                full_name: formData.get('fullName'),
                email: formData.get('email'),
                industry: formData.get('industry'),
                experience_level: formData.get('experienceLevel'),
                skills: formData.get('skills'),
                summary: formData.get('professionalSummary')
            };

            await generateResume(userData);
        });
    }

    // Resume Optimization Form
    if (optimizationForm) {
        optimizationForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(optimizationForm);
            const existingResume = formData.get('existingResume');
            const jobDescription = formData.get('jobDescription');

            await optimizeResume(existingResume, jobDescription);
        });
    }
});
