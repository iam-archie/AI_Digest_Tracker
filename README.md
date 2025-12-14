# 🤖 AI Daily Digest

> Automated AI news aggregator that scrapes multiple sources, categorizes content intelligently, and generates beautiful daily digests - solving AI information overload.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40+-green.svg)](https://playwright.dev/python/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)](https://github.com/yourusername/ai-daily-digest/graphs/commit-activity)

## 📋 Table of Contents

- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Customization](#-customization)
- [Scheduling](#-scheduling)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [License](#-license)

## 🎯 The Problem

Staying updated on AI developments is overwhelming:

- 🌊 **Information Overload**: 10+ websites to check daily
- ⏰ **Time Consuming**: 2+ hours spent browsing news sites
- 📰 **Scattered Sources**: Professional news + community discussions spread across platforms
- 🔍 **Signal vs Noise**: Hard to filter relevant AI content from generic tech news
- 📈 **Rapid Evolution**: New models, papers, and startups launching weekly

**Result**: Missing important developments while drowning in information.

## ✨ The Solution

**AI Daily Digest** automates your AI news consumption:

```
Multiple Sources → Smart Scraping → AI Categorization → Beautiful Digest
```

One command generates a personalized HTML digest with:
- ✅ Latest AI news from 5+ specialized sources
- ✅ Intelligent categorization into 8 AI domains
- ✅ Beautiful, responsive design with purple/blue gradient theme
- ✅ Direct links to full articles
- ✅ Source screenshots and JSON export
- ✅ **Time saved: 2 hours → 2 minutes**

## 🚀 Features

### Multi-Source Aggregation
- **VentureBeat AI** - Industry and business news
- **MIT Technology Review AI** - In-depth analysis and research
- **The Decoder** - Latest AI model releases
- **Reddit r/artificial** - AI community discussions
- **Reddit r/MachineLearning** - Research and papers
- **Hacker News** - AI-filtered tech stories

### Intelligent AI Categorization
- 💬 **LLMs & Chatbots** - GPT, Claude, Gemini, language models
- 👁️ **Computer Vision & Image Gen** - DALL-E, Stable Diffusion, Midjourney
- 🔬 **AI Research** - Papers, benchmarks, models, training
- ⚖️ **AI Ethics & Safety** - Alignment, regulation, bias, fairness
- 💼 **AI Business & Industry** - Startups, funding, enterprise AI
- 🤖 **AI Agents & Automation** - Autonomous systems, tool use
- ⚡ **AI Hardware** - GPUs, chips, compute infrastructure
- 🧠 **General AI News** - Everything else AI-related

### Beautiful Output
- 📊 **Stats Dashboard** - Article count, categories, sources
- 🎨 **Modern Design** - Purple/blue gradient, card-based layout
- 📱 **Responsive** - Works perfectly on desktop and mobile
- 📸 **Screenshots** - Visual previews of news sources
- 💾 **Data Export** - JSON format for further analysis

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-daily-digest.git
cd ai-daily-digest
```

2. **Install dependencies**
```bash
pip install playwright
```

3. **Install browser drivers**
```bash
playwright install chromium
```

4. **Run the script**
```bash
python ai_daily_digest.py
```

5. **Open the digest**
```bash
# The script will create a folder like: ai_digest_20241214_143052/
# Open ai_digest.html in your browser
```

## 💻 Usage

### Basic Usage
```bash
python ai_daily_digest.py
```

### Terminal Output Example
```bash
🤖 AI DAILY DIGEST - YOUR PERSONALIZED AI NEWS ROUNDUP
======================================================================

🤖 Scraping VentureBeat AI...
  ✓ OpenAI releases GPT-4.5 with improved reasoning capabilities...
  ✓ Anthropic's Claude 3.5 surpasses benchmarks in coding tasks...
✅ Scraped 12 AI articles from VentureBeat

🎓 Scraping MIT Technology Review AI...
  ✓ New research breakthrough in AI alignment techniques...
✅ Scraped 10 AI articles from MIT Tech Review

✅ AI NEWS AGGREGATION COMPLETE!
======================================================================
📊 Statistics:
   Total AI Articles: 45
   AI Categories: 7
   AI Sources: 5

💡 Open ai_digest.html in your browser to read your AI news digest!
```

### Headless Mode (Faster)
Edit the script (line ~430):
```python
browser = p.chromium.launch(headless=True)  # No browser window
```

## ⚙️ Configuration

### Adding New AI Sources

```python
def scrape_custom_ai_source(self, page):
    """Scrape from your favorite AI news site"""
    print("\n📰 Scraping Custom AI Source...")
    
    try:
        page.goto("https://your-ai-news-site.com", timeout=30000)
        articles = page.locator('article h2 a').all()
        
        for article in articles[:10]:
            headline = article.text_content().strip()
            link = article.get_attribute('href')
            # Process article...
            
    except Exception as e:
        print(f"❌ Error: {e}")

# Add to run_aggregation():
self.scrape_custom_ai_source(page)
```

### Filtering by Interest

```python
# Only show specific categories
interested_categories = ['LLMs & Chatbots', 'AI Research']
self.articles = [a for a in self.articles 
                 if a['category'] in interested_categories]
```

## 📁 Project Structure

```
ai-daily-digest/
│
├── ai_daily_digest.py          # Main script
├── requirements.txt             # Python dependencies
├── README.md                    # Documentation
├── LICENSE                      # MIT License
│
└── ai_digest_YYYYMMDD_HHMMSS/  # Generated output
    ├── ai_digest.html          # Beautiful HTML digest ⭐
    ├── ai_news_data.json       # Raw data export
    └── *.png                   # Source screenshots
```

## ⏰ Scheduling

### Linux/macOS (crontab)

```bash
# Run daily at 7 AM
crontab -e

# Add this line:
0 7 * * * cd /path/to/ai-daily-digest && python3 ai_daily_digest.py
```

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task → "AI Daily Digest"
3. Trigger: Daily at 7:00 AM
4. Action: Start `python.exe` with argument `ai_daily_digest.py`

## 🎨 Customization

### Change Theme Colors

```python
# In generate_html_digest(), modify CSS:
background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);

# Try different gradients:
# Green: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
# Orange: linear-gradient(135deg, #ff6a00 0%, #ee0979 100%);
```

### Add Custom Categories

```python
# In categorize_ai_article():
robotics_keywords = ['robot', 'robotics', 'autonomous vehicle', 'drone']

if any(keyword in headline_lower for keyword in robotics_keywords):
    return 'AI Robotics'
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contribution
- Add new AI news sources
- Improve categorization accuracy
- Enhance UI/UX design
- Add email delivery feature
- Implement sentiment analysis
- Create browser extension

## 🗺️ Roadmap

### Version 2.0
- [ ] Email delivery integration
- [ ] Sentiment analysis for articles
- [ ] Trend detection over time
- [ ] More AI sources (ArXiv, Papers With Code)
- [ ] Slack/Discord notifications

### Version 3.0
- [ ] AI-powered article summarization
- [ ] Personalized recommendations
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Browser extension

## 📊 Performance

- **Execution Time**: 2-3 minutes
- **Articles Scraped**: 40-60 per run
- **Categorization Accuracy**: 85%+
- **Time Saved**: 2 hours → 2 minutes daily
- **Memory Usage**: ~200MB
- **Storage**: ~5MB per digest

## 🐛 Troubleshooting

**Issue**: Website selectors not working
**Solution**: Sites change their HTML. Check issues or update selectors.

**Issue**: "Playwright not found"
**Solution**: Run `pip install playwright && playwright install chromium`

**Issue**: Timeout errors
**Solution**: Increase timeout: `page.goto(url, timeout=60000)`

**Issue**: Too few AI articles
**Solution**: Expand AI keywords or add more sources

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

You can use, modify, and distribute this project freely.

## 🙏 Acknowledgments

- Playwright Team - Excellent automation framework
- AI News Sources - VentureBeat, MIT Tech Review, The Decoder
- Python Community - Amazing ecosystem
- All Contributors - Thank you!

## 🌟 Support

If this project helps you:

- ⭐ Star this repository
- 🔗 Share on social media
- 📝 Write about your experience
- 🐛 Report bugs or suggest features

## 📧 Contact

- **Author**: Sathish
- **GitHub**: @https://github.com/iam-archie/
- **Email**: sathishaiops@gmail.com

## 💡 Inspiration

Built while transitioning from DevOps to Gen AI architecture. Spending 2+ hours daily browsing AI news was unsustainable. This tool solves that problem.

**Philosophy**: The best automation projects solve YOUR pain points first.

---

<div align="center">

**Made with ❤️ for the AI community**

[⬆ Back to Top](#-ai-daily-digest)

</div>
