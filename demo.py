#!/usr/bin/env python3
"""
Demo script for the Word Cloud GUI Application
This script demonstrates how the GUI application works and provides some test URLs
"""

def demo_urls():
    """Return a list of good websites to test with the word cloud GUI"""
    return [
        "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "https://en.wikipedia.org/wiki/Artificial_intelligence", 
        "https://en.wikipedia.org/wiki/Machine_learning",
        "https://www.python.org/about/",
        "https://docs.python.org/3/tutorial/",
        "https://en.wikipedia.org/wiki/Data_science",
        "https://en.wikipedia.org/wiki/Natural_language_processing"
    ]

def print_demo_info():
    """Print information about using the GUI application"""
    print("=== Word Cloud GUI Application Demo ===")
    print("\nThis GUI application creates word clouds from website content!")
    print("\nFeatures:")
    print("• Enter any website URL")
    print("• Automatically scrapes and processes text content")
    print("• Generates beautiful word clouds")
    print("• Customizable colors, word count, and filters")
    print("• Save images as PNG or JPEG")
    
    print("\nSuggested URLs to try:")
    for i, url in enumerate(demo_urls(), 1):
        print(f"{i}. {url}")
    
    print("\nHow to use:")
    print("1. Run: python word_cloud_gui.py")
    print("2. Copy one of the URLs above")
    print("3. Paste it into the URL field")
    print("4. Click 'Generate Word Cloud'")
    print("5. Wait for processing to complete")
    print("6. Optionally adjust settings and regenerate")
    print("7. Save your word cloud image")
    
    print("\nTips:")
    print("• Wikipedia articles work great for testing")
    print("• News websites and blogs are also good sources")
    print("• Some websites may block automated requests")
    print("• Larger websites take longer to process")
    print("• Try different color schemes for variety")

if __name__ == "__main__":
    print_demo_info()