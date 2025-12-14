"""
AI News Daily Digest - Playwright Automation
Author: Sathish
Purpose: Automatically scrape AI-related news from multiple specialized sources
         and create a personalized daily AI digest
"""

from playwright.sync_api import sync_playwright
import json
from datetime import datetime
import os
import re
from collections import defaultdict

class AIDailyDigest:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_dir = f"ai_digest_{self.timestamp}"
        os.makedirs(self.report_dir, exist_ok=True)
        self.articles = []
        self.categories = defaultdict(list)
        
    def scrape_venturebeat_ai(self, page):
        """Scrape AI news from VentureBeat AI section"""
        print("\n🤖 Scraping VentureBeat AI...")
        
        try:
            page.goto("https://venturebeat.com/ai/", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2000)
            
            # Find article headlines
            articles = page.locator('article').all()
            
            count = 0
            for article in articles[:12]:
                try:
                    # Find headline within article
                    headline_elem = article.locator('h2 a, h3 a').first
                    if headline_elem.count() > 0:
                        text = headline_elem.text_content().strip()
                        link = headline_elem.get_attribute('href')
                        
                        if text and len(text) > 20:
                            if link and not link.startswith('http'):
                                link = f"https://venturebeat.com{link}"
                            
                            article_data = {
                                'source': 'VentureBeat AI',
                                'headline': text,
                                'link': link,
                                'category': self.categorize_ai_article(text),
                                'scraped_at': datetime.now().isoformat()
                            }
                            
                            self.articles.append(article_data)
                            self.categories[article_data['category']].append(article_data)
                            count += 1
                            print(f"  ✓ {text[:60]}...")
                        
                except Exception as e:
                    continue
            
            print(f"✅ Scraped {count} AI articles from VentureBeat")
            
        except Exception as e:
            print(f"❌ Error scraping VentureBeat AI: {e}")
    
    def scrape_mit_tech_review_ai(self, page):
        """Scrape AI news from MIT Technology Review"""
        print("\n🎓 Scraping MIT Technology Review AI...")
        
        try:
            page.goto("https://www.technologyreview.com/topic/artificial-intelligence/", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2000)
            
            # Find article links
            article_links = page.locator('h3 a, h2 a').all()
            
            count = 0
            for link_elem in article_links[:12]:
                try:
                    headline = link_elem.text_content().strip()
                    link = link_elem.get_attribute('href')
                    
                    if headline and link and len(headline) > 20:
                        if not link.startswith('http'):
                            link = f"https://www.technologyreview.com{link}"
                        
                        article_data = {
                            'source': 'MIT Tech Review',
                            'headline': headline,
                            'link': link,
                            'category': self.categorize_ai_article(headline),
                            'scraped_at': datetime.now().isoformat()
                        }
                        
                        self.articles.append(article_data)
                        self.categories[article_data['category']].append(article_data)
                        count += 1
                        print(f"  ✓ {headline[:60]}...")
                        
                except Exception as e:
                    continue
            
            print(f"✅ Scraped {count} AI articles from MIT Tech Review")
            
        except Exception as e:
            print(f"❌ Error scraping MIT Tech Review: {e}")
    
    def scrape_reddit_ai(self, page):
        """Scrape AI discussions from Reddit r/artificial and r/MachineLearning"""
        print("\n🔥 Scraping Reddit AI Communities...")
        
        subreddits = ['artificial', 'MachineLearning']
        
        for subreddit in subreddits:
            try:
                page.goto(f"https://www.reddit.com/r/{subreddit}", wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3000)
                
                # Find post titles
                posts = page.locator('h3').all()
                
                count = 0
                for post in posts[:8]:
                    try:
                        title = post.text_content().strip()
                        
                        if len(title) > 20 and not title.startswith('r/'):
                            # Try to find the link
                            parent_link = post.locator('xpath=ancestor::a').first
                            link = parent_link.get_attribute('href') if parent_link.count() > 0 else ""
                            
                            if link and not link.startswith('http'):
                                link = f"https://www.reddit.com{link}"
                            
                            article_data = {
                                'source': f'Reddit r/{subreddit}',
                                'headline': title,
                                'link': link,
                                'category': self.categorize_ai_article(title),
                                'scraped_at': datetime.now().isoformat()
                            }
                            
                            self.articles.append(article_data)
                            self.categories[article_data['category']].append(article_data)
                            count += 1
                            print(f"  ✓ r/{subreddit}: {title[:50]}...")
                            
                    except Exception as e:
                        continue
                
                print(f"✅ Scraped {count} posts from r/{subreddit}")
                
            except Exception as e:
                print(f"❌ Error scraping r/{subreddit}: {e}")
    
    def scrape_hacker_news_ai(self, page):
        """Scrape AI-related stories from Hacker News"""
        print("\n🚀 Scraping Hacker News (AI filtered)...")
        
        try:
            page.goto("https://news.ycombinator.com", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2000)
            
            # Find story titles
            story_links = page.locator('span.titleline > a').all()
            
            # AI-related keywords for filtering
            ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning',
                          'neural', 'gpt', 'llm', 'chatgpt', 'openai', 'anthropic', 'claude',
                          'gemini', 'transformer', 'diffusion', 'gen ai', 'generative']
            
            count = 0
            for link_elem in story_links[:30]:  # Check more stories to find AI ones
                try:
                    headline = link_elem.text_content().strip()
                    link = link_elem.get_attribute('href')
                    
                    # Filter for AI-related content
                    headline_lower = headline.lower()
                    if any(keyword in headline_lower for keyword in ai_keywords):
                        # Make relative links absolute
                        if link and not link.startswith('http'):
                            link = f"https://news.ycombinator.com/{link}"
                        
                        if headline and link:
                            article_data = {
                                'source': 'Hacker News',
                                'headline': headline,
                                'link': link,
                                'category': self.categorize_ai_article(headline),
                                'scraped_at': datetime.now().isoformat()
                            }
                            
                            self.articles.append(article_data)
                            self.categories[article_data['category']].append(article_data)
                            count += 1
                            print(f"  ✓ {headline[:60]}...")
                        
                except Exception as e:
                    continue
            
            print(f"✅ Scraped {count} AI-related stories from Hacker News")
            
        except Exception as e:
            print(f"❌ Error scraping Hacker News: {e}")
    
    def scrape_the_decoder(self, page):
        """Scrape AI news from The Decoder"""
        print("\n📡 Scraping The Decoder...")
        
        try:
            page.goto("https://the-decoder.com", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2000)
            
            # Find article headlines
            article_links = page.locator('h2.entry-title a, h3.entry-title a').all()
            
            count = 0
            for link_elem in article_links[:10]:
                try:
                    headline = link_elem.text_content().strip()
                    link = link_elem.get_attribute('href')
                    
                    if headline and link and len(headline) > 15:
                        article_data = {
                            'source': 'The Decoder',
                            'headline': headline,
                            'link': link,
                            'category': self.categorize_ai_article(headline),
                            'scraped_at': datetime.now().isoformat()
                        }
                        
                        self.articles.append(article_data)
                        self.categories[article_data['category']].append(article_data)
                        count += 1
                        print(f"  ✓ {headline[:60]}...")
                        
                except Exception as e:
                    continue
            
            print(f"✅ Scraped {count} AI articles from The Decoder")
            
        except Exception as e:
            print(f"❌ Error scraping The Decoder: {e}")
    
    def categorize_ai_article(self, headline):
        """Categorize AI articles into specific AI domains"""
        headline_lower = headline.lower()
        
        # LLMs & Chatbots
        llm_keywords = ['llm', 'gpt', 'chatgpt', 'claude', 'gemini', 'language model',
                       'chatbot', 'chat', 'openai', 'anthropic', 'transformer', 
                       'prompt', 'token', 'reasoning']
        
        # Computer Vision & Image Gen
        vision_keywords = ['vision', 'image', 'dalle', 'midjourney', 'stable diffusion',
                          'diffusion', 'video', 'visual', 'image generation', 'picture',
                          'photograph', 'sora', 'gan']
        
        # ML Research & Models
        research_keywords = ['research', 'paper', 'arxiv', 'model', 'training', 'dataset',
                            'benchmark', 'algorithm', 'neural', 'deep learning', 
                            'machine learning', 'reinforcement learning']
        
        # AI Ethics & Safety
        ethics_keywords = ['ethics', 'safety', 'alignment', 'bias', 'fairness', 
                          'regulation', 'policy', 'risk', 'governance', 'responsible ai',
                          'ai safety', 'misuse', 'deepfake']
        
        # Business & Industry
        business_keywords = ['startup', 'funding', 'investment', 'company', 'enterprise',
                            'business', 'market', 'revenue', 'acquisition', 'launch',
                            'product', 'service']
        
        # AI Agents & Automation
        agents_keywords = ['agent', 'automation', 'autonomous', 'robot', 'workflow',
                          'tool use', 'function calling', 'orchestration', 'agentic']
        
        # Hardware & Infrastructure
        hardware_keywords = ['gpu', 'chip', 'hardware', 'nvidia', 'tpu', 'compute',
                            'infrastructure', 'data center', 'semiconductor']
        
        # Check categories
        if any(keyword in headline_lower for keyword in llm_keywords):
            return 'LLMs & Chatbots'
        elif any(keyword in headline_lower for keyword in vision_keywords):
            return 'Computer Vision & Image Gen'
        elif any(keyword in headline_lower for keyword in ethics_keywords):
            return 'AI Ethics & Safety'
        elif any(keyword in headline_lower for keyword in agents_keywords):
            return 'AI Agents & Automation'
        elif any(keyword in headline_lower for keyword in business_keywords):
            return 'AI Business & Industry'
        elif any(keyword in headline_lower for keyword in hardware_keywords):
            return 'AI Hardware'
        elif any(keyword in headline_lower for keyword in research_keywords):
            return 'AI Research'
        else:
            return 'General AI News'
    

    def take_source_screenshots(self, page, sources):
        """Capture screenshots of AI news sources"""
        print("\n📸 Capturing AI source screenshots...")
        
        screenshots = {}
        
        for source_name, url in sources.items():
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(2000)
                
                screenshot_path = os.path.join(self.report_dir, f"{source_name.lower().replace(' ', '_')}.png")
                page.screenshot(path=screenshot_path, full_page=False)
                screenshots[source_name] = screenshot_path
                print(f"  ✓ {source_name} screenshot saved")
                
            except Exception as e:
                print(f"  ⚠️ Failed to screenshot {source_name}: {e}")
        
        return screenshots
    
    def generate_html_digest(self, screenshots):
        """Generate beautiful HTML AI news digest"""
        print("\n📊 Generating AI HTML digest...")
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Daily Digest - {datetime.now().strftime('%B %d, %Y')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
            padding: 20px;
            color: #333;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
            color: white;
            padding: 50px 40px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        .header .tagline {{
            font-size: 1.2em;
            opacity: 0.95;
            font-weight: 300;
            margin-bottom: 10px;
        }}
        .header .date {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .header .stats {{
            margin-top: 20px;
            display: flex;
            justify-content: center;
            gap: 40px;
            font-size: 1.1em;
        }}
        .stat {{
            background: rgba(255,255,255,0.2);
            padding: 15px 30px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }}
        .stat strong {{
            display: block;
            font-size: 2em;
            margin-bottom: 5px;
        }}
        .content {{
            padding: 40px;
        }}
        .category-section {{
            margin-bottom: 50px;
        }}
        .category-header {{
            display: flex;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid #7e22ce;
        }}
        .category-icon {{
            font-size: 2em;
            margin-right: 15px;
        }}
        .category-title {{
            font-size: 2em;
            color: #7e22ce;
            font-weight: 700;
        }}
        .category-count {{
            margin-left: auto;
            background: #7e22ce;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        .articles-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}
        .article-card {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 25px;
            transition: all 0.3s ease;
            border-left: 4px solid #7e22ce;
            cursor: pointer;
        }}
        .article-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(126, 34, 206, 0.2);
            background: white;
        }}
        .article-source {{
            display: inline-block;
            background: #7e22ce;
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: 600;
            margin-bottom: 12px;
        }}
        .article-headline {{
            font-size: 1.2em;
            color: #2c3e50;
            margin-bottom: 12px;
            font-weight: 600;
            line-height: 1.4;
        }}
        .article-link {{
            color: #7e22ce;
            text-decoration: none;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            font-size: 0.9em;
        }}
        .article-link:hover {{
            text-decoration: underline;
        }}
        .article-link::after {{
            content: ' →';
            margin-left: 5px;
        }}
        .screenshots-section {{
            margin-top: 50px;
            padding-top: 40px;
            border-top: 2px solid #e0e0e0;
        }}
        .screenshots-title {{
            font-size: 2em;
            color: #7e22ce;
            margin-bottom: 25px;
            text-align: center;
        }}
        .screenshots-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
        }}
        .screenshot-card {{
            background: #f8f9fa;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .screenshot-card img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .screenshot-label {{
            padding: 15px;
            text-align: center;
            font-weight: 600;
            background: white;
            color: #7e22ce;
        }}
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .footer p {{
            margin: 5px 0;
        }}
        .empty-category {{
            text-align: center;
            padding: 40px;
            color: #999;
            font-style: italic;
        }}
        
        @media (max-width: 768px) {{
            .articles-grid {{
                grid-template-columns: 1fr;
            }}
            .screenshots-grid {{
                grid-template-columns: 1fr;
            }}
            .header h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Daily Digest</h1>
            <p class="tagline">Your Personalized Artificial Intelligence News Roundup</p>
            <p class="date">{datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}</p>
            <div class="stats">
                <div class="stat">
                    <strong>{len(self.articles)}</strong>
                    <span>AI Articles</span>
                </div>
                <div class="stat">
                    <strong>{len(self.categories)}</strong>
                    <span>AI Categories</span>
                </div>
                <div class="stat">
                    <strong>{len(set(article['source'] for article in self.articles))}</strong>
                    <span>AI Sources</span>
                </div>
            </div>
        </div>
        <div class="content">
"""
        
        # AI Category icons
        category_icons = {
            'LLMs & Chatbots': '💬',
            'Computer Vision & Image Gen': '👁️',
            'AI Research': '🔬',
            'AI Ethics & Safety': '⚖️',
            'AI Business & Industry': '💼',
            'AI Agents & Automation': '🤖',
            'AI Hardware': '⚡',
            'General AI News': '🧠'
        }
        
        # Sort categories by article count
        sorted_categories = sorted(self.categories.items(), 
                                   key=lambda x: len(x[1]), 
                                   reverse=True)
        
        # Generate category sections
        for category, articles in sorted_categories:
            if articles:
                icon = category_icons.get(category, '📄')
                html_content += f"""
            <div class="category-section">
                <div class="category-header">
                    <span class="category-icon">{icon}</span>
                    <h2 class="category-title">{category}</h2>
                    <span class="category-count">{len(articles)} articles</span>
                </div>
                <div class="articles-grid">
"""
                
                for article in articles:
                    html_content += f"""
                    <div class="article-card">
                        <span class="article-source">{article['source']}</span>
                        <h3 class="article-headline">{article['headline']}</h3>
                        <a href="{article['link']}" target="_blank" class="article-link">Read Full Article</a>
                    </div>
"""
                
                html_content += """
                </div>
            </div>
"""
        
        # Add screenshots section
        if screenshots:
            html_content += """
            <div class="screenshots-section">
                <h2 class="screenshots-title">📸 Source Screenshots</h2>
                <div class="screenshots-grid">
"""
            
            for source, path in screenshots.items():
                filename = os.path.basename(path)
                html_content += f"""
                    <div class="screenshot-card">
                        <img src="{filename}" alt="{source}">
                        <div class="screenshot-label">{source}</div>
                    </div>
"""
            
            html_content += """
                </div>
            </div>
"""
        
        html_content += f"""
        </div>
        <div class="footer">
            <p><strong>AI Daily Digest</strong></p>
            <p>Powered by Playwright Automation | Curated AI News</p>
            <p>Stay updated on the latest in Artificial Intelligence! 🤖</p>
            <p style="margin-top: 15px; font-size: 0.9em; opacity: 0.8;">
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </div>
    </div>
</body>
</html>
"""
        
        report_path = os.path.join(self.report_dir, "ai_digest.html")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ AI HTML digest saved: {report_path}")
        return report_path
    
    def save_json_data(self):
        """Save raw AI news data as JSON"""
        json_path = os.path.join(self.report_dir, "ai_news_data.json")
        
        data = {
            'generated_at': datetime.now().isoformat(),
            'total_articles': len(self.articles),
            'categories': {cat: len(articles) for cat, articles in self.categories.items()},
            'articles': self.articles
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON data saved: {json_path}")
        return json_path
    
    def run_aggregation(self):
        """Run the complete AI news aggregation"""
        print("\n" + "=" * 70)
        print("🤖 AI DAILY DIGEST - YOUR PERSONALIZED AI NEWS ROUNDUP")
        print("=" * 70)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()
            
            try:
                # Scrape from AI-focused sources
                self.scrape_venturebeat_ai(page)
                self.scrape_mit_tech_review_ai(page)
                self.scrape_the_decoder(page)
                self.scrape_reddit_ai(page)
                self.scrape_hacker_news_ai(page)
                
                # Take screenshots
                print("\n" + "=" * 70)
                sources = {
                    'VentureBeat AI': 'https://venturebeat.com/ai/',
                    'MIT Tech Review AI': 'https://www.technologyreview.com/topic/artificial-intelligence/',
                    'The Decoder': 'https://the-decoder.com',
                    'Reddit r/artificial': 'https://www.reddit.com/r/artificial',
                    'Hacker News': 'https://news.ycombinator.com'
                }
                screenshots = self.take_source_screenshots(page, sources)
                
            finally:
                browser.close()
        
        # Generate reports
        print("\n" + "=" * 70)
        print("📊 GENERATING AI DIGEST")
        print("=" * 70)
        
        html_report = self.generate_html_digest(screenshots)
        json_data = self.save_json_data()
        
        # Summary
        print("\n" + "=" * 70)
        print("✅ AI NEWS AGGREGATION COMPLETE!")
        print("=" * 70)
        print(f"\n📊 Statistics:")
        print(f"   Total AI Articles: {len(self.articles)}")
        print(f"   AI Categories: {len(self.categories)}")
        print(f"   AI Sources: {len(set(article['source'] for article in self.articles))}")
        print(f"\n📁 Files saved in: {self.report_dir}/")
        print(f"   - AI HTML Digest: ai_digest.html")
        print(f"   - AI JSON Data: ai_news_data.json")
        print(f"   - Screenshots: *.png files")
        print("\n💡 Open ai_digest.html in your browser to read your AI news digest!")
        print("=" * 70 + "\n")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🤖 WELCOME TO AI DAILY DIGEST")
    print("=" * 70)
    print("\nYour personalized daily roundup of AI news and developments!")
    print("This tool will:")
    print("  ✓ Scrape AI news from VentureBeat, MIT Tech Review, The Decoder")
    print("  ✓ Filter AI discussions from Reddit (r/artificial, r/MachineLearning)")
    print("  ✓ Find AI stories on Hacker News")
    print("  ✓ Categorize by AI domains (LLMs, Vision, Research, Ethics, etc.)")
    print("  ✓ Create a beautiful personalized AI digest")
    print("\n⚠️  Note: This will open a browser and visit AI news websites.")
    print("=" * 70 + "\n")
    
    user_input = input("Press ENTER to start AI news aggregation or 'q' to quit: ")
    
    if user_input.lower() != 'q':
        aggregator = AIDailyDigest()
        aggregator.run_aggregation()
    else:
        print("\n👋 Goodbye! Stay updated on AI!")
