from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/generated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class FreeAdGenerator:
    def generate_image_ad(self, prompt, style="modern"):
        try:
            enhanced = f"{prompt}, {style} style, advertisement, high quality, professional"
            encoded = requests.utils.quote(enhanced)
            url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=576&nologo=true"
            r = requests.get(url, timeout=60)
            if r.status_code == 200:
                fn = f"ad_{uuid.uuid4().hex[:8]}.png"
                fp = os.path.join(app.config['UPLOAD_FOLDER'], fn)
                with open(fp, 'wb') as f:
                    f.write(r.content)
                return {"success": True, "url": f"/static/generated/{fn}", "type": "image"}
            return {"success": False, "error": "Service busy"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_ad_copy(self, product, audience, tone="professional"):
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
            "urgent": f"Time's running out! {product} is flying off shelves!"
        }
        ctas = {"professional": "Get Started", "casual": "Grab Yours!", "exciting": "Claim Now!",
                "luxury": "Experience It", "humorous": "Treat Yourself", "urgent": "Act Now!"}
        return {"success": True, "copy": f"HEADLINE:\n{headlines.get(tone, headlines['professional'])}\n\nTEXT:\n{bodies.get(tone, bodies['professional'])}\n\nCTA:\n{ctas.get(tone, ctas['professional'])}\n\nHASHTAGS:\n#{product.replace(' ','')} #MustHave", "type": "text"}

ad_gen = FreeAdGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate/image', methods=['POST'])
def gen_image():
    d = request.json
    return jsonify(ad_gen.generate_image_ad(d.get('prompt',''), d.get('style','modern')))

@app.route('/api/generate/copy', methods=['POST'])
def gen_copy():
    d = request.json
    return jsonify(ad_gen.generate_ad_copy(d.get('product_name',''), d.get('target_audience',''), d.get('tone','professional')))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
