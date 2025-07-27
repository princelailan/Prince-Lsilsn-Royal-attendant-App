<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Prince Lailan's Royal Attendant Animated README</title>
<style>
  body {
    margin: 0; 
    background: linear-gradient(135deg, #fad0c4 0%, #ffd1ff 100%);
    overflow: hidden;
    font-family: 'Fira Code', monospace;
  }
  canvas {
    display: block;
    margin: auto;
    background: transparent;
  }
</style>
</head>
<body>
<canvas id="canvas" width="900" height="950"></canvas>
<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const WIDTH = canvas.width;
const HEIGHT = canvas.height;

// Sparkles for background
const sparkles = [];
for(let i = 0; i < 120; i++) {
  sparkles.push({
    x: Math.random() * WIDTH,
    y: Math.random() * HEIGHT,
    r: Math.random() * 1.5 + 0.5,
    alpha: Math.random(),
    alphaDir: Math.random() > 0.5 ? 0.01 : -0.01,
  });
}

// Marquee text setup
const marqueeText = "✨ Auto Join + Slay ✨ | 🧠 Smart Cam-Off | 📸 Screenshot Mode | 🐰 Bunny Kingdom UI";
let marqueeX = WIDTH;

// Lines of text to render (with styling info)
const lines = [
  { text: "👑 Prince Lailan's Royal Attendant App 💅", size: 48, color: "#F72585", glow:true, y: 80, center:true },
  { text: "A sassy, girlish, bunny-fied meeting attendant bot made by Joseph Onyango & Daltone Tonny for Gen Z devs who like their tools functional and fabulous.", size: 20, color: "#720026", y: 130, maxWidth: 820, center:true },
  { marquee: true, y: 180, size: 26, color: "#F72585" },
  
  { text: "🌐 Live Preview", size: 32, color: "#F72585", glow:true, y: 250 },
  { text: "👉 Launch the Royal Attendant: https://prince-lailan-royal-attendant-app.netlify.app", size: 18, color: "#720026", y: 280 },
  { text: "\"No more boring joins — just click and let it slay.\"", size: 18, color: "#F72585", italic:true, y: 310 },
  
  { text: "🎯 What This Bot Slays At", size: 28, color: "#F72585", glow:true, y: 350 },
  { text: "✅ Auto-joins Zoom + Google Meet from schedule or link", size: 18, color: "#720026", y: 380 },
  { text: "📴 Turns off cam + mic like a shy princess", size: 18, color: "#720026", y: 405 },
  { text: "🔘 Clicks the Join buttons for you (UI-based detection)", size: 18, color: "#720026", y: 430 },
  { text: "📷 Takes attendance screenshots (saved locally)", size: 18, color: "#720026", y: 455 },
  { text: "🧚‍♀️ Magical girly UI with animated Easter eggs", size: 18, color: "#720026", y: 480 },
  { text: "🕵️ Idle checker to catch ghosted meetings", size: 18, color: "#720026", y: 505 },
  { text: "🗓️ Schedule auto-attend like a queen", size: 18, color: "#720026", y: 530 },
  
  { text: "⚙️ Setup Like Royalty", size: 28, color: "#F72585", glow:true, y: 570 },
  { text: "npm install", size: 18, color: "#720026", y: 600 },
  { text: "npm run dev", size: 18, color: "#720026", y: 625 },
  
  { text: "👯 Meet the Sassy Duo", size: 28, color: "#F72585", glow:true, y: 665 },
  { text: "Joseph Onyango — Lead Dev + UI Overlord 💅 Bunnyfier 👑", size: 18, color: "#720026", y: 700 },
  { text: "Daltone Tonny — AI Tamer & Logic Sorcerer 🔮 Feature King", size: 18, color: "#720026", y: 725 },
  
  { text: "🎥 Pitch Deck", size: 28, color: "#F72585", glow:true, y: 770 },
  { text: "Check out the live deck: https://gamma.app/docs/Royal-Attendant-Bot--ftx9vzwgustviyr", size: 18, color: "#720026", y: 800 },
  
  { text: "💖 Feedback? Suggestions? Add More Sass? Slide into the Issues like it's hot:", size: 20, color: "#F72585", italic:true, y: 840, center:true },
  { text: "https://github.com/princelailan/Prince-Lsilsn-Royal-attendant-App/issues", size: 18, color: "#720026", y: 870, center:true, underline:true }
];

// Text wrap helper
function wrapText(context, text, x, y, maxWidth, lineHeight) {
  const words = text.split(' ');
  let line = '';
  let currentY = y;
  for (let n = 0; n < words.length; n++) {
    const testLine = line + words[n] + ' ';
    const testWidth = context.measureText(testLine).width;
    if (testWidth > maxWidth && n > 0) {
      context.fillText(line, x, currentY);
      line = words[n] + ' ';
      currentY += lineHeight;
    } else {
      line = testLine;
    }
  }
  context.fillText(line, x, currentY);
  return currentY;
}

function draw() {
  ctx.clearRect(0, 0, WIDTH, HEIGHT);

  // Background gradient
  const bgGrad = ctx.createLinearGradient(0, 0, 0, HEIGHT);
  bgGrad.addColorStop(0, '#FAD0C4');
  bgGrad.addColorStop(1, '#FFD1FF');
  ctx.fillStyle = bgGrad;
  ctx.fillRect(0, 0, WIDTH, HEIGHT);

  // Draw sparkles
  sparkles.forEach(s => {
    ctx.beginPath();
    ctx.fillStyle = `rgba(247,37,133,${s.alpha})`;
    ctx.shadowColor = '#F72585';
    ctx.shadowBlur = 10;
    ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
    ctx.fill();

    s.alpha += s.alphaDir;
    if (s.alpha >= 1) s.alphaDir = -0.01;
    else if (s.alpha <= 0) s.alphaDir = 0.01;
  });

  // Draw lines of text
  lines.forEach(line => {
    if(line.marquee){
      ctx.font = `bold ${line.size}px Fira Code`;
      ctx.fillStyle = line.color;
      ctx.shadowColor = '#FF85A1';
      ctx.shadowBlur = 20;
      ctx.textAlign = 'left';
      ctx.fillText(marqueeText, marqueeX, line.y);
      marqueeX -= 2;
      if(marqueeX < -ctx.measureText(marqueeText).width) {
        marqueeX = WIDTH;
      }
      return;
    }
    ctx.font = `${line.italic ? 'italic ' : ''}${line.glow ? 'bold ' : ''}${line.size}px Fira Code`;
    ctx.fillStyle = line.color;
    ctx.shadowColor = line.glow ? '#FF85A1' : 'transparent';
    ctx.shadowBlur = line.glow ? 20 : 0;
    ctx.textAlign = line.center ? 'center' : 'left';

    if(line.maxWidth) {
      let startX = line.center ? WIDTH/2 - line.maxWidth/2 : 40;
      wrapText(ctx, line.text, startX, line.y, line.maxWidth, line.size + 8);
    } else {
      ctx.fillText(line.text, line.center ? WIDTH/2 : 40, line.y);
    }

    if(line.underline) {
      let textWidth = ctx.measureText(line.text).width;
      let startX = line.center ? WIDTH/2 - textWidth/2 : 40;
      ctx.beginPath();
      ctx.strokeStyle = line.color;
      ctx.lineWidth = 2;
      ctx.moveTo(startX, line.y + 5);
      ctx.lineTo(startX + textWidth, line.y + 5);
      ctx.stroke();
    }
  });

  requestAnimationFrame(draw);
}

draw();
</script>
</body>
</html>
