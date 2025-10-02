#!/usr/bin/env python3
"""
Word Cloud GUI Application
This application provides a modern graphical interface for creating word clouds from website content.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from wordcloud import WordCloud
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import threading
from urllib.parse import urlparse
import os
import random

class ModernWordCloudGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Cloud Generator | v2.0")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Modern color scheme
        self.colors = {
            'primary': '#2c3e50',      # Dark blue-gray
            'secondary': '#3498db',     # Blue
            'accent': '#e74c3c',       # Red
            'success': '#27ae60',      # Green
            'warning': '#f39c12',      # Orange
            'light': '#ecf0f1',        # Light gray
            'dark': '#34495e',         # Dark gray
            'white': '#ffffff',
            'text': '#2c3e50'
        }
        
        # Configure root styling
        self.root.configure(bg=self.colors['light'])
        
        # Configure modern ttk styling
        self.setup_styles()
        
        # Variables
        self.word_frequencies = {}
        self.current_wordcloud = None
        self.processing = False
        
        # Create GUI elements
        self.create_widgets()
        
        # Add keyboard shortcuts
        self.setup_shortcuts()
        
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        
        # Configure modern button style
        style.configure('Modern.TButton',
                       padding=(20, 10),
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0)
        
        # Configure accent button style
        style.configure('Accent.TButton',
                       padding=(25, 12),
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0)
        
        # Configure label style
        style.configure('Modern.TLabel',
                       font=('Segoe UI', 10),
                       background=self.colors['white'],
                       foreground=self.colors['text'])
        
        # Configure heading style
        style.configure('Heading.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       background=self.colors['white'],
                       foreground=self.colors['primary'])
        
        # Configure entry style
        style.configure('Modern.TEntry',
                       padding=(10, 8),
                       font=('Segoe UI', 10),
                       borderwidth=1,
                       relief='solid')
        
        # Configure combobox style
        style.configure('Modern.TCombobox',
                       padding=(10, 8),
                       font=('Segoe UI', 10))
        
        # Configure frame style
        style.configure('Card.TFrame',
                       background=self.colors['white'],
                       relief='solid',
                       borderwidth=1)
        
        # Configure labelframe style
        style.configure('Card.TLabelframe',
                       background=self.colors['white'],
                       relief='solid',
                       borderwidth=1)
        
        style.configure('Card.TLabelframe.Label',
                       font=('Segoe UI', 11, 'bold'),
                       background=self.colors['white'],
                       foreground=self.colors['primary'])

    def create_widgets(self):
        """Create and arrange modern GUI widgets"""
        
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['light'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        header_frame = tk.Frame(main_container, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # App title
        title_label = tk.Label(header_frame, 
                              text="Word Cloud Generator",
                              font=('Segoe UI', 18, 'bold'),
                              bg=self.colors['primary'],
                              fg=self.colors['white'])
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame,
                                 text="Transform website content into beautiful visualisations",
                                 font=('Segoe UI', 10),
                                 bg=self.colors['primary'],
                                 fg=self.colors['light'])
        subtitle_label.pack()
        
        # Content area
        content_frame = tk.Frame(main_container, bg=self.colors['light'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for controls
        left_panel = tk.Frame(content_frame, bg=self.colors['light'], width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Right panel for visualization
        right_panel = tk.Frame(content_frame, bg=self.colors['light'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # === LEFT PANEL CONTENT ===
        
        # URL Input Card
        url_card = ttk.LabelFrame(left_panel, text="Website URL", style='Card.TLabelframe', padding=20)
        url_card.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(url_card, text="Enter website URL:", style='Modern.TLabel').pack(anchor=tk.W, pady=(0, 8))
        
        url_frame = tk.Frame(url_card, bg=self.colors['white'])
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.url_var = tk.StringVar(value="https://en.wikipedia.org/wiki/Artificial_intelligence")
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, style='Modern.TEntry', width=35)
        self.url_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Generate button
        self.generate_btn = ttk.Button(url_frame, text="Generate Word Cloud", 
                                      command=self.generate_wordcloud, style='Accent.TButton')
        self.generate_btn.pack(fill=tk.X)
        
        # Progress bar
        self.progress = ttk.Progressbar(url_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(10, 0))
        
        # Options Card
        options_card = ttk.LabelFrame(left_panel, text="Customisation Options", style='Card.TLabelframe', padding=20)
        options_card.pack(fill=tk.X, pady=(0, 15))
        
        # Word count options
        words_frame = tk.Frame(options_card, bg=self.colors['white'])
        words_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(words_frame, text="Maximum Words:", style='Modern.TLabel').pack(anchor=tk.W)
        self.max_words_var = tk.StringVar(value="150")
        max_words_entry = ttk.Entry(words_frame, textvariable=self.max_words_var, style='Modern.TEntry', width=10)
        max_words_entry.pack(anchor=tk.W, pady=(5, 0))
        
        # Minimum word length
        length_frame = tk.Frame(options_card, bg=self.colors['white'])
        length_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(length_frame, text="Minimum Word Length:", style='Modern.TLabel').pack(anchor=tk.W)
        self.min_length_var = tk.StringVar(value="3")
        min_length_entry = ttk.Entry(length_frame, textvariable=self.min_length_var, style='Modern.TEntry', width=10)
        min_length_entry.pack(anchor=tk.W, pady=(5, 0))
        
        # Color scheme
        color_frame = tk.Frame(options_card, bg=self.colors['white'])
        color_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(color_frame, text="Color Scheme:", style='Modern.TLabel').pack(anchor=tk.W)
        self.colormap_var = tk.StringVar(value="viridis")
        colormap_combo = ttk.Combobox(color_frame, textvariable=self.colormap_var, style='Modern.TCombobox', width=20)
        colormap_combo['values'] = ('viridis', 'plasma', 'inferno', 'magma', 'coolwarm', 'tab10', 'Set3', 'rainbow', 'spring', 'summer')
        colormap_combo.pack(anchor=tk.W, pady=(5, 0))
        colormap_combo.state(['readonly'])
        colormap_combo.bind('<<ComboboxSelected>>', self.refresh_wordcloud_style)
        
        # Background color
        bg_frame = tk.Frame(options_card, bg=self.colors['white'])
        bg_frame.pack(fill=tk.X)
        
        ttk.Label(bg_frame, text="Background Color:", style='Modern.TLabel').pack(anchor=tk.W)
        self.background_var = tk.StringVar(value="white")
        bg_combo = ttk.Combobox(bg_frame, textvariable=self.background_var, style='Modern.TCombobox', width=20)
        bg_combo['values'] = ('white', 'black', 'lightgray', 'navy', 'darkgreen', 'darkblue', 'maroon')
        bg_combo.pack(anchor=tk.W, pady=(5, 0))
        bg_combo.state(['readonly'])
        bg_combo.bind('<<ComboboxSelected>>', self.refresh_wordcloud_style)
        
        # Action Buttons Card
        actions_card = ttk.LabelFrame(left_panel, text="Actions", style='Card.TLabelframe', padding=20)
        actions_card.pack(fill=tk.X, pady=(0, 15))
        
        # Save button
        self.save_btn = ttk.Button(actions_card, text="Save Image", 
                                  command=self.save_image, style='Modern.TButton', state='disabled')
        self.save_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Clear button
        self.clear_btn = ttk.Button(actions_card, text="Clear Display", 
                                   command=self.clear_display, style='Modern.TButton')
        self.clear_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Demo button
        self.demo_btn = ttk.Button(actions_card, text="Try Demo URL", 
                                  command=self.load_demo_url, style='Modern.TButton')
        self.demo_btn.pack(fill=tk.X)
        
        # Info Card
        info_card = ttk.LabelFrame(left_panel, text="Quick Tips", style='Card.TLabelframe', padding=15)
        info_card.pack(fill=tk.X)
        
        tips_text = """• Wikipedia articles work great
• News sites and blogs are good sources
• Larger sites take longer to process
• Try different color schemes
• Adjust word count for clarity"""
        
        tips_label = tk.Label(info_card, text=tips_text, 
                             font=('Segoe UI', 9), 
                             bg=self.colors['white'],
                             fg=self.colors['dark'],
                             justify=tk.LEFT,
                             anchor=tk.W)
        tips_label.pack(fill=tk.X)
        
        # === RIGHT PANEL CONTENT ===
        
        # Visualization Card
        viz_card = ttk.LabelFrame(right_panel, text="Word Cloud Visualization", style='Card.TLabelframe', padding=20)
        viz_card.pack(fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure with modern styling
        try:
            plt.style.use('seaborn-v0_8-whitegrid')
        except:
            try:
                plt.style.use('seaborn-whitegrid')
            except:
                plt.style.use('default')
                
        self.fig, self.ax = plt.subplots(figsize=(12, 8), facecolor='white')
        self.ax.set_facecolor('white')
        self.ax.axis('off')
        
        # Welcome message
        welcome_text = """Welcome to Word Cloud Generator
        
Enter a website URL and click "Generate Word Cloud" to create beautiful visualizations.

Try the demo URL or paste your own website link to get started!"""
        
        self.ax.text(0.5, 0.5, welcome_text, 
                    horizontalalignment='center', 
                    verticalalignment='center', 
                    transform=self.ax.transAxes, 
                    fontsize=14, 
                    color=self.colors['dark'],
                    bbox=dict(boxstyle="round,pad=0.5", facecolor=self.colors['light'], alpha=0.8))
        
        self.canvas = FigureCanvasTkAgg(self.fig, viz_card)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        status_frame = tk.Frame(main_container, bg=self.colors['primary'], height=30)
        status_frame.pack(fill=tk.X, pady=(20, 0))
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="Ready • Word Cloud Generator v2.0")
        status_label = tk.Label(status_frame, textvariable=self.status_var, 
                               font=('Segoe UI', 9),
                               bg=self.colors['primary'], 
                               fg=self.colors['white'])
        status_label.pack(expand=True)

    def load_demo_url(self):
        """Load a demo URL for testing"""
        demo_urls = [
            "https://en.wikipedia.org/wiki/Artificial_intelligence",
            "https://en.wikipedia.org/wiki/Machine_learning",
            "https://en.wikipedia.org/wiki/Python_(programming_language)",
            "https://docs.python.org/3/tutorial/",
            "https://en.wikipedia.org/wiki/Data_science"
        ]
        demo_url = random.choice(demo_urls)
        self.url_var.set(demo_url)
        self.status_var.set(f"Loaded demo URL: {demo_url.split('/')[-1].replace('_', ' ').title()}")
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-Return>', lambda e: self.generate_wordcloud())
        self.root.bind('<F5>', lambda e: self.generate_wordcloud())
        self.root.bind('<Control-s>', lambda e: self.save_image())
        self.root.bind('<Control-l>', lambda e: self.clear_display())
        self.root.bind('<Control-d>', lambda e: self.load_demo_url())

    def fetch_website_content(self, url):
        """Fetch and parse website content"""
        try:
            # Validate URL
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                raise ValueError("Invalid URL format")
            
            # Set headers to mimic a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Fetch the webpage
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean and process text
            text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
            text = text.strip()
            
            return text
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching website: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing website content: {str(e)}")
    
    def process_text(self, text):
        """Process text and return word frequencies"""
        try:
            min_length = int(self.min_length_var.get())
        except ValueError:
            min_length = 3
            
        # Convert to lowercase and extract words
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Filter words by length and remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
            'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
            'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
            'than', 'too', 'very', 'can', 'will', 'just', 'don', 'should', 'now', 'get', 'has',
            'had', 'have', 'was', 'were', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'is',
            'are', 'am', 'be', 'this', 'that', 'these', 'those', 'i', 'me', 'my', 'myself',
            'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves',
            'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
            'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
            'whose', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing'
        }
        
        filtered_words = [word for word in words if len(word) >= min_length and word not in stop_words]
        
        # Count word frequencies
        word_freq = Counter(filtered_words)
        
        return dict(word_freq)
    
    def create_wordcloud_image(self, word_frequencies):
        """Create word cloud from frequencies"""
        try:
            max_words = int(self.max_words_var.get())
        except ValueError:
            max_words = 150
            
        wordcloud = WordCloud(
            width=1000,
            height=600,
            background_color=self.background_var.get(),
            colormap=self.colormap_var.get(),
            max_words=max_words,
            relative_scaling=0.5,
            min_font_size=12,
            max_font_size=100,
            prefer_horizontal=0.7,
            collocations=False,
            margin=20
        ).generate_from_frequencies(word_frequencies)
        
        return wordcloud
    
    def update_display(self, wordcloud):
        """Update the matplotlib display with new word cloud"""
        self.ax.clear()
        
        # Fix upside down display by setting origin to 'upper'
        self.ax.imshow(wordcloud, interpolation='bilinear', origin='upper')
        self.ax.axis('off')
        
        # Add a subtle border effect
        self.ax.set_xlim(0, wordcloud.width)
        self.ax.set_ylim(wordcloud.height, 0)  # Flip Y-axis to match image orientation
        
        self.canvas.draw()
        self.current_wordcloud = wordcloud
        self.save_btn.config(state='normal')
        
        # Show word count in status
        word_count = len(self.word_frequencies) if hasattr(self, 'word_frequencies') else 0
        self.status_var.set(f"Word cloud created successfully! ({word_count} unique words processed)")
    
    def generate_wordcloud_thread(self):
        """Generate word cloud in separate thread"""
        url = self.url_var.get().strip()
        
        if not url or url == "https://":
            messagebox.showerror("Error", "Please enter a valid website URL")
            self.progress.stop()
            self.generate_btn.config(state='normal')
            self.status_var.set("Ready • Word Cloud Generator v2.0")
            return
        
        try:
            self.status_var.set("Fetching website content...")
            text = self.fetch_website_content(url)
            
            if not text.strip():
                raise Exception("No text content found on the website")
            
            self.status_var.set("Processing text and analyzing words...")
            word_frequencies = self.process_text(text)
            self.word_frequencies = word_frequencies
            
            if not word_frequencies:
                raise Exception("No valid words found after processing")
            
            self.status_var.set("Creating beautiful word cloud...")
            wordcloud = self.create_wordcloud_image(word_frequencies)
            
            # Update GUI in main thread
            self.root.after(0, lambda: self.update_display(wordcloud))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, lambda: self.status_var.set("Error occurred - Please try again"))
        finally:
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.generate_btn.config(state='normal'))
    
    def generate_wordcloud(self):
        """Start word cloud generation"""
        if self.processing:
            return
            
        self.processing = True
        self.generate_btn.config(state='disabled')
        self.progress.start(10)
        
        # Run in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self.generate_wordcloud_thread)
        thread.daemon = True
        thread.start()
    
    def save_image(self):
        """Save the current word cloud image"""
        if self.current_wordcloud is None:
            messagebox.showwarning("Warning", "No word cloud to save")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            title="Save Word Cloud Image"
        )
        
        if filename:
            try:
                self.current_wordcloud.to_file(filename)
                messagebox.showinfo("Success", f"Word cloud saved successfully!\n\nLocation: {filename}")
                self.status_var.set(f"Image saved: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def clear_display(self):
        """Clear the word cloud display"""
        self.ax.clear()
        
        welcome_text = """Welcome to Word Cloud Generator
        
Enter a website URL and click "Generate Word Cloud" to create beautiful visualizations.

Try the demo URL or paste your own website link to get started!"""
        
        self.ax.text(0.5, 0.5, welcome_text, 
                    horizontalalignment='center', 
                    verticalalignment='center', 
                    transform=self.ax.transAxes, 
                    fontsize=14, 
                    color=self.colors['dark'],
                    bbox=dict(boxstyle="round,pad=0.5", facecolor=self.colors['light'], alpha=0.8))
        
        self.canvas.draw()
        self.current_wordcloud = None
        self.save_btn.config(state='disabled')
        self.status_var.set("Ready • Word Cloud Generator v2.0")

def main():
    """Main function to run the modern GUI application"""
    root = tk.Tk()
    app = ModernWordCloudGUI(root)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()