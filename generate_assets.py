from PIL import Image, ImageDraw, ImageFont
import os

# Create assets directory if it doesn't exist
assets_dir = 'assets'
os.makedirs(assets_dir, exist_ok=True)

# Function to create a placeholder image
def create_placeholder(filename, width, height, text=None):
    image = Image.new('RGB', (width, height), color='#E0E0E0')
    draw = ImageDraw.Draw(image)
    
    # Try to use a default system font
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
    
    # Add text if provided
    if text:
        # Use getbbox to get text dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((width-text_width)/2, (height-text_height)/2)
        draw.text(position, text, fill='#2196F3', font=font)
    
    # Draw a border
    draw.rectangle([0, 0, width-1, height-1], outline='#2196F3')
    
    image.save(os.path.join(assets_dir, filename))

# Generate various placeholder images
create_placeholder('resume-mockup.png', 500, 300, 'Resume Mockup')
create_placeholder('resume-generation.gif', 400, 250, 'Resume Generation')
create_placeholder('cover-letter-generation.gif', 400, 250, 'Cover Letter Generation')

# Testimonial images
create_placeholder('testimonial-1.jpg', 100, 100, 'Sarah')
create_placeholder('testimonial-2.jpg', 100, 100, 'Michael')

# Tech stack logos
create_placeholder('react-logo.png', 100, 100, 'React.js')
create_placeholder('nodejs-logo.png', 100, 100, 'Node.js')
create_placeholder('openai-logo.png', 100, 100, 'OpenAI')
create_placeholder('aws-logo.png', 100, 100, 'AWS')

print("Placeholder assets generated successfully!")
