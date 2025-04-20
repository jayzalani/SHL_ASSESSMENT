
import requests
from bs4 import BeautifulSoup
import re
import csv

# Target URL for SHL catalog
TARGET_URL = "https://www.shl.com/solutions/products/product-catalog/"

# Initialize the list of discovered URLs
urls_to_visit = [TARGET_URL]
visited_urls = set()

# Regex for assessment page URLs
assessment_pattern = re.compile(r'/solutions/products/product-catalog/view/[^/]+/?$')

# Storage for scraped data
assessments_data = []

# Crawl limit
MAX_CRAWL = 50


assessment_type_map = {
    'A': 'Ability & Aptitude',
    'B': 'Biodata & Situational Judgement',
    'C': 'Competencies',
    'D': 'Development & 360',
    'E': 'Assessment Exercises',
    'K': 'Knowledge & Skills',
    'P': 'Personality & Behavior',
    'S': 'Simulations'
}


def crawler():
    crawl_count = 0
    while urls_to_visit and crawl_count < MAX_CRAWL:
        current_url = urls_to_visit.pop(0)
        if current_url in visited_urls:
            continue
        visited_urls.add(current_url)
        print(f"Visiting: {current_url}")

        try:
            response = requests.get(current_url)
            response.raise_for_status()
        except Exception as e:
            print(f"Error fetching {current_url}: {e}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")

        # Enqueue new links
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('/'):
                absolute = f"https://www.shl.com{href}"
            else:
                absolute = requests.compat.urljoin(current_url, href)
            if absolute.startswith("https://www.shl.com") and absolute not in visited_urls:
                if assessment_pattern.search(absolute):
                    urls_to_visit.insert(0, absolute)
                elif "/solutions/products/product-catalog/" in absolute:
                    urls_to_visit.append(absolute)

        # Scrape details if it's an assessment page
        if assessment_pattern.search(current_url):
            try:
                title_el = soup.find('h1') or soup.find('h2', class_='product-title')
                title = title_el.get_text(strip=True) if title_el else "Unknown Assessment"

                # Description
                desc_el = soup.find('div', class_='description') or soup.find('div', id='description')
                if desc_el:
                    description = desc_el.get_text(strip=True)
                else:
                    main_area = soup.find('main') or soup.find('div', class_='content-area')
                    paragraphs = main_area.find_all('p') if main_area else []
                    description = paragraphs[0].get_text(strip=True) if paragraphs else ""

                # Duration: improved extraction by scanning <p> tags
                duration = 0
                for p in soup.find_all('p'):
                    text = p.get_text(strip=True)
                    if re.search(r'Approximate Completion Time in minutes|Assessment length', text, re.IGNORECASE):
                        # Extract first integer found
                        num_match = re.search(r'(\d+)', text)
                        if num_match:
                            duration = int(num_match.group(1))
                            break

                # Test Types
                test_types = []
                type_label = soup.find(text=re.compile(r'Test Type:', re.IGNORECASE))
                if type_label:
                    parent = type_label.parent
                    for indicator in parent.find_all(text=re.compile(r'[A-Z]')):
                        for ch in indicator.strip():
                            if ch in assessment_type_map:
                                test_types.append(assessment_type_map[ch])

                # Remote Testing
                remote_support = 'No'
                remote_label = soup.find(text=re.compile(r'Remote Testing:', re.IGNORECASE))
                if remote_label and remote_label.parent.find('span', class_=re.compile(r'green|circle|dot|indicator')):
                    remote_support = 'Yes'

                # Adaptive/IRT (default No; extend if available)
                adaptive_support = 'No'

                assessments_data.append({
                    'url': current_url,
                    'title': title,
                    'description': description,
                    'duration': duration,
                    'test_type': test_types,
                    'remote_support': remote_support,
                    'adaptive_support': adaptive_support
                })
                print(f"Extracted: {title} ({duration} min)")

            except Exception as e:
                print(f"Error extracting data from {current_url}: {e}")

        crawl_count += 1

# Run crawler and save to CSV
crawler()

with open('shl_assessments.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['url', 'title', 'description', 'duration', 'test_type', 'remote_support', 'adaptive_support']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for item in assessments_data:
        row = item.copy()
        row['test_type'] = ', '.join(item['test_type'])
        writer.writerow(row)

print(f"Saved {len(assessments_data)} assessments to CSV.")
