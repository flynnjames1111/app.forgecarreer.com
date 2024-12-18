const { GoogleGenerativeAI } = require('@google/generative-ai');

exports.handler = async (event, context) => {
  // Ensure this is a POST request
  if (event.httpMethod !== 'POST') {
    return { 
      statusCode: 405, 
      body: JSON.stringify({ message: 'Method Not Allowed' }) 
    };
  }

  try {
    // Parse the incoming request body
    const { resume_content, job_description } = JSON.parse(event.body);

    // Initialize Google Generative AI
    const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    const model = genAI.getGenerativeModel({ model: "gemini-pro"});

    // Generate resume improvements
    const prompt = `
      You are an expert resume optimizer. 
      Given the following resume content and job description, 
      provide targeted improvements:

      Resume Content:
      ${resume_content}

      Job Description:
      ${job_description}

      Please provide:
      1. Specific keyword alignments
      2. Suggested content improvements
      3. Formatting recommendations
    `;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();

    return {
      statusCode: 200,
      body: JSON.stringify({
        improvements: text
      }),
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    };

  } catch (error) {
    console.error('Error in resume generation:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ 
        message: 'Error generating resume improvements', 
        error: error.message 
      })
    };
  }
};
