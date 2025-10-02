# Word Cloud GUI Application

A graphical user interface application that creates word clouds from website content. Simply enter a website URL and the application will automatically fetch the content, process the text, and generate a beautiful word cloud visualization.

## Features

- **Modern GUI**: Responsive two-panel layout with rich styling and handy keyboard shortcuts
- **Web scraping**: Automatically fetches and processes content from any website
- **Customizable options**:
  - Adjust maximum number of words
  - Set minimum word length filter
  - Choose from multiple colour schemes even after the cloud is generated
  - Switch background colours on the fly to preview different looks
- **Real-time progress**: Progress bar and status updates during processing
- **Demo shortcuts**: One-click demo URL loader for instant experimentation
- **Save functionality**: Export word clouds as PNG or JPEG images
- **Smart text processing**: Automatically removes common stop words and HTML tags

## Installation

1. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the modern interface**:

   ```bash
   python word_cloud_gui_modern.py
   ```

   Prefer the classic layout? Run `python word_cloud_gui.py` instead.

## What's New

- Live styling updates: change the colour map or background after generation without reprocessing the webpage.
- Streamlined processing queue keeps the app responsive between runs.
- Refreshed UI styling with clearer status messaging and demo URL picker.

## Usage

1. **Enter Website URL**: Type or paste a website URL in the input field.
2. **Adjust Options** (optional): Configure maximum words, minimum word length, colour scheme, and background colour before generating.
3. **Generate**: Click "Generate Word Cloud" (or press `Ctrl+Enter` / `F5`) to create the visualisation.
4. **Tweak Styling**: Select new colour schemes or backgrounds to immediately refresh the cloud.
5. **Save**: Once satisfied, use "Save Image" to export the word cloud.
6. **Clear**: Use "Clear" to reset the display.

## Supported Websites

The application works with most public websites that allow web scraping. Some websites may block automated requests or require special handling.

## Dependencies

- **matplotlib**: For creating and displaying visualisations
- **wordcloud**: Core word cloud generation library
- **requests**: For fetching website content
- **beautifulsoup4**: For parsing HTML content
- **Pillow**: For image processing
- **tkinter**: GUI framework (included with Python)

## Example Websites to Try

- News websites (BBC, CNN, etc.)
- Wikipedia articles
- Blog posts
- Company websites
- Documentation sites

## Troubleshooting

**"Error fetching website"**:

- Check if the URL is correct and accessible
- Some websites block automated requests
- Try a different website

**"No valid words found"**:

- The website might have very little text content
- Try lowering the minimum word length
- Check if the website loaded properly

**GUI not responding**:

- The application processes content in the background
- Wait for the progress bar to complete
- Large websites may take longer to process

## Original Word Cloud Example

This GUI application is based on the original `word_cloud_example.py` which demonstrates basic word cloud creation with sample data. The GUI version extends this functionality with web scraping and a user-friendly interface.
