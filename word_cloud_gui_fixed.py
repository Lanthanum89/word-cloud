#!/usr/bin/env python3
"""
Word Cloud GUI Application
This application provides a graphical interface for creating word clouds from website content.
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

class WordCloudGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Website Word Cloud Generator")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.word_frequencies = {}
        self.current_wordcloud = None
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # URL input section
        url_frame = ttk.LabelFrame(main_frame, text="Website URL", padding="10")
        url_frame.grid(row=0, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
        url_frame.columnconfigure(1, weight=1)
        
        ttk.Label(url_frame, text="URL:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.url_var = tk.StringVar(value="https://")
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=(0, 10))
        
        self.generate_btn = ttk.Button(url_frame, text="Generate Word Cloud", command=self.generate_wordcloud)
        self.generate_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(url_frame, mode='indeterminate')
        self.progress.grid(row=1, column=0, columnspan=3, sticky=tk.W+tk.E, pady=(10, 0))
        
        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
        
        # Left column options
        left_options = ttk.Frame(options_frame)
        left_options.grid(row=0, column=0, sticky=tk.W+tk.N, padx=(0, 20))
        
        ttk.Label(left_options, text="Max Words:").grid(row=0, column=0, sticky=tk.W)
        self.max_words_var = tk.StringVar(value="100")
        ttk.Entry(left_options, textvariable=self.max_words_var, width=10).grid(row=0, column=1, padx=(10, 0))
        
        ttk.Label(left_options, text="Min Word Length:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.min_length_var = tk.StringVar(value="3")
        ttk.Entry(left_options, textvariable=self.min_length_var, width=10).grid(row=1, column=1, padx=(10, 0), pady=(5, 0))
        
        # Right column options
        right_options = ttk.Frame(options_frame)
        right_options.grid(row=0, column=1, sticky=tk.W+tk.N)
        
        ttk.Label(right_options, text="Color Scheme:").grid(row=0, column=0, sticky=tk.W)
        self.colormap_var = tk.StringVar(value="plasma")
        colormap_combo = ttk.Combobox(right_options, textvariable=self.colormap_var, width=15)
        colormap_combo['values'] = ('plasma', 'viridis', 'inferno', 'magma', 'coolwarm', 'tab10', 'Set3')
        colormap_combo.grid(row=0, column=1, padx=(10, 0))
        colormap_combo.state(['readonly'])
        
        ttk.Label(right_options, text="Background:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.background_var = tk.StringVar(value="white")
        bg_combo = ttk.Combobox(right_options, textvariable=self.background_var, width=15)
        bg_combo['values'] = ('white', 'black', 'lightgray', 'navy', 'darkgreen')
        bg_combo.grid(row=1, column=1, padx=(10, 0), pady=(5, 0))
        bg_combo.state(['readonly'])
        
        # Word cloud display area
        display_frame = ttk.LabelFrame(main_frame, text="Word Cloud", padding="10")
        display_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.axis('off')
        self.ax.text(0.5, 0.5, 'Enter a website URL and click "Generate Word Cloud" to begin', 
                    horizontalalignment='center', verticalalignment='center', 
                    transform=self.ax.transAxes, fontsize=14, color='gray')
        
        self.canvas = FigureCanvasTkAgg(self.fig, display_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        self.save_btn = ttk.Button(buttons_frame, text="Save Image", command=self.save_image, state='disabled')
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(buttons_frame, text="Clear", command=self.clear_display)
        self.clear_btn.pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(10, 0))
        
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
            max_words = 100
            
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color=self.background_var.get(),
            colormap=self.colormap_var.get(),
            max_words=max_words,
            relative_scaling=0.5,
            min_font_size=10,
            max_font_size=80,
            prefer_horizontal=0.8,
            collocations=False,
            margin=10
        ).generate_from_frequencies(word_frequencies)
        
        return wordcloud
    
    def update_display(self, wordcloud):
        """Update the matplotlib display with new word cloud"""
        self.ax.clear()
        # Fix upside down display by setting origin to 'upper'
        self.ax.imshow(wordcloud, interpolation='bilinear', origin='upper')
        self.ax.axis('off')
        self.canvas.draw()
        self.current_wordcloud = wordcloud
        self.save_btn.config(state='normal')
    
    def generate_wordcloud_thread(self):
        """Generate word cloud in separate thread"""
        url = self.url_var.get().strip()
        
        if not url or url == "https://":
            messagebox.showerror("Error", "Please enter a valid website URL")
            self.progress.stop()
            self.generate_btn.config(state='normal')
            self.status_var.set("Ready")
            return
        
        try:
            self.status_var.set("Fetching website content...")
            text = self.fetch_website_content(url)
            
            if not text.strip():
                raise Exception("No text content found on the website")
            
            self.status_var.set("Processing text...")
            word_frequencies = self.process_text(text)
            
            if not word_frequencies:
                raise Exception("No valid words found after processing")
            
            self.status_var.set("Creating word cloud...")
            wordcloud = self.create_wordcloud_image(word_frequencies)
            
            # Update GUI in main thread
            self.root.after(0, lambda: self.update_display(wordcloud))
            self.root.after(0, lambda: self.status_var.set(f"Word cloud created from {len(word_frequencies)} unique words"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, lambda: self.status_var.set("Error occurred"))
        finally:
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.generate_btn.config(state='normal'))
    
    def generate_wordcloud(self):
        """Start word cloud generation"""
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
                messagebox.showinfo("Success", f"Word cloud saved as {filename}")
                self.status_var.set(f"Image saved: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def clear_display(self):
        """Clear the word cloud display"""
        self.ax.clear()
        self.ax.text(0.5, 0.5, 'Enter a website URL and click "Generate Word Cloud" to begin', 
                    horizontalalignment='center', verticalalignment='center', 
                    transform=self.ax.transAxes, fontsize=14, color='gray')
        self.canvas.draw()
        self.current_wordcloud = None
        self.save_btn.config(state='disabled')
        self.status_var.set("Ready")

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = WordCloudGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()