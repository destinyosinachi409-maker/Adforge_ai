from flask import Flask, render_template, request, jsonify
import requests
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'static/generated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate/image', methods=['POST'])
def generate_image():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        style = data.get('style', 'modern')
        
        enhanced = f"{prompt}, {style} style, advertisement, high quality, professional"
        encoded = requests.utils.quote(enhanced)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=576&nologo=true"
        
        r = requests.get(url, timeout=60)
        
        if r.status_code == 200:
            fn = f"ad_{uuid.uuid4().hex[:8]}.png"
            fp = os.path.join(UPLOAD_FOLDER, fn)
            with open(fp, 'wb') as f:
                f.write(r.content)
            return jsonify({"success": True, "url": f"/static/generated/{fn}"})
        else:
            return jsonify({"success": False, "error": "Image service busy"})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/generate/copy', methods=['POST'])
def generate_copy():
    try:
        data = request.get_json()
        product = data.get('product_name', 'Product')
        audience = data.get('target_audience', 'Everyone')
        tone = data.get('tone', 'professional')
        
        headlines = {
            "professional": f"Elevate Your Standards with {product}",
            "casual": f"Your New Favorite {product} is Here!",
            "exciting": f"🚀 {product}: The Future is NOW!",
            "luxury": f"Exquisite {product} for the Discerning",
            "humorous": f"{product}: Because Adulting is Hard",
            "urgent": f"⚡ Limited: {product} Selling Fast!"
        }
        
        bodies = {
            "professional": f"Designed for {audience}, {product} delivers unmatched quality.",
            "casual": f"Hey! {product} is made for {audience} who want great results.",
            "exciting": f"OMG! {product} is here! Perfect for {audience}!",
            "luxury": f"Experience excellence with {product}. Crafted for {audience}.",
            "humorous": f"{audience} deserve better. {product} is way cooler.",
            "urgent": f"Time is running out! {product} is flying off shelves!"
        }
        
        ctas = {
            "professional": "Get Started",
            "casual": "Grab Yours!",
            "exciting": "Claim Now!",
            "luxury": "Experience It",
            "humorous": "Treat Yourself",
            "urgent": "Act Now!"
        }
        
        copy_text = f"""HEADLINE:
{headlines.get(tone, headlines['professional'])}

PRIMARY TEXT:
{bodies.get(tone, bodies['professional'])}

CALL-TO-ACTION:
{ctas.get(tone, ctas['professional'])}

HASHTAGS:
#{product.replace(' ', '')} #MustHave"""
        
        return jsonify({"success": True, "copy": copy_text})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
