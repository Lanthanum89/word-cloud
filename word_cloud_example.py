
"""
Simple Word Cloud Example
This script demonstrates how to create a word cloud where bigger words represent higher frequency.
"""

import matplotlib.pyplot as plt
from wordcloud import WordCloud

def create_word_cloud(word_frequencies, title="Word Cloud", filename="example_wordcloud.png"):
    """
    Create a word cloud from word frequency data
    
    Args:
        word_frequencies (dict): Dictionary with words as keys and frequencies as values
        title (str): Title for the plot
        filename (str): Filename to save the image
    """
    if not word_frequencies:
        print("No word frequency data provided")
        return
    
    # Create WordCloud object with customized settings
    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color='white',
        colormap='plasma',  # Try: 'viridis', 'plasma', 'inferno', 'magma', 'coolwarm'
        max_words=100,
        relative_scaling=0.5,  # Controls size difference between words
        min_font_size=12,
        max_font_size=120,
        prefer_horizontal=0.8,
        collocations=False,
        margin=10
    ).generate_from_frequencies(word_frequencies)
    
    # Create and display the plot
    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=18, pad=20)
    plt.tight_layout(pad=0)
    
    # Save the image
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Word cloud saved as '{filename}'")
    
    # Display the plot
    plt.show()

def demo_word_cloud():
    """Demonstrate word cloud with sample data"""
    
    # Sample word frequency data - you can replace this with your own data
    sample_data = {
        'python': 45,
        'programming': 35,
        'data': 30,
        'analysis': 25,
        'machine': 22,
        'learning': 20,
        'visualization': 18,
        'science': 16,
        'algorithm': 15,
        'database': 14,
        'artificial': 12,
        'intelligence': 11,
        'code': 10,
        'development': 9,
        'software': 8,
        'engineering': 7,
        'statistics': 6,
        'research': 5,
        'technology': 4,
        'innovation': 3
    }
    
    print("Sample word frequencies:")
    for word, freq in list(sample_data.items())[:10]:
        print(f"  {word}: {freq}")
    
    print("\nCreating word cloud...")
    create_word_cloud(
        sample_data, 
        "Sample Word Cloud - Size = Frequency",
        "sample_wordcloud.png"
    )

if __name__ == "__main__":
    demo_word_cloud()