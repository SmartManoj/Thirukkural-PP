import markdown

markdown_content = '[Artificial general intelligence (AGI)](https://en.wikipedia.org/wiki/Artificial_general_intelligence)'

html_content = markdown.markdown(markdown_content)

# Print or use the HTML content
print(html_content)
